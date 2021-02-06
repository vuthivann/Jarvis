'''this is kit assistant'''
import random
import psutil
from autocorrect import spell
from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import subprocess
import webbrowser
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import wikipedia
import datetime
from tkinter import *
import requests
import json

# initialize
RECOGNIZER = sr.Recognizer()
NOW = datetime.datetime.now().hour
KITA = Tk()
KITA.geometry("600x300")
OPTIONS = ["Gmail", "Slack", "GitHub"]
ITEMS = StringVar(KITA)
ITEMS.set(OPTIONS[0])

def text_to_speech(text):
    '''function to speak'''
    tts = gTTS(text, lang='en-US')
    tts.save("good.mp3")
    label = Label(KITA, text=text, wraplength=250)
    label.pack()
    KITA.update()
    print(text)
    playsound('good.mp3')

def register():
    '''function to save the user's email and pwd'''
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
    dropdown = OptionMenu(KITA, ITEMS, *OPTIONS)
    dropdown.pack()
    username_lable = Label(KITA, text="Username * ")
    username_lable.pack()
    username_entry = Entry(KITA, textvariable=username)
    username_entry.pack()
    password_lable = Label(KITA, text="Password * ")
    password_lable.pack()
    password_entry = Entry(KITA, textvariable=password, show='*')
    password_entry.pack()
    Label(KITA, text="").pack()
    Button(KITA, text="Register", width=10, height=1, bg="#4dffa6", command=register_user).pack()


