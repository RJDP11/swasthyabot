PPT: [swasthyabot(Team(CLB)_3_16).pptx](https://github.com/user-attachments/files/21417439/swasthyabot.Team.CLB._3_16.pptx)

👨‍💻 Team CLB_3_16:
   Rajdeep Patnaik,
   Abinash Panda,
   Arpit Pradhan,
   Anmol Sahu,
  ---------------------
# 🩺 SwasthyaBoT
**SwasthyaBot** is a multilingual AI-powered healthcare chatbot built for rural and semi-urban India. It helps users diagnose common health issues through symptom-based input — supporting **voice**, **translation**, and **Ayurvedic remedies** in **English, Hindi, and Odia**. Designed with simplicity, accessibility, and offline-friendliness in mind.



## 🌟 Features

- 🎙️ **Speech-to-Text**: Speak your symptoms — supports Hindi, Odia, and English.
- 🧾 **Text Diagnosis**: Enter multiple symptoms via text for accurate suggestions.
- 🌿 **Ayurvedic Remedies**: Local home-based suggestions for common illnesses.
- 🌐 **Multilingual Output**: Translates advice to user's chosen language.
- 🔈 **Text-to-Speech**: Speaks out diagnosis and advice for non-literate users.
- 🧑‍⚕️ **Local Doctor Listing**: Filters doctors by Rayagada district blocks like Gunupur and Bissam Cuttack.



## 🧠 Technologies Used

- `Python`
- `Streamlit` – UI Framework
- `SpeechRecognition` – Speech to Text
- `gTTS` – Text to Speech
- `Googletrans` – Language Translation
- `Base64` – Audio Embedding
- `Pyaudio` – Microphone Support



## 🛠️ Setup Instructions

### ✅ Prerequisites

- Python 3.8 or above
- pip (Python package manager)
- Microphone-enabled device (for speech input)
- Internet connection (for TTS & translation)

### 📦 Install Dependencies

```bash
pip install streamlit
pip install SpeechRecognition
pip install gTTS
pip install googletrans==4.0.0-rc1
pip install pyaudio

#run the app
streamlit run swasthyabot.py


_________________________________________
##Project Structure*

swasthyabot/
├── swasthyabot.py       # Main application code
├── README.md            # Project documentation
├── requirements.txt     # Optional: package list
└── assets/              # (Optional) Images or audio assets
