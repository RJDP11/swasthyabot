import streamlit as st
import random
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import tempfile
import os
import base64

# Page config
st.set_page_config(page_title="SwasthyaBot", page_icon="🩺", layout="centered")

# Translator
translator = Translator()

# Style
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #111827;
            color: #E5E7EB;
        }
        .main {
            padding: 20px;
        }
        .stButton>button {
            background-color: #1E293B;
            color: white;
            border: 1px solid #3B82F6;
            padding: 0.5em 1em;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; color: #8B5CF6;'>🩺 SwasthyaBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>AI-Powered Rural Health Diagnostic Chatbot</p>", unsafe_allow_html=True)
st.markdown("---")

# Health tip
tips = [
    "Stay hydrated 🥤", "Avoid junk food 🍔", "Wash hands 🧼",
    "Sleep 7+ hours 😴", "Eat fruits & veggies 🍎", "Exercise daily 🏃"
]
st.info(f"💡 Health Tip: {random.choice(tips)}")

# -------------------- Diagnosis --------------------
def diagnose(symptoms):
    symptoms = [s.strip().lower() for s in symptoms]
    if "fever" in symptoms and "cough" in symptoms:
        return {"disease": "Flu", "advice": "Drink tulsi-ginger tea, rest well, take warm liquids."}
    elif "headache" in symptoms and "nausea" in symptoms:
        return {"disease": "Migraine", "advice": "Apply sandalwood paste on forehead, avoid sunlight, rest."}
    elif "headache" in symptoms:
        return {"disease": "Headache", "advice": "Drink ginger tea, massage forehead with peppermint oil, rest."}
    elif "stomach pain" in symptoms:
        return {"disease": "Gastritis", "advice": "Drink jeera water, avoid spicy food, eat curd rice."}
    elif "fever" in symptoms:
        return {"disease": "Mild Viral", "advice": "Drink giloy kadha, take rest, eat light food."}
    elif "cough" in symptoms:
        return {"disease": "Cold/Cough", "advice": "Use steam inhalation, honey with tulsi juice, avoid cold food."}
    else:
        return {"disease": "Unknown", "advice": "Consult a doctor for accurate diagnosis."}


# -------------------- TTS --------------------
def speak(text, lang_code="en"):
    try:
        tts = gTTS(text=text, lang=lang_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            audio_path = tmp.name

        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            b64 = base64.b64encode(audio_bytes).decode()
            audio_tag = f"""
                <audio autoplay controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_tag, unsafe_allow_html=True)
        os.remove(audio_path)
    except Exception as e:
        st.error(f"TTS failed: {e}")

# -------------------- STT --------------------
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        try:
            audio = r.listen(source, timeout=5)
            return r.recognize_google(audio)
        except:
            st.warning("❌ Could not recognize speech")
            return None

# -------------------- UI --------------------
st.subheader("😷 Describe your symptoms")
st.markdown("Enter symptoms separated by commas (e.g., <code>fever, cough</code>)", unsafe_allow_html=True)

lang_choice = st.selectbox("🌐 Select Language", ["English", "Hindi", "Odia"])
lang_map = {"English": "en", "Hindi": "hi", "Odia": "or"}
lang_code = lang_map[lang_choice]

symptom_input = st.text_input("📝 Your Symptoms")
submit = st.button("🔍 Check Diagnosis")
mic_btn = st.button("🎙️ Use Mic to Speak Symptoms")

if mic_btn:
    spoken = recognize_speech()
    if spoken:
        st.success(f"You said: {spoken}")
        symptom_input = spoken
        submit = True

if submit and symptom_input:
    # ✨ Translate non-English input to English before diagnosis
    if lang_code != "en":
        translated_input = translator.translate(symptom_input, dest="en").text
        translated_symptoms = translated_input.split(",")
    else:
        translated_symptoms = symptom_input.split(",")

    result = diagnose(translated_symptoms)
    st.success(f"🦠 Possible Condition: **{result['disease']}**")
    st.info(f"📌 Ayurvedic Advice: {result['advice']}")

    translated_disease = translator.translate(result['disease'], dest=lang_code).text
    translated_advice = translator.translate(result['advice'], dest=lang_code).text

    st.markdown("---")
    st.markdown(f"🌐 **Translated Output ({lang_choice})**")
    st.markdown(f"- बीमारी: `{translated_disease}`")
    st.markdown(f"- सलाह: `{translated_advice}`")

    speak(f"{translated_disease}. {translated_advice}", lang_code=lang_code)

# -------------------- Doctor List --------------------
st.markdown("---")
st.subheader("👨‍⚕️ Find Doctors in Rayagada District")

blocks = ["All", "Gunupur", "Bissam Cuttack"]
selected_block = st.selectbox("📍 Filter by Block", blocks)

doctor_data = [
    {"name": "Dr. Suresh Kumar", "specialty": "General Physician", "location": "Gunupur"},
    {"name": "Dr. Priya Mohanty", "specialty": "Pediatrician", "location": "Rayagada"},
    {"name": "Dr. Anil Rath", "specialty": "ENT Specialist", "location": "JK Pur"},
    {"name": "Dr. Swapna Rani", "specialty": "Gynecologist", "location": "Gunupur"},
    {"name": "Dr. Manas Padhi", "specialty": "Homeopathy", "location": "Bissam Cuttack"},
    {"name": "Dr. Laxmi Naik", "specialty": "Ayurveda", "location": "Bissam Cuttack"},
]

for doc in doctor_data:
    if selected_block == "All" or selected_block.lower() in doc["location"].lower():
        st.markdown(f"🔹 **{doc['name']}**  \n🩺 {doc['specialty']}  \n📍 {doc['location']}")
