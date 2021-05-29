from logging import PlaceHolder
import random
import tkinter
from tkinter import *
import datetime
import pyttsx3
from twitter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import subprocess
import webbrowser
import ctypes
from tkinter import _tkinter
from PIL import ImageTk, Image
from googlesearch import search
import speech_recognition as sr
from googletrans import Translator
import wolframalpha
import wikipedia
from PyDictionary import PyDictionary
import pyowm
import pyautogui as pg
import sys
import tweepy as tw
import speedtest
import smtplib
import requests
import psutil
import platform
import wmi
from time import strftime
from googlesearch import search
import spotify
import psutil
from spotify_client import SpotifyClient
from pywikihow import search_wikihow
import ctypes


try:
    app = wolframalpha.Client("KWLEX5-UEA5U52P92")
except Exception as e:
    print(e)


MASTER = "SHIV"
city = "Ambala"

consumer_key = 'ChOVckIoiSDAegrpxUqAnsvYz'
consumer_secret = 'KFpCu7ozK6wLkry0NCoQbn5bIBydriwrvLw71f9hHAKPWJQnAy'
access_token = '1361310618863636487-BpimTTfY3EF2EtAJujtcpSn4pUX1mT'
access_token_secret = 'uyxjvXcAK3kZoqFp3cULewi5AhC8UjcWjKktJLjGFES6G'
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


twitter = Twitter(auth=OAuth(access_token,
                  access_token_secret,
                  consumer_key,
                  consumer_secret))

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', rate-62)
window = Tk()
window.geometry("490x490")
window.configure(bg="white")

global ques
global ques2


