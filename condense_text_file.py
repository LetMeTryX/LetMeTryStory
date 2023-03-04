import openai
import os
import sys
import tokenizers
import tiktoken
import time

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


openai.api_key = os.environ.get("OPENAI_API_KEY")

def condense_file(file_path):
    with open(file_path, "r") as f:
        text = f.read()
    condense_text(text, 400, 600)    
        

def condense_text(text, range_from, range_to):
    ai_inaccuracy=50 # AI may not return extract the requested number or words.
    
    print("Original text:")
    print(text)
    original_len = num_tokens_from_string(text, 'gpt2')
    
    max = 4096 - 200; # new engine may calculate tokens differently, reserved some buff 200. may revise in future. 
    
    if original_len < max/2:
        target_len = int(original_len * 0.9)
    else:
        target_len = max - original_len
    
    print("Original words:", len(text))
    print("Original tokens:", original_len)
    print("Target tokens:", target_len)
    
    prompt = f"Can you please summarize the following text into a response that is between [{range_from}] and [{range_to}] words?\n{text}"
    print(prompt)
    
    text_size = len(text)
    condensed_text = text
    call_count =0
    while text_size < range_from or text_size > range_to+ai_inaccuracy:
        call_count+=1
        print(f"Calling openai #{call_count} for size in [{range_from},{range_to}]...")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=target_len,
            n=1,
            stop=None,
            temperature=0.3,
        )

        condensed_text = response.choices[0].text.strip()
        condensed_len = num_tokens_from_string(condensed_text, 'gpt2')
        length_diff = original_len - condensed_len

        print("Condensed text:")
        print(condensed_text)
        print("Condensed words:", len(condensed_text))
        print("Condensed tokens:")
        print(condensed_len)
        print("tokens difference:", length_diff)
        text_size=len(condensed_text)
        time.sleep(10)
    return condensed_text
        
    
    
def main():
    if len(sys.argv) != 2:
        print("Please provide the file path as a parameter.")
        return
    
    file_path = sys.argv[1]
    condense_file(file_path)
    print("Text condensed successfully.")

if __name__ == "__main__":
    main()
#else:
#    condense_file("old-story-summary.txt")
