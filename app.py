from flask import Flask, request, render_template, jsonify
from flask_cors import cross_origin
import pickle
import pandas as pd
import os
import numpy as np
import joblib

"""This module is all about taking the required information from the user and applying all the preprocessing 
techniques performed on the original data, so as to predict the price of the flight ticket"""

params_path="params.yaml"
webapp_root="webapp"

static_dir=os.path.join(webapp_root,"static")
template_dir=os.path.join(webapp_root,"templates")
#wert


app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
#model = pickle.load(open("model.pkl", "rb"))
# config = read_params(params_path)
# model_dir_path = config["webapp_model_dir"]
model = joblib.load("prediction_service/model/model.joblib")


# def read_params(config_path=params_path):
#     with open(config_path) as yaml_file:
#         config = yaml.safe_load(yaml_file)
#     return config

# def predict(Total_Stops,
#                 journey_day,
#                 journey_month,
#                 Dep_Time_hour,
#                 Dep_Time_min,
#                 Arrival_Time_hour,
#                 Arrival_Time_min,
#                 Duration_hours,
#                 Duration_mins,
#                 Air_India,
#                 GoAir,
#                 IndiGo,
#                 Jet_Airways,
#                 Jet_Airways_Business,
#                 Multiple_carriers,
#                 Multiple_carriers_Premium_economy,
#                 SpiceJet,
#                 Trujet,
#                 Vistara,
#                 Vistara_Premium_economy,
#                 Chennai,
#                 Delhi,
#                 Kolkata,
#                 Mumbai,
#                 d_Cochin,
#                 d_Delhi,
#                 d_Hyderabad,
#                 d_Kolkata,
#                 d_New_Delhi):
#     config = read_params(params_path)
#     model_dir_path = config["webapp_model_dir"]
#     model = joblib.load(model_dir_path)
#     prediction = model.predict(Total_Stops,
#                 journey_day,
#                 journey_month,
#                 Dep_Time_hour,
#                 Dep_Time_min,
#                 Arrival_Time_hour,
#                 Arrival_Time_min,
#                 Duration_hours,
#                 Duration_mins,
#                 Air_India,
#                 GoAir,
#                 IndiGo,
#                 Jet_Airways,
#                 Jet_Airways_Business,
#                 Multiple_carriers,
#                 Multiple_carriers_Premium_economy,
#                 SpiceJet,
#                 Trujet,
#                 Vistara,
#                 Vistara_Premium_economy,
#                 Chennai,
#                 Delhi,
#                 Kolkata,
#                 Mumbai,
#                 d_Cochin,
#                 d_Delhi,
#                 d_Hyderabad,
#                 d_Kolkata,
#                 d_New_Delhi)
#     print(prediction)
#     return prediction


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/prediction", methods=["GET", "POST"])
@cross_origin()
def predict():
    try:
        if request.method == "POST":

            # app.logger.info("ready to take input form the user")

            # Date_of_Journey
            date_dep = request.form["Dep_Time"]
            # app.logger.info("the user gave the input for data departure as" + ' ' + str(date_dep))
            journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
            # app.logger.info("the day is being extracted from the input" + ' ' + str(
            #     date_dep) + ' ' + "the extracted value is" + ' ' + str(journey_day))
            journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
            # app.logger.info("the month is being extracted from the input" + ' ' + str(
            #     date_dep) + ' ' + "the extracted value is" + ' ' + str(journey_month))
            # print("Journey Date : ",journey_day, journey_month)

            # Departure
            Dep_Time_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
            # app.logger.info("the hour is being extracted from the input" + ' ' + str(
            #     date_dep) + ' ' + "the extracted value is" + ' ' + str(Dep_Time_hour))
            Dep_Time_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
            # app.logger.info("the minutes is being extracted from the input" + ' ' + str(
            #     date_dep) + ' ' + "the extracted value is" + ' ' + str(Dep_Time_min))

            # print("Departure : ",Dep_Time_hour, Dep_Time_min)

            # Arrival
            date_arr = request.form["Arrival_Time"]
            # app.logger.info("the user gave the input for date arrival as" + ' ' + str(date_arr))
            Arrival_Time_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
            #app.logger.info("the hours is being extracted from the input" + ' ' + str(
             #   date_arr) + ' ' + "the extracted value is" + ' ' + str(Arrival_Time_hour))
            Arrival_Time_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)
            # app.logger.info("the minutes is being extracted from the input" + ' ' + str(
            #     date_arr) + ' ' + "the extracted value is" + ' ' + str(Arrival_Time_min))
            # print("Arrival : ", Arrival_Time_hour, Arrival_Time_min)

            # Duration
            Duration_hours = abs(Arrival_Time_hour - Dep_Time_hour)
            # app.logger.info("retrieving the absolute value of" + ' ' + str(Duration_hours) + ' ' + "from" + ' ' + str(
            #     Arrival_Time_hour) + ' ' + "and" + ' ' + str(Dep_Time_hour))
            Duration_mins = abs(Arrival_Time_min - Dep_Time_min)
            # app.logger.info("retrieving the absolute value of" + ' ' + str(Duration_mins) + ' ' + "from" + ' ' + str(
            #     Arrival_Time_min) + ' ' + "and" + ' ' + str(Dep_Time_min))
            # print("Duration : ", Duration_hours, Duration_mins)

            # Total Stops
            Total_Stops = int(request.form["stops"])
            # app.logger.info("the user gave the input for total stops as" + ' ' + str(Total_Stops))
            # print(Total_Stops)

            # Airline
            # AIR ASIA = 0 (not in column)
            airline = request.form['airline']
            # app.logger.info("the user gave the input for airlines as" + ' ' + str(airline))
            if airline == 'Jet Airways':
                Jet_Airways = 1
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif airline == 'IndiGo':
                Jet_Airways = 0
                IndiGo = 1
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif airline == 'Air India':
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 1
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif airline == 'Multiple carriers':
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 1
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif airline == 'SpiceJet':
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 1
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif airline == 'Vistara':
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 1
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif airline == 'GoAir':
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 1
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif airline == 'Multiple carriers Premium economy':
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 1
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            elif airline == 'Jet Airways Business':
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 1
                Vistara_Premium_economy = 0
                Trujet = 0

            elif airline == 'Vistara Premium economy':
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 1
                Trujet = 0

            elif airline == 'Trujet':
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 1

            else:
                Jet_Airways = 0
                IndiGo = 0
                Air_India = 0
                Multiple_carriers = 0
                SpiceJet = 0
                Vistara = 0
                GoAir = 0
                Multiple_carriers_Premium_economy = 0
                Jet_Airways_Business = 0
                Vistara_Premium_economy = 0
                Trujet = 0

            # app.logger.info(
            #     "the input given by the users are" + ' ' + str(Jet_Airways) + ' ' + str(IndiGo) + ' ' + str(
            #         Air_India) + ' ' + str(
            #         Multiple_carriers) + ' ' + str(SpiceJet) + ' ' + str(Vistara) + ' ' + str(GoAir) + ' ' + str(
            #         Multiple_carriers_Premium_economy) + ' ' + str(Jet_Airways_Business) + ' ' + str(
            #         Vistara_Premium_economy) + ' ' + str(
            #         Trujet))

            # print(Jet_Airways,
            #     IndiGo,
            #     Air_India,
            #     Multiple_carriers,
            #     SpiceJet,
            #     Vistara,
            #     GoAir,
            #     Multiple_carriers_Premium_economy,
            #     Jet_Airways_Business,
            #     Vistara_Premium_economy,
            #     Trujet)

            # Source
            # Banglore = 0 (not in column)
            Source = request.form["Source"]
            # app.logger.info("the user gave the input for source as" + ' ' + str(Source))
            if Source == 'Delhi':
                Delhi = 1
                Kolkata = 0
                Mumbai = 0
                Chennai = 0

            elif Source == 'Kolkata':
                Delhi = 0
                Kolkata = 1
                Mumbai = 0
                Chennai = 0

            elif Source == 'Mumbai':
                Delhi = 0
                Kolkata = 0
                Mumbai = 1
                Chennai = 0

            elif Source == 'Chennai':
                Delhi = 0
                Kolkata = 0
                Mumbai = 0
                Chennai = 1

            else:
                Delhi = 0
                Kolkata = 0
                Mumbai = 0
                Chennai = 0

            # app.logger.info(
            #     "the input given by the users are" + ' ' + str(Delhi) + ' ' + str(Kolkata) + ' ' + str(
            #         Mumbai) + ' ' + str(Chennai))

            # print(Delhi,
            #     Kolkata,
            #     Mumbai,
            #     Chennai)

            # Destination
            # Banglore = 0 (not in column)
            Destination = request.form["Destination"]
            # app.logger.info("the user gave the input for source as" + ' ' + str(Destination))
            if Destination == 'Cochin':
                d_Cochin = 1
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 0

            elif Destination == 'Delhi':
                d_Cochin = 0
                d_Delhi = 1
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 0

            elif Destination == 'New_Delhi':
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 1
                d_Hyderabad = 0
                d_Kolkata = 0

            elif Destination == 'Hyderabad':
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 1
                d_Kolkata = 0

            elif Destination == 'Kolkata':
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 1

            else:
                d_Cochin = 0
                d_Delhi = 0
                d_New_Delhi = 0
                d_Hyderabad = 0
                d_Kolkata = 0

            # app.logger.info("the input given by the users are" + ' ' + str(Cochin) + ' ' + str(Delhi) + ' ' + str(
            #     New_Delhi) + ' ' + str(
            #     Hyderabad) + ' ' + str(Kolkata))

            # print(
            #     Cochin,
            #     Delhi,
            #     New_Delhi,
            #     Hyderabad,
            #     Kolkata
            # )

            #     ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
            #    'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
            #    'Duration_mins', 'Air_India', 'GoAir', 'IndiGo',
            #    'Jet_Airways', 'Jet_Airways_Business',
            #    'Multiple_carriers',
            #    'Multiple_carriers_Premium_economy', 'SpiceJet',
            #    'Trujet', 'Vistara', 'Vistara_Premium_economy',
            #    'Chennai', 'Delhi', 'Kolkata', 'Mumbai',
            #    'Cochin', 'Delhi', 'Hyderabad',
            #    'Kolkata', 'New Delhi']

            # finally after taking all the inputs from the users, and giving it to the model

            prediction = model.predict([[
                Total_Stops,
                journey_day,
                journey_month,
                Dep_Time_hour,
                Dep_Time_min,
                Arrival_Time_hour,
                Arrival_Time_min,
                Duration_hours,
                Duration_mins,
                Air_India,
                GoAir,
                IndiGo,
                Jet_Airways,
                Jet_Airways_Business,
                Multiple_carriers,
                Multiple_carriers_Premium_economy,
                SpiceJet,
                Trujet,
                Vistara,
                Vistara_Premium_economy,
                Chennai,
                Delhi,
                Kolkata,
                Mumbai,
                d_Cochin,
                d_Delhi,
                d_Hyderabad,
                d_Kolkata,
                d_New_Delhi
            ]])

            output = round(prediction[0], 2)
            # app.logger.info("displaying the predicted price to the user as:" + ' ' + str(output))

            # app.logger.warning("rendering the results to the user on the interface:" + ' ' + str(output))
            return render_template('home.html',
                                   Flight_Price="Your journey costs about, Rs. {} \nThank You for visiting our "
                                                "website have a safe journey😊".format(
                                       output))

        # app.logger.info("rendering the template to the html page")
        return render_template("home.html")

    except Exception as e:
        # app.logger.error("an error has occurred during the execution of the program, which is:" + ' ' + str(e))
        return "the exception occurred is" + ' ' + str(e)


if __name__ == "__main__":
    app.run(debug=True)
