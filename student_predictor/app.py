from flask import Flask, render_template, request
import pickle
import numpy as np
from db_config import get_connection

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    hours = float(request.form['hours'])
    attendance = int(request.form['attendance'])
    internal = int(request.form['internal'])

    input_data = np.array([[hours, attendance, internal]])
    prediction = float(model.predict(input_data)[0])  # Convert numpy.float64 → float


    # Save to DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (hours_studied, attendance, internal_marks, predicted_score)
        VALUES (%s, %s, %s, %s)
    """, (hours, attendance, internal, prediction))
    conn.commit()
    conn.close()

    return render_template('index.html', result=round(prediction, 2),
                           hours=hours, attendance=attendance, internal=internal)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
