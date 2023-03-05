import openai
import os
from condense_text_file import condense_text
from generate_new_section import call_openai_with_template, save_to_file

def process_files():
    # Get OpenAI API key from environment variable
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        print("Error: OPENAI_API_KEY environment variable not found.")
        return
    
    # Read files
    with open("old-story-background.txt", "r") as f:
        story_background = f.read()
    with open("old-personage-introduction.txt", "r") as f:
        personage_introduction = f.read()
    with open("old-story-summary.txt", "r") as f:
        story_summary = f.read()
    
    
    new_section_input = ""
        
    new_personage_introduction = call_openai_with_template("new-personage-introduction", "new-personage-introduction-prompt-template.txt", story_background, personage_introduction, story_summary, new_section_input, 150, 300)
    new_personage_introduction = condense_text(new_personage_introduction, 150, 300)
    save_to_file("old-personage-introduction.txt", new_personage_introduction)
    
process_files()