def command():
    window.update()
    ques2.delete(1.0, "end")
    window.update()

    if 'wikipedia' in ques.get():
        query = ques.get().split(' ')
        query = " ".join(query[0:])
        speak("I am searching for " + query)
        speak("You can check the output screen for your results")
        window.update()
        ques2.insert(1.0, wikipedia.summary(query, sentences=3))
        window.update()

    if 'temperature' or 'weather' in ques.get():
        try:
            res = app.query(ques.get())
            window.update()
            ques2.insert(1.0, next(res.results).text)
            window.update()
            speak(next(res.results).text)
        except Exception as e:
            print(e)

    if "search" in ques.get():
        outputList = []
        speak('What should I search for ?')
        query = input("Input Here:=> ")
        searchOnGoogle(query, outputList)
        speak('Here are your links. Tell me which link you want to open ?')
        openLink(outputList)

    if "screenshot" in ques.get():
        Screenshot()

    if "take note" in ques.get():
        speak("What you want to be noted down?")
        text = takeCommand()
        window.update()
        ques2.insert(1.0, text)
        window.update()
        note(text)

    if "who are you" in ques.get() or "define yourself" in ques.get():
        window.update()
        ques2.insert(1.0, "Hello, I am gaabe. Your personal Assistant. I am here to make your life easier. You can command me to perform various tasks such as calculating sums or opening applications etcetra")
        window.update()
        speak('Hello, I am gaabe. Your personal Assistant. I am here to make your life easier. You can command me to perform various tasks such as calculating sums or opening applications etcetra')

    if "play songs" in ques.get() or "play music" in ques.get():
        speak("Here’s your music. Enjoy !")
        music_dir = r"D:\New folder\PICTURES\kirtii\Gaane"
        songs = os.listdir(music_dir)
        print(songs)
        ran_num = random.randint(0, len(songs)-1)
        os.startfile(os.path.join(music_dir, songs[ran_num]))

    if "active how to do" in ques.get():
        speak("How to do mod is activated please tell me what you want to know")
        how = takeCommand2()
        max_results = 1
        how_to = search_wikihow(how, max_results)
        speak("I am writing down the details of "+how+" in the Output screen")
        assert len(how_to) == 1
        ques2.delete(1.0, "end")
        window.update()
        ques2.insert(1.0, how_to[0].summary)
        window.update()

    if "system status" in ques.get():
        battery = psutil.sensors_battery()
        percentage = battery.percent
        c = wmi.WMI()
        avail_mem = psutil.virtual_memory().available * 100 / \
            psutil.virtual_memory().total
        my_system = c.Win32_ComputerSystem()[0]
        my_system2 = platform.uname()
        avail_mem = round(avail_mem, 2)
        speak("System status has been printed on the Output Screen")
        window.update()
        ques2.insert(1.0,
                     f"System: {my_system2.system}\nNode Name: {my_system2.node}\nRelease: {my_system2.release}\nVersion:  {my_system2.version}\nMachine: {my_system2.machine}\nProcessor: {my_system2.processor}\nManufacturer: {my_system.Manufacturer}\nModel: {my_system.Model}\nSystem Family: {my_system.SystemFamily}\nNumber of Processor: {my_system.NumberOfProcessors}\nSystem Type: {my_system.SystemType}\nSystem Battery: {percentage} % \nSystem Available Memory: {avail_mem} % ")
        window.update()

    if "translate" in ques.get():
        text = ques.get().split("translate to")
        dest = ques.get()[1]
        langtranslator()

    if "lock system" in ques.get():
        ctypes.windll.user32.LockWorkStation()

    if "restart system" in ques.get():
        speak("Restarting your system")
        os.system("shutdown /r /t 1")

    if "volume up" in ques.get():
        pg.press("volumeup")

    if "volume down" in ques.get():
        pg.press("volumedown")

    if "volume mute" in ques.get():
        pg.press("volumemute")

    if "speed test" in ques.get():
        speak("We are checking out your network speed. Please wait for a while")
        st = speedtest.Speedtest()
        dl = st.download()
        up = st.upload()
        dl = dl/8000000
        up = up/8000000
        dl = round(dl, 2)
        up = round(up, 2)
        window.update()
        ques2.insert(1.0,
                     f"sir we have {dl} MB per second downloading speed and {up} MB per second uploading speed"
                     )
        window.update()
        speak(
            f"sir we have {dl} MB per second downloading speed and {up} MB per second uploading speed")

    if "open reddit" in ques.get():
        ques2.insert(1.0, "Opening Reddit")
        speak('opening reddit')
        webbrowser.open("reddit.com")

    if 'the time' in ques.get():
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        window.update()
        ques2.insert(1.0, f"{MASTER} the time is {strTime}")
        window.update()
        speak(f"{MASTER} the time is {strTime}")

    if "open code" in ques.get() or "open visual studio" in ques.get():
        speak('opening visual studio')
        codePath = r"C:\Users\lenovo\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        os.startfile(codePath)

    if 'shutdown' in ques.get():
        os.system("shutdown now -h")
        speak("ok sir i am shutting down the computer")

    if 'switch window' in ques.get():
        pg.keyDown('alt')
        pg.press('tab')
        pg.keyUp('alt')

    if 'open stackoverflow' in ques.get():
        window.update()
        ques2.insert(1.0, "Opening Stackoverflow")
        window.update()
        speak("ok sir i will open the stck over flow website")
        webbrowser.open("https://wwww.stackoverflow.com")

    if 'trending hashtags' in ques.get():
        results = twitter.trends.place(_id=23424848)
        speak("Here are some Hashtags Trending in India. You can check them out in the output box")
        i = 0
        for location in results:
            for trend in location["trends"]:
                if i == 5:
                    break
                window.update()
                ques2.insert(1.0, trend["name"]+"\n")
                window.update()
                i = i+1

    if 'open website' in ques.get():
        speak("which website sir ")
        website = input("Input=> ")
        webbrowser.open("https://"+website+".com")

    if "tell jokes" in ques.get():
        tellAJoke()

    if "close application" in ques.get():
        speak("Which application you want to close")
        name = takeCommand2()
        os.system('taskkill /f /im '+name+'.exe')

    if "open explorer" in ques.get():
        subprocess.run(["explorer", ","])

    if 'open mail' in ques.get():
        speak("ok sir i will open gmail.com")
        window.update()
        ques2.insert(1.0, "Opening G-Mail")
        window.update()
        webbrowser.open("https://www.gmail.com")

    if 'open google' in ques.get():
        speak("ok sir i will open google.com")
        window.update()
        ques2.insert(1.0, "Opening google")
        window.update()
        webbrowser.open("https://www.google.com")

    if 'youtube' in ques.get():
        speak("What do you want to search on youtube")
        query = takeCommand2()
        speak("opening youtube")
        webbrowser.open_new_tab(
            f"https://www.youtube.com/results?search_query={query}")

    if 'exit' in ques.get():
        window.update()
        ques2.insert(1.0, "good bye sir have a good day")
        window.update()
        speak("good bye sir have a good day")
        sys.exit()

    if 'quit' in ques.get():
        window.update()
        ques2.insert(1.0, "good bye sir have a good day")
        window.update()
        speak("good bye sir have a good day")
        sys.exit()


def takeCommand2():
    return str(input('Command: '))


def takeCommand():
    ques.delete(0, END)
    txt = "Listening..."
    window.update()
    ques.insert(0, txt)
    window.update()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said : {query}\n")

    except Exception as e:
        print(e)
    window.update()
    ques.delete(0, END)
    ques.insert(0, query.lower())
    window.update()
    command()
    return query


L1 = Label(window, text="Input here")
L1.pack(anchor=NW, padx=80)


