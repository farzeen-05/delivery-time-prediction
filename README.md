# 🚚 Delivery Time Prediction — ML Regression Web App

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render)
![License](https://img.shields.io/badge/License-MIT-yellow)

> A machine learning regression app that predicts the exact delivery time of an order based on distance, delivery partner details, and real-world conditions like weather and traffic.

🔗 **Live Demo:** [https://delivery-time-prediction-tcvk.onrender.com](https://delivery-time-prediction-tcvk.onrender.com/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features Used](#features-used)
- [Model](#model)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment](#deployment)

---

## Overview

Delivery time is one of the most important factors in customer satisfaction for logistics and food-delivery platforms — underestimating it is far more costly than overestimating it. This project builds a regression pipeline that takes real order and delivery-partner details as input and predicts the estimated delivery time in minutes, served through a simple Flask web interface.

**What it does:**
- Accepts delivery-related inputs through a web form
- Runs the trained regression model to predict delivery time
- Returns the predicted time instantly to the user
- Deployed as a live, publicly accessible web app

---

## Architecture

```
User (Web Form)
      │
      ▼
Flask App (delivery details submitted)
      │
      ▼
Preprocessing (feature encoding/scaling)
      │
      ▼
Trained Regression Model (scikit-learn)
      │
      ▼
Predicted Delivery Time → rendered back to user
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask |
| Machine Learning | Scikit-learn (Linear Regression / Random Forest / XGBoost) |
| Data Processing | Pandas, NumPy |
| Frontend | HTML, CSS |
| Deployment | Render |

---

## Features Used

The model predicts delivery time based on:

| Feature | Description |
|---------|-------------|
| Distance | Distance between pickup and delivery location |
| Delivery Person Age | Age of the delivery partner |
| Delivery Person Rating | Historical rating of the delivery partner |
| Weather Conditions | Weather at the time of delivery |
| Traffic Conditions | Traffic density on the route |
| Order Preparation Time | Time taken to prepare the order before dispatch |
| Vehicle Type | Type of vehicle used for delivery |

---

## Model

Multiple regression algorithms were evaluated using scikit-learn, including **Linear Regression**, **Random Forest Regressor**, and **XGBoost Regressor**, with the best-performing model selected based on evaluation metrics (e.g. MAE / RMSE / R²) on a held-out test set.

**Pipeline steps:**
1. Data cleaning and handling of missing values
2. Feature encoding for categorical variables (weather, traffic, vehicle type)
3. Feature scaling for numeric inputs
4. Model training and hyperparameter tuning
5. Model evaluation and selection
6. Serialization of the final model (`pickle`/`joblib`) for inference in the Flask app

---

## Project Structure

```
delivery-time-prediction/
├── app.py                  # Flask application entry point
├── model/
│   └── model.pkl            # Trained regression model
├── templates/
│   └── index.html            # Web form UI
├── static/                 # CSS/JS assets
├── notebooks/               # EDA & model training notebooks
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- pip

### Local Setup

```bash
# Clone the repository
git clone https://github.com/farzeen-05/delivery-time-prediction.git
cd delivery-time-prediction

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open `http://localhost:5000` in your browser.

---

## Deployment

Deployed on **Render**, serving the Flask app directly with the pre-trained model bundled into the deployment — no external database or GPU required, making it lightweight and easy to host on a free tier.

---

## Author

**Farzeen Abdul Khadir**
ECE Graduate | ML & Full-Stack Developer | MLOps & Cloud

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?logo=linkedin)](https://www.linkedin.com/in/farzeen-abdul-khadir-8921ba2a1)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?logo=github)](https://github.com/farzeen-05)
[![Email](https://img.shields.io/badge/Email-farzeen99453@gmail.com-EA4335?style=flat&logo=gmail)](mailto:farzeen99453@gmail.com)
---

## License

This project is licensed under the MIT License.
