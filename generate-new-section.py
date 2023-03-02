import openai
import os

def process_files():
    # Read in the API key from the environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("API key not found in environment variable OPENAI_API_KEY.")
        print("Please set the variable with your API key.")
        return
    
    # Set up the OpenAI API client
    openai.api_key = api_key
    engine = "text-davinci-002"
    
    # Define the filenames to be processed
    filenames = ["new-section-prompt-template.txt",
                 "old-story-summary.txt",
                 "new-section-input.txt",
                 "new-section.txt",
                 "new-story-summary.txt"]
    
    # Read in the content of each file
    files_content = []
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            files_content.append(content)
        print(f"Read {len(content)} characters from {filename}")
    
    # Fill in the prompt template
    prompt_template = files_content[0]
    old_summary = files_content[1]
    new_section_input = files_content[2]
    prompt_filled = prompt_template.replace("STORY_SUMMARY", old_summary)
    prompt_filled = prompt_filled.replace("NEW_SECTION_INPUT", new_section_input)
    with open("new-section-prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt_filled)
    print(f"Filled prompt template and wrote to new-section-prompt.txt")
    
    # Call the OpenAI API to generate new text based on the prompt
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt_filled,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    new_section = response.choices[0].text
    with open("new-section.txt", "w", encoding="utf-8") as f:
        f.write(new_section)
    print(f"Generated new section with {len(new_section)} characters and wrote to new-section.txt")
    
    # Append the new section to the old story summary and write to new-story-summary.txt
    new_summary = old_summary + new_section
    with open("new-story-summary.txt", "w", encoding="utf-8") as f:
        f.write(new_summary)
    print(f"Appended new section to old story summary and wrote to new-story-summary.txt")

process_files()