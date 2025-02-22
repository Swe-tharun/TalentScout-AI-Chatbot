import os
import streamlit as st
import requests
import time
import json
import re
import base64

# Retrieve API key from environment variable
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Admin credentials
ADMIN_EMAIL = "tharunsivaraj0325@gmail.com"
ADMIN_PASSWORD = "123456789"

# Initialize Streamlit app with custom title styling
st.markdown(
    """
    <style>
    .title {
        color: white;
        text-align: center;
        font-size: 36px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h1 class="title">TalentScout AI Hiring Chatbot 🤖</h1>', unsafe_allow_html=True)

# Set background image using a local asset
def set_background():
    image_path = "assets/Light Blue Wallpaper High Definition Quality Widescreen.jpg"
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_background()

# Add animated greeting CSS and additional CSS to force input label text to white
st.markdown("""
<style>
/* Existing animation styles */
@keyframes shine {
    0% { color: #ff7f50; text-shadow: 0 0 5px #ff7f50; }
    50% { color: #ffd700; text-shadow: 0 0 15px #ffd700; }
    100% { color: #ff7f50; text-shadow: 0 0 5px #ff7f50; }
}
@keyframes jumble {
    0% { transform: translateY(0); }
    25% { transform: translateY(-5px); }
    50% { transform: translateY(0); }
    75% { transform: translateY(5px); }
    100% { transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Glowing White Text for animated greetings */
.shine-text {
    animation: shine 2s infinite ease-in-out;
    font-size: 24px;
    font-weight: bold;
}
.jumble-text {
    animation: jumble 1s infinite ease-in-out, fadeIn 2s;
    font-size: 24px;
    font-weight: bold;
    color: white;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
}
/* New class for static glowing text */
.glow-text {
    font-size: 18px;
    color: white;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
}

/* Override default label color for input fields to white */
label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Animated greeting texts
st.markdown('<p class="shine-text">Hello! I am your AI Hiring Assistant.</p>', unsafe_allow_html=True)
st.markdown('<p class="jumble-text">Let\'s start your interview! 🚀</p>', unsafe_allow_html=True)

# Basic information prompt in glowing white text
st.markdown('<p class="glow-text">Let\'s start by collecting some basic information.</p>', unsafe_allow_html=True)

# Session state initialization
if "stage" not in st.session_state:
    st.session_state.stage = "intro"
    st.session_state.user_data = {}
    st.session_state.questions = []
    st.session_state.current_question_index = 0
    st.session_state.responses = {}
    st.session_state.admin_logged_in = False

# Function to reset interview session
def reset_interview():
    st.session_state.stage = "intro"
    st.session_state.user_data = {}
    st.session_state.questions = []
    st.session_state.current_question_index = 0
    st.session_state.responses = {}
    st.rerun()

# Validation functions
def is_valid_name(name):
    return bool(re.fullmatch(r"^[A-Za-z\s'-]+$", name))
def is_valid_email(email):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))
def is_valid_phone(phone):
    return bool(re.fullmatch(r"\d{10,15}", phone))
def is_valid_experience(experience):
    return isinstance(experience, int) and 0 <= experience <= 50
def is_valid_position(position):
    return bool(re.fullmatch(r"^[A-Za-z\s'-]+$", position))
def is_valid_location(location):
    return bool(re.fullmatch(r"^[A-Za-z\s,'-]+$", location))
def is_valid_tech_stack(tech_stack):
    return bool(re.fullmatch(r"^[A-Za-z0-9\s,.-]+$", tech_stack))
def fallback_response():
    st.warning("I didn't understand that. Could you please rephrase or provide a valid response?")
def check_for_exit_keywords(user_input):
    exit_keywords = ["exit", "quit", "end", "stop"]
    return any(keyword in user_input.lower() for keyword in exit_keywords)

# Chatbot workflow
if st.session_state.stage == "intro":
    st.write("Let's start by collecting some basic information.")
    if st.button("Start Interview"): 
        st.session_state.stage = "collect_name"
        st.rerun()

elif st.session_state.stage == "collect_name":
    name = st.text_input("👤 What is your full name?")
    if name:
        if check_for_exit_keywords(name):
            st.write("Thank you for your time. Have a great day!")
            reset_interview()
        elif not is_valid_name(name):
            st.error("Please enter a valid name (only letters, spaces, hyphens, and apostrophes).")
        else:
            st.session_state.user_data["name"] = name
            st.session_state.stage = "collect_email"
            st.rerun()

elif st.session_state.stage == "collect_email":
    email = st.text_input("📧 What is your email address?")
    if email:
        if check_for_exit_keywords(email):
            st.write("Thank you for your time. Have a great day!")
            reset_interview()
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        else:
            st.session_state.user_data["email"] = email
            st.session_state.stage = "collect_phone"
            st.rerun()

elif st.session_state.stage == "collect_phone":
    phone = st.text_input("📱 What is your phone number?")
    if phone:
        if check_for_exit_keywords(phone):
            st.write("Thank you for your time. Have a great day!")
            reset_interview()
        elif not is_valid_phone(phone):
            st.error("Please enter a valid phone number (10-15 digits).")
        else:
            st.session_state.user_data["phone"] = phone
            st.session_state.stage = "collect_experience"
            st.rerun()

elif st.session_state.stage == "collect_experience":
    experience = st.number_input("🌟 How many years of experience do you have?", min_value=0, max_value=50, step=1)
    if st.button("Submit Experience"):
        if not is_valid_experience(experience):
            st.error("Please enter a valid number of years (0-50).")
        else:
            st.session_state.user_data["experience"] = experience
            st.session_state.stage = "collect_position"
            st.rerun()

elif st.session_state.stage == "collect_position":
    position = st.text_input("🎯 What is your desired position?")
    if position:
        if check_for_exit_keywords(position):
            st.write("Thank you for your time. Have a great day!")
            reset_interview()
        elif not is_valid_position(position):
            st.error("Please enter a valid position (only letters, spaces, hyphens, and apostrophes).")
        else:
            st.session_state.user_data["position"] = position
            st.session_state.stage = "collect_location"
            st.rerun()

elif st.session_state.stage == "collect_location":
    location = st.text_input("📍 What is your current location?")
    if location:
        if check_for_exit_keywords(location):
            st.write("Thank you for your time. Have a great day!")
            reset_interview()
        elif not is_valid_location(location):
            st.error("Please enter a valid location (only letters, spaces, commas, hyphens, and apostrophes).")
        else:
            st.session_state.user_data["location"] = location
            st.session_state.stage = "collect_tech_stack"
            st.rerun()

elif st.session_state.stage == "collect_tech_stack":
    tech_stack = st.text_area("🛠 What technologies do you work with? (e.g., Python, React, MySQL, etc.)")
    if tech_stack:
        if check_for_exit_keywords(tech_stack):
            st.write("Thank you for your time. Have a great day!")
            reset_interview()
        elif not is_valid_tech_stack(tech_stack):
            st.error("Please enter a valid tech stack (only letters, numbers, spaces, commas, periods, and hyphens).")
        else:
            st.session_state.user_data["tech_stack"] = tech_stack
            if st.button("Generate Questions"): 
                st.session_state.stage = "generate_questions"
                st.rerun()

elif st.session_state.stage == "generate_questions":
    if not st.session_state.questions:
        if not MISTRAL_API_KEY:
            st.error("⚠ API key not found! Please set the MISTRAL_API_KEY environment variable.")
        else:
            st.success(f"Generating technical questions for {st.session_state.user_data['position']}...")
            prompt = f"""
            You are an AI hiring assistant.
            A candidate has applied for a {st.session_state.user_data['position']} role with the following details:
            - Name: {st.session_state.user_data['name']}
            - Experience: {st.session_state.user_data['experience']} years
            - Tech Stack: {st.session_state.user_data['tech_stack']}
            Generate 5 relevant technical interview questions.
            """
            headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
            data = {"model": "mistral-tiny", "messages": [{"role": "user", "content": prompt}]}
            response = requests.post("https://api.mistral.ai/v1/chat/completions", json=data, headers=headers)
            if response.status_code == 200:
                questions = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").split("\n")
                st.session_state.questions = [q for q in questions if q.strip()]
                st.session_state.stage = "ask_question"
            else:
                st.error(f"🚨 API Error: {response.status_code} - {response.text}")
    st.rerun()

elif st.session_state.stage == "ask_question":
    index = st.session_state.current_question_index
    if index < len(st.session_state.questions):
        question = st.session_state.questions[index]
        st.markdown(f"<h3 style='color: white;'>📌 Question {index + 1}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: white;'>{question}</p>", unsafe_allow_html=True)
        answer = st.text_area("✍ Your Answer", key=f"answer_{index}")
        if st.button("Submit Answer"):
            if check_for_exit_keywords(answer):
                st.write("Thank you for your time. Have a great day!")
                reset_interview()
            else:
                st.session_state.responses[question] = answer
                st.success("✅ Answer saved! Moving to next question...")
                time.sleep(1)
                st.session_state.current_question_index += 1
                st.rerun()
    else:
        if st.button("End Test"):
            st.session_state.stage = "end_interview"
            st.rerun()

elif st.session_state.stage == "end_interview":
    st.write("🎉 You have completed the interview! Your responses are being saved.")
    user_data = {
        "user_data": st.session_state.user_data,
        "responses": st.session_state.responses
    }
    with open("user_responses.json", "w") as f:
        json.dump(user_data, f, indent=4)
    st.success("📁 Your answers have been saved!")
    st.write("### Thank You for Your Time!")
    st.write("We truly appreciate the effort and time you've taken to complete this interview.")
    st.write("Our team will carefully review your responses and get back to you shortly.")
    st.write("Wishing you the best of luck in your career endeavors! 🌟")
    if st.button("Restart Interview"):
        reset_interview()

# Admin Panel with Login
st.sidebar.title("Admin Login")
admin_email = st.sidebar.text_input("📧 Enter Admin Email")
admin_password = st.sidebar.text_input("🔑 Enter Password", type="password")
if st.sidebar.button("Login"):
    if admin_email == ADMIN_EMAIL and admin_password == ADMIN_PASSWORD:
        st.session_state.admin_logged_in = True
        st.sidebar.success("✅ Login Successful!")
    else:
        st.sidebar.error("❌ Invalid Credentials!")
if st.session_state.admin_logged_in:
    if st.sidebar.button("View Responses"):
        try:
            with open("user_responses.json", "r") as f:
                data = json.load(f)
            st.sidebar.write("### User Details:")
            st.sidebar.write(f"**Name:** {data['user_data']['name']}")
            st.sidebar.write(f"**Email:** {data['user_data']['email']}")
            st.sidebar.write(f"**Phone:** {data['user_data']['phone']}")
            st.sidebar.write(f"**Experience:** {data['user_data']['experience']} years")
            st.sidebar.write(f"**Desired Position:** {data['user_data']['position']}")
            st.sidebar.write(f"**Location:** {data['user_data']['location']}")
            st.sidebar.write(f"**Tech Stack:** {data['user_data']['tech_stack']}")
            st.sidebar.write("### Interview Responses:")
            for i, (question, answer) in enumerate(data['responses'].items(), 1):
                st.sidebar.write(f"**Question {i}:** {question}")
                st.sidebar.write(f"**Answer {i}:** {answer}")
                st.sidebar.write("---")
        except FileNotFoundError:
            st.sidebar.error("No responses found!")
