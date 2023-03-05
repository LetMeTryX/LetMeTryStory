import openai
import os
import datetime
import time
from conversational_chatbot import ask_chatbot 
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


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
   
        '''
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
        '''
        target_value=ask_chatbot(prompt)
        text_size=len(target_value)
        if(text_size == 0):
            print("got 0 from openai, sth wrong, sleep 60s...")
            time.sleep(60)
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
