import openai
import os
import datetime
from condense_text_file import condense_text, num_tokens_from_string
import time
from conversational_chatbot import ask_chatbot 
from generate_new_background import generate_new_background
from story_util import *

def process_files():
    # Get OpenAI API key from environment variable
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        print("Error: OPENAI_API_KEY environment variable not found.")
        return
    
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    
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

    '''
    new_background = call_openai_with_template("new-background", "new-background-prompt-template.txt", story_background, personage_introduction, story_summary, new_section_input, 150, 300)    
    new_background = condense_text(new_background, 150, 300).replace('\n', ' ')
    save_to_file("old-story-background.txt", new_background)
    '''
    generate_new_background()
    
    new_personage_introduction = call_openai_with_template("new-personage-introduction", "new-personage-introduction-prompt-template.txt", story_background, personage_introduction, story_summary, new_section_input, 150, 300)
    new_personage_introduction = condense_text(new_personage_introduction, 150, 300)
    save_to_file("old-personage-introduction.txt", new_personage_introduction)
        
if __name__ == "__main__":
    process_files()