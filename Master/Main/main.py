import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from fridayui import Ui_MainWindow
import pyttsx3
from datetime import datetime
import datetime
import speech_recognition as s
import wikipedia
import os
import smtplib
import subprocess
import pywhatkit as kit
import random
import winsound
from threading import Thread
import openai

openai.api_key = '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'

audio = pyttsx3.init("sapi5")
voices = audio.getProperty('voices')
audio.setProperty('voice',voices[1].id)
audio.setProperty('rate',180)

def speak(str):
    audio.say(str)
    audio.runAndWait()

def wish():
    current_time = int(datetime.datetime.now().hour)
    if current_time>=5 and current_time<12:
        speak("Good Morning, Sir")
    elif current_time>=12 and current_time<18:
        speak("Good Afternoon, Sir")
    else:
        speak("Good Evening, sir")
    reply=["I am friday, how may i help you","sir,did you call me"]
    choice=random.choice(reply)

    speak(choice)

def playOnYoutube(video):
    speak(f"playing {video} song on youtube")
    kit.playonyt(video)

def googleSearch(my_search):
    speak(f"searching {my_search} on google")
    kit.search(my_search)

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('dk78834@gmail.com','7011238959')
    server.sendmail('dk78834@gmail.com',to,content)
    server.close()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    def showTime(self):
        
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()

        label_time = current_time.toString("hh:mm:ss")
        label_date = current_date.toString(Qt.ISODate)

        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

