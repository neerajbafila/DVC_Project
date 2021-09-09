
# importing the necessary dependencies
from flask import Flask, render_template, request
from flask_cors import cross_origin
import pickle
import os
from scipy.sparse import data
import yaml
import joblib
import numpy as np


params_path = "params.yaml"
webapp_root = "webapp"
static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")


application = Flask(__name__, static_folder=static_dir,template_folder=template_dir) # initializing a flask app
# app=application

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
        return config

def predict(gre_score,toefl_score,university_rating,sop,lor,cgpa,research):
    try:
        config = read_params(params_path)
        model_dir_path = config['webapp_model_dir']
        scaler_dir_path = config['webapp_scaler_dir']
        model = joblib.load(model_dir_path)
        scaler = joblib.load(scaler_dir_path)
        data = scaler.transform([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]])
        # data = scaler.fit_transform([gre_score,toefl_score,university_rating,sop,lor,cgpa,research])
        prediction = model.predict(data)
        print(prediction)
        return prediction
    except Exception as e:
            print(e)

@application.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@application.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            gre_score=float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            is_research = request.form['research']
            if(is_research=='yes'):
                research=1
            else:
                research=0
            prediction = predict(gre_score,toefl_score,university_rating,sop,lor,cgpa,research)
            # filename = 'finalized_model.pickle'
            # loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # # predictions using the loaded model file
            # prediction=loaded_model.predict([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]])
            # print('prediction is', prediction)
            # # showing the prediction results in a UI
            return render_template('results.html',prediction=np.round(100*prediction[0][0],4))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	application.run(debug=True) # running the app
   