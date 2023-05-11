import asyncio
import re
from gtts import gTTS 
import speech_recognition as sr
import pyttsx3
import pyaudio
import pydub
from EdgeGPT import Chatbot, ConversationStyle

wit_api_key = 'RAWZEC4AYA5JDCG4ZTY63ARKLZLHFDZK'

tts = pyttsx3.init()
bot = Chatbot(cookie_path = './bing_cookie.json')
rec = sr.Recognizer()
p = pyaudio.PyAudio()


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

def transcription(filename):
    listening = ""
    print(listening)
    speak(listening)
    
    with sr.AudioFile(filename) as source:
        audio = rec.listen(source)
    
    try:
        user_input = rec.recognize_google(audio)
        return user_input
    except:
        recog_error = "I couldn't recognize your voice"
        print(recog_error)
        speak(recog_error)
        user_input = "None"
        return user_input


def speak(word):
    tts.setProperty('rate', 135)
    tts.setProperty('volume', 0.8)

    voices = tts.getProperty('voices')
    tts.setProperty('voice', voices[1].id)

    tts.say(str(word))
    tts.runAndWait()
    tts.stop()

async def main():
    
    
    init_msg = "say 'genius' to start recording...."
    print(init_msg)
    speak(init_msg)
        
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=2)
        audio = rec.listen(source)
            
        
        
        transcript = rec.recognize_google(audio)
                
        if transcript.lower() == 'genius':
            filename= "input.wav"
            request_qn = "please ask..."
            print(request_qn)
            speak(request_qn)
                    
            while True:

                with sr.Microphone() as source:
                    rec.adjust_for_ambient_noise(source, duration=2)
                    source.pause_treshold = 1
                    audio = rec.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, 'wb') as f:
                        f.write(audio.get_wav_data())

                user_input = transcription(filename) 
                print("You : ", user_input)       
                
                if user_input == "exit":
                    break
                
                elif user_input == "None":
                    user_input = " "
                    bot_response ="Bot : "
                    continue
                
                elif user_input == "help":
            
                    help_msg = "help - Show this help message      exit - Exit the program      reset - Reset the conversation"
            
                    print(help_msg)
                    speak(help_msg)

                elif user_input == "reset":
                    await bot.reset()
                    continue
        
                else:
                    response = await bot.ask(prompt = user_input, conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub")
    
                    for message in response["item"]["messages"]:
                        if message["author"] == "bot":
                            bot_response = message["text"]
    
                    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)

                    print("Bot :", bot_response)
                    speak(bot_response)

                    await bot.close()
            

if __name__ == "__main__":
    asyncio.run(main())
