# 🧠 MindMap: Student Psychological Health Assessment

**MindMap** is an AI-powered Data Science project designed to evaluate and understand the psychological health of students. Built using Streamlit, this web application takes inputs regarding a student's daily routine, academic stress, digital comfort, and social interactions, and then predicts key psychological scores (Stress, Anxiety, Motivation, etc.) using Machine Learning models.

> **Note:** This documentation is written to be easily understandable by anyone, regardless of technical background. (सर्वांना सहज समजेल अशा सोप्या भाषेत ही माहिती दिली आहे.)

---

## 🌟 What does this project do? (हा प्रोजेक्ट काय करतो?)

College life can be stressful. Students often undergo anxiety, pressure, and social isolation. MindMap acts as an initial diagnostic tool that:
1. Asks a series of questions about routine, sleep, study habits, and feelings (Assessment).
2. Processes this data to calculate scores for Anxiety, Stress, Motivation, Social Isolation, and Digital Comfort.
3. Uses Machine Learning models to identify patterns and flag potential academic risks.
4. Provides detailed reports for the Student, Parents, and Teachers, so they can take the right actions.

It even supports **English, Marathi, and Hindi**, making it accessible to a wider audience!

---

## 🔄 Project Workflow (प्रोजेक्ट कसा काम करतो?)

Here is the step-by-step flow of how the MindMap application works from start to finish.

```mermaid
flowchart TD
    A([👤 User/Student]) --> B{🌐 Select Language (En/Mr/Hi)}
    B --> C[🏠 Explore Home & Global Context pages]
    C --> D[📝 Take Assessment Questionnaire]
    
    subgraph Data Processing & Machine Learning
        D -->|Raw Answers| E[⚙️ Preprocessor: Calculate Base Scores]
        E -->|Encodes Data| F[🤖 ML Models: K-Means, Label Encoders, Scalers]
        F -->|Archetype & Predictions| G[📊 Calculate Overall Health Score]
    end
    
    G --> H[🏆 View Results Dashboard]
    H --> I[📄 Generate Detailed PDF Report]
    
    H --> J[👨‍👩‍👦 Parent View: Actionable Advice]
    H --> K[👨‍🏫 Teacher / Admin View: Class Trends]
```

### Flow Explanation (थोडक्यात माहिती):
1. **User Interaction**: The student visits the app and selects their preferred language.
2. **Assessment**: The student answers questions about their sleep, studies, and personal feelings.
3. **Data Processing**: The app's backend (`preprocessor.py`) converts words into numbers.
4. **Machine Learning**: The encoded data is passed into pre-trained models to calculate their stress, anxiety, motivation, and overall psychological health.
5. **Dashboard & Report**: The student sees a colorful dashboard mapping their mental health and can download a PDF report.
6. **Parent & Teacher Portals**: Special views are provided so parents and teachers can understand the student's needs without seeing overly complicated data.

---

## ✨ Key Features (प्रोजेक्टची वैशिष्ट्ये)

- **🌍 Multi-language Support**: Easily switch between English (🇬🇧), Marathi (🇮🇳 मराठी), and Hindi (🇮🇳 हिंदी).
- **📈 Advanced Scoring System**: Calculates complex metrics like Stress Index, Anxiety Level, Motivation Score, Social Isolation Index, and Digital Comfort.
- **🤖 Machine Learning Driven**: Groups students into "Archetypes" (like Stressed, Balanced, etc.) using K-Means clustering.
- **👨‍👩‍👧 Dedicated Views**: Special pages for Students (Results), Parents (Parent View), and Teachers (Teacher View) to offer perspective-specific insights.
- **📄 PDF Reports**: Generates downloadable PDF reports with data visualization using Plotly.

---

## 🛠️ Tech Stack (वापरलेले तंत्रज्ञान)

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **Data Manipulation**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn (K-Means, Scalers, Label Encoders), XGBoost
- **Data Visualization**: Plotly, Matplotlib, Seaborn
- **Others**: fpdf2 for PDF generation, joblib for loading models.

---

## 🚀 How to Run the App (ॲप कसे सुरू करावे)

Make sure you have Python installed. Follow these steps to run the project locally:

1. **Install Dependencies**:
   Open terminal and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Data & Train Models (If not already done)**:
   ```bash
   python generate_data_and_train.py
   ```

3. **Start the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

4. **Access the Web App**:
   Open your browser and navigate to `http://localhost:8501`.

---

**Disclaimer (सूचना):** MindMap is an educational screening tool and *not a clinical diagnostic device*. It provides insights, but severe cases should always consult mental health professionals.
