import pandas as pd

df = pd.read_csv("symptoms_data.csv")

def diagnose(user_input):
    user_symptoms = [s.strip().lower() for s in user_input.split(",")]
    matched_diseases = []

    for _, row in df.iterrows():
        disease_symptoms = [s.strip().lower() for s in row['symptoms'].split(";")]
        match_score = sum(symptom in disease_symptoms for symptom in user_symptoms)

        if match_score > 0:
            matched_diseases.append({
                "disease": row['disease'],
                "recommendation": row['recommendation'],
                "match_score": match_score
            })

    matched_diseases.sort(key=lambda x: x['match_score'], reverse=True)

    if matched_diseases:
        return matched_diseases
    else:
        return [{"disease": "Unknown", "recommendation": "Please consult a doctor for diagnosis", "match_score": 0}]
