import cmd
import openai

class ChatCLI(cmd.Cmd):
    intro = "Welcome to ChatGPT CLI. Type 'help' for a list of commands.\n" \
            "Usage: Ask your question directly, `quit` for exit"
    prompt = "(ChatGPT) "

    def do_quit(self, arg):
        """Exit the program"""
        print("Quitting...")
        return True

    def default(self, line: str):
        process_files(line)
        return False


def process_files(arg):
    # Generate API_KEY from https://platform.openai.com/account/api-keys
    api_key = '[Replace_By_APIKEY]'
    if not api_key:
        print("API key not found in environment variable OPENAI_API_KEY.")
        print("Please set the variable with your API key.")
        return

    # Set up the OpenAI API client
    openai.api_key = api_key
    engine = "text-davinci-003"

    prompt_filled = arg

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
    print(new_section)


if __name__ == '__main__':
    cli = ChatCLI()
    cli.cmdloop()
