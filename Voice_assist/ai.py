##################################################import modules####################################################
import pyttsx3
import os
import datetime
import speech_recognition as s
import webbrowser
import wikipedia
import smtplib
import poplib
import string
from io import StringIO
import plone.rfc822
from text import password,user
#################################################Function Module####################################################
#Voice engine declaration#
eng=pyttsx3.init('sapi5')
voice=eng.getProperty('voices')
eng.setProperty('voices',voice[0].id)
#Allows the voice engine to speak#
def speak(audio):
    eng.say(audio)
    eng.runAndWait()
#Wishes you accordingly#
def wish():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("good morning")
    elif hour>=12 and hour <15:
        speak("good afternoon")
    elif hour>=15 and hour <18:
        speak("good evening")
    else:
        speak("good night")
#Take Command#
def command():
    r=s.Recognizer()
    with s.Microphone() as source:
        print("Waiting for your command")
        speak("Waiting for your command")
        r.pause_threshold=9
        audio=r.listen(source)
    try:
        print("Recognizing command.....")
        speak("Recognizing command.....")
        query=r.recognize_google(audio,language='en-in')
        print("You said",query)
    except Exception as e:
        print(e)
        speak("Command at fault")
        return "None"
    return query
#Send Email#
def Email(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login(user,password)
    server.sendmail(user,to,content)
    server.close()
#Read Email#
def ReadEmail():
    server=poplib.POP3('pop.gmail.com')
    server.user(user)
    server.pass_(password)
    resp, items, octets = server.list()
    id, size = string.split(items[0])
    resp, text, octets = server.retr(id)
    text = string.join(text, "\n")
    file = StringIO.StringIO(text)
    message = plone.rfc822.Message(file)
    speak(message['From']),
    speak(message['Subject']),
    speak(message['Date']),
    speak(message.fp.read()) 
######################################################Main Function##########################################################
if __name__=="__main__":
    wish()
    speak("I am your AI ,what do you want?")
    while True:
        query=command().lower()
        if 'wikipedia' in query:
            speak("Searching in wikipedia")
            query=query.replace("wikipedia","")
            result=wikipedia.summary(query,sentences=9)
            speak("The information that I obtained is")
            speak(result)
        elif 'open youtube' in query:
            speak("opening youtube....")
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("opening google")
            webbrowser.open("google.com")
        elif 'play music' in query:
            md=""
            songs=os.listdir(md)
            os.startfile(os.path.join(md,songs[0]))
        elif 'time rightnow' in query: 
            speak("The time right now is",datetime.datetime.now().strftime("%H:%M:%S"))
        elif 'send email' in query:
            try:
                speak("What is the content of the email i should send")
                speak("Whom should i send an email")
                to=command()
                speak("What is that you want to send ")
                content=command()
                Email(to,content)
                speak("Email has been sent")
            except Exception as e:
                speak("I am not able to send the email due to ",e)
        elif 'read email' in query:
            try:
                speak("Fetching The emails you have recieved")
                ReadEmail()
            except Exception as e:
                print(e)
                speak("Sorry i am unable to connect to gmail")
        elif 'quit' in query:
            exit()