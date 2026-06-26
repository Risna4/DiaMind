import sqlite3
import joblib
import numpy as np
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load your trained machine learning model parameters safely
try:
    model = joblib.load("diabetes_model.pkl")
except Exception as e:
    print(f"Warning: Could not load 'diabetes_model.pkl'. Error: {e}")
    model = None

DB_FILE = "predictions_history.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # 1. Background log history table (keeps tracks of individual analytical runs)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                glucose INTEGER, bmi REAL, age INTEGER, result TEXT
            )
        """)
        # 2. Saved patients ledger (name tracking marked UNIQUE to allow UPSERT updates)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                name TEXT UNIQUE, pregnancies INTEGER, glucose INTEGER, 
                blood_pressure INTEGER, skin_thickness INTEGER, 
                insulin INTEGER, bmi REAL, pedigree REAL, age INTEGER, result TEXT
            )
        """)
        conn.commit()

init_db()

class ChatMessage(BaseModel):
    message: str

# --- WORKSPACE ROUTING VIEWPORTS ---

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="diabetes.html", context={})

@app.get("/predict", response_class=HTMLResponse)
def predict(
    request: Request, name: str, pregnancies: int, glucose: int, blood_pressure: int,
    skin_thickness: int, insulin: int, bmi: float, diabetes_pedigree_function: float, age: int
):
    if model is None:
        return templates.TemplateResponse(
            request=request, name="diabetes.html", 
            context={"saved_msg": "Model error: Unable to compute prediction."}
        )

    features = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]])
    prediction = model.predict(features)
    result = "Diabetic" if prediction[0] == 1 else "Not Diabetic"

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (glucose, bmi, age, result) VALUES (?, ?, ?, ?)", (glucose, bmi, age, result))
        conn.commit()

    return templates.TemplateResponse(
        request=request, name="diabetes.html",
        context={
            "result": result, "name": name, "pregnancies": pregnancies, "glucose": glucose,
            "blood_pressure": blood_pressure, "skin_thickness": skin_thickness, "insulin": insulin,
            "bmi": bmi, "diabetes_pedigree_function": diabetes_pedigree_function, "age": age,
            "show_recommendations": True
        }
    )

@app.get("/save-patient", response_class=HTMLResponse)
def save_patient(
    request: Request, name: str, pregnancies: int, glucose: int, blood_pressure: int,
    skin_thickness: int, insulin: int, bmi: float, diabetes_pedigree_function: float, age: int
):
    if model is None:
         raise HTTPException(status_code=500, detail="ML Model not available.")

    clean_name = name.strip()
    features = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]])
    prediction = model.predict(features)
    result = "Diabetic" if prediction[0] == 1 else "Not Diabetic"

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO saved_patients (name, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree, age, result) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                timestamp = CURRENT_TIMESTAMP,
                pregnancies = excluded.pregnancies,
                glucose = excluded.glucose,
                blood_pressure = excluded.blood_pressure,
                skin_thickness = excluded.skin_thickness,
                insulin = excluded.insulin,
                bmi = excluded.bmi,
                pedigree = excluded.pedigree,
                age = excluded.age,
                result = excluded.result
        """, (clean_name, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age, result))
        conn.commit()

    return templates.TemplateResponse(
        request=request, name="diabetes.html",
        context={
            "saved_msg": f"Success! Profile for '{clean_name}' has been updated/saved.",
            "result": result, "name": clean_name, "pregnancies": pregnancies, "glucose": glucose,
            "blood_pressure": blood_pressure, "skin_thickness": skin_thickness, "insulin": insulin,
            "bmi": bmi, "diabetes_pedigree_function": diabetes_pedigree_function, "age": age,
            "show_recommendations": True
        }
    )

@app.get("/history", response_class=HTMLResponse)
def view_history(request: Request):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, glucose, bmi, age, result FROM history ORDER BY id DESC")
        history = cursor.fetchall()
    return templates.TemplateResponse(request=request, name="history.html", context={"history": history})

@app.get("/saved-details", response_class=HTMLResponse)
def view_saved_details(request: Request):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, name, age, glucose, bmi, result FROM saved_patients ORDER BY id DESC")
        patients = cursor.fetchall()
    return templates.TemplateResponse(request=request, name="saved_details.html", context={"patients": patients})

@app.get("/edit-patient/{patient_id}", response_class=HTMLResponse)
def edit_patient(request: Request, patient_id: int):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM saved_patients WHERE id = ?", (patient_id,))
        patient = cursor.fetchone()
        
    if not patient:
        # Use status code 303 See Other for safe browser redirection
        return RedirectResponse(url="/saved-details", status_code=303)

    return templates.TemplateResponse(
        request=request, name="diabetes.html", 
        context={
            "name": patient["name"], "pregnancies": patient["pregnancies"], "glucose": patient["glucose"],
            "blood_pressure": patient["blood_pressure"], "skin_thickness": patient["skin_thickness"],
            "insulin": patient["insulin"], "bmi": patient["bmi"], "diabetes_pedigree_function": patient["pedigree"],
            "age": patient["age"], "result": patient["result"]
        }
    )

# --- FLOATING CHATBOT CORE API ENGINE ---

@app.post("/chat-api")
def chat_response(data: ChatMessage):
    user_text = data.message.lower().strip()
    
    if "diet" in user_text or "food" in user_text or "eat" in user_text:
        reply = (
            "<strong>🥗 Dietary Measures:</strong><br>"
            "• Focus on complex carbohydrates with low Glycemic Index values (oats, leafy vegetables).<br>"
            "• Strictly avoid refined white sugars, processed sweet bakery goods, and sodas.<br>"
            "• Balance meal plates out with lean proteins (fish, skinless poultry, beans)."
        )
    elif "exercise" in user_text or "workout" in user_text or "walk" in user_text:
        reply = (
            "<strong>🏃‍♂️ Activity Measures:</strong><br>"
            "• Perform at least 150 minutes of moderate structural aerobic physical therapy weekly.<br>"
            "• Take brief 10 to 15-minute walks directly following heavy meals to suppress sugar spikes.<br>"
            "• Introduce low-impact weight resistance training sequences two days out of the week."
        )
    elif "measure" in user_text or "high" in user_text or "vitals" in user_text or "monitor" in user_text:
        reply = (
            "<strong>🩺 Management Measures:</strong><br>"
            "• Perform routine fasting plasma sugar checks. Target range is 80-130 mg/dL.<br>"
            "• Arrange clinical laboratory HbA1c observations to analyze your 90-day mean scales.<br>"
            "• Keep peripheral blood pressure benchmarks consistently below a 130/80 threshold limit."
        )
    else:
        reply = (
            "Hello! I am your AI Care Assistant. Type a request or ask about:<br>"
            "• Safe diabetic <strong>Diet</strong> choices<br>"
            "• <strong>Exercise</strong> and active routines<br>"
            "• Vital monitoring <strong>Measures</strong> to take"
        )
    return JSONResponse(content={"reply": reply})

# Optional local entry point execution check
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)