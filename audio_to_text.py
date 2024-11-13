import speech_recognition as sr
import pyaudio

def recognize_speech():
    # Check if an input device is available
    audio = pyaudio.PyAudio()
    try:
        if audio.get_default_input_device_info():  # Check for default input device
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                audio_data = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio_data)
                print(f"Recognized text: {text}")
                return text
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand the audio."
            except sr.RequestError:
                return "Sorry, the service is down."
        else:
            return "No microphone input device found. Please connect a microphone."
    except OSError as e:
        return "No default input device available. Please check your microphone connection."
    finally:
        audio.terminate()
