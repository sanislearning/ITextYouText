# ITextYouText

A lightweight web app built with Flask that lets you upload exported WhatsApp chat files (`.txt`) and visualize messaging statistics like:

- Total messages sent by each participant
- Average words per message

Built with simplicity and mobile responsiveness in mind.

---

## 🚀 Features

- 📊 Interactive bar chart with Chart.js
- 📁 Upload `.txt` chat exports directly from WhatsApp
- 📱 Mobile-friendly and minimal UI
- ⚙️ Deployed easily using [Render](https://render.com/)

---

## 📂 Project Structure
```
ITextYouText/
├── whatsapp_analyzer/
│ ├── static/
│ │ └── styles.css
│ ├── templates/
│ │ └── index.html
│ ├── app.py
│ ├── requirements.txt
│ ├── Procfile
│ └── .gitignore
├── README.md
├── main.py
```

---

## 📄 How to Use

1. Export your WhatsApp chat as a `.txt` file (without media).
2. Upload the file via the homepage.
3. View message count and average words per message for each user.
4. Works best with English chats or chats using standard WhatsApp export formatting.

---

## 🛠️ Tech Stack

- Python 3.11
- Flask 3.1
- Chart.js
- HTML + CSS

---

## 📦 Installation (For Local Use)

```bash
# Clone the repository
git clone https://github.com/sanislearning/ITextYouText.git
cd ITextYouText/whatsapp_analyzer

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

## 🌐 Deployment (Render)
Settings for Render:
Root Directory: whatsapp_analyzer/

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app