def openHelpWindow():
    newWindow = Toplevel(window)
    newWindow.title("Help")
    newWindow.geometry("500x500")
    ques3 = Text(newWindow, height=80, width=70, )
    ques3.pack()
    ques3.insert(1.0, "Thankyou for Using G.A.A.B.E. Assistant.\nHere You can write or Speak these Commands!\n(1) Wikipedia => You can Wikipedia anything by Entering or speaking Wikipedia <Query>.\n(2) Temperature or Weather of <City/State> => You will get the Detailed info of the weather/temperature.\n(3) Search => You can search anything here on the Google.\n(4) Screenshot => You can Took the Screenshot and save them as per your choice.\n(5) Take note => You can note down anything by speaking your notes to G.A.A.B.E and save them for later view.\n(6) Who are you => G.A.A.B.E will tell you about herself.\n(7) Play Songs => You can Play any songs stored in your system.\n(8) Active how to do => This will activate how to mode and it will help us to know the stuff like How to bake cake or how to make tea etc etc.\n(9) System Status => This will give you the detailed info of your System.\n(10) Translate => You can translate your words or sentences or paragraphs into any Language.\n(11) Lock System => You can lock your System.\n(12) Restart System/Shutdown => You can Restart/Shutdown Your System.\n(13) Volume up\down\mute => It Will up\down\mute the Volume.\n(14) Speed Test => It Will give you the Speed of your Network in MegaBytes.\n(15) Open Redit/Code/Stackoverflow/websites/explorer/mail/google => It Will open what ever you tell her to open any one of them.\n(16) The Time => You can get the Current Time.\n(17) Trending Hashtags => It will list you the Top 5 Trending Hashtags in India.\n(18) Tell Jokes => It will tell you the Jokes.\n(19) Close Application => You can close any application by entering his process name.\n(20) Youtube => You can search anything on Youtube here.\n(21) Exit/Quit => It will close the G.A.A.B.E\nThankyou..!")


ques = Entry(window, width=40, bg="white",
             fg="black", font=('arial', 11, 'bold'))
ques.pack(padx=10)

btn = Button(bg="black", fg="white", width=20, activeforeground="black",
             activebackground="white", text="Speak", command=takeCommand).pack(pady=1, padx=3)

btn = Button(bg="black", fg="white", width=20, activeforeground="black",
             activebackground="grey", text="command", command=command).pack(side=TOP, pady=1, padx=3)


btn3 = Button(bg="black", fg="white", width=20, activeforeground="black",
              activebackground="white", text="Help", command=openHelpWindow).pack(anchor=E, pady=1, padx=3)

L2 = Label(window, text="G.A.A.B.E :")
L2.pack(anchor=W, padx=10, pady=10)

ques2 = Text(window, height=80, width=70)
ques2.pack()


def speak(audio):
    print("Gaabe: "+audio)
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    
    
    if hour>= 0 and hour<12:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f" Good morning {MASTER} the time is {strTime}")
    elif hour>= 12 and hour<18:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f" Good Afternoon {MASTER} the time is {strTime}") 
  
    else:
       strTime = datetime.datetime.now().strftime("%H:%M:%S")
       speak(f" Good Evening {MASTER} the time is {strTime}")
  


def Screenshot():
    image = pg.screenshot()
    speak("screen shot taken")
    speak("what do you want to save it as?")
    filename = takeCommand2()
    image.save(filename+".png")
    speak("do you want me to show it? Yes or No")
    ans = takeCommand2().lower()
    if "yes" in ans:
        os.startfile(filename+".png")
    else:
        speak("never mind")


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def langtranslator():
    print("Language Translator Function()")
    try:
        trans = Translator()
        speak("Say the language to translate in")
        language = str(input("Language:"))
        print("Language:", language)

        speak("what to translate")
        content = str(input("Data:"))
        print("Content:", content)

        t = trans.translate(text=content+"",  dest=language)
        print("Result:", t.text)
        print("Pronounciation", t.pronunciation)
        speak(t.pronunciation)
        window.update()
        ques2.insert(1.0, f"{t.text}")
        window.update()
    except Exception as e:
        print(e)


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'password')
    server.sendmail("shiv@codewithshiv.com", to, content)
    server.close()


def find(name, path):
    for root, files, *_ in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def tellAJoke():
    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept": "application/json"}
    )
    if res.status_code == 200:
        speak("Okay. Here's one")
        window.update()
        ques2.insert(1.0, str(req.json()['joke']))
        window.update()
        speak(str(res.json()['joke']))
    else:
        speak('Oops!I ran out of jokes')


def searchOnGoogle(query, outputList):
    speak('The top five search results from Google  are listed below.')
    i = 1
    for output in search(query, tld="co.in", num=10, stop=5, pause=2):
        print(f"{i}=> {output} ")
        i = i+1
        outputList.append(output)
    return outputList


def openLink(outputList):
    link_no = int(input("Link Number:=> "))
    while 1:
        if link_no > len(outputList):
            print('Link doesnt exists')
            link_no = int(input("Link Number:=> "))
        if link_no <= len(outputList):
            webbrowser.open(outputList[link_no-1])
            break


def win():
    speak("ok sir i will open the google")
    webbrowser.open("https://www.google.com")


def main():
    speak('Gaabe here.')
    wishMe()
    speak('What would you like me to do for you ?')

    window.title("G.A.A.B.E")
    canvas = Canvas(
        window, width=200, height=200, bg="#000000")

    canvas.configure(bg="black")
    canvas.pack()
    window.mainloop()

    while True:
        window.mainloop()


def ball():
    canvas = Canvas()


if __name__ == "__main__":
    speak('Initialising Gaabe')
    main()


window.mainloop()
