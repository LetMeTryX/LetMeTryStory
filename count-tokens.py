import sys
import tokenizers
import tiktoken

def count_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        return num_tokens_from_string(content, 'gpt2')
    
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def count_tokens2(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        tokens = content.split()
        return len(tokens)
    
def count_tokens3(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        
        return len(content)

def main():
    if len(sys.argv) != 2:
        print('Usage: python count_tokens.py <file>')
        sys.exit(1)
    file_path = sys.argv[1]
    count = count_tokens(file_path)
    print('Number of GPT tokens:', count)
    print('Number of space split word tokens:', count_tokens2(file_path))
    print('Number of string tokens:', count_tokens3(file_path))

if __name__ == '__main__':
    main()

