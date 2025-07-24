import streamlit as st
import random
import pyttsx3
import speech_recognition as sr
from googletrans import Translator

# ----------------- Config ----------------- #
st.set_page_config(page_title="SwasthyaBot", page_icon="🩺", layout="centered")

# ----------------- Styles ----------------- #
st.markdown("""
    <style>
        html, body, [class*="css"]  {
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

# ----------------- Translator ----------------- #
translator = Translator()

def translate(text, lang_code):
    try:
        return translator.translate(text, dest=lang_code).text
    except:
        return "Translation failed."

# ----------------- Branding ----------------- #
st.markdown("<h1 style='text-align: center; color: #8B5CF6;'>🩺 SwasthyaBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>AI-Powered Rural Health Diagnostic Chatbot</p>", unsafe_allow_html=True)
st.markdown("---")

# ----------------- Health Tip ----------------- #
tips = [
    "Stay hydrated 🥤", "Avoid junk food 🍔", "Wash hands 🧼",
    "Sleep 7+ hours 😴", "Eat fruits & veggies 🍎", "Exercise daily 🏃"
]
st.info(f"💡 Health Tip: {random.choice(tips)}")

# ----------------- Diagnosis Logic ----------------- #
def diagnose(symptoms):
    symptoms = [s.strip().lower() for s in symptoms]
    if "fever" in symptoms and "cough" in symptoms:
        return {"disease": "Flu", "advice": "Take rest and stay hydrated. Use paracetamol if needed."}
    elif "headache" in symptoms and "nausea" in symptoms:
        return {"disease": "Migraine", "advice": "Avoid light and noise. Rest and drink fluids."}
    elif "stomach pain" in symptoms:
        return {"disease": "Gastritis", "advice": "Avoid spicy foods. Drink plenty of water."}
    elif "fever" in symptoms:
        return {"disease": "Mild Viral", "advice": "Rest and monitor temperature."}
    else:
        return {"disease": "Unknown", "advice": "Consult a doctor for better diagnosis."}

# ----------------- TTS ----------------- #
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ----------------- STT ----------------- #
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

# ----------------- Input Form ----------------- #
st.subheader("😷 Describe your symptoms")
st.markdown("Enter symptoms separated by commas (e.g., <code>fever, cough</code>)", unsafe_allow_html=True)

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
    result = diagnose(symptom_input.split(','))
    st.success(f"🦠 Possible Condition: **{result['disease']}**")
    st.info(f"📌 Recommendation: {result['advice']}")
    
    # Speak in English
    speak(f"Possible disease is {result['disease']}. Recommendation: {result['advice']}")

    # Translations
    st.markdown("---")
    st.markdown("🌐 **Translations**")
    st.markdown(f"👉 **Hindi:**\n- बीमारी: `{translate(result['disease'], 'hi')}`\n- सलाह: `{translate(result['advice'], 'hi')}`")
    st.markdown(f"👉 **Odia (ଓଡ଼ିଆ):**\n- ରୋଗ: `{translate(result['disease'], 'or')}`\n- ପରାମର୍ଶ: `{translate(result['advice'], 'or')}`")

# ----------------- Doctor List ----------------- #
st.markdown("---")
st.subheader("👨‍⚕️ Nearby Doctors (Sample)")
doctor_data = [
    {"name": "Dr. Suresh Kumar", "specialty": "General Physician", "location": "Gunupur CHC"},
    {"name": "Dr. Priya Mohanty", "specialty": "Pediatrician", "location": "Rayagada DHH"},
    {"name": "Dr. Anil Rath", "specialty": "ENT Specialist", "location": "JK Pur Clinic"},
    {"name": "Dr. Swapna Rani", "specialty": "Gynecologist", "location": "Gunupur Private Hospital"}
]

for doc in doctor_data:
    st.markdown(f"🔹 **{doc['name']}**  \n🩺 {doc['specialty']}  \n📍 {doc['location']}")

