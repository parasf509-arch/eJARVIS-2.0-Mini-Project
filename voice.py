
import speech_recognition as sr
import subprocess
import base64


class VoiceAssistant:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        """Use Windows built-in speech engine."""

        try:
            # Convert message into Base64 for safe PowerShell transfer
            message_bytes = text.encode("utf-8")
            encoded_message = base64.b64encode(
                message_bytes
            ).decode("ascii")

            script = f"""
            Add-Type -AssemblyName System.Speech

            $message = [Text.Encoding]::UTF8.GetString(
                [Convert]::FromBase64String('{encoded_message}')
            )

            $speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $speaker.Volume = 100
            $speaker.Rate = 0
            $speaker.Speak($message)
            $speaker.Dispose()
            """

            encoded_script = base64.b64encode(
                script.encode("utf-16le")
            ).decode("ascii")

            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-EncodedCommand",
                    encoded_script
                ],
                capture_output=True,
                text=True,
                timeout=40
            )

            if result.returncode != 0:
                print("Speech error:", result.stderr)
                return False

            return True

        except Exception as error:
            print("Voice output error:", error)
            return False

    def listen(self):
        try:
            with sr.Microphone() as source:

                print("Listening...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.7
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=8,
                    phrase_time_limit=8
                )

            try:
                return self.recognizer.recognize_google(
                    audio,
                    language="en-IN"
                )

            except sr.UnknownValueError:
                return self.recognizer.recognize_google(
                    audio,
                    language="hi-IN"
                )

        except sr.WaitTimeoutError:
            return "No speech detected. Please try again."

        except sr.UnknownValueError:
            return "Sorry, I could not understand your voice."

        except sr.RequestError:
            return "Internet connection is required for voice recognition."

        except OSError:
            return "Microphone not detected. Please check your microphone."

        except Exception as error:
            return f"Voice error: {error}"
