import openai
import os
import datetime
from condense_text_file import condense_text

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
    
    new_section = call_openai_with_template("new-section", "new-section-prompt-template.txt", story_background, personage_introduction, story_summary, new_section_input)
    new_story_summary = story_summary + "\n" + new_section
    save_to_file_with_timestamp("new-story-summary", new_story_summary)   
    new_story_summary = condense_text(new_story_summary, 400, 600)
    save_to_file("old-story-summary.txt", new_story_summary)
    
    
    os.rename("new-section-input.txt", "new-section-input-"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".txt")

    
    new_background = call_openai_with_template("new-background", "new-background-prompt-template.txt", story_background, personage_introduction, story_summary, new_section_input)    
    new_background = condense_text(new_background, 150, 300)
    save_to_file("old-story-background.txt", new_background)
    
    new_personage_introduction = call_openai_with_template("new-personage-introduction", "new-personage-introduction-prompt-template.txt", story_background, personage_introduction, story_summary, new_section_input)
    new_personage_introduction = condense_text(new_personage_introduction, 150, 300)
    save_to_file("old-personage-introduction.txt", new_personage_introduction)

def call_openai_with_template(target_name, prompt_template_file, story_background, personage_introduction, story_summary, new_section_input):  
    with open(prompt_template_file, "r") as f:
        prompt_template = f.read()
        
    # Fill prompt template
    prompt = prompt_template.replace("STORY_BACKGROUND", story_background)
    prompt = prompt.replace("PERSONAGE_INTRODUCTION", personage_introduction)
    prompt = prompt.replace("STORY_SUMMARY", story_summary)
    prompt = prompt.replace("NEW_SECTION_INPUT", new_section_input)
    
    save_to_file_with_timestamp(target_name+"-prompt", prompt)
    
    # Call OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    target_value = response.choices[0].text.strip()
    save_to_file_with_timestamp(target_name, target_value)
    return target_value
    
def save_to_file(filename, content):
    print("Save {} words to {} with content:\n{} ",len(content), filename, content)
    with open(filename, "w") as f:
        f.write(content)
        
def save_to_file_with_timestamp(filename_prefix, content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename=filename_prefix+'-'+timestamp+".txt"
    save_to_file(filename, content)
        
process_files()