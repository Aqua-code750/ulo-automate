import speech_recognition as sr
import threading

def listen_in_background(callback):
    """
    Listens for speech in the background and returns the text via a callback.
    """
    def _listen():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                text = r.recognize_google(audio)
                callback(text, None)
            except sr.WaitTimeoutError:
                callback(None, "Listening timed out.")
            except sr.UnknownValueError:
                callback(None, "Could not understand audio.")
            except sr.RequestError as e:
                callback(None, f"Could not request results; {e}")
            except Exception as e:
                callback(None, f"Error: {e}")
                
    t = threading.Thread(target=_listen)
    t.start()
