import pyttsx3
import threading
import queue

# Initialize the pyttsx3 engine once
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Queue to handle text-to-speech commands sequentially
tts_queue = queue.Queue()

def tts_worker():
    while True:
        text, voice = tts_queue.get()  # Get the next TTS task
        if text is None:
            break  # If None, exit the thread

        # Set the voice
        voices = engine.getProperty('voices')
        for v in voices:
            if voice in v.id:
                engine.setProperty('voice', v.id)
                break

        # Speak the text
        engine.say(text)
        engine.runAndWait()  # Ensure it's done before moving to the next

        tts_queue.task_done()

# Start the TTS worker thread
tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def speak(text: str, voice: str = 'en-US-JennyNeural') -> None:
    try:
        # Add the TTS task to the queue
        tts_queue.put((text, voice))

    except Exception as e:
        print(f"Error in text-to-speech: {e}")

# Optional: Function to stop the TTS thread (if needed)
def stop_tts():
    tts_queue.put((None, None))  # This will signal the thread to stop