class MainThread(QThread):
    def __init__(self):
        super().__init__()

     
    def run(self):
        self.friday()

    def speechToText(self):
        sr=s.Recognizer()
        with s.Microphone() as m:
            print("Listening....")
            sr.pause_threshold=1
            audio=sr.listen(m)

        try:
            print("Recognition....")
            output=sr.recognize_google(audio)

        except Exception as e:
                speak("Unable to understand\nsir please Speak again")
                return "None"
        return output
    
    def sTT(self):
        sr=s.Recognizer()
        with s.Microphone() as m:
            print("listening...")
            audio=sr.listen(m)

        try:
            print("Recognition...")
            output=sr.recognize_google(audio)

        except Exception as e:
                return "None"
        return output

    def fridayWake(self):
        while True:
            self.output=self.sTT().lower()
            if 'wake up' in self.output or 'activate' in self.output or 'start' in self.output:
                self.friday()
            else:
                continue

    def friday(self):
        wish()
        while True:
            self.output=self.speechToText().lower()
            if 'friday stop' == self.output or 'friday shutdown' == self.output or 'stop' in self.output:
                speak("Ok Sir, as your wish")
                break
            
            elif 'none' == self.output:
                continue

            elif 'wikipedia' in self.output:
                output = self.output.replace("wikipedia","")
                speak(f"Searching {output} on wikipedia")
                results = wikipedia.summary(output, sentences=4)
                speak("According to wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in self.output:
                speak("Opening Youtube")
                subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'youtube.com'])

            elif 'play song on youtube' in self.output:
                speak("Which song sir")
                video = self.speechToText().lower()
                playOnYoutube(video)

            elif 'open google' in self.output:
                speak("Opening Google")
                subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'google.com'])

            elif 'search on google' in self.output:
                speak("What you want search")
                my_search = self.speechToText().lower()
                googleSearch(my_search)

            elif 'open gmail' in self.output:
                speak("Opening Gmail")
                subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'gmail.com'])

            elif 'send email' in self.output:
                try:
                    speak("To whom do you want you send mail")
                    person = self.speechToText().lower()
                    speak("what you want to send")
                    content = self.speechToText().lower()
                    print(content)
                    to = "dk78834@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent!..")

                except Exception as e:
                    print(e)
                    print("Sorry Sir, i am not able to send mail,\nplease try again later....")
                    speak("Sorry Sir, i am not able to send mail,\nplease try again later....")

            elif 'open whatsapp' in self.output:
                speak("Opening Whatapp")
                os.startfile('C:\\Users\\Yogender Kumar\\Desktop\\WhatsApp.lnk')

            elif 'message on whatsapp' in self.output:
                speak("to whom do you want to send message")
                person='none'
                while 'none' in person:
                    person = self.speechToText().lower()
                speak("what message you want to send")
                my_message = self.speechToText().lower()
                current_time=datetime.datetime.now()
                h=current_time.hour
                m=current_time.minute+2
                # kit.sendwhatmsg(contact_dic[person], my_message,h,m)
                kit.sendwhatmsg_instantly(contact_dic[person], my_message)

            elif 'open irctc' in self.output:
                speak("opeaning IRCTC")
                subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'irctc.co.in'])

            elif 'play music' in self.output:
                speak("Playing music for you")
                music_dir = 'C:\\Users\\Yogender Kumar\\Desktop\\song'
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))

            elif 'set alarm' in self.output:
                speak("Alright sir, what time do you want to set alarm")
                start_alarm.start()
                break

            elif 'set reminder' in self.output:
                start_reminder.start()
                break

            
            elif 'time' in self.output:
                current_time = datetime.datetime.now()
                h=current_time.hour
                m=current_time.minute
                if h>=1 and h<5:
                    if m==0:
                        speak(f"sir, it's {h} o clock of Night")
                    else:
                        speak(f"sir, it's {h}{m} AM of Night")
                elif h>=5 and h<12:
                    if m==0:
                        speak(f"sir, it's {h} o clock of morning")
                    else:
                        speak(f"sir, it's {h}{m} AM of morning")
                elif h>=12 and h<18:
                    if m==0:
                        speak(f"sir, it's {h} o clock of afternoon")
                    else:
                        speak(f"sir, it's {h}{m} PM of afternoon")
                elif h>=18 and h<20:
                    if m==0:
                        speak(f"sir, it's {h} o clock of evening")
                    else:
                        speak(f"sir, it's {h}{m} PM of evening")
                elif h>20 and h<24:
                    if m==0:
                        speak(f"sir, it's {h} o clock of night")
                    else:
                        speak(f"sir, it's {h}{m} PM of night")

            elif 'open code' == self.output:
                speak("Opening Visual stdio code")
                path_1 = "C:\\Users\\Yogender Kumar\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(path_1)

            elif 'open chrome' in self.output:
                speak("Opening Google chrome")
                path_2 = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(path_2)

            elif 'open ms access' in self.output:
                speak("Opening Microsoft Access")
                path_3 = "C:\\Program Files\\Microsoft Office\\root\\Office16\\MSACCESS.EXE"
                os.startfile(path_3)

            elif 'open excel' in self.output:
                speak("Opening Microsoft excel")
                path_4 = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
                os.startfile(path_4)

            elif 'open word' == self.output:
                speak("Opening Microsoft word")
                path_5 = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                os.startfile(path_5)

            elif 'open powerpoint' in self.output:
                speak("Opening Microsoft powerpoint")
                path_6 = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
                os.startfile(path_6)

            elif 'open code blocks' in self.output:
                speak("Opening Codeblocks")
                path_7 = "C:\\Program Files\\CodeBlocks\\codeblocks.exe"
                os.startfile(path_7)

            elif 'open typing master' in self.output:
                speak("Opening Typing master")
                path_8 = "C:\\Program Files (x86)\\TypingMaster11\\TypingMaster.exe"
                os.startfile(path_8)
           
            elif 'open notepad' in self.output:
                speak("Opening Notepad")
                subprocess.Popen('C:\\Windows\\system32\\notepad.exe')
           
            elif 'open wordpad' in self.output:
                speak("Opening wordpad")
                subprocess.Popen('C:\\Program Files\\Windows NT\\Accessories\\wordpad.exe')
            
            elif 'open paint' in self.output:
                speak("Opening Microsoft paint")
                subprocess.Popen('C:\\Windows\\system32\\mspaint.exe')
            
            elif 'open calculator' in self.output:
                speak("Opening Calculator")
                subprocess.Popen('C:\\Windows\\system32\\calc.exe')
            
            elif 'open command prompt' in self.output:
                speak("Opening Command prompt")
                subprocess.Popen('C:\\Windows\\system32\\cmd.exe')
            
            elif 'open control panel' in self.output:
                speak("Opening control panel")
                self.load2()
                subprocess.Popen('C:\\Windows\\system32\\control.exe')

            elif 'help me' in self.output:
                reply=["how can i help you, sir",
                "What can i do for you, sir"]
                choice=random.choice(reply)
                speak(choice)

            elif 'who are you' in self.output:
                reply=["i am friday, sir",
                "i am a virtual assistant, which is based on an AI model"]
                choice=random.choice(reply)
                speak(choice)

            elif 'how are you' in self.output:
                reply=["i am fine, sir, how are you",
                "Today, i am feeling happy"]
                choice=random.choice(reply)
                speak(choice)

            elif 'what are you doing' in self.output:
                reply=["helping you to opearate this computer, sir",
                "i am learning from others, sir","Working on my skills, sir",
                "Finding way to find better results, sir"]
                choice=random.choice(reply)
                speak(choice)
                
            elif 'tell me about yourself' in self.output:
                reply=["AI language model created by OpenAI, I don't possess personal experiences or emotions, but I can provide information and assist you with various topics. My purpose is to help answer questions, engage in conversations, and provide useful information based on the input I receive.",]
                choice=random.choice(reply)
                speak(choice)


            elif 'what happen' in self.output:
                reply=["Nothing, i am always availabel",
                "Trying to give my best","Working on my skills, sir"
                "Nothing, sir"]
                choice=random.choice(reply)
                speak(choice)
            
            elif 'good' in self.output:
                reply=["ok, sir","thanks you, sir"]
                choice=random.choice(reply)
                speak(choice)                

            elif 'sing a song' in self.output:
                speak("Yes sir, please wait i try to sing a song")

            elif 'ok' in self.output:
                reply=["my pleasure, sir","It's ok, sir"]
                choice=random.choice(reply)
                speak(choice)

            elif 'friday' in self.output:
                reply=["Yes Sir","how can i help you, sir",
                "thanks to remeber me, sir"]
                choice=random.choice(reply)
                speak(choice)

            else:
                prompt=self.output
                response = openai.Completion.create(engine="text-davinci-003",prompt=prompt,max_tokens=50)
                generated_text = response['choices'][0]['text']
                speak(generated_text)

