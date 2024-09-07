# voice.py

from FastVoice import speak  # Import the new text-to-speech function

def play_text_to_speech(text, language='en'):
    try:
        # Use the new speak function with 'en-US-JennyNeural' as the default voice
        speak(text, voice='en-US-JennyNeural')
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