def register_user():
    '''function after click the button register'''
    username_info = username.get()
    password_info = password.get()
    basedir = os.path.dirname(os.path.abspath(__file__))
    categorization_file = os.path.join(basedir, '')
    filepath = os.path.join(categorization_file, ITEMS.get())
    file = open(filepath, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    Label(KITA, text="Registration Success", fg="green", font=("calibri", 11)).pack()
    KITA.update()
    BrowserFunction().slack()

def dictionary():
    '''gui with a text box'''
    global search_word
    search_word = StringVar()
    word_lable = Label(KITA, text="Enter the word")
    word_lable.pack()
    word_entry = Entry(KITA, textvariable=search_word)
    word_entry.pack()
    Button(KITA, text="Search", width=10, height=1, bg="#4dffa6", command=search_dict).pack()

def search_dict():
    '''function to search in dictionary'''
    app_id = 'e30b4616'
    app_key = '3dc1910026b6263252db58f6546535f6'
    language = 'en'
    word_id = spell(search_word.get())
    url = 'https://od-api.oxforddictionaries.\
           com:443/api/v2/entries/'  + language + '/' + word_id.lower()
    urlfr = 'https://od-api.oxforddictionaries.\
             com:443/api/v2/stats/frequency/word/'\
             + language + '/?corpus=nmc&lemma=' + word_id.lower()
    request = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
    json_dict = request.json()
    word = json_dict["id"]
    definitions = json_dict["results"][0]["lexicalEntries"][0]\
                  ["entries"][0]["senses"][0]["definitions"][0]
    part_of_speech = json_dict["results"][0]["lexicalEntries"][0]["lexicalCategory"]["id"]
    print(f"{word.capitalize()} ({part_of_speech}): is {definitions}.")
    full_meaning = (word + "\n" + part_of_speech + "\n" + definitions)
    text_to_speech(full_meaning)


def audio():
    '''function of voice'''
    global KITA
    global command
    global voice
    with sr.Microphone() as source:
        printtxt("Listening...")
        voice = RECOGNIZER.listen(source)
        command = RECOGNIZER.recognize_google(voice)
        printtxt(command)
        command_function(command)


def command_function(command):
    try:
        if "YouTube" in command:
            BrowserFunction().go_youtube()

        elif ("hello" or "hola" or "hi") in command:
            text = "Hello, How are you today?", "Hi", "hello", "Hi, didn't you have a nice day?"
            text_to_speech(random.choice(text))

        elif "open Wikipedia" in command:
            BrowserFunction().go_wiki()

        elif "Wikipedia" in command:
            text_to_speech("searching in Wikipedia")
            search = command.replace("Wikipedia", "")
            result = wikipedia.summary(search, sentences=2)
            text_to_speech(result)

        elif "search" in command:
            text_to_speech('what do you want to search?')
            printtxt("Listening...")
            BrowserFunction.browser_search()

        elif command == "open GitHub":
            BrowserFunction().github()

        elif "shut down" in command:
            ComputerFunction().shutdown()

        elif command == "hello":
            text_to_speech("hi")

        elif "Slack" in command:
            basedir = os.path.dirname(os.path.abspath(__file__))
            categorization_file = os.path.join(basedir, '')
            filepath = os.path.join(categorization_file, "Gmail")
            if Path(filepath).is_file():
                text_to_speech("Working on it and please confirm the account in your Gmail")
                BrowserFunction().slack()
            else:
                register()
        elif "code"in command:
            text_to_speech("You mean Visual Studio code?")
            ComputerFunction().visual()

        elif 'time' in command:
            strtime = datetime.datetime.now().strftime("%H:%M")
            text_to_speech(f" the time is {strtime}")
            print(f"{strtime}")

        elif 'date' in command:
            strday = datetime.datetime.now().strftime("%d,%m,%Y")
            text_to_speech(f"the date is{strday}")
            print(f"{strday}")

        elif "battery" in command:
            ComputerFunction().battery()

        elif "restart" in command:
            os.system('systemctl reboot -i')

        elif "emergency" in command:
            text_to_speech("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

        elif 'weather' in command:
            text_to_speech("Okay! please wait! We are processing")
            printtxt("Processing...")
            city = 'Kampong Chhnang'
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&\
                    appid=322e70e904cc615a09504912b2a0ae50&units=metric'.format(city)
            res = requests.get(url)
            data = res.json()
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            latitude = data['coord']['lat']
            longitude = data['coord']['lon']
            description = data['weather'][0]['description']
            printtxt('Temperature : {} degree celcius'.format(temp))
            printtxt('Wind Speed : {} m/s'.format(wind_speed))
            printtxt('Latitude : {}'.format(latitude))
            printtxt('Longitude : {}'.format(longitude))
            printtxt('Description : {}'.format(description))
            text_to_speech(f'In your current location, temperature is{temp} degree\
                            celcius. wind speed {wind_speed}. Latitude {latitude}.\
                            Longitude {longitude} and description{description}')
            if int(temp) > 25 and int(temp) < 28:
                text_to_speech('Enjoy your day!')
            elif int(temp) > 18 and int(temp) <= 25:
                text_to_speech('Today is a bit cold. please take care of your health.')
            elif int(temp) <= 18:
                text_to_speech('Today is cold. please wear a jacket.')
            elif int(temp) >= 28:
                text_to_speech('Today is hot. please drink more water.')
        elif "work station" in command:
            ComputerFunction().workstation()

        elif "dictionary" in command:
            text_to_speech("Please enter the word you want to know")
            dictionary()
        
        elif "schedule" in command:
            ComputerFunction().schedule()

        elif "remind me to" in command:
            global remind
            remind = command.replace("remind me to", "")
            ComputerFunction().reminder()

        elif "who are you" in command:
            respone1 = ("I am your personal assitant",
                        "I am kita , You forgot me huh",
                        "I am you , just kidding , i am your assistant",
                        "hey enough of me , how can i help you")
            text_to_speech(random.choice(respone1))
            audio()

        elif "Siri" in command:
            respone2 = ("no I'm not",
                        "i don't even know what that siri stuff is",
                        "Am i suppose to know siri",
                        "why do you ask me like that, you want to flirt with siri or what?",
                        "don't ask me about that stuff")
            text_to_speech(random.choice(respone2))
        elif "i love you" in command:
            respone3 = ("I love you too",
                        "no i can't love you",
                        "sorry we can't be in that way",
                        "I'm your assistant , not your girlfriend")
            text_to_speech(random.choice(respone3))

        elif "tell me a joke" in command:
            respone4 = ("hello world",
                        "I dreamed I was forced to eat a giant marshmallow.\
                        When I woke up, my pillow was gone.",
                        "I asked God for a bike, but I know God doesn’t work that way.\
                        So I stole a bike and asked for forgiveness.",
                        "If you think women are the weaker sex, try pulling\
                        the blanket back to your side.",
                        "I tell you what always catches my eye. Short people with an umbrella.",
                        "Knock knock! Who’s there? Suck. Suck who? Sucks to be you")
            text_to_speech(random.choice(respone4))
        elif "hello" in command:
            respone5 = "hey how are you today", "yes I'm already here"
            text_to_speech(random.choice(respone5))
        elif ("I'm sad" or "I'm happy") in command:
            text_to_speech("You know, you should study instead of doing that")

        # else:
        #     text_to_speech("Sorry, I couldn't understand what you said")
    except sr.UnknownValueError:
        text_to_speech("Could not understand audio")


class BrowserFunction():

    '''the class of function in browser'''

    @staticmethod
    def go_youtube():
        '''function to open youtube'''
        text_to_speech("opening")
        webbrowser.open_new_tab("https://www.youtube.com/")

    @staticmethod
    def go_wiki():
        '''function to open wikipedia'''
        text_to_speech("opening")
        webbrowser.open_new_tab("https://www.wikipedia.org/")

    @staticmethod
    def browser_search():
        '''function to search in chrome'''
        audio()
        text_to_speech("Searching...")
        webbrowser.open_new_tab("https://www.google.com.tr/search?q={}".format(command))

    @staticmethod
    def github():
        '''function to open github'''
        text_to_speech("opening")
        webbrowser.open_new_tab("https://github.com/")

    @staticmethod
    def slack():
        '''function go to slack'''
        basedir = os.path.dirname(os.path.abspath(__file__))
        categorization_file = os.path.join(basedir, '')
        filepath = os.path.join(categorization_file, "Gmail")
        if Path(filepath).is_file():
            acc = open(filepath, "r")
            info = acc.read().split("\n")
            gmail = info[0]
            pwd = info[1]
        print(gmail)
        print(pwd)
        url_slack = 'https://slack.com/get-started#/find'
        url_gmail = 'https://accounts.google.com/signin/v2/identifier?service=mail&passive=\
                    true&rm=false&continue=https%3A%2F' \
                    '%2Fmail.google.com%2Fmail%2F&ss=1&scc=1&ltmpl\
                    =default&ltmplcache=2&emr=1&osid=1&flowName=GlifWebSignIn' \
                    '&flowEntry=ServiceLogin '
        basedir = os.path.dirname(os.path.abspath(__file__))
        categorization_file = os.path.join(basedir, '')
        driver = webdriver.Chrome(f"{categorization_file}chromedriver")
        # open slack
        driver.get(url_slack)
        driver.find_element_by_id('signup_email').send_keys(gmail)
        driver.find_element_by_id('submit_btn').click()
        driver.get(url_gmail)
        driver.find_element_by_id('identifierId').send_keys(gmail)
        driver.find_element_by_id("identifierId").send_keys(Keys.ENTER)
        time.sleep(2)
        driver.find_element_by_name("password").send_keys(pwd)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)


class ComputerFunction():
    '''class of computer function'''

    @staticmethod
    def shutdown():
        '''shutdown the computer'''
        text_to_speech("when to shut down?")
        audio()
        if "o'clock" in command:
            wait_time = re.sub(r"[A-Za-z]", "", command)
            text_to_speech("Okay i noted")
            if int(NOW) == int(wait_time):
                text_to_speech(f"Shutting down")
                subprocess.call(["shutdown", "-h", "now"])
        elif "minutes" or "minute" in command:
            wait_time = re.sub(r"[A-Za-z]", "", command)
            text_to_speech("Okay i noted")
            time.sleep(int(wait_time) * 60)
            text_to_speech(f"Shutting down")
            subprocess.call(["shutdown", "-h", "now"])
        elif "hours" or "hour" in command:
            wait_time = re.sub(r"[A-Za-z]", "", command)
            text_to_speech("Okay i noted")
            time.sleep(int(wait_time) * 3600)
            text_to_speech(f"Shutting down")
            subprocess.call(["shutdown", "-h", "now"])
        elif "now" in command:
            subprocess.call(["shutdown", "-h", "now"])

    @staticmethod
    def visual():
        '''function to open visual studio'''
        audio()
        if command == "Yes" or command == "yes":
            os.system("code")
        elif command == "No" or command == "no":
            text_to_speech("Ok")
    @staticmethod
    def workstation():
        '''function to open our work station'''
        os.system("code")
        os.system("slack")
        os.system("google-chrome")

    @staticmethod
    def connected_to_internet(url='http://www.google.com/', timeout=5):
        '''function when no interconnection'''
        try:
            _ = requests.get(url, timeout=timeout)
            return None
        except requests.ConnectionError:
            printtxt("We're having trouble with the connection, please try again later")
            playsound("nowifi.mp3")
        return False
    @staticmethod
    def battery():
        '''function to tell the battery'''
        battery_percent = round(psutil.sensors_battery().percent)
        if battery_percent < 20:
            text_to_speech(f"Your computer is at {battery_percent}%, low battery")
            time.sleep(60)
            text_to_speech("low battery")
        elif battery_percent > 50:
            text_to_speech(f"Your computer is at {battery_percent}%,\
                            Don't worry, I still can live very long")

    @staticmethod
    def reminder():
        '''function to set a reminder'''
        text_to_speech("when to remind")
        audio()
        if "o'clock" in command:
            wait_time = re.sub(r"[A-Za-z]", "", command)
            text_to_speech("Okay i noted")
            if int(NOW) == int(wait_time):
                text_to_speech(f"It's time to {remind}")
        elif "minutes" or "minute" in command:
            wait_time = re.sub(r"[A-Za-z]", "", command)
            text_to_speech("Okay i noted")
            time.sleep(int(wait_time) * 60)
            text_to_speech(f"It's time to {remind}")
        elif "hours" or "hour" in command:
            wait_time = re.sub(r"[A-Za-z]", "", command)
            text_to_speech("Okay i noted")
            time.sleep(int(wait_time) * 3600)
            text_to_speech(f"It's time to {remind}")
        elif "second" or "seconds" in command:
            wait_time = re.sub(r"[A-Za-z]", "", command)
            text_to_speech("Okay i noted")
            time.sleep(int(wait_time))
            text_to_speech(f"It's time to {remind}")
    @staticmethod
    def schedule():
        global Sec
        global json_schedule
        global string_time
        url = 'https://raw.githubusercontent.com/Bunnet12/Share/master/schedule.json'
        request_schedule = requests.get(url)
        json_schedule = request_schedule.json()
        current = datetime.datetime.now()
        string_time = current.strftime("%d.%m")
        text_to_speech("which section are you in?")
        audio()
        if "section A" in command:
            Sec = "Section A"
            ComputerFunction().call_schedule()
        elif "section B" in command:
            Sec = "Section B"
            ComputerFunction().call_schedule()
        elif "section C" in command:
            Sec = "Section C"
            ComputerFunction().call_schedule()
        else:
            text_to_speech("I couldn't find your section")
    @staticmethod
    def call_schedule():
        text_to_speech("Morning, Afternoon or All day?")
        audio()
        if "morning" in command:
            time_schedule = "Morning"
        elif "afternoon" in command:
            time_schedule = "Afternoon"
        else:
            text_to_speech("This time has no schedule")
        speak_schedule = json_schedule[Sec][0][string_time][0][time_schedule]
        text_to_speech(f"{Sec} + \n + {time }+ \n + {speak_schedule}")

def greeting():

    '''greeting function'''

    if 12 > int(NOW) >= 0:
        text_to_speech('Good Morning sir! What can I help you?')

    elif 12 <= int(NOW) < 18:
        text_to_speech('Good Afternoon sir! What can I help you?')

    elif 18 <= int(NOW) != 0:
        text_to_speech("Good Evening sir! What can I help you?")


def click():
    '''all the function in one'''
    ComputerFunction().connected_to_internet()
    audio()

def printtxt(text):
    '''function to display label on gui'''
    global KITA
    label = Label(KITA, text=text, wraplength=250)
    label.pack()
    KITA.update()

# get audio from the microphone
KITA.title("KIT Assistant")
greeting()
audio()
BUTTON = Button(text="click me", command=click)
BUTTON.pack()
KITA.mainloop()
