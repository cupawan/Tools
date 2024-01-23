import speech_recognition as sr
from gtts import gTTS
import os
import time
import pygame



class Speech():
    def __init__(self,timeout):
        self.timeout = timeout
    def speech_to_text(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say Something... ")
            audio = r.listen(source,timeout = self.timeout) 
        try:
            print("You said: " + r.recognize(audio).title())
            return r.recognize(audio)    
        except Exception as e:                            
            print(str(e))
            return None
    
    def play_audio(self, filename):
        pygame.mixer.init()
        pygame.mixer.music.load(f"Files/{filename}")
        pygame.mixer.music.play()

    def delete_audio(self,filename, time_to_delete):
        while time_to_delete > 0:
            print(f"Deleting audio from system in: {time_to_delete} seconds", end='\r')
            time.sleep(1)
            time_to_delete -= 1
        os.remove(f"Files/{filename}")
        print(f"{filename} deleted successfully")

    def text_to_speech(self,text, lang = "en",slow = False):
        obj = gTTS(text = text,lang = lang, slow = slow)
        os.makedirs("Files",exist_ok = True)
        filename = text.replace(" ", "_") + ".mp3"
        obj.save(f"Files/{filename}")
        print("file saved", filename)
        self.play_audio(filename=filename)
        self.delete_audio(filename=filename,time_to_delete=10)

if __name__ == "__main__":
    s = Speech(timeout=10)
    transcript = s.speech_to_text()
    if transcript:
        speech = s.text_to_speech(text=transcript)
    else:
        speech = s.text_to_speech(text= "Please try again")



