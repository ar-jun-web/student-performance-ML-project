# 🎓 Student Performance Prediction System

A machine learning web application that predicts student academic performance based on study habits, sleep patterns, and other behavioral factors.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)

## 📊 Project Overview

This project uses **Linear Regression** to predict student performance index (0-100 scale) based on five key features:
- Hours studied per day
- Previous exam scores
- Extracurricular activity participation
- Sleep hours per night
- Number of sample papers practiced

The model achieves an **R² score of ~0.99** on the test dataset.

## 📸 Screenshots

![App Screenshot](Screenshots/screenshot1.png)
![Prediction Results](Screenshots/screenshot2.png)

## 🛠️ Technologies Used

- **Python 3.8+**
- **Scikit-learn** - Machine learning model training
- **Pandas & NumPy** - Data manipulation
- **Streamlit** - Web application framework
- **Plotly** - Data visualization

## 📁 Project Structure
# 🎓 Student Performance Prediction System

A machine learning web application that predicts student academic performance based on study habits, sleep patterns, and other behavioral factors.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)

## 📊 Project Overview

This project uses **Linear Regression** to predict student performance index (0-100 scale) based on five key features:
- Hours studied per day
- Previous exam scores
- Extracurricular activity participation
- Sleep hours per night
- Number of sample papers practiced

The model achieves an **R² score of ~0.99** on the test dataset.

## 📸 Screenshots

![App Screenshot](Screenshots/screenshot1.png)
![Prediction Results](Screenshots/screenshot2.png)

## 🛠️ Technologies Used

- **Python 3.8+**
- **Scikit-learn** - Machine learning model training
- **Pandas & NumPy** - Data manipulation
- **Streamlit** - Web application framework
- **Plotly** - Data visualization

## 📁 Project Structure
```
student-performance-predictor/
├── app.py                              # Streamlit web application
├── student.ipynb                       # Model training notebook
├── student_performance_model.pkl       # Trained ML model
├── Student_Performance.csv             # Dataset
├── requirements.txt                    # Dependencies
├── README.md                           # Documentation
└── Screenshots/                        # App screenshots
```

## 💻 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR-USERNAME/student-performance-predictor.git
   cd student-performance-predictor
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Run the application**
```bash
   streamlit run app.py
```

4. **Open browser at** `http://localhost:8501/`

## 📊 Dataset Information

Dataset contains 10,000 student records with features:

| Feature | Range |
|---------|-------|
| Hours Studied | 1-9 hours |
| Previous Scores | 40-99 |
| Extracurricular Activities | Yes/No |
| Sleep Hours | 4-9 hours |
| Sample Papers Practiced | 0-9 papers |

## 🧠 Model Performance

- **Algorithm**: Linear Regression
- **R² Score**: ~0.99
- **MAE**: ~1.5
- **RMSE**: ~2.0

## ✨ Key Features

- Real-time predictions with interactive sliders
- Performance gauges and visualizations
- Student profile radar chart
- Feature importance analysis
- What-if scenario explorer
- Smart insights and recommendations

## 🎯 Use Cases

- Academic counselors identifying at-risk students
- Students understanding study habit impacts
- Educational institutions for data-driven planning
- Parents monitoring student progress

## 🔮 Future Enhancements

- [ ] Add ensemble models (Random Forest, XGBoost)
- [ ] CSV upload for batch predictions
- [ ] Downloadable PDF reports
- [ ] User authentication
- [ ] Mobile app version

## 👨‍💻 Author

**BARANI**
- GitHub: [lynxofficial7777-hash](https://github.com/lynxofficial7777-hash)
- Email: baranimoorthy77@gmail.com

## 🙏 Acknowledgments

Built as a Final Year Machine Learning Project

---

⭐ If you found this project helpful, please give it a star!