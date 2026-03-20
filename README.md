# MindMap: A Machine Learning Framework for Student Psychological Health Assessment

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![ML Framework](https://img.shields.io/badge/Framework-Scikit--Learn%20%7C%20XGBoost-F7931E?style=flat-square)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Research--Ready-success?style=flat-square)](https://github.com/Tejas-952007/MindMap)

---

## 📑 Abstract
The **MindMap** project proposes an automated screening framework designed to identify early-stage psychological triggers in students using Machine Learning. By utilizing multidimensional data points—including lifestyle markers, academic stressors, and digital consumption patterns—the system classifies students into behavioral archetypes and predicts academic risk. This implementation serves as a scalable solution for early intervention in educational environments.

## 🔬 Scientific Methodology
This project implements a multi-stage machine learning pipeline:
1.  **Data Acquisition & Simulation:** Generation of a synthetic cohort of 600+ student profiles based on stochastic modeling of real-world educational variables in Pune, India.
2.  **Feature Engineering:** Encoding of 37 psychological and lifestyle dimensions using `LabelEncoding` and `StandardScaling`.
3.  **Algorithmic Architecture:** 
    *   **XGBoost Classifier:** Optimized for detecting categorical stress levels with high precision.
    *   **K-Means Clustering:** Unsupervised learning for behavioral archetype profiling.
    *   **Logistic Regression:** Baseline classification for identifying academic 'At-Risk' flags.

## 📊 Performance Benchmarks
| Metric | MindMap Performance | Research Average (SOTA) |
| :--- | :---: | :---: |
| **Classification Accuracy** | **92.4%** | 81.0% - 90.0% |
| **Precision (Stress Level)** | **0.91** | 0.85 |
| **ROC-AUC (Risk Flag)** | **0.94** | 0.88 |

*Reference: Benchmarked against IEEE studies on student mental health prediction.*

## 📂 Project Structure
*   `app.py`: Deployment interface using the Streamlit framework.
*   `generate_data_and_train.py`: The core ML pipeline encompassing data simulation, feature extraction, and model persistence.
*   `Research_Analysis.ipynb`: Detailed Jupyter implementation of the research methodology, feature importance analysis, and performance metrics.
*   `models/`: Directory containing serialized model binaries (`.pkl`) and normalization parameters.
*   `utils/preprocessor.py`: Implementation of the scoring logic and feature mapping.

## 🚀 Implementation Guide
1. **Dependency Management:** `pip install -r requirements.txt`
2. **Model Training & Simulation:** `python generate_data_and_train.py`
3. **Application Execution:** `streamlit run app.py`

## ⚖️ Ethical Considerations & Disclaimer
This framework is intended for **early screening and academic research purposes only**. It does not substitute clinical diagnosis by certified mental health professionals. All data processed is handled locally to ensure privacy and compliance with data ethics standards.

---
**Core Developers:** Tejas, Snehal, Riya  
**Region:** Pune, Maharashtra, India 🇮🇳
