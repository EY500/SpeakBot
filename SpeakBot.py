import asyncio
import re
from gtts import gTTS
import speech_recognition as sr
import pyaudio
import pydub
from googletrans import Translator
from EdgeGPT import Chatbot, ConversationStyle

#for mandarin no tld, for others put "tld=tld_for_tts" besides 'lang=...' in 'tts=gTTS(....'
#tld is accent
input_lang = 'en'
output_lang = 'ja'
tld_for_tts = 'us'

if input_lang == 'en' :
    wit_api_key = 'RAWZEC4AYA5JDCG4ZTY63ARKLZLHFDZK'
    exit_input = 'Exit'
    reset_input = 'Reset'
    help_input = 'Help'

elif input_lang == 'ja' :
    wit_api_key = 'V7ZQZCY5OB7RHVYOLGJHNWO57UX2B2EV'
    exit_input = '赤' #'あか' aka =red
    reset_input = '紫' #murasaki =purple
    help_input = '緑' #midori =green

elif input_lang == 'ko' :
    wit_api_key = '7MOW4EIVNUJQ6GRAMDKIDPBZVXRDX5CE'
    exit_input = '붉은' #bulg-eun =red
    reset_input = '보라' #bola =purple
    help_input = '녹색' #nogseag =green

else :
    print('select valid input language...')
    exit()

rec = sr.Recognizer()
p = pyaudio.PyAudio()
translator = Translator()
bot = Chatbot(cookie_path = 'bing_cookie.json')


device_count = p.get_device_count()

for i in range(device_count):
    device_info = p.get_device_info_by_index(i)
    device_name = device_info['name']
    print(f"Device {i}: {device_name}")
    
output_device_index = int(input("Select Output device as 'Cable Input' : "))

def play_sound(audio_output):
    
    p = pyaudio.PyAudio()

    sound = pydub.AudioSegment.from_file(audio_output)

    audio_data = sound.raw_data

    sample_rate = sound.frame_rate
    sample_width = sound.sample_width
    channels = sound.channels

    device_info = p.get_device_info_by_index(output_device_index)
    device_name = device_info['name']
    device_id = device_info['index']

    stream = p.open(format=p.get_format_from_width(sample_width),
                channels=channels,
                rate=sample_rate,
                output=True,
                output_device_index=output_device_index)

    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    p.terminate()

def speak(word):
    tts = gTTS(text=word, lang=output_lang, tld=tld_for_tts)
    tts.save('output_gTTS.mp3')
    play_sound('output_gTTS.mp3')

async def main():

                    
    while True:
                
        print('Recording...')
    
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source, duration=2)
            source.pause_treshold = 1
            audio = rec.listen(source, phrase_time_limit=None, timeout=None)

        try:
            print('...')
            
            if input_lang == 'en' :
                user_input = rec.recognize_wit(audio, key=wit_api_key)
                print("You :", user_input)

                if user_input == exit_input:
                    print('Exiting')
                    break
                    
                elif user_input == help_input:
                
                    help_msg = "help - Shows this help message ////// exit - Exits the program ////// reset - Resets the conversation"
                
                    print(help_msg)
                    speak(help_msg)

                elif user_input == reset_input:
                    await bot.reset()
                    print('reset done')
                    continue
            
                else:
                    print('processing...')
                    response = await bot.ask(prompt = user_input, conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub")
        
                    for message in response["item"]["messages"]:
                        if message["author"] == "bot":
                            bot_response = message["text"]
        
                    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
                    bot_response = bot_response.replace('[/\*]', '')
                    
                    if output_lang == 'en' :
                        
                        print('Bot : ', bot_response)
                        speak(bot_response)

                    else :

                        bot_translated = translator.translate(bot_response, src='en', dest=output_lang)

                        print("Bot EN :", bot_response)
                        print("Bot", output_lang.upper(), ":", bot_translated.text)
                        speak(bot_translated.text)

                    await bot.close()

            else:
                user_input_raw = rec.recognize_wit(audio, key=wit_api_key)
                user_input = translator.translate(user_input_raw, src=input_lang, dest='en')
                user_input = user_input.text
                print("You", input_lang.upper(), " : ", user_input_raw)
                print("You EN : ", user_input)

                if user_input_raw == exit_input:
                    print('Exiting')
                    break
                    
                elif user_input_raw == help_input:
                
                    help_msg = "help - Shows this help message ////// exit - Exits the program ////// reset - Resets the conversation"
                
                    print(help_msg)
                    speak(help_msg)

                elif user_input_raw == reset_input:
                    await bot.reset()
                    print('reset done')
                    continue
            
                else:
                    print('processing...')
                    response = await bot.ask(prompt = user_input, conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub")
        
                    for message in response["item"]["messages"]:
                        if message["author"] == "bot":
                            bot_response = message["text"]
        
                    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
                    bot_response = bot_response.replace('[/\*]', '')
                    
                    if output_lang == 'en' :
                        
                        print('Bot : ', bot_response)
                        speak(bot_response)

                    else :

                        bot_translated = translator.translate(bot_response, src='en', dest=output_lang)

                        print("Bot EN :", bot_response)
                        print("Bot", output_lang.upper(), ":", bot_translated.text)
                        speak(bot_translated.text)

                    await bot.close()

        except Exception as e:
            print("An error occured...")
            print(e)
            speak('An error occured')
            

if __name__ == "__main__":
    asyncio.run(main())
