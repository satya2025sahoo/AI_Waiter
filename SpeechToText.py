import speech_recognition as sr
from mtranslate import translate
from colorama import Fore, init
import time

# Initialize colorama
init(autoreset=True)

def translate_hindi_to_english(txt):
    try:
        english_txt = translate(txt, to_language='en')
        return english_txt
    except Exception as e:
        print(Fore.RED + f"Translation error: {e}")
        return txt

def listen_and_translate():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 3000  # Adjust as needed

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            print(Fore.LIGHTGREEN_EX + 'Listening...')

            try:
                # Listen with a timeout for a reasonable duration
                audio = recognizer.listen(source, timeout=10)  # Increased timeout to make listening more controlled
                print(Fore.LIGHTYELLOW_EX + "Recognizing...")

                recognized_txt = recognizer.recognize_google(audio, language="hi-IN").lower()
                print(Fore.CYAN + "Recognized: " + recognized_txt)

                translated_txt = translate_hindi_to_english(recognized_txt)
                print(Fore.BLUE + "Translated: " + translated_txt)

                return translated_txt

            except sr.UnknownValueError:
                print(Fore.RED + "Sorry, I didn't catch that.")
                # Sleep for a short period before attempting to listen again
                time.sleep(4)  # Adjust the sleep duration as needed

            except sr.RequestError as e:
                print(Fore.RED + f"Could not request results; {e}")
                return None  # Exit the loop if there is an API request error

            # Introduce a delay between listening attempts to reduce continuous listening
            time.sleep(6)  # Adjust the sleep duration as needed
