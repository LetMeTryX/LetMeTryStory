from revChatGPT.V1 import Chatbot
import json
import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

def ask_chatbot(subject):
    # Generate access token through https://chat.openai.com/api/auth/session
    chatbot = Chatbot(config=json.load(open("chatgpt_config.json")))

    #subject = 'how many questions did I ask you so far?'

    # Call Chatgpt to get reply, better to define conversation id to prevent create new conversation each time
    response = ""
    for data in chatbot.ask(
        subject,
        conversation_id='b86d121e-a4dc-45b0-a04c-b7f52839e0a7'
    ):
        response = data["message"]
    logging.info("Get reply from Chatgpt: %s", response)
    print (response)
    return response