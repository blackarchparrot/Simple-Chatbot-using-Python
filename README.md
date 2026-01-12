# Simple-Chatbot-using-Python

**AI Voice Chatbot with Typing Animation & Chat Bubbles**

A desktop voice-enabled AI chatbot built in Python with a WhatsApp-style chat interface, featuring:

Gradual typing animation (letter-by-letter like ChatGPT)

Voice input (speech-to-text)

Voice output (text-to-speech)

Chat bubbles for a modern UI

Short-term and long-term memory (conversation saved to file)

Time & date query support

Weather information (free, no API key required)

Demo

Bot types replies gradually while user watches, can speak them aloud, and responds to voice input.

Features
Feature	Description
Typing Animation	Bot types letter-by-letter for a realistic ChatGPT feel
Voice Input	Press 🎤 button to speak, converted to text
Voice Output	Bot replies are spoken aloud
Chat Bubbles	WhatsApp-style chat bubbles, user right / bot left
Long-Term Memory	Saves last 20 messages to chat_memory.json
Time & Date	Ask the bot for current time or date
Weather	Ask "weather in [city]" — powered by free wttr.in
Cross-Platform	Works on Windows, Linux, FydeOS
Requirements

Python 3.8+

Libraries:
```
pip install openai speechrecognition pyttsx3 pyaudio requests
```

Linux / FydeOS (for pyaudio):
```
sudo apt install portaudio19-dev
```
```
pip install pyaudio
```

Microphone & speaker for voice features

Setup

Clone or download the repository

**Set your OpenAI API key**

No weather API key is required. The bot uses free wttr.in.

Run the chatbot:
```
python bot.py
```
# Usage

Typing: Type a message in the input box and press Send

Voice Input: Press 🎤 button to speak

Time/Date: Ask “What time is it?” or “What is today’s date?”

Weather: Ask “Weather in Dhaka” or any city

Exit: Close the window to quit

File Structure
project/
│
├─ bot.py                      # Main Python script
├─ chat_memory.json            # Saved conversation (auto-generated)
├─ README.md                   # This file

# Notes

Typing speed: Adjustable via root.after(30, ...) (smaller number → faster)

Memory: Saves last 20 messages by default

Weather: Free and works worldwide using wttr.in

Voice: Input requires working microphone; output uses system TTS

Future Improvements

Dark mode support

Avatar icons for user/bot

Typing indicator (animated dots)

Mobile / web interface

Multi-language support
