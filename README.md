# Vedic-Astro-Therapist-app
# ✨ Vedic Astro-Therapist 🌙

Welcome to the **Vedic Astro-Therapist** – an AI-powered spiritual and emotional guidance app rooted in the principles of **Vedic astrology** (Jyotisha). This project blends ancient Indian cosmic wisdom with modern artificial intelligence (NLP via Hugging Face) to deliver **personalized daily horoscopes** based on your Moon Nakshatra.

---

## 🧠 What It Does

✨ This app analyzes your:
- 📅 Date of Birth
- 🕒 Time of Birth
- 📍 Place of Birth

Using this information, it:
1. Calculates your **Moon's sidereal position** (as per Lahiri Ayanamsa).
2. Determines your **Moon Nakshatra (birth star)** and **Rashi (zodiac sign)**.
3. Retrieves emotional traits, challenges, and mantras associated with that Nakshatra.
4. Determines today’s **current Moon Nakshatra**.
5. Generates a **personalized, poetic daily horoscope** using **AI (Mistral-7B from Hugging Face)**.
6. Infers and displays a **mood vibe color** (Peaceful, Balanced, or Intense).

---

## 🧘 What is Vedic Astrology?

**Vedic astrology** (Jyotisha) is an ancient Indian system that uses sidereal (star-based) calculations. Unlike Western astrology, which is solar-focused, Vedic astrology gives prime importance to the **Moon** — specifically the **Nakshatra** (constellation) the Moon resides in at your time of birth.

- There are **27 Nakshatras**, each with its own deity, personality, emotional style, and challenges.
- Vedic thought believes your **Moon Nakshatra defines your inner world**, subconscious drives, and emotional intelligence.

This app uses **Ashwini to Revati** Nakshatras with curated **emotional traits**, **common challenges**, and **healing mantras**.

---

## ⚙️ How It Works

### 🔭 Astrology Engine
- Uses the [`swisseph`](https://pypi.org/project/pyswisseph/) library to calculate precise astronomical positions.
- Sidereal positions are used (Lahiri ayanamsa) for Moon longitude and Nakshatra determination.

### 🌐 Geolocation
- Geocodes your birth city using [`geopy`](https://pypi.org/project/geopy/) and [`timezonefinder`](https://pypi.org/project/timezonefinder/) to localize your time.

### 🤖 AI Horoscope Generation
- Uses **`mistralai/Mistral-7B-Instruct-v0.1`** model from Hugging Face via `InferenceClient`.
- A prompt is crafted using your Nakshatra traits + today’s moon constellation.
- Horoscope begins with a salutation (`Dear Seeker` or `Dear [name]`) and ends with a **recommended mantra**.

### 🎨 Mood Vibe Indicator
- Based on the horoscope text, keywords like “calm”, “challenge”, or “growth” are detected.
- The app assigns a **color-coded pulse box**:
  - 🟢 **Peaceful** = calm, relaxing, harmonious
  - 🟡 **Balanced** = growth, awareness, aligned
  - 🔴 **Intense** = transformative, energetic, challenging

---

## 🌟 Features

- 🧘 **Moon-based personalized daily horoscope**
- 📿 **Healing mantra** and emotional remedies
- 🌙 **Nakshatra emotional trait profiling**
- 🎨 **Animated mood color badge** (auto-inferred)
- ⚡ Powered by **Open Source AI (Hugging Face Mistral-7B)**
- 🌍 Built with **Streamlit** – fully interactive and responsive

---

## 🚀 How to Run Locally

### 1. Clone the Repository

git clone https://github.com/yourusername/vedic-astro-therapist.git
cd vedic-astro-therapist
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Create .streamlit/secrets.toml
toml
Copy
Edit
HUGGINGFACEHUB_API_TOKEN = "your_huggingface_token_here"
You can get your token from https://huggingface.co/settings/tokens

4. Run Streamlit App
bash
Copy
Edit
streamlit run app.py
☁️ How to Deploy on Streamlit Cloud (Free Hosting)
Push your code to GitHub

Go to https://streamlit.io/cloud

Connect your GitHub account

Deploy your app with:

Path to app.py

Add HUGGINGFACEHUB_API_TOKEN under secrets

Done! Your link will be live and shareable 🚀

📁 Project Structure
graphql
Copy
Edit
vedic-astro-therapist/
│
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── emotional_traits.json       # Traits summary for emotional insight
├── nakshatra_emotional_traits.json  # Full Nakshatra emotional dataset
└── .streamlit/
    └── secrets.toml            # Contains HuggingFace API token
🧠 Example Prompts Sent to Hugging Face
txt
Copy
Edit
You are a Vedic Astro-Therapist. The user was born in the Nakshatra "Ashwini", and today's Moon is in "Uttara Phalguni".

Generate a poetic, personalized daily horoscope. Include:
- Emotional energy of the day
- Gentle advice or mantra
- Emotional traits and mood guidance

Traits of birth Nakshatra: Energetic, adventurous, healing, fast-acting
Traits of today's Nakshatra: Diplomatic, harmonious, balanced
Start your response with the salutation: "Dear Seeker,"
Conclude the response with the mantra: "Om Ashwinibhyam Namaha"
🙏 Credits
🌌 Astrology calculations by Swiss Ephemeris (swisseph)

💬 AI generation via Hugging Face

🌍 Location and timezone by geopy & timezonefinder

🧘 Emotional insight and Nakshatra content adapted from Vedic texts and interpretations.
⭐ Star the Repo if You Like It!
If this project sparked insight or joy ✨, please consider giving it a ⭐ on GitHub to support more open-source astrological tools!

