import openai
import os

def process_files():
    # Get OpenAI API key from environment variable
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        print("Error: OPENAI_API_KEY environment variable not found.")
        return
    
    # Read files
    with open("new-personage-introduction-prompt-template.txt", "r") as f:
        prompt_template = f.read()
    with open("old-story-background.txt", "r") as f:
        story_background = f.read()
    with open("old-personage-introduction.txt", "r") as f:
        personage_introduction = f.read()
    with open("old-story-summary.txt", "r") as f:
        story_summary = f.read()
    with open("new-section-input.txt", "r") as f:
        new_section_input = f.read()
    
    # Fill prompt template
    prompt = prompt_template.replace("STORY_BACKGROUND", story_background)
    prompt = prompt.replace("PERSONAGE_INTRODUCTION", personage_introduction)
    prompt = prompt.replace("STORY_SUMMARY", story_summary)
    prompt = prompt.replace("NEW_SECTION_INPUT", new_section_input)
    
    print("Filled prompt:")
    print(prompt)
    with open("new-personage-introduction-prompt.txt", "w") as f:
        f.write(prompt)
    
    # Call OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    new_section = response.choices[0].text.strip()
    
    print("New personage-introduction:")
    print(new_section)
    
    # Save new section to file
    with open("new-personage-introduction.txt", "w") as f:
        f.write(new_section)
    
    
process_files()