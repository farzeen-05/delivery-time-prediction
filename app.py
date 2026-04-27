from flask import Flask,render_template,request,redirect,url_for,flash,session
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
import re
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = '9945'

#saving model
model=joblib.load("delivery_time1_model.pkl")
scaler=joblib.load("scaler1.pkl")

#Database connection
def get_db_connection():
    url = os.getenv("DATABASE_URL")

    # split the URL
    import urllib.parse as urlparse
    urlparse.uses_netloc.append("mysql")
    parsed = urlparse.urlparse(url)

    return mysql.connector.connect(
        host=parsed.hostname,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path.lstrip('/'),
        port=parsed.port
    )

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    if 'user_id' not in session:
        flash("Please login to access the prediction system", "warning")
        return redirect(url_for('register'))

    prediction = None 

    if request.method == "POST":
        Distance_km = float(request.form['Distance_km'])
        Traffic_Level = request.form['Traffic_Level']
        Preparation_Time_min = int(request.form['Preparation_Time_min'])
        Courier_Experience_yrs = int(request.form['Courier_Experience_yrs'])
        weather = request.form['Weather']
        time_of_day = request.form['Time_of_Day']
        vehicle = request.form['Vehicle_Type']

        # weather
        Weather_Clear = 1 if weather == "clear" else 0
        Weather_Foggy = 1 if weather == "foggy" else 0
        Weather_Rainy = 1 if weather == "rainy" else 0
        Weather_Snowy = 1 if weather == "snowy" else 0
        Weather_Windy = 1 if weather == "windy" else 0

        # time
        Time_of_Day_Morning = 1 if time_of_day == "morning" else 0
        Time_of_Day_Afternoon = 1 if time_of_day == "afternoon" else 0
        Time_of_Day_Evening = 1 if time_of_day == "evening" else 0
        Time_of_Day_Night = 1 if time_of_day == "night" else 0

        # vehicle
        Vehicle_Type_Bike = 1 if vehicle == "bike" else 0
        Vehicle_Type_Car = 1 if vehicle == "car" else 0
        Vehicle_Type_Scooter = 1 if vehicle == "scooter" else 0

        order_features = {
            "Distance_km": Distance_km,
            "Traffic_Level": Traffic_Level,
            "Preparation_Time_min": Preparation_Time_min,
            "Courier_Experience_yrs": Courier_Experience_yrs,
            "Weather_Clear": Weather_Clear,
            "Weather_Foggy": Weather_Foggy,
            "Weather_Rainy": Weather_Rainy,
            "Weather_Snowy": Weather_Snowy,
            "Weather_Windy": Weather_Windy,
            "Time_of_Day_Afternoon": Time_of_Day_Afternoon,
            "Time_of_Day_Evening": Time_of_Day_Evening,
            "Time_of_Day_Morning": Time_of_Day_Morning,
            "Time_of_Day_Night": Time_of_Day_Night,
            "Vehicle_Type_Bike": Vehicle_Type_Bike,
            "Vehicle_Type_Car": Vehicle_Type_Car,
            "Vehicle_Type_Scooter": Vehicle_Type_Scooter
        }

        order_df = pd.DataFrame([order_features])

        test_scaled = scaler.transform(order_df)
        prediction = model.predict(test_scaled)
        prediction = round(float(model.predict(test_scaled)[0]), 2)

        hours = int(prediction // 60)
        minutes = int(prediction % 60)

        formatted_time = f"{hours} hr {minutes} min" if hours > 0 else f"{minutes} min"

        return render_template('predict.html', prediction=formatted_time)
    return render_template('predict.html', prediction=prediction)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format", "danger")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters", "danger")
            return redirect(url_for('register'))    

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email =%s" ,(email,))
        user=cursor.fetchone()
        cursor.close()
        cursor.close()

        if user and check_password_hash (user['password'],password):
            session['user_id']=user['u_id']
            session['username']=user['u_name']
            return redirect(url_for('index'))    
        else:
            flash("Invalid email or password ","danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u_name = request.form['u_name']
        email = request.form['email']
        password = request.form['password']

        # validation INSIDE POST
        if not u_name.strip():
            flash("Username is required", "danger")
            return redirect(url_for('register'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format", "danger")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters", "danger")
            return redirect(url_for('register'))

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT u_id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            flash("Email already registered", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (u_name, email, password) VALUES (%s, %s, %s)",
            (u_name, email, hashed_password)
        )
        conn.commit()

        cursor.close()
        conn.close()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for('login'))

    #  GET request safe
    return render_template('register.html')
   

if __name__ == '__main__':
    app.run(debug=True, port=4000)

