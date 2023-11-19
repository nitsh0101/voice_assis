import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import webbrowser
import smtplib
import pygame
from datetime import datetime


def get_current_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")


def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Wait for a short time before attempting to remove the file
    pygame.time.wait(500)

    try:
        os.remove("output.mp3")
    except Exception as e:
        print(f"Error removing file: {e}")


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en')
        print(f"User: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't get that. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None


def send_email(receiver, subject, body):
    # You need to set up your email account and password
    sender_email = "avneesh1112@gmail.com"
    sender_password = "Avneesh@8755"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, receiver, message)
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def main():
    speak("Hello! How can I assist you today?")

    while True:
        query = listen()

        if query:
            if "google search" in query:
                query = query.replace("google search", "")
                webbrowser.open(f"https://www.google.com/search?q={query}")
            elif "send email" in query:
                speak("Who is the recipient?")
                recipient = listen()
                speak("What is the subject of the email?")
                subject = listen()
                speak("What should be the content of the email?")
                body = listen()

                if recipient and subject and body:
                    send_email(recipient, subject, body)

            elif "current time" in query:
                get_current_time()
            elif "exit" or "stop" in query:
                speak("Goodbye! Have a nice day.")
                break
            else:
                speak("I'm sorry, I can't perform that action.")


if _name_ == "_main_":
    main()
