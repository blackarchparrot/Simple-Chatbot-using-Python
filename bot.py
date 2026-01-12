import tkinter as tk
from tkinter import Frame, Canvas, Scrollbar
from openai import OpenAI
import speech_recognition as sr
import pyttsx3
import requests
import os, json
from datetime import datetime

OPENAI_API_KEY="your_openai_key"
rate = 1

MEMORY_FILE = "chat_memory.json"
client = OpenAI()

engine = pyttsx3.init()
engine.setProperty(rate, 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as src:
        r.adjust_for_ambient_noise(src)
        audio = r.listen(src)
    try:
        return r.recognize_google(audio)
    except:
        return None

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE) as f:
            return json.load(f)
    return [{"role": "system", "content": "You are a helpful assistant."}]

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages[-20:], f, indent=2)

messages = load_memory()

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=5)
        return response.text
    except:
        return "Sorry, I couldn't get the weather right now."

def process_message(text):
    lower = text.lower()

    if "time" in lower or "date" in lower:
        return datetime.now().strftime("📅 %A, %d %B %Y\n⏰ %I:%M %p")

    if "weather" in lower:
        city = lower.replace("weather", "").replace("in", "").strip()
        return get_weather(city)

    messages.append({"role": "user", "content": text})
    res = client.responses.create(
        model="gpt-5-nano",
        input=messages
    )
    reply = res.output_text
    messages.append({"role": "assistant", "content": reply})
    save_memory()
    return reply

root = tk.Tk()
root.title("AI Chatbot")
root.geometry("520x650")
root.configure(bg="white")

canvas = Canvas(root, bg="white")
scrollbar = Scrollbar(root, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="top", fill="both", expand=True)

chat_frame = Frame(canvas, bg="white")
canvas.create_window((0, 0), window=chat_frame, anchor="nw")

chat_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

def create_bubble(sender):
    bg = "#F1F1F1" if sender == "bot" else "#0084FF"
    fg = "black" if sender == "bot" else "white"

    bubble = Frame(chat_frame, bg=bg, padx=10, pady=6)
    label = tk.Label(
        bubble,
        text="",
        bg=bg,
        fg=fg,
        wraplength=300,
        justify="left",
        font=("Arial", 11)
    )
    label.pack()

    bubble.pack(
        anchor="w" if sender == "bot" else "e",
        pady=5,
        padx=10
    )

    canvas.update_idletasks()
    canvas.yview_moveto(1)
    return label

is_typing = False

def type_writer(label, text, i=0):
    global is_typing

    if i == 0:
        is_typing = True
        entry.config(state="disabled")

    if i < len(text):
        label.config(text=label.cget("text") + text[i])
        root.after(30, lambda: type_writer(label, text, i + 1))
    else:
        is_typing = False
        entry.config(state="normal")
        speak(text)

def send_text():
    global is_typing
    if is_typing:
        return

    text = entry.get().strip()
    if not text:
        return

    entry.delete(0, tk.END)

    user_label = create_bubble("user")
    user_label.config(text=text)

    reply = process_message(text)

    bot_label = create_bubble("bot")
    type_writer(bot_label, reply)

def voice_input():
    global is_typing
    if is_typing:
        return

    bot_label = create_bubble("bot")
    bot_label.config(text="🎤 Listening...")

    text = listen()
    if not text:
        bot_label.config(text="❌ Couldn't hear")
        return

    user_label = create_bubble("user")
    user_label.config(text=text)

    reply = process_message(text)

    bot_label = create_bubble("bot")
    type_writer(bot_label, reply)

bottom = Frame(root, bg="white")
bottom.pack(fill="x", pady=6)

entry = tk.Entry(bottom, font=("Arial", 12))
entry.pack(side="left", expand=True, fill="x", padx=6)

tk.Button(bottom, text="Send", command=send_text).pack(side="left")
tk.Button(bottom, text="🎤", command=voice_input).pack(side="left")

welcome = create_bubble("bot")
type_writer(welcome, "👋 Hello! I type replies just like ChatGPT.")

root.mainloop()
