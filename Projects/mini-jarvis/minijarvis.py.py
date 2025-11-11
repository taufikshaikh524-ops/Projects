import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
from PIL import Image

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # female voice (try 0 for male)

# Initialize Speech Recognizer
recognizer = sr.Recognizer()

# Create Main Window
window = ctk.CTk()
window.title("Mini Jarvis Assistant")
window.geometry("950x600")
ctk.set_appearance_mode("dark")

# ======= FUNCTIONS =======

def speak(text):
    chat_box.insert("end", f"🤖 Jarvis: {text}\n", "jarvis")
    chat_box.see("end")
    engine.say(text)
    engine.runAndWait()

def set_status(text, color="#00ff00"):
    status_label.configure(text=text, text_color=color)
    window.update_idletasks()

def update_chat(role, text):
    if role == "You":
        chat_box.insert("end", f"\n🧍 You: {text}\n", "user")
    else:
        chat_box.insert("end", f"🤖 Jarvis: {text}\n", "jarvis")

    chat_box.tag_config("user", foreground="#00bfff")  # Blue for user
    chat_box.tag_config("jarvis", foreground="#00ff99")  # Green for Jarvis
    chat_box.see("end")

def process_command(command):
    command = command.lower()

    if "hello" in command:
        speak("Hi there! How can I help you today?")
    elif "your name" in command:
        speak("My name is Mini Jarvis.")
    elif "how are you" in command:
        speak("I'm doing great! Thanks for asking.")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "date" in command or "today" in command:
        today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today_date}.")
    elif "open google" in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching for {query} on Google.")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("Please tell me what to search for.")
    elif "youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
    elif "notepad" in command:
        speak("Opening Notepad...")
        os.system("notepad.exe")
    elif "exit" in command or "stop" in command:
        speak("Goodbye! Have a nice day!")
        window.destroy()
    else:
        speak("Sorry, I didn’t understand that command yet.")

def listen_voice():
    set_status("🎤 Listening...", "#ffff00")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    set_status("🟢 Online", "#00ff00")

    try:
        text = recognizer.recognize_google(audio)
        update_chat("You", text)
        process_command(text)
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that.")
    except sr.RequestError:
        speak("Speech service not available.")

def send_text():
    user_input = entry_box.get().strip()
    if user_input:
        update_chat("You", user_input)
        entry_box.delete(0, "end")
        process_command(user_input)

def clear_chat():
    chat_box.delete("1.0", "end")

def update_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    time_label.configure(text=f"⏰ {now}")
    window.after(1000, update_time)

# ======= LEFT SIDEBAR =======
sidebar = ctk.CTkFrame(window, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

title_label = ctk.CTkLabel(sidebar, text="🤖 MINI JARVIS", font=("Arial Rounded MT Bold", 20))
title_label.pack(pady=(30, 10))

divider = ctk.CTkLabel(sidebar, text="------------------------------", text_color="#555")
divider.pack()

user_label = ctk.CTkLabel(sidebar, text="🧍 User: Taufik", font=("Arial", 14))
user_label.pack(pady=(10, 5))

status_label = ctk.CTkLabel(sidebar, text="🟢 Online", font=("Arial", 14), text_color="#00ff00")
status_label.pack()

# Profile Image
try:
    profile_image = ctk.CTkImage(
        light_image=Image.open("jarvis.png"),
        dark_image=Image.open("jarvis.png"),
        size=(100, 100)
    )
    profile_label = ctk.CTkLabel(sidebar, text="", image=profile_image)
    profile_label.pack(pady=20)
except Exception:
    pass

# Buttons
clear_btn = ctk.CTkButton(sidebar, text="🧹 Clear Chat", width=180, command=clear_chat)
clear_btn.pack(pady=10)

exit_btn = ctk.CTkButton(sidebar, text="🔴 Exit", width=180, fg_color="#ff4d4d",
                         hover_color="#ff1a1a", command=window.destroy)
exit_btn.pack(pady=5)

# Time Label
time_label = ctk.CTkLabel(sidebar, text="", font=("Arial", 14))
time_label.pack(pady=(30, 10))
update_time()

# ======= MAIN AREA =======
main_frame = ctk.CTkFrame(window)
main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

chat_box = ctk.CTkTextbox(main_frame, font=("Consolas", 13), corner_radius=10,
                          fg_color="#1f1f1f", text_color="white")
chat_box.pack(expand=True, fill="both", padx=10, pady=10)

entry_frame = ctk.CTkFrame(main_frame)
entry_frame.pack(fill="x", padx=10, pady=10)

entry_box = ctk.CTkEntry(entry_frame, placeholder_text="Type your command here...",
                         height=40, corner_radius=10)
entry_box.pack(side="left", fill="x", expand=True, padx=5)

send_button = ctk.CTkButton(entry_frame, text="Send", width=80, command=send_text)
send_button.pack(side="left", padx=5)

mic_button = ctk.CTkButton(entry_frame, text="🎤 Speak", width=80, command=listen_voice)
mic_button.pack(side="left", padx=5)

# ======= START APP =======
window.mainloop()
