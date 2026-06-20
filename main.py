import speech_recognition as sr
from dotenv import load_dotenv
import webbrowser
import pyttsx3
import musicLibrary
import requests
from groq import Groq
import os
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


newsapi="54d9e921eb54469693043a9dad892dcc"


#processCammand function
def processCammand(c):
    #opening some social media platforms
    if ("open google" in c):
        webbrowser.open("https://google.com")
    elif ("open youtube" in c):
        webbrowser.open("https://youtube.com")
    elif ("open facebook" in c):
        webbrowser.open("https://facebook.com")
    elif ("open instagram" in c):
        webbrowser.open("https://instagram.com")
    elif ("open linkedin" in c):
        webbrowser.open("https://linkedin.com")
    #playing music
    elif(c.lower().startswith("play")):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)

    #listening some news
    elif "news" in c.lower():
        speak("Fetching latest news")

        r = requests.get(
            f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&apiKey={newsapi}"
        )

        data = r.json()

        for article in data["articles"][:5]:
            headline = article["title"]
            print(headline)
            speak(headline)
    #intergrated with gemini model to amswer other questions
    else:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Sophia, a personal AI assistant.
                    Never mention Groq or Gemini.
                    Answer briefly and identify yourself as Sophia if asked your name.
                    """
                },
                {
                    "role": "user",
                    "content": c
                }
            ]
        )

        answer = response.choices[0].message.content

        print(answer)
        speak(answer)
        
    

# Convert text to speech
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

#intializing sophia
if (__name__=="__main__"):
    speak("Intializing Sophia")
    
    while True:
        r = sr.Recognizer()
        
        try:
            #obtain audio from microphone for the wake word
            with sr.Microphone() as source:
                print("Listening!")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            print("processing")
            
            #recognize wake word
            word=r.recognize_google(audio)
            if "sophia" in word.lower() or "sofia" in word.lower():
                speak("yes")

            # obtain audio for cammand
            with sr.Microphone() as source:
                print("Sophia active")
                audio = r.listen(source)
            
            #recognize the cammand
            command = r.recognize_google(audio)
            print("Command:", command)

            #processCammand
            processCammand(command.lower())
        
        except Exception as e:
            print("error; {0}".format(e))
