from flask import Flask, render_template, request
import joblib

# Load the trained ML model
model = joblib.load('model.joblib')

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Other static pages
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Prediction route
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            # Get form values
            brand_name = request.form['brand_name']
            owner = float(request.form['owner'])
            kms_driven = float(request.form['kms_driven'])
            age = float(request.form['age'])
            power = float(request.form['power'])

            # Encode brand
            bike_numbers = {
                'TVS': 0, 'Royal Enfield': 1, 'Triumph': 2, 'Yamaha': 3,
                'Honda': 4, 'Hero': 5, 'Bajaj': 6, 'Suzuki': 7, 'Benelli': 8,
                'KTM': 9, 'Mahindra': 10, 'Kawasaki': 11, 'Ducati': 12,
                'Hyosung': 13, 'Harley-Davidson': 14, 'Jawa': 15, 'BMW': 16,
                'Indian': 17, 'Rajdoot': 18, 'LML': 19, 'Yezdi': 20,
                'MV': 21, 'Ideal': 22
            }
            brand_name_encode = float(bike_numbers[brand_name])

            # Prepare input for prediction
            lst = [[kms_driven, owner, age, power, brand_name_encode]]
            print("Input to model:", lst)

            
            # Make prediction
            pred = float(model.predict(lst)[0])  # convert to float first
            pred = round(pred, 2)


            # Render result
            return render_template('project.html', prediction=pred)

        except Exception as e:
            return f"Prediction Error: {e}"

    return render_template('project.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
