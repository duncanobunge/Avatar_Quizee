# Interactive Avatar Assistant

An interactive 3D avatar system that combines speech recognition, text-to-speech, and natural language processing to create an engaging conversational interface. The avatar responds to voice commands and queries using a trained Rasa chatbot model, providing both visual and audio feedback.

## Features

- 🎭 3D Avatar Visualization using Open3D
- 🎤 Speech Recognition with support for various audio inputs
- 🔊 Text-to-Speech capabilities
- 🤖 Natural Language Processing using Rasa
- 🎧 Support for various audio devices (including Bluetooth headsets/AirPods)
- 📝 Comprehensive logging system
- ⚡ Real-time interaction

## Prerequisites

```bash
python 3.8+
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/interactive-3d-avatar.git
cd interactive-3d-avatar
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Required Packages

```plaintext
open3d
numpy
SpeechRecognition
pyttsx3
rasa
pyaudio
```

## Project Structure

```
interactive-3d-avatar/
├── models/                     # Rasa model files
│   └── 20250207-120145-sparse-rhea.tar.gz
├── rasa/                      # Rasa configuration files
│   ├── config.yml
│   ├── domain.yml
│   ├── data/
│   │   ├── nlu.yml
│   │   └── stories.yml
├── src/
│   ├── avatar_system.py       # Main avatar system implementation
│   ├── test_mic.py           # Microphone testing utility
│   └── test_tts.py           # Text-to-speech testing utility
├── requirements.txt
└── README.md
```

## Setting Up Rasa

1. Train the Rasa model:
```bash
cd rasa
rasa train
```

2. The trained model will be saved in the `models` directory.

## Usage

1. Run the main avatar system:
```bash
python src/avatar_system.py
```

2. Test specific components:
```bash
# Test microphone
python src/test_mic.py

# Test text-to-speech
python src/test_tts.py
```

## Supported Voice Commands

The avatar can respond to various commands including:
- Greetings ("hello", "hi")
- Questions about its capabilities ("what can you do?")
- Small talk ("how are you?")
- Farewells ("goodbye", "exit")

## Audio Device Support

The system supports various audio input/output devices:
- Built-in microphones
- External headsets
- Bluetooth devices (including AirPods)
- USB audio interfaces

### Bluetooth Device Configuration

For Bluetooth devices (like AirPods):
1. Connect your device to your computer
2. Set it as the default input/output device in your system settings
3. The avatar system will automatically detect and use the Bluetooth device

## Troubleshooting

### Common Issues

1. No audio input detected:
   - Check microphone permissions
   - Verify default audio input device
   - Test with `test_mic.py`

2. No audio output:
   - Check speaker/headphone connection
   - Verify default audio output device
   - Test with `test_tts.py`

3. Avatar not displaying:
   - Verify Open3D installation
   - Check graphics drivers
   - Try running with administrative privileges

### Logging

The system generates detailed logs for troubleshooting. Check the console output for:
- Audio device detection
- Speech recognition status
- Chatbot responses
- Error messages

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Open3D for 3D visualization
- Rasa for natural language processing
- Google Speech Recognition API
- pyttsx3 for text-to-speech capabilities

## Contact

Your Name - [@duncanobunge](https://github.com/duncanobunge/Avatar_Quizee)

Project Link: [[https://github.com/duncanobunge/interactive-3d-avatar](https://github.com/duncanobunge/Avatar_Quizee/)]([https://github.com/duncanobunge/interactive-3d-avatar](https://github.com/duncanobunge/Avatar_Quizee/))
