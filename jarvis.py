from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import torch
from torchvision import models, transforms
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import speech_recognition as sr
import sys
import requests
import time
from deep_translator import GoogleTranslator  # Updated translator

root = Tk()
root.title("JARVIS")
root.geometry("400x300")
root["bg"] = "sky blue"

label1 = Label(root, text="JARVIS", bg="dark blue", fg="white", font=300)
label1.pack(padx=20, pady=20)
label1["width"] = 50

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def engine_talk(text):
    engine.say(text)
    engine.runAndWait()

def user_commands():
    command = ''
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            print("Start Speaking!!")
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)  # Set a timeout for listening
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                print("User command:", command)
    except sr.UnknownValueError:
        print("Sorry, I did not understand what you said.")
        engine_talk("Sorry, I did not understand what you said.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        engine_talk("I am having trouble connecting to the speech recognition service.")
    except Exception as e:
        print(f"An error occurred: {e}")
        engine_talk("An error occurred while processing the command.")
    return command

# Function to upload and recognize an image
def upload_and_recognize_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        recognize_image(img)

def recognize_image(img):
    # Preprocess the image
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    img_t = preprocess(img)
    img_t = img_t.unsqueeze(0)  # Add batch dimension

    # Load a pre-trained ResNet model
    model = models.resnet50(pretrained=True)
    model.eval()

    # Predict the object class
    with torch.no_grad():
        output = model(img_t)
    _, predicted_class = output.max(1)

    # Load the class names from the internet
    url = 'https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt'
    response = requests.get(url)
    class_names = response.text.splitlines()

    predicted_label = class_names[predicted_class.item()]

    # Speak out the result
    engine_talk(f'The object in the image is {predicted_label}')
    print(f'The object in the image is: {predicted_label}')

# Function to translate Sanskrit to English using deep_translator
def translate_sanskrit_to_english(text):
    try:
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        engine_talk(f'The English translation is: {translated_text}')
        print(f'Translated Text: {translated_text}')
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        engine_talk("Sorry, I couldn't translate the text.")

# Function to run Jarvis and handle commands
def run_jarvis():
    while True:
        command = user_commands()
        if command:
            if 'play' in command:
                song = command.replace('play', '')
                engine_talk('Playing' + song)
                pywhatkit.playonyt(song)
            elif 'name' in command:
                engine_talk("Hi, I am Jarvis.")
                print("Hi, I am Jarvis.")
            elif 'what can you do' in command:
                x = ("I can play songs on YouTube, tell the time, "
                     "tell a joke, search things on Google, detect objects in images, "
                     "and translate Sanskrit to English.")
                engine_talk(x)
                print(x)
            elif 'time' in command:
                current_time = datetime.datetime.now().strftime('%H:%M %p')
                engine_talk('The current time is ' + current_time)
                print(current_time)
            elif 'who is' in command:
                name = command.replace('who is', '')
                info = wikipedia.summary(name, 1)
                print(info)
                engine_talk(info)
            elif 'joke' in command:
                engine_talk(pyjokes.get_joke())
            elif 'detect an image' in command:
                engine_talk('Please upload an image')
                upload_and_recognize_image()
            elif 'convert to english' in command:  # Check for "convert to English"
                engine_talk('Please paste the Sanskrit text in the terminal below:')
                sanskrit_text = input("Paste the Sanskrit text: ")
                translate_sanskrit_to_english(sanskrit_text)
            elif 'stop' in command:
                engine_talk('Goodbye!')
                root.destroy()
                sys.exit()
            else:
                engine_talk('I could not understand your command.')
        time.sleep(1)  # Add a short delay before the next attempt to listen

# Speak button to start Jarvis
button1 = Button(root, text="Speak", bg="dark blue", fg="white", font=300, command=run_jarvis)
button1.pack(padx=20, pady=100)
button1["width"] = 25

root.mainloop()