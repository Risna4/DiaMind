# 🩺 DiaMind - AI-Powered Diabetes Risk Assessment System

## 📖 Overview

DiaMind is a Machine Learning-powered web application that predicts the likelihood of diabetes using patient health information. The application is developed with **FastAPI** and provides a modern web interface for diabetes assessment, patient record management, prediction history, and an integrated AI healthcare assistant.

The system combines Machine Learning with a lightweight SQLite database to help users perform diabetes risk assessments while maintaining patient records and viewing previous prediction history.

---

# ✨ Features

* 🩺 Diabetes Risk Prediction using Machine Learning
* 📋 Interactive Patient Assessment Form
* 💾 Save Patient Profiles
* ✏️ Edit Existing Patient Records
* 📜 Prediction History Log
* 🗄️ SQLite Database Integration
* 🤖 AI Healthcare Assistant
* 🥗 Diet Recommendations
* 🏃 Exercise Recommendations
* 🩺 Health Monitoring Guidance
* ⚡ FastAPI Backend
* 🎨 Responsive and User-Friendly Interface

---

# 🛠️ Technologies Used

### Backend

* Python
* FastAPI
* SQLite3
* NumPy
* Joblib
* Jinja2

### Machine Learning

* Scikit-learn
* Pandas
* NumPy

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

---

# 📂 Project Structure

```text
DiaMind/
│
├── templates/
│   ├── diabetes.html
│   ├── history.html
│   └── saved_details.html
│
├── prediction.py
├── diabetes_model.pkl
├── diabetes.csv
├── predictions_history.db
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/DiaMind.git
```

## 2. Navigate to the Project Folder

```bash
cd DiaMind
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Start the Application

```bash
fastapi dev prediction.py
```

## 5. Open in Browser

```
http://127.0.0.1:8000
```

---

# 🧠 Machine Learning Model

The application predicts diabetes risk using a trained Machine Learning model (`diabetes_model.pkl`) based on the following medical attributes:

* Pregnancies
* Glucose Level
* Blood Pressure
* Skin Thickness
* Insulin Level
* Body Mass Index (BMI)
* Diabetes Pedigree Function
* Age

---

# 💾 Database Functionality

DiaMind automatically creates a SQLite database (`predictions_history.db`) to manage application data.

The database stores:

* Prediction history
* Saved patient profiles
* Updated patient information
* Assessment timestamps

---

# 🤖 AI Healthcare Assistant

The built-in chatbot provides general healthcare guidance related to:

* Healthy diabetic diet recommendations
* Exercise suggestions
* Lifestyle improvements
* Blood sugar monitoring advice

The chatbot is designed for educational purposes and should not replace professional medical consultation.

---

# 📊 Dataset

The Machine Learning model was trained using the **diabetes.csv** dataset before being exported as `diabetes_model.pkl`.

---

# 📌 Future Enhancements

* User Authentication
* Doctor Dashboard
* PDF Report Generation
* Email Notifications
* Cloud Database Support
* Advanced AI Healthcare Chatbot
* Mobile Responsive Interface

---

# ⚠️ Disclaimer

This application is developed for educational and learning purposes only.

The prediction results and AI assistant recommendations should not be considered professional medical advice. Always consult a qualified healthcare professional for medical diagnosis and treatment.

---

# 👩‍💻 Developer

**Risna Jaleel**

AI & Machine Learning Internship Project

---

# ⭐ If you found this project useful, consider giving it a star on GitHub!
