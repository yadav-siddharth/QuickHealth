# Python program to translate
# speech to text and text to speech


from email.mime import audio
import speech_recognition as sr

def record():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    mic = sr.Microphone()

    with mic as source:
        print("Say something\n")
        recognizer.adjust_for_ambient_noise(source,duration=2)
        print("Ready to record\n")
        audio = recognizer.listen(source)
        print("Audio captured\n")
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Say again please\n")
        except sr.RequestError:
            print("Speech service down\n")

