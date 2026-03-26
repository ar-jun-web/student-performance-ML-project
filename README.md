# 🎓 AcademyFlow AI - Student Performance Prediction System

> **Final Year B.Sc Data Science Project**  
> **Sathyabama University**

An advanced machine learning web application that predicts student academic performance based on study habits and behavioral patterns. Built with ensemble ML models achieving **99.14% accuracy**.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4.0-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 👥 Team Members

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/ar-jun-web.png" width="100px;" alt="Arjun"/><br />
      <sub><b>Arjun</b></sub><br />
      <sub>Backend & ML Development</sub><br />
      <a href="https://github.com/ar-jun-web">GitHub</a>
    </td>
    <td align="center">
      <img src="https://github.com/identicons/barani.png" width="100px;" alt="Barani"/><br />
      <sub><b>Barani</b></sub><br />
      <sub>Frontend & UI/UX Design</sub><br />
      <a href="https://github.com/barani">GitHub</a>
    </td>
  </tr>
</table>

**Collaborative Development:** This project was built through pair programming and collaborative problem-solving, combining expertise in machine learning, data science, and web development.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Model Performance](#model-performance)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Screenshots](#screenshots)
- [Development Process](#development-process)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🌟 Overview

AcademyFlow AI is a comprehensive student performance prediction system that uses machine learning to:
- Predict academic performance based on 5 key behavioral factors
- Provide personalized study recommendations
- Enable goal tracking and progress monitoring
- Offer peer comparison analytics
- Generate actionable insights for improvement

**Problem Solved:** Traditional educational assessment methods are reactive, identifying struggling students only after poor performance. AcademyFlow enables **proactive intervention** through predictive analytics.

---

## ✨ Features

### 🎯 Core Functionality
- **Real-time Performance Prediction** - Instant predictions with <100ms response time
- **Multi-Model Ensemble** - Compares 3 ML algorithms (Linear Regression, Random Forest, Gradient Boosting)
- **Advanced Feature Engineering** - 4 engineered features to boost accuracy from 98.97% to 99.14%
- **Interactive Visualizations** - Plotly-powered gauges, radar charts, and bar graphs
- **Modern UI Design** - Glassmorphism aesthetic with responsive layout

### 📊 Analysis Modules

#### 1️⃣ Performance Analysis Tab
- Real-time gauge charts for study hours, previous scores, and sleep
- Comprehensive radar chart showing complete student profile
- AI-powered predictions with performance bands (Excellent/Good/Average/Critical)
- Feature importance breakdown visualization

#### 2️⃣ Goal Tracker Tab
- Interactive target score setting
- Visual progress bars showing gap to goal
- Gap analysis with recommended actions
- Personalized improvement roadmap

#### 3️⃣ Peer Comparison Tab
- Student vs class average benchmarking
- Automatic strength identification (above-average areas)
- Weakness detection with improvement suggestions
- Interactive comparative bar charts

#### 4️⃣ Study Insights Tab
- Personalized study hour recommendations
- Sleep optimization suggestions based on performance data
- Practice paper targets
- Extracurricular activity impact analysis
- What-if scenario modeling

---

## 🎬 Demo

### Live Application
```bash
cd MLmodels
streamlit run app.py
```
Access at: `http://localhost:8501`

### Input Parameters
- **Hours Studied:** 1-12 hours per day
- **Previous Scores:** 0-100%
- **Extracurricular Activities:** Yes/No
- **Sleep Hours:** 4-12 hours per night
- **Practice Papers Completed:** 0-10 mock tests

### Output
- **Performance Index:** Predicted score (0-100 scale)
- **Performance Band:** Excellent (90+) / Good (80-89) / Average (70-79) / Needs Improvement (60-69) / Critical (<60)
- **Personalized Recommendations:** Tailored action items for improvement

---

## 🛠️ Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Language** | Python | 3.11+ | Core development |
| **ML Framework** | Scikit-learn | 1.4.0 | Model training & prediction |
| **Web Framework** | Streamlit | 1.31.0 | UI & deployment |
| **Data Processing** | Pandas | 2.2.0 | Data manipulation |
| **Numerical Computing** | NumPy | 1.26.3 | Mathematical operations |
| **Visualization** | Plotly | 5.18.0 | Interactive charts |
| **Model Serialization** | Joblib | 1.3.2 | Model persistence |
| **Environment** | Jupyter Notebook | - | Model development |
| **Version Control** | Git & GitHub | - | Collaboration |

---

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Git (for cloning)

### Step 1: Clone Repository
```bash
git clone https://github.com/ar-jun-web/student-performance-ML-project.git
cd student-performance-ML-project/MLmodels
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
```txt
streamlit==1.31.0
scikit-learn==1.4.0
pandas==2.2.0
numpy==1.26.3
plotly==5.18.0
joblib==1.3.2
```

### Step 3: Verify Installation
```bash
python -c "import streamlit; import sklearn; import plotly; print('✅ Installation successful!')"
```

---

## 🚀 Usage

### Running the Application

```bash
# Navigate to project directory
cd MLmodels

# Launch Streamlit app
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

### Using the Interface

1. **Adjust Input Sliders** (left sidebar)
   - Set study hours, previous scores, sleep hours, etc.
   
2. **Click "🎯 Predict Performance"**
   - View real-time prediction with performance band

3. **Explore Analysis Tabs**
   - Performance Analysis: Overall metrics and visualizations
   - Goal Tracker: Set targets and track progress
   - Peer Comparison: Benchmark against class averages
   - Study Insights: Get personalized recommendations

4. **Interact with Visualizations**
   - Hover over charts for detailed information
   - Compare different scenarios by adjusting inputs

---

## 📈 Model Performance

### Algorithm Comparison

| Model | R² Score | MAE | RMSE | Status |
|-------|----------|-----|------|--------|
| Linear Regression | 0.9897 | 1.52 | 1.98 | Baseline |
| **Random Forest** ✅ | **0.9914** | **1.38** | **1.81** | **Selected** |
| Gradient Boosting | 0.9905 | 1.45 | 1.89 | Evaluated |

**Selected Model:** Random Forest Regressor
- **Accuracy:** 99.14% (R² = 0.9914)
- **Error Range:** ±1.81 points (RMSE)
- **Prediction Speed:** <100ms
- **Hyperparameters:** n_estimators=100, max_depth=10, random_state=42

### Feature Importance (Random Forest Analysis)

1. **Previous Scores** - Strongest predictor (42% importance)
2. **Hours Studied** - High impact (28% importance)
3. **Practice Papers** - Significant factor (18% importance)
4. **Sleep Hours** - Moderate influence (8% importance)
5. **Extracurricular Activities** - Minor but positive effect (4% importance)

### Validation Methodology

- **Cross-Validation:** 5-fold CV performed (consistent performance across folds)
- **Train-Test Split:** 75% training (7,500 samples), 25% testing (2,500 samples)
- **Random State:** 42 (ensures reproducible results)
- **Dataset Size:** 10,000 student records with complete data (no missing values)

---

## 📁 Project Structure

```
student-performance-ML-project/
│
├── MLmodels/
│   ├── app.py                              # Main Streamlit application (850+ lines)
│   ├── enhanced_model_training.ipynb       # Model training & comparison notebook
│   ├── enhanced_model.pkl                  # Trained Random Forest model (production)
│   ├── model.pkl                           # Legacy Linear Regression model (backup)
│   ├── Student_Performance.csv             # Dataset (10,000 records)
│   ├── requirements.txt                    # Python dependencies
│   ├── student.ipynb                       # Original training notebook
│   └── Screenshots/                        # Application screenshots
│       ├── screenshot1.png                 # Performance Analysis tab
│       ├── screenshot2.png                 # Goal Tracker tab
│       ├── screenshot3.png                 # Peer Comparison tab
│       └── screenshot4.png                 # Study Insights tab
│
├── .gitignore                              # Git ignore rules
├── .python-version                         # Python version specification
├── README.md                               # This file
└── pyproject.toml                          # Project metadata
```

---

## 🔬 How It Works

### 1. Data Preprocessing
```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv('Student_Performance.csv')

# Encode categorical variables
df['Extracurricular Activities'] = df['Extracurricular Activities'].map({'Yes': 1, 'No': 0})

# Split features and target
X = df.drop('Performance Index', axis=1)
y = df['Performance Index']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
```

### 2. Feature Engineering
Created 4 engineered features to improve model performance from 98.97% to 99.14%:

```python
# Study-Sleep Balance - captures efficiency of effort vs rest
df['Study_Sleep_Ratio'] = df['Hours Studied'] / (df['Sleep Hours'] + 1)

# Combined Academic Effort
df['Total_Effort'] = df['Hours Studied'] + df['Sample Question Papers Practiced']

# Normalized Previous Performance (0-1 scale)
df['Previous_Score_Normalized'] = df['Previous Scores'] / 100

# Sleep Quality Interaction Term
df['Sleep_Efficiency'] = df['Sleep Hours'] * df['Previous_Score_Normalized']
```

### 3. Model Training & Selection
```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import cross_val_score

# Train multiple models
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
}

# Compare performance
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    
    print(f"{name}: R²={r2:.4f}, MAE={mae:.2f}, RMSE={rmse:.2f}")
    print(f"CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# Select best model (Random Forest)
best_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
best_model.fit(X_train, y_train)
```

### 4. Model Serialization
```python
import joblib

# Package model with metadata
model_package = {
    'best_model': best_model,
    'best_model_name': 'Random Forest Regressor',
    'feature_names': list(X.columns),
    'results': {
        'r2_score': 0.9914,
        'mae': 1.38,
        'rmse': 1.81
    }
}

# Save for deployment
joblib.dump(model_package, 'enhanced_model.pkl')
```

### 5. Web Application Deployment
```python
import streamlit as st
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="AcademyFlow | Student Performance AI",
    page_icon="🎯",
    layout="wide"
)

# Load model (cached for performance)
@st.cache_resource
def load_model():
    return joblib.load('enhanced_model.pkl')

model_data = load_model()
model = model_data['best_model']

# User inputs
hours_studied = st.slider("Hours Studied", 1, 12, 6)
previous_scores = st.slider("Previous Scores", 0, 100, 75)
# ... more inputs

# Make prediction
input_data = prepare_features(hours_studied, previous_scores, ...)
prediction = model.predict(input_data)[0]

# Display results
st.metric("Predicted Performance Index", f"{prediction:.2f}")
```

---

## 📸 Screenshots

### Performance Analysis Tab
![Performance Analysis](Screenshots/screenshot1.png)
*Real-time gauge charts and radar visualization of student profile*

### Goal Tracker Tab
![Goal Tracker](Screenshots/screenshot2.png)
*Interactive goal setting with progress tracking and recommendations*

### Peer Comparison Tab
![Peer Comparison](Screenshots/screenshot3.png)
*Benchmarking against class averages with strength/weakness analysis*

### Study Insights Tab
![Study Insights](Screenshots/screenshot4.png)
*Personalized recommendations and what-if scenario modeling*

---

## 🔄 Development Process

### Phase 1: Planning & Research (Week 1)
- Problem identification and literature review
- Dataset selection and exploratory data analysis
- Technology stack evaluation

### Phase 2: Model Development (Week 2-3)
**Led by: Arjun**
- Data preprocessing and feature engineering
- Multiple algorithm training and comparison
- Hyperparameter tuning and cross-validation
- Model serialization and testing

### Phase 3: Web Application (Week 4-5)
**Led by: Barani**
- Streamlit application architecture
- UI/UX design with glassmorphism theme
- Interactive visualization development
- Four-tab analysis module implementation

### Phase 4: Integration & Testing (Week 6)
**Collaborative**
- Backend-frontend integration
- End-to-end testing
- Performance optimization
- Documentation and presentation preparation

### Key Challenges & Solutions

#### Challenge 1: Model Selection
- **Problem:** Initial Linear Regression model showed 98.97% accuracy but struggled with non-linear patterns
- **Solution:** Implemented ensemble methods (Random Forest, Gradient Boosting) and achieved 99.14% accuracy

#### Challenge 2: Feature Engineering
- **Problem:** Raw features didn't capture interaction effects
- **Solution:** Created 4 engineered features representing study-sleep balance, total effort, normalized scores, and sleep efficiency

#### Challenge 3: UI Performance
- **Problem:** Real-time chart updates caused lag
- **Solution:** Implemented Streamlit caching and optimized Plotly rendering

#### Challenge 4: Kernel Issues
- **Problem:** Jupyter notebook kernel interruptions in VS Code
- **Solution:** Identified correct Python kernel (ml-project 3.14.0) and configured proper environment

---

## 🤝 Contributing

We welcome contributions! If you'd like to improve AcademyFlow:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add YourFeature"
   ```
4. **Push to your branch**
   ```bash
   git push origin feature/YourFeature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Add docstrings to all functions
- Update README for new features
- Include unit tests where applicable
- Test thoroughly before submitting PR

---

## 🐛 Known Issues & Future Roadmap

### Current Limitations
- No user authentication or data persistence
- Single-user mode (no multi-user support)
- Static class averages (not dynamically calculated from real data)
- Desktop-only interface (no mobile app)

### Future Enhancements (v2.0 Roadmap)

#### Short-term (Next 3 months)
- [ ] User authentication system (login/signup)
- [ ] Cloud database integration (Firebase/MongoDB)
- [ ] Export to PDF functionality
- [ ] Dark mode toggle

#### Medium-term (Next 6 months)
- [ ] Deep learning models (LSTM, Neural Networks)
- [ ] Time-series tracking for individual students
- [ ] Subject-wise performance breakdown
- [ ] Multi-language support (Hindi, Tamil)

#### Long-term (Next 12 months)
- [ ] Mobile application (React Native)
- [ ] LMS integration (Moodle, Canvas, Google Classroom)
- [ ] Real-time collaborative features for teachers
- [ ] Advanced analytics dashboard for institutions
- [ ] API for third-party integrations

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024 Barani & Arjun - AcademyFlow AI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 📧 Contact

### Team AcademyFlow

**Arjun**
- GitHub: [@ar-jun-web](https://github.com/ar-jun-web)
- Role: Backend Development & Machine Learning
- Email: arjun@example.com

**Barani**
- GitHub: [@barani](https://github.com/barani)
- Role: Frontend Development & UI/UX Design , ML Model Training & Feature Engineering
- Email: barani@example.com

**Project Repository:** [https://github.com/ar-jun-web/student-performance-ML-project](https://github.com/ar-jun-web/student-performance-ML-project)

**Institution:** Sathyabama University, Chennai  
**Course:** B.Sc Data Science (Final Year)  
**Academic Year:** 2024-2025

---

## 🙏 Acknowledgments

- **Academic Advisor:** [] - For guidance and mentorship
- **Dataset Source:** Student Performance Dataset (Kaggle/UCI Repository)
- **Framework Credits:** Streamlit for rapid prototyping capabilities
- **ML Library:** Scikit-learn for robust ML algorithms
- **Visualization:** Plotly for interactive charts
- **Institution:** Sathyabama University for resources and support
- **Community:** Stack Overflow and GitHub communities for troubleshooting help

---

## 📊 Project Statistics

![GitHub Stars](https://img.shields.io/github/stars/ar-jun-web/student-performance-ML-project?style=social)
![GitHub Forks](https://img.shields.io/github/forks/ar-jun-web/student-performance-ML-project?style=social)
![GitHub Issues](https://img.shields.io/github/issues/ar-jun-web/student-performance-ML-project)
![GitHub Last Commit](https://img.shields.io/github/last-commit/ar-jun-web/student-performance-ML-project)
![Code Size](https://img.shields.io/github/languages/code-size/ar-jun-web/student-performance-ML-project)

**Lines of Code:** ~1,500+ (Python, Markdown, Config)  
**Development Time:** 6 weeks  
**Commits:** 50+  
**Files:** 15+

---

<div align="center">

## ⭐ If you found this project helpful, please give it a star!

### Made with ❤️ by Team AcademyFlow
**Barani & Arjun**

*Turning data into insights, one prediction at a time* 🎓📊

</div>

---

## 📝 Citation

If you use this project in your research or work, please cite:

```bibtex
@software{academyflow2024,
  title = {AcademyFlow AI: Student Performance Prediction System},
  author = {Barani and Arjun},
  year = {2024},
  institution = {Sathyabama University},
  url = {https://github.com/ar-jun-web/student-performance-ML-project}
}
```
