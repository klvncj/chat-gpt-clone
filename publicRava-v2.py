import os
import speech_recognition as sr
import playsound
from gtts import gTTS
import openai
import uuid

api_key = str(input('Enter Your OpenAI API Key : '))
name = str(input('What Would You Like To Call Your AI : '))
terminate_phrase = str(input('Choose You Terminate Word / Phrase : '))

lang = 'en'

openai.api_key = api_key

guy = ""

while True:
    def start_rava():
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            print(f'{name} is listening...')
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
                global guy
                guy = said
                if name in said:
                    new_string = said.replace(name, "")
                    new_string = new_string.strip()
                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_string}])
                    text = completion.choices[0].message.content
                    print(text)
                    speech = gTTS(text=text, lang=lang, slow=False, tld="ca")
                    file_name = f"welcome_{str(uuid.uuid4())}.mp3"
                    speech.save(file_name)
                    playsound.playsound(file_name, block=False)
                    os.remove(file_name)

            except Exception as e:
                print(f"Exception: {str(e)}")

        return said
      
    if terminate_phrase in guy:
        break

    start_rava()