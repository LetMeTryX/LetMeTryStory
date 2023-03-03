import openai
import os
import sys
import tokenizers
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


openai.api_key = os.environ.get("OPENAI_API_KEY")

def condense_text(file_path):
    with open(file_path, "r") as f:
        text = f.read()
    
    print("Original text:")
    print(text)
    original_len = num_tokens_from_string(text, 'gpt2')
    
    max = 4096 - 200; # new engine may calculate tokens differently, reserved some buff. may revise in future. 
    
    if original_len < max/2:
        target_len = int(original_len * 0.9)
    else:
        target_len = max - original_len
    
    print("Original words:", len(text))
    print("Original tokens:", original_len)
    print("Target tokens:", target_len)
    
    prompt = f"Summary the following text with 400 to 600 charactors:\n\n{text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=target_len,
        n=1,
        stop=None,
        temperature=0.2,
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
    
def main():
    if len(sys.argv) != 2:
        print("Please provide the file path as a parameter.")
        return
    
    file_path = sys.argv[1]
    condense_text(file_path)
    print("Text condensed successfully.")

if __name__ == "__main__":
    main()
else:
    condense_text("old-story-summary.txt")
