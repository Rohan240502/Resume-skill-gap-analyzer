<div align="center">
  
# ⚡ SkillScope AI
### AI-Powered Resume & Skill Gap Analyzer

[![Live Demo](https://img.shields.io/badge/Live_Demo-Play_Now-00F5FF?style=for-the-badge&logo=vercel)](https://ai-resume-analyzer-vvq4.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-7C3AED?style=for-the-badge&logo=python&logoColor=white)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)]()
  
<p align="center">
  <strong>Analyze your resume, visualize your skill gaps, and get ATS-ready instantly.</strong>
</p>

</div>

---

## 🎯 About The Project

**SkillScope AI** is a premium, automated resume analyzer that goes beyond simple keyword matching. Built for job seekers, recruiters, and data enthusiasts, it uses Natural Language Processing (NLP) to read your resume and compare it against any job description, providing a deep, weighted analysis of your qualifications.

### ✨ Key Features

* **🧠 200+ Skills Tracked:** Extracts granular hard and soft skills across dozens of tech domains.
* **⚖️ Weighted Scoring:** Not all skills are equal. SkillScope assigns priority to critical structural skills over optional ones.
* **🤖 ATS Intelligence:** Simulates Application Tracking Systems to generate an estimated pass/fail score.
* **🎯 Critical Gap Detection:** Identifies exact missing keywords holding your resume back.
* **📊 Visual Analytics:** View your match data via custom Plotly-powered Donut, Bar, and Interactive Radar charts.
* **🎨 Premium UI:** Custom glassmorphism design, dark mode, and micro-animations built natively in Streamlit. 

---

## 🚀 Live Demo

Check out the live application here: **[SkillScope AI (Live on Render)](https://ai-resume-analyzer-vvq4.onrender.com/)**

---

## 🛠️ Tech Stack

* **Frontend/Framework:** [Streamlit](https://streamlit.io/) with custom HTML/CSS injections.
* **Data Processing:** Pandas, NumPy
* **NLP & Extraction:** NLTK, Scikit-Learn (TF-IDF mapping)
* **Document Parsing:** pdfplumber (PDF), python-docx (DOCX)
* **Data Visualization:** Plotly Graph Objects & Express

---

## 💻 Local Installation

To run this project on your local machine, follow these steps:

**1. Clone the repository:**
```bash
git clone https://github.com/Rohan240502/Resume-skill-gap-analyzer.git
cd Resume-skill-gap-analyzer
```

**2. Create a virtual environment (optional but recommended):**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

**3. Install the dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the application:**
```bash
streamlit run app.py
```

---

<div align="center">
  <i>Built with ❤️ using Python and Streamlit.</i>
</div>
