import asyncio
import re
from EdgeGPT import Chatbot, ConversationStyle

async def main():
    
    bot = Chatbot(cookiePath = 'bing_cookie.json')
    
    while True:
        user_input = input("You : ")
        
        if user_input == "!exit":
            break

        if user_input == "!help":
            print(    
            """
            !help - Show this help message
            !exit - Exit the program
            !reset - Reset the conversation
            """
            )

        elif user_input == "!reset":
            await bot.reset()
            continue
        
        else:
            response = await bot.ask(prompt = user_input, conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub")
        
            for message in response["item"]["messages"]:
                if message["author"] == "bot":
                    bot_response = message["text"]
    
            bot_response = re.sub('\[\^\d+\^\]', '', bot_response)

            print("Bot :", bot_response)
            await bot.close()
    

if __name__ == "__main__":
    asyncio.run(main())
