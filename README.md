# 🧠 MindMap / Student Psychological Health Assessment

MindMap is an **AI-powered web application** designed to evaluate and understand the psychological health of students. Built using Streamlit and Machine Learning, it assesses student stress, anxiety, and motivation based on their daily routines and behaviors, and provides intelligent insights.

---

## 📚 Table of Contents
1. [What is MindMap?](#-what-is-mindmap)
2. [What's New — Key Features](#-whats-new--key-features)
3. [How the App Works — Flowcharts](#-how-the-app-works--flowcharts)
4. [Using the Dashboards](#-using-the-dashboards)
5. [Tech Stack](#%EF%B8%8F-tech-stack)
6. [Getting Started (Beginner Friendly)](#-getting-started-beginner-friendly)
7. [Project File Structure](#-project-file-structure)

---

## 🤔 What is MindMap?
College life can be tough. Students often face anxiety, academic pressure, and social isolation. **MindMap** is an initial screening tool that helps identify these issues early.

Instead of a boring form, it acts as an intelligent assistant:
> 📝 *Student answers simple questions about sleep, study habits, and mood.*  
> 🤖 *MindMap processes this using Machine Learning.*  
> 📊 *It instantly generates scores for Stress, Anxiety, Motivation, and Overall Health.*

It runs beautifully in your browser and supports **English, Marathi, and Hindi**, making it accessible to a wider audience!

---

## ✨ What's New — Key Features

1. **🌍 Multilingual Interface**
   - Seamlessly switch between **English**, **मराठी (Marathi)**, and **हिंदी (Hindi)**.
   - All questions, reports, and insights are fully translated.

2. **🤖 Machine Learning Driven Scoring**
   - Uses pre-trained algorithms (K-Means, XGBoost) to predict psychological patterns.
   - Groups students into "Archetypes" (e.g., Stressed, Balanced).

3. **📊 Dynamic Result Dashboards**
   - **Student View:** Colorful gauges and charts showing personal health scores.
   - **Parent View:** Easy-to-understand actionable advice without confusing data.
   - **Teacher View:** Class-level trends and academic risk flagging.

4. **📄 PDF Report Generation**
   - Downloadable, printer-friendly PDF reports containing charts and detailed analysis.

---

## 🔄 How the App Works — Flowcharts

### 1. Overall App Flow
```mermaid
flowchart TD
    A([🚀 App Starts]) --> B{🌐 Select Language}
    B -->|English / मराठी / हिंदी| C[🏠 View Home / Global Context]
    C --> D[📝 Take Assessment Questionnaire]
    
    D --> E{User Submits Form?}
    E -->|Yes| F[⚙️ Preprocessor: Calculate Base Scores]
    E -->|No| D
    
    F --> G[🤖 ML Models: K-Means, XGBoost]
    G --> H[📊 Calculate Overall Health]
    
    H --> I[Dashboard Navigation]
    I -->|Results| J[🏆 View Results Dashboard]
    I -->|Report| K[📄 Generate PDF]
    I -->|Parent| L[👨‍👩‍👦 View Parent Insights]
    I -->|Teacher| M[👨‍🏫 View Teacher Analytics]
```

### 2. Data Processing Flow
```mermaid
flowchart LR
    A[Raw Answers\\n(e.g., Sleep, Study Hrs)] --> B[Pre-processing\\n(utils/preprocessor.py)]
    B --> C[Label Encoders\\n(Convert Text to Numbers)]
    C --> D[Scalers\\n(Normalize Data)]
    D --> E[Feature Vector Creation]
    E --> F[K-Means Clustering\\n(Predict Archetype)]
    E --> G[Mathematical Models\\n(Stress & Anxiety Index)]
    F --> H[Final Output to UI]
    G --> H
```

---

## 📈 Using the Dashboards

### For Students
- Go to the **Assessment** tab and honestly answer the questions.
- Once submitted, head to **Results** to see your "Overall Health Score", "Anxiety Level", and "Stress Index".
- Click **Report** to download your personalized PDF.

### For Parents
- Go to the **Parent** tab.
- Here, you won't see complicated charts. Instead, you'll see simple, actionable advice on how to support your child based on their recent assessment.

### For Teachers
- Go to the **Teacher** tab.
- Teachers can see aggregated data (trends) and identify if a student has an **"Academic Risk Flag"** indicating they might need extra attention.

---

## 🛠️ Tech Stack

- **Frontend Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** `pandas`, `numpy`
- **Machine Learning:** `scikit-learn` (K-Means, Scalers, Label Encoders), `xgboost`
- **Data Visualization:** `plotly`, `matplotlib`, `seaborn`
- **Tools:** `fpdf2` (for PDF generation), `joblib` (for loading models).

---

## 🚀 Getting Started (Beginner Friendly)

### Step 1 — You need:
- A computer with **Python** installed (Python 3.8 or higher is recommended).

### Step 2 — Download the project
**Option A — Download ZIP (easiest):**
1. Go to: [MindMap GitHub Repo](https://github.com/Tejas-952007/MindMap)
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Unzip the downloaded file

**Option B — Git clone:**
```bash
git clone https://github.com/Tejas-952007/MindMap.git
cd MindMap
```

### Step 3 — Install Requirements
Open your terminal (or Command Prompt) inside the folder and run:
```bash
pip install -r requirements.txt
```

### Step 4 — Run the App!
If you are running this for the very first time, generate the data and train the models:
```bash
python generate_data_and_train.py
```

Then, start the web app:
```bash
streamlit run app.py
```
> The app will automatically open in your browser at `http://localhost:8501`.

---

## 📁 Project File Structure

Here is what each file and folder does:

| Folder / File | What it does |
|--------------|--------------|
| `app.py` | The main file that runs the Streamlit application and sidebar navigation. |
| `page_modules/` | Contains the code for different pages (Home, Assessment, Results, Parent View, etc.). |
| `models/` | Stores the trained Machine Learning models (`.pkl` files) generated by Python. |
| `utils/` | Helper files, like `preprocessor.py` for data calculations and translations. |
| `data/` | Where generated dummy dataset files are stored. |
| `assets/` | Stores the CSS styling files (colors, layout) and images. |
| `generate_data_and_train.py` | The script that generates dummy data and trains the ML models before you start the app. |
| `requirements.txt` | The list of all Python packages needed to run this project. |

---

**Disclaimer:** MindMap is an educational screening tool and *not a clinical diagnostic device*. It provides insights to help students, parents, and teachers take timely actions. Severe cases should always consult mental health professionals.
