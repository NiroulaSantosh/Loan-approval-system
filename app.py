import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pickle

model = pickle.load(open('c:/Users/Ranzan/Desktop/Mini Project/model.pkl','rb'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ranzankoirala@localhost/loandata'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    contacts = db.Column(db.String(50))
    email = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    marital_status = db.Column(db.String(50))
    education_status = db.Column(db.String(50))
    no_of_dependents = db.Column(db.Integer)
    job_exp = db.Column(db.Integer)
    income = db.Column(db.Integer)
    loan_amount = db.Column(db.Integer)
    interest_rate = db.Column(db.Integer)
    loan_term = db.Column(db.Integer)
    eligibility = db.Column(db.String(50))

    def __init__(self, name, address, contacts, email, gender, marital_status, education_status, no_of_dependents, job_exp, income, loan_amount, interest_rate, loan_term, eligibility):
        self.name = name
        self.address = address
        self.contacts = contacts
        self.email = email
        self.gender = gender
        self.marital_status = marital_status
        self.education_status = education_status
        self.no_of_dependents = no_of_dependents
        self.job_exp = job_exp
        self.income = income
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.loan_term = loan_term
        self.eligibility = eligibility

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/predict.html')
def predict():
    return render_template('predict.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/more.html')
def more():
    return render_template('more.html')

@app.route('/process',methods=['POST'])
def process():
    '''
    For rendering results on HTML GUI
    '''
    name = request.form['name']
    address = request.form['address']
    contacts = request.form['contacts']
    email = request.form['email']
    loan_amount = int(request.form['loan_amount'])
    income = int(request.form['income'])
    interest_rate = int(request.form['interest_rate'])
    tenure = int(request.form['tenure'])
    dependents = int(request.form['dependents'])
    job_duration = int(request.form['job_duration'])

    gender = request.form['gender']
    if gender == 'male':
        gender_val = 1
    else:
        gender_val = 0

    education = request.form['education']
    if education == 'undergraduate':
        education_val = 0
    elif education == 'graduate':
        education_val = 1
    else:
        education_val = 2

    marital_status = request.form['marital_status']
    if marital_status == 'married':
        marital_status_val = 1
    else:
        marital_status_val = 0

    
    int_features = [loan_amount, income, interest_rate, tenure, dependents, gender_val, education_val, job_duration, marital_status_val]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    prediction_int = prediction[0]
    if prediction_int == 1 :
        eligibility = "Eligible"
    else :
        eligibility = "Not Eligible"

    user = User(name, address, contacts, email, gender, marital_status, education, dependents, job_duration, income, loan_amount, interest_rate, tenure, eligibility)
    db.session.add(user)
    db.session.commit()

    return render_template('result.html', name = 'Name   : {}'.format(name), address = 'Address   : {}'.format(address), contacts = 'Contacts   : {}'.format(contacts), Email = 'Email   : {}'.format(email), gender = 'Gender   : {}'.format(gender), marital_status = 'Marital Status  : {}'.format(marital_status), education = 'Education Status   : {}'.format(education), dependents = 'No. of Dependents   : {}'.format(dependents), job_duration = 'Job Experience   : {}'.format(job_duration), income = 'Monthly Income   : {}'.format(income), loan_amount = 'Loan Amount   : {}'.format(loan_amount), interest_rate = 'Interest Rate   : {}%'.format(interest_rate), tenure = 'Loan Term (in months)  : {}'.format(tenure), prediction_text= 'The Loan Applicant is {}'.format(eligibility))

if __name__ == "__main__":
    app.run(debug=True)