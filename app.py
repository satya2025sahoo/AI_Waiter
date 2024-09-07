import os
import wave
import pyaudio
import FastVoice  # Updated to import the new voice module
from SpeechToText import listen_and_translate  # Import the speech-to-text function
from AI import AIVoiceAssistant
import time

ai_assistant = AIVoiceAssistant()

def main():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    customer_input_transcription = ""

    try:
        while True:
            print("_")

            # Use the new speech-to-text function (listen and translate)
            transcription = listen_and_translate()  # Listen and translate to English
            if transcription:
                print(f"Customer: {transcription}")
                
                # Add customer input to transcript
                customer_input_transcription += "Customer: " + transcription + "\n"
                
                # Process customer input and get response from AI assistant
                output = ai_assistant.interact_with_llm(transcription)
                if output:
                    output = output.lstrip()  # Clean leading spaces
                    
                    # Pause microphone input here (close the stream)
                    stream.stop_stream()

                    # Use the voice module to convert text-to-speech
                    FastVoice.speak(output, 'en-US-JennyNeural')
                    print(f"AI Assistant: {output}")

                    # Wait until TTS is done (give some delay to avoid premature listening)
                    time.sleep(2)  # Adjust this as needed for longer TTS responses

                    # Resume microphone input (restart the stream)
                    stream.start_stream()

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    main()
