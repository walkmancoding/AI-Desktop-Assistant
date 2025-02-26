import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import webbrowser
import os
import threading
from PIL import Image, ImageTk

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    display_response(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        display_response("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        display_command("You: " + command)
        return command.lower()
    except sr.UnknownValueError:
        display_response("I couldn't understand that.")
        return ""
    except sr.RequestError:
        display_response("Check your internet connection.")
        return ""

def get_date():
    return datetime.date.today().strftime("%A, %B %d, %Y")

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def open_application(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
    }
    
    if app_name in apps:
        os.startfile(apps[app_name])
        speak(f"Opening {app_name}")
    else:
        speak("Sorry, I don't have that application configured.")

def open_website(site_name, query=None):
    websites = {
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com"
    }
    
    if site_name == "youtube" and query:
        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        speak(f"Playing {query} on YouTube")
    elif site_name in websites:
        webbrowser.open(websites[site_name])
        speak(f"Opening {site_name}")


def process_command(command):
    if "stop" in command or "exit" in command:
        speak("Goodbye!")
        root.destroy()
    elif "time" in command:
        speak(f"The current time is {get_time()}")
    elif "date" in command:
        speak(f"Today's date is {get_date()}")
    elif "search" in command:
        speak("What do you want to search for?")
        query = listen()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Here are the search results for {query}")
    elif "wikipedia" in command:
        speak("What topic should I search on Wikipedia?")
        topic = listen()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except:
            speak("I couldn't find anything on Wikipedia.")
    elif "open" in command:
        app_name = command.replace("open ", "").strip()
        if app_name in ["youtube", "instagram", "facebook", "twitter"]:
            open_website(app_name)
        else:
            open_application(app_name)
    elif "play" in command and "youtube" in command:
        song = command.replace("play", "").replace("on youtube", "").strip()
        open_website("youtube", song)
    else:
        speak("I didn't catch that. Try again.")

def display_response(response):
    chat_box.insert("end", "Nemo: " + response + "\n", "response")
    chat_box.yview("end")

def display_command(command):
    chat_box.insert("end", command + "\n", "command")
    chat_box.yview("end")

def on_user_input():
    command = user_input.get()
    user_input.set("")
    display_command("You: " + command)
    threading.Thread(target=process_command, args=(command.lower(),)).start()

# GUI Setup
root = ctk.CTk()
root.title("Nemo AI Assistant")
root.geometry("700x750")
root.configure(bg="#121212")

# Header
header = ctk.CTkLabel(root, text="Nemo Desktop Assistant", font=("Segoe UI Bold", 28, "bold"), fg_color="#003049", corner_radius=20, text_color="#edede9")
header.pack(pady=15, padx=10, fill="x")

# Chat Box
chat_frame = ctk.CTkFrame(root, fg_color="#83c5be", corner_radius=15)
chat_frame.pack(pady=10, padx=20, fill="both", expand=True)
chat_box = ctk.CTkTextbox(chat_frame, wrap="word", font=("Arial", 18), fg_color="#006d77", text_color="#edede9")
chat_box.pack(padx=10, pady=10, fill="both", expand=True)
chat_box.tag_config("command", foreground="#edf6f9")
chat_box.tag_config("response", foreground="#ffcc00")

# Input Box
user_input = ctk.StringVar()
input_frame = ctk.CTkFrame(root, fg_color="#1e1e1e", corner_radius=15)
input_frame.pack(pady=10, padx=20, fill="x")
input_box = ctk.CTkEntry(input_frame, textvariable=user_input, font=("Arial", 14), width=500)
input_box.pack(pady=10, padx=10, side="left", expand=True)

# Buttons
button_frame = ctk.CTkFrame(root, fg_color="#1e1e1e", corner_radius=15)
button_frame.pack(pady=10)

speak_button = ctk.CTkButton(button_frame, text="Speak", font=("Arial", 14), fg_color="#ffcc00", text_color="#121212", corner_radius=15, command=lambda: threading.Thread(target=process_command, args=(listen(),)).start())
speak_button.pack(side="left", padx=5)

send_button = ctk.CTkButton(button_frame, text="Send", font=("Arial", 14), fg_color="#00ffcc", text_color="#121212", corner_radius=15, command=on_user_input)
send_button.pack(side="right", padx=5)

# Run GUI
root.mainloop()
