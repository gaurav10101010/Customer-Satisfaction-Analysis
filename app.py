from flask import Flask, render_template, request
import joblib
from satisfactiondata import create_table, insert_data  # type: ignore # Import functions from your database module

# Load your pre-trained model
model = joblib.load(r"C:\Users\asus\Desktop\projects\customer_satisfaction\model\logistic_regression (1).lb")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/prediction', methods=['POST'])
def prediction():
    if request.method == "POST":
        # Retrieve form data and convert to appropriate types
        age = int(request.form['age'])
        flight_distance = int(request.form['flight_distance'])
        inflight_entertainment = int(request.form["inflight_entertainment"])
        baggage_handling = int(request.form["baggage_handling"])
        cleanliness = int(request.form["cleanliness"])
        departure_delay = int(request.form["departure_delay"])
        arrival_delay = int(request.form["arrival_delay"])
        gender = (request.form["gender"])
        customer_type = (request.form["customer_type"])
        travel_type = (request.form["travel_type"])
        class_type = (request.form["class_type"])

        # Create dummy variables for class types
        Class_Eco = 1 if class_type == 'ECO' else 0
        Class_Eco_Plus = 1 if class_type == 'ECO_PLUS' else 0

        gender = 1 if class_type == 'male' else 0
        gender = 1 if class_type == 'female' else 0

        customer_type = 1 if class_type == 'loyal' else 0
        customer_type = 1 if class_type == 'new' else 0

        travel_type = 1 if class_type == 'personal' else 0
        gender = 1 if class_type == 'bussiness' else 0

        # Prepare the input data for prediction
        UNSEEN_DATA = [[
            age, flight_distance, inflight_entertainment, baggage_handling,
            cleanliness, departure_delay, arrival_delay, gender,
            customer_type, travel_type, Class_Eco, Class_Eco_Plus
        ]]

        # Make prediction
        prediction = model.predict(UNSEEN_DATA)[0]
        labels = {1: "SATISFIED", 0: "DISSATISFIED"}

        # Insert data into the database
        data = (
            age, flight_distance, inflight_entertainment, baggage_handling,
            cleanliness, departure_delay, arrival_delay, gender, customer_type,
            travel_type, class_type, labels[prediction]
        )
        insert_data(data)

        # Render output.html with prediction and input data
        return render_template('output.html',
                               output=labels[prediction],
                               age=age,
                               flight_distance=flight_distance,
                               inflight_entertainment=inflight_entertainment,
                               baggage_handling=baggage_handling,
                               cleanliness=cleanliness,
                               departure_delay=departure_delay,
                               arrival_delay=arrival_delay,
                               gender=gender,
                               customer_type=customer_type,
                               travel_type=travel_type,
                               class_type=class_type)

if __name__ == "__main__":
    create_table()  # Ensure the table is created before running the app
    app.run(debug=True)