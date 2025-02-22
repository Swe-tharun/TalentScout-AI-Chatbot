# TalentScout AI Hiring Assistant

## 🚀 Project Overview
TalentScout AI Hiring Assistant is a chatbot designed to streamline the hiring process by assisting recruiters with candidate evaluation, scheduling, and technical question generation. The chatbot is powered by AI and integrates with various APIs to deliver a seamless experience.

🌐 **Live Demo:** [Streamlit Deployment](https://hiringassistantpy-x8dil4bndqfnx3atrbewkb.streamlit.app/)

## 📌 Features
- AI-powered candidate screening
- Automated technical question generation
- Interactive chat-based interface
- Data storage and retrieval system

## 🛠️ Tech Stack
- **Python** (Core backend logic)
- **Streamlit** (Frontend UI and deployment)
- **Mistral API** (AI-powered chatbot functionality)
- **SQLite** (Database management)
- **JSON** (Data handling)

## 🔧 Installation Guide
Follow these steps to set up the project locally:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Swe-tharun/TalentScout-AI-Chatbot.git
cd TalentScout-AI-Chatbot
```

### 2️⃣ Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Key
You need to generate your **Mistral API Key** and store it in your environment variables to use the chatbot.

#### 🔑 Setting API Key (Linux/MacOS)
```bash
export MISTRAL_API_KEY="your_api_key_here"
```

#### 🔑 Setting API Key (Windows - PowerShell)
```powershell
$env:MISTRAL_API_KEY="your_api_key_here"
```

> **Note:** Do **NOT** hardcode the API key in the codebase. Always use environment variables.

### 5️⃣ Run the Application
```bash
streamlit run hiring_assistant.py
```

## 🌍 Accessing the Deployed App
If you don't want to set up locally, you can use the **hosted version** directly:
🔗 [Access Here](https://hiringassistantpy-x8dil4bndqfnx3atrbewkb.streamlit.app/)

## ⚙️ Admin Configuration
To customize the admin settings:
- Navigate to `hiring_assistant.py`
- Modify the **credentials** section to set your preferred admin access.

## 🎯 Prompt Design
The chatbot is designed with structured prompts to handle candidate evaluations and generate relevant interview questions. It uses:
- **Dynamic Prompt Engineering** for personalized responses.
- **API-based Retrieval** for real-time answers.

## 🚀 Challenges & Solutions
| Challenge               | Solution Implemented |
|------------------------|---------------------|
| API Response Latency | Optimized API calls using caching |
| User Input Variability | Implemented NLP-based filtering |
| UI Responsiveness | Deployed on Streamlit for an interactive UI |

---
### 💡 Contributing
If you’d like to contribute, feel free to fork this repository and submit a pull request!

Happy Hiring! 🚀

