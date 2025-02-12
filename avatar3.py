import open3d as o3d
import numpy as np
import speech_recognition as sr
import pyttsx3
from rasa.core.agent import Agent
import logging
from typing import Optional, Tuple
import os
import time

class AvatarSystem:
    def __init__(self, model_path: str = "models/20250207-120145-sparse-rhea.tar.gz"):
        """Initialize the avatar system with all necessary components."""
        self.logger = self._setup_logger()
        self.avatar = None
        self.tts_engine = None
        self.chatbot = None
        self.recognizer = sr.Recognizer()
        # Adjust noise handling for Bluetooth devices
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 400  # Higher threshold for Bluetooth mics
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_adjustment_ratio = 1.5
        
        self.model_path = os.path.abspath(model_path)
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Rasa model not found at: {self.model_path}")

    def _setup_logger(self) -> logging.Logger:
        """Configure logging for the system."""
        logger = logging.getLogger('AvatarSystem')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def load_avatar(self) -> None:
        """Load and configure the 3D avatar model."""
        try:
            self.avatar = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)
            self.avatar.paint_uniform_color([0.5, 0.5, 0.5])
            self.logger.info("Avatar model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load avatar: {str(e)}")
            raise

    def setup_tts(self, rate: int = 150, voice: str = None) -> None:
        """Initialize and configure text-to-speech engine."""
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', rate)
            
            # Get available voices and log them
            voices = self.tts_engine.getProperty('voices')
            self.logger.info(f"Available voices: {[v.name for v in voices]}")
            
            # Set up audio device
            if voice:
                for v in voices:
                    if voice in v.name:
                        self.tts_engine.setProperty('voice', v.id)
                        break
            
            self.logger.info("TTS engine initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS: {str(e)}")
            raise

    def find_bluetooth_device(self) -> Optional[sr.Microphone]:
        """Find and set up Bluetooth audio device."""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            self.logger.info(f"Available audio devices: {mic_list}")
            
            # Look for AirPods or other Bluetooth devices
            bluetooth_keywords = ['airpod', 'bluetooth', 'wireless']
            for idx, name in enumerate(mic_list):
                name_lower = name.lower()
                if any(keyword in name_lower for keyword in bluetooth_keywords):
                    self.logger.info(f"Found Bluetooth device: {name}")
                    return sr.Microphone(device_index=idx)
            
            self.logger.warning("No Bluetooth device found, using default microphone")
            return sr.Microphone()
        except Exception as e:
            self.logger.error(f"Error finding Bluetooth device: {str(e)}")
            return sr.Microphone()

    def speech_to_text(self, timeout: int = 7) -> Tuple[bool, str]:
        """
        Convert speech to text with enhanced Bluetooth support.
        Returns: Tuple of (success: bool, text: str)
        """
        mic = self.find_bluetooth_device()
        try:
            with mic as source:
                self.logger.info("Adjusting for ambient noise...")
                # Longer adjustment period for Bluetooth devices
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                self.logger.info("Listening for input...")
                # Increased timeout and phrase_time_limit for Bluetooth latency
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=10
                )
                
                # Add small delay to handle Bluetooth audio buffering
                time.sleep(0.3)
                
                text = self.recognizer.recognize_google(audio)
                self.logger.info(f"Recognized: {text}")
                return True, text
                
        except sr.WaitTimeoutError:
            self.logger.warning("Listening timed out - Bluetooth device might be disconnected")
            return False, "Listening timed out. Please check your Bluetooth connection."
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio")
            return False, "Could not understand audio. Please speak clearly."
        except sr.RequestError as e:
            self.logger.error(f"Recognition service error: {str(e)}")
            return False, f"Service error: {str(e)}"
        except Exception as e:
            self.logger.error(f"Unexpected error in speech recognition: {str(e)}")
            return False, f"Error: {str(e)}"

    def load_chatbot(self) -> None:
        """Load and initialize the Rasa chatbot."""
        try:
            self.logger.info(f"Loading Rasa model from: {self.model_path}")
            self.chatbot = Agent.load(self.model_path)
            self.logger.info("Chatbot loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load chatbot: {str(e)}")
            raise

    def display_avatar(self) -> None:
        """Display the avatar in a visualization window."""
        if self.avatar:
            o3d.visualization.draw_geometries([self.avatar])
        else:
            self.logger.error("Avatar not loaded")

    def speak_response(self, text: str) -> None:
        """Convert text to speech with Bluetooth optimization."""
        if self.tts_engine and text:
            try:
                # Add small delay before speaking to prevent audio cutoff
                time.sleep(0.2)
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                # Add delay after speaking
                time.sleep(0.2)
            except Exception as e:
                self.logger.error(f"TTS error: {str(e)}")

    def run(self) -> None:
        """Main interaction loop."""
        try:
            self.load_avatar()
            self.setup_tts()
            self.load_chatbot()
            self.display_avatar()

            # Initial connection check
            self.logger.info("Testing audio connection...")
            mic = self.find_bluetooth_device()
            if mic:
                self.speak_response("Audio system ready. You can start speaking.")

            while True:
                success, user_input = self.speech_to_text()
                
                if not success:
                    if "bluetooth" in user_input.lower():
                        self.speak_response("Please check your Bluetooth connection and try again.")
                    else:
                        self.speak_response("I'm sorry, could you repeat that?")
                    continue
                    
                if user_input.lower() in ['exit', 'quit', 'goodbye']:
                    self.speak_response("Goodbye!")
                    break

                if self.chatbot:
                    responses = self.chatbot.handle_text(user_input)
                    if responses and len(responses) > 0:
                        response_text = responses[0]['text']
                        self.speak_response(response_text)
                else:
                    self.logger.error("Chatbot not initialized")
                    break

        except Exception as e:
            self.logger.error(f"Runtime error: {str(e)}")
        finally:
            self.logger.info("Shutting down avatar system")

def main():
    avatar_system = AvatarSystem()
    avatar_system.run()

if __name__ == "__main__":
    main()
