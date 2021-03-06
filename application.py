
# importing the necessary dependencies
from flask import Flask, render_template, request
from flask_cors import cross_origin
import pickle
import os
from scipy.sparse import data
import yaml
import joblib
import numpy as np
from prediction_service import predict

webapp_root = "webapp"
static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")


application = Flask(__name__, static_folder=static_dir,template_folder=template_dir) # initializing a flask app
# app=application


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
            GRE_Score=float(request.form['gre_score'])
            TOEFL_Score = float(request.form['toefl_score'])
            University_Rating = float(request.form['university_rating'])
            SOP = float(request.form['sop'])
            LOR = float(request.form['lor'])
            CGPA = float(request.form['cgpa'])
            is_research = request.form['research']
            if(is_research=='yes'):
                research=1
            else:
                research=0
            data_dic = {"GRE_Score": GRE_Score,
                        "TOEFL_Score": TOEFL_Score,
                        "University_Rating": University_Rating,
                        "SOP":SOP,
                        "LOR": LOR,
                        "CGPA":CGPA,
                        "Research": research}
            prediction = predict.form_response(data_dic)
            # prediction = predict(gre_score,toefl_score,university_rating,sop,lor,cgpa,research)
            # filename = 'finalized_model.pickle'
            # loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # # predictions using the loaded model file
            # prediction=loaded_model.predict([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]])
            # print('prediction is', prediction)
            # # showing the prediction results in a UI
            return render_template('results.html',prediction=np.round(100*prediction[0][0],4))
        except Exception as e:
            print('The Exception message is: ',e)
            # return 'something is wrong'
            return str(e)
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	application.run(debug=True) # running the app
   