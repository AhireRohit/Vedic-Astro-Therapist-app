import streamlit as st
import pyswisseph as swe
import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import json
import os
import random
from huggingface_hub import InferenceClient

# Set up Hugging Face API
hf_token = st.secrets.get("HUGGINGFACEHUB_API_TOKEN")

if not hf_token:
    st.error("❌ Hugging Face API token not found in environment variables.")
    st.stop()

client = InferenceClient(token=hf_token)

# Load emotional data
with open("emotional_traits.json", encoding="utf-8") as f:
    response_templates = json.load(f)

with open("nakshatra_emotional_traits.json", encoding="utf-8") as f:
    nakshatra_data = json.load(f)

# UI Inputs
st.markdown("""
    <style>
    .pulse-box {
        animation: glow 2s infinite alternate;
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        font-weight: bold;
        color: white;
    }
    @keyframes glow {
        0% { filter: brightness(1); }
        100% { filter: brightness(1.4); }
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Vedic Astro-Therapist")
user_name = st.text_input("Enter your name (optional)")
from datetime import date

birth_date = st.date_input(
    "Enter your date of birth",
    value=date(2000, 1, 1),              # Default selected date
    min_value=date(1900, 1, 1),          # Earliest date user can pick
    max_value=date.today()              # Latest allowed date (today)
)
birth_time = st.time_input("Enter your time of birth", step=60)
birth_place = st.text_input("Enter your place of birth (City, Country)")

if st.button("Get My Horoscope"):
    try:
        birth_dt = datetime.datetime.combine(birth_date, birth_time)
        geolocator = Nominatim(user_agent="astro_bot")
        location = geolocator.geocode(birth_place)
        if not location:
            st.error("Could not find location.")
            st.stop()

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
        timezone = pytz.timezone(timezone_str)
        local_dt = timezone.localize(birth_dt)
        utc_dt = local_dt.astimezone(pytz.utc)

        jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)
        swe.set_ephe_path('.')
        swe.set_sid_mode(swe.SIDM_LAHIRI)

        moon_long = swe.calc_ut(jd_ut, swe.MOON)[0][0]
        ayanamsa = swe.get_ayanamsa(jd_ut)
        moon_long_sidereal = moon_long - ayanamsa

        rashi_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                       "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        nakshatra_names = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
            "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
            "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
            "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]

        rashi_index = int(moon_long_sidereal // 30)
        nak_index = int((moon_long_sidereal % 360) // (360 / 27))
        moon_rashi = rashi_names[rashi_index]
        nakshatra = nakshatra_names[nak_index]

        def get_today_moon_nakshatra():
            now = datetime.datetime.utcnow()
            jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60)
            moon_long = swe.calc_ut(jd, swe.MOON)[0][0]
            ayanamsa = swe.get_ayanamsa(jd)
            sidereal_moon = moon_long - ayanamsa
            index = int((sidereal_moon % 360) // (360 / 27))
            return nakshatra_names[index]

        today_nakshatra = get_today_moon_nakshatra()

        mantra = nakshatra_data[nakshatra]["recommended_mantra"]
        emotions = nakshatra_data[nakshatra]["emotional_traits"]
        challenges = nakshatra_data[nakshatra]["common_challenges"]
        today_traits = nakshatra_data[today_nakshatra]["emotional_traits"]

        greeting = f"Dear {user_name.strip()}" if user_name.strip() else "Dear Seeker"

        prompt = f"""
        You are a Vedic Astro-Therapist. The user was born in the Nakshatra "{nakshatra}", and today's Moon is in "{today_nakshatra}".

        Generate a poetic, personalized daily horoscope. Include:
        - Emotional energy of the day
        - Gentle advice or mantra
        - Emotional traits and mood guidance

        Traits of birth Nakshatra: {', '.join(emotions)}
        Traits of today's Nakshatra: {', '.join(today_traits)}
        Start your response with the salutation: "{greeting},"
        Conclude the response with the mantra: "{mantra}"

        """

        response = client.text_generation(
            model="tiiuae/falcon-7b-instruct",
            prompt=prompt,
            temperature=0.7,
            max_new_tokens=500
        )

        def infer_mood_from_horoscope(text):
            lower = text.lower()
            if any(word in lower for word in ["peace", "calm", "soothing", "relax", "stillness"]):
                return "Peaceful", "#22c55e"
            elif any(word in lower for word in ["growth", "balance", "harmony", "stability", "alignment"]):
                return "Balanced", "#eab308"
            elif any(word in lower for word in ["intense", "challenge", "power", "bold", "transformation"]):
                return "Intense", "#ef4444"
            else:
                return "Balanced", "#eab308"

        mood_label, mood_color = infer_mood_from_horoscope(response)

        st.markdown(
            f"""
            <div class='pulse-box' style='background-color:{mood_color};'>
                <strong>🌈 Mood Vibe of the Day:</strong> {mood_label}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("Your Vedic Profile")
        st.markdown(f"**Nakshatra**: {nakshatra}\n\n**Rashi**: {moon_rashi}\n\n**Mantra**: {mantra}")

        st.subheader("Emotional Traits")
        st.markdown("\n".join([f"• {trait}" for trait in emotions]))

        st.subheader("Today's Moon Nakshatra")
        st.write(today_nakshatra)

        st.subheader("💫 Today's Horoscope")
        st.markdown(response)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
