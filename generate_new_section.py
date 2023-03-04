import openai
import os
import datetime
from condense_text_file import condense_text, num_tokens_from_string
import time

def process_files():
    # Get OpenAI API key from environment variable
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        print("Error: OPENAI_API_KEY environment variable not found.")
        return
    
    with open("old-story-background.txt", "r") as f:
        story_background = f.read()
    with open("old-personage-introduction.txt", "r") as f:
        personage_introduction = f.read()
    with open("old-story-summary.txt", "r") as f:
        story_summary = f.read()
    with open("new-section-input.txt", "r") as f:
        new_section_input = f.read()
    
    new_section = call_openai_with_template("new-section", "new-section-prompt-template.txt", story_background, personage_introduction, story_summary, new_section_input, 400, 600)
    save_to_file("new-section.txt", new_section) 
 
    new_story_summary = story_summary + "\n" + new_section   
    save_to_file_with_timestamp("new-story-summary", new_story_summary)   
    new_story_summary = condense_text(new_story_summary, 400, 600)
    save_to_file("old-story-summary.txt", new_story_summary)
    
    #to make sure new section input is not used multiple times once accepted as summary.
    os.rename("new-section-input.txt", "./tmp/new-section-input-"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".txt")

    
    new_background = call_openai_with_template("new-background", "new-background-prompt-template.txt", story_background, personage_introduction, story_summary, new_section_input, 150, 300)    
    new_background = condense_text(new_background, 150, 300).replace('\n', ' ')
    save_to_file("old-story-background.txt", new_background)
    
    new_personage_introduction = call_openai_with_template("new-personage-introduction", "new-personage-introduction-prompt-template.txt", story_background, personage_introduction, story_summary, new_section_input, 150, 300)
    new_personage_introduction = condense_text(new_personage_introduction, 150, 300)
    save_to_file("old-personage-introduction.txt", new_personage_introduction)

def call_openai_with_template(target_name, prompt_template_file, story_background, personage_introduction, story_summary, new_section_input, range_from,range_to):  
    with open(prompt_template_file, "r") as f:
        prompt_template = f.read()
        
    # Fill prompt template
    prompt = prompt_template.replace("STORY_BACKGROUND", story_background)
    prompt = prompt.replace("PERSONAGE_INTRODUCTION", personage_introduction)
    prompt = prompt.replace("STORY_SUMMARY", story_summary)
    prompt = prompt.replace("NEW_SECTION_INPUT", new_section_input)
    
    save_to_file_with_timestamp(target_name+"-prompt", prompt)
    
    target_value=call_openai_with_size_expectation(prompt, range_from,range_to)
        
    save_to_file_with_timestamp(target_name, target_value)
    
    return target_value

def call_openai_with_size_expectation(prompt, range_from, range_to):
    prompt_tokens = num_tokens_from_string(prompt, 'gpt2')
    target_tokens = 4096 - 200 - prompt_tokens
    
    ai_inaccuracy=50
    text_size = 0
    target_value=""
    call_count =0
    while text_size < range_from or text_size > range_to+ai_inaccuracy:
        call_count+=1
        print(f"Calling openai #{call_count} with tokens {prompt_tokens}+{target_tokens} for size in [{range_from},{range_to}]...")
   
        # Call OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=target_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )

        target_value = response.choices[0].text.strip()
        text_size=len(target_value)
        print(f"Got {text_size} from openai: \n {target_value}")
        time.sleep(10)
    return target_value

def save_to_file(filename, content):
    print(f"Save {len(content)} words to {filename} with content:\n{content} ")
    with open(filename, "w") as f:
        f.write(content)
        
def save_to_file_with_timestamp(filename_prefix, content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename=filename_prefix+'-'+timestamp+".txt"
    save_to_file("./tmp/"+filename, content)
        
if __name__ == "__main__":
    process_files()