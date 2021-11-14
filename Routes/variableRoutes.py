from flask import Blueprint, render_template, request,  redirect, url_for
from database import db
import pandas as pd
import datetime
from mapRoutes import mapData, APIData

variables = Blueprint("variables", __name__ )

@variables.route('/variables')
def variable_page():
    API_var = request.args.get('API', default = '****', type = str)
    locationName_var = request.args.get('location', default = 'Chennai', type = str)
    latitude_var = request.args.get('latitude', default = 13.067439, type = float)
    longitude_var = request.args.get('longitude', default = 80.237617, type = float)
    fogData_var = request.args.get('fogData', default = 0, type = int)
    tempData_var = request.args.get('tempData', default = 0, type = int)
    humiData_var = request.args.get('humiData', default = 0, type = int)
    lightData_var = request.args.get('lightData', default = 0, type = int)

    Data = APIData.query.filter(APIData.APICode.like(API_var)).first()
    if Data:
        Data = mapData.query.filter(mapData.locationName.like(locationName_var)).filter(mapData.latitude.like(latitude_var)).filter(mapData.longitude.like(longitude_var)).first()
        if Data:
            Data.fogData = fogData_var
            Data.temperatureData = tempData_var
            Data.humidityData = humiData_var
            Data.lightData = lightData_var
            Data.dateTime = datetime.datetime.now()
            db.session.commit()

    return redirect(url_for('maps.map_page'))

@variables.route('/pushBack')
def pushBack():
    df = pd.read_excel("Mapdata.xlsx")
    for i in range(len(df)):
        Data = mapData(locationName = df.loc[i]['Area'], latitude = df.loc[i]['Latitude'], 
                        longitude = df.loc[i]['Longitude'], dateTime=datetime.datetime.now(), fogData= 0, 
                        temperatureData=0, humidityData=0, lightData=0)
        db.session.add(Data)
        db.session.commit()
    return redirect(url_for('maps.map_page'))