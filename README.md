# SpeakBot
Speakbot is an AI chatbot that allows users to interact with the app using voice input and output. The app uses Bing AI with 'Edge GPT' github repo for generating responses, Google TTS for audio output, Google Translate for text translation, and Wit AI for speech recognition.

When the user speaks into the app, the speech is converted into text using Wit AI's speech recognition technology. The text is then translated into English using Google Translate, which is provided as input to the Bing AI, generating a response in English.

The app then translates this English response back into the user's preferred language using Google Translate, and the translated response is spoken out loud using Google TTS. This process ensures that the user can understand the response from the Speakbot in their own language, even if the chatbot doesn't speak that language.

# Details

Works with 'Japanese(ja)', 'Korean(ko)', 'English(en)' as input languages and output language can be anything that Google TTS supports

In this particular program, users have the option to choose their desired output sound playback device. This allows them to specify where the audio output should be directed, whether it be to a specific set of speakers or headphones.

Furthermore, the program can also utilize VB Cable, which is a virtual audio cable that allows users to route audio output from one program to another. This means that users can use the output of this program as input audio for other programs like Discord or WhatsApp, and the other person will only hear what the program is speaking.

Overall, this program's audio routing capabilities allow users to customize their audio output and use it in a variety of ways, including streaming audio to other programs or devices. This flexibility can greatly enhance the user's audio experience and make it more tailored to their specific needs.

# Config

You need to  use 'Microsoft Edge' and an extension to export the cookie file when the bing chat ai is opened in the browser.
Copy the contents and Save that file as 'bing_cookie.json'.

If you installed VB audio virtual cable, choose 'VB virtual cable audio input' as the playback device in program when prompted in the start.
