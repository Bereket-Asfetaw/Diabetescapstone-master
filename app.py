"""importing standard library """
import os
import pandas as pd
import numpy as np
import dill
from flask import Flask, render_template, request 

#Create an instance of Fask
APP = Flask(__name__)

""" Create local  folder  to keep all assets (image and static resources)"""
PEOPLE_FOLDER = os.path.join('/static', 'image')
APP.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


"""
Create a new DataFrame store the input data and.provided to the model and predict a result
"""
def ConvertUserFormToDataFrame(User_Input_data):
     #receive user data
    UserInput = User_Input_data
    column = ['AGE', 'SEX', 'BMI', 'BP', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6']
    predict_input = pd.DataFrame(columns=column)
    inputvalue = np.zeros(10)
    #prepare the input to the appropriate  format 
    Values = list(UserInput.values())
    #convert and save user input
    for idx, val in enumerate(Values):
        if val == 'female':
            inputvalue[idx] = 1
        elif val == 'male':
            inputvalue[idx] = 2
        elif val == '':
            #check if your didn't input value after the fourth serum. use the average value
            average_imputation = {7:4.07 , 8:4.6, 9:91.26 }
            inputvalue[idx] = average_imputation[idx]
        else:
            try:
                inputvalue[idx] = float(val)
            except SystemError as s:
                predicted_value = "Ooops!  Unabale to process your request . please provide only  numeric data "  + str(s)
                return render_template('Capstoneproject.html', Result = predicted_value)

        predict_input.loc[0] = inputvalue
    #return user input in the form of DataFrame
    return predict_input

def Predict(UserData):
    #Load the serialized model
    estimator = dill.load(open("./static/image/KNN_est.dill", "rb"))
    try:
        predicted_value = float(estimator.predict(UserData))
        flag = ""
        if predicted_value >= 55.0 and predicted_value <= 109.0:
            flag = "Normal"
        if predicted_value >= 110.0 and predicted_value <= 125.0:
            flag = "Pre-diabetic"
        if predicted_value >= 126.0:
            flag = "Diabetic"
        #return render_template('Capstoneproject.html', Result=predicted_value , Flag=flag)
        return predicted_value,flag
    except SystemError:
        Error_Message = "Ooops!  Unabale to process your request . please provide only  numeric data "  + str(SyntaxError), " "
        return  Error_Message," "

    

@APP.route('/mainform', methods=['POST', 'GET'])
def capstoneproject():
    if request.method == 'POST':
        #return render_template('Capstoneproject.html', Result = (request.form.to_dict()).values())
        try: 
                 
            #Convert User Information into DataFrame
            UserInfo = ConvertUserFormToDataFrame(request.form.to_dict())   
            #Predict User Data
            
            result, flag = Predict(UserInfo)
            
            #return result
            return render_template('Capstoneproject.html', Result=result, Flag=flag)
            
        except ValueError as e:
            result = "Ooops!  Unabale to process your request .Internal server  problem"  + str(e)
            flag=""
            return render_template('Capstoneproject.html', Result = result, Flag=flag)

@APP.route('/Visualize/')
def Visualize():
    #render the visualization template
    return render_template('Visualize.html')

@APP.route('/contact/')
def contact():
    # render the contact template
    return render_template('contact.html')

@APP.route('/')
def index():
    return render_template('Capstoneproject.html')

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 33507))
    APP.run(debug=True,host='0.0.0.0', port=PORT)
