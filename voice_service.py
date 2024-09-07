from gtts import gTTS
import tempfile
import threading
import os
import time  # Import time module for delay

def speak(text: str, delay_time: float = 5.0) -> None:
    try:
        # Generate speech using gTTS
        tts = gTTS(text=text, lang='en', slow=False)

        # Save the speech to a file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
            output_file = tmpfile.name
            tts.save(output_file)

        # Play the file (similar to your original function)
        def play_and_remove(file):
            try:
                import pygame
                pygame.mixer.init()

                # Introduce a delay before playing the audio
                print(f"Waiting for {delay_time} seconds before playing audio...")
                #time.sleep(delay_time)  # Delay playback

                pygame.mixer.music.load(file)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            finally:
                pygame.mixer.quit()
                os.remove(file)

        # Start playing the audio file after the delay in a separate thread
        threading.Thread(target=play_and_remove, args=(output_file,), daemon=True).start()

    except Exception as e:
        print(f"Error in gTTS conversion: {e}")