class myreminder(QThread):
        def __init__(self):
            super().__init__()
        def run(self):
            speak("What's the reminder sir")
            reminder=self.takecommand().lower()
            speak("Alright sir, When do you want to remind it")
            reminder_time = self.takecommand().lower()
            reminder_time = reminder_time.replace(".","")
            reminder_time = reminder_time.replace(":"," ")
            reminder_time = reminder_time.upper()
            speak(f"Ok sir, i will remind you at {reminder_time}")
            print(reminder_time)
            self.cheacking(reminder_time,reminder)
                                                                                                                     
        def takecommand(self):
            sr=s.Recognizer()
            with s.Microphone() as m:
                print("Listening....")
                audio=sr.listen(m)

            try:
                print("Recognition....")
                output=sr.recognize_google(audio)

            except Exception as e:
                    speak("Unable to understand\nsir please Speak again")
                    return "None"
            return output
    

        def cheacking(self,reminder_time,reminder):
            reminder_time=str(reminder_time)
            hour_var=reminder_time[0:2]
            hour_var=int(hour_var)
            if hour_var < 10:
                minute_var=reminder_time[2:4]
            else:
                minute_var=reminder_time[3:5]

            minute_var = int(minute_var)
            if (hour_var < 10) and (minute_var < 10):
                alarm_hour = reminder_time[0:1]
                alarm_minute = reminder_time[2:3]
            elif(hour_var < 10) and (minute_var >= 10):
                alarm_hour = reminder_time[0:1]
                alarm_minute = reminder_time[2:4]
            elif (hour_var >= 10) and (minute_var < 10):
                alarm_hour = reminder_time[0:2]
                alarm_minute = reminder_time[3:4]
            else:
                alarm_hour = reminder_time[0:2]
                alarm_minute = reminder_time[3:5]
                
            alarm_hour=int(alarm_hour)
            alarm_minute=int(alarm_minute)
            while True:
                now = datetime.datetime.now()
                time=now.strftime('%Y/%m/%d %I:%M:%S')
                current_hour=time[11:13]
                current_minute=time[14:16]
                
                print(current_hour,current_minute)
                if alarm_hour == current_hour:
                    if alarm_minute == current_minute:
                        speak(f"Sir, it's {reminder}")
                        # winsound.PlaySound('abc',winsound.SND_LOOP)
                    elif alarm_minute <= current_minute:
                        continue





class myalarm(QThread):
        def __init__(self):
            super().__init__()
        def run(self):
            alarm_time = self.takecommand().lower()
            alarm_time = alarm_time.replace(".","")
            alarm_time = alarm_time.replace(":"," ")
            alarm_time = alarm_time.upper()
            speak(f"ok sir, your alarm is set up for {alarm_time}")
            print(alarm_time)
            self.cheacking(alarm_time)
                                                                                                                     
        def takecommand(self):
            sr=s.Recognizer()
            with s.Microphone() as m:
                print("Listening....")
                audio=sr.listen(m)

            try:
                print("Recognition....")
                output=sr.recognize_google(audio)

            except Exception as e:
                    speak("Unable to understand\nsir please Speak again")
                    return "None"
            return output
    

        def cheacking(self,alarm_time):
            alarm_time=str(alarm_time)
            hour_var=alarm_time[0:2]
            hour_var=int(hour_var)
            if hour_var < 10:
                minute_var=alarm_time[2:4]
            else:
                minute_var=alarm_time[3:5]

            minute_var = int(minute_var)
            if (hour_var < 10) and (minute_var < 10):
                alarm_hour = alarm_time[0:1]
                alarm_minute = alarm_time[2:3]
            elif(hour_var < 10) and (minute_var >= 10):
                alarm_hour = alarm_time[0:1]
                alarm_minute = alarm_time[2:4]
            elif (hour_var >= 10) and (minute_var < 10):
                alarm_hour = alarm_time[0:2]
                alarm_minute = alarm_time[3:4]
            else:
                alarm_hour = alarm_time[0:2]
                alarm_minute = alarm_time[3:5]
                
            alarm_hour=int(alarm_hour)
            alarm_minute=int(alarm_minute)
            while True:
                current_time = datetime.datetime.now()
                current_time=datetime.strptime()
                current_hour= current_time.hour
                current_minute = current_time.minute
                if alarm_hour == current_hour:
                    if alarm_minute == current_minute:
                        winsound.PlaySound('abc',winsound.SND_LOOP)
                    elif alarm_minute <= current_minute:
                        continue

fridayStart = MainThread()
start_alarm = myalarm()
start_reminder = myreminder()

if __name__=="__main__":

    app = QApplication(sys.argv)
    interface = Main()
    interface.setFixedSize(1366,700)
    interface.show()
    fridayStart.start()
    exit(app.exec_())





