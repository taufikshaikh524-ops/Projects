"""
AI-Powered Voice-Controlled Presentation Assistant
--------------------------------------------------
Features:
- Voice command recognition (start, next, previous, end)
- Natural language intent mapping
- Slide control via keyboard automation
- AI-powered summarization stub (optional)
- Text-to-speech feedback
- Modular structure — all in one file
- Opens your PowerPoint file automatically
- Continuous listening without delay
"""

import speech_recognition as sr
import pyttsx3
import pyautogui
import time
import re
import os

# -------------------------------
# 1. INITIAL SETUP
# -------------------------------
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# -------------------------------
# 2. INTENT DETECTION
# -------------------------------
def detect_intent(command):
    command = command.lower().strip()
    intents = {
        "next": ["next slide", "go next", "forward", "continue", "move ahead"],
        "previous": ["previous slide", "go back", "back", "earlier slide"],
        "start": ["start presentation", "begin slideshow", "start show"],
        "end": ["end presentation", "stop slideshow", "exit presentation"],
        "summarize": ["summarize", "explain", "tell me about this slide"],
        "highlight": ["highlight", "focus", "zoom"],
        "pause": ["pause", "wait", "hold on"]
    }

    for intent, patterns in intents.items():
        for phrase in patterns:
            if re.search(rf"\b{phrase}\b", command):
                return intent
    return "unknown"

# -------------------------------
# 3. ACTION HANDLERS
# -------------------------------
def handle_intent(intent):
    if intent == "next":
        pyautogui.press("right")
        speak("Next slide.")
    elif intent == "previous":
        pyautogui.press("left")
        speak("Previous slide.")
    elif intent == "start":
        pyautogui.press("f5")
        speak("Starting presentation.")
    elif intent == "end":
        pyautogui.press("esc")
        speak("Ending presentation.")
    elif intent == "pause":
        speak("Pausing.")
        time.sleep(2)
    elif intent == "highlight":
        pyautogui.moveRel(50, 0, duration=0.3)
        speak("Highlighting key point.")
    elif intent == "summarize":
        speak("This slide discusses the main insights.")
    else:
        speak("Sorry, I didn't catch that command.")

# -------------------------------
# 4. OPEN PRESENTATION FILE
# -------------------------------
def open_presentation(file_path):
    if os.path.exists(file_path):
        os.startfile(file_path)  # Windows only
        speak("Opening your PowerPoint presentation.")
        time.sleep(5)
    else:
        speak("Presentation file not found. Please check the path.")

# -------------------------------
# 5. CONTINUOUS LISTENING LOOP (Improved)
# -------------------------------
def listen_loop():
    speak("Voice Presentation Assistant ready. Say 'start presentation' to begin.")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        speak("Listening continuously...")
        while True:
            try:
                # Listen for short phrases with small timeout to avoid lag
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=4)
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")
                intent = detect_intent(command)
                handle_intent(intent)
            except sr.WaitTimeoutError:
                # No speech detected quickly, just keep listening
                continue
            except sr.UnknownValueError:
                # Speech detected but not understood
                print("Didn't understand. Listening again...")
                continue
            except sr.RequestError:
                speak("Network error. Check internet connection.")
                time.sleep(2)

# -------------------------------
# 6. MAIN EXECUTION
# -------------------------------
if __name__ == "__main__":
    try:
        speak("Initializing voice assistant...")
        time.sleep(1)
        ppt_path = r"C:\Users\YourName\Documents\MyPresentation.pptx"
        open_presentation(ppt_path)
        listen_loop()
    except KeyboardInterrupt:
        speak("Assistant stopped.")
        print("\nExiting gracefully.")
