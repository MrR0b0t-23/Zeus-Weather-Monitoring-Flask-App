from flask import Blueprint, render_template, request, redirect, url_for, make_response
from database import db
import datetime
import folium

maps = Blueprint("maps", __name__ , template_folder='Templates', static_folder= 'static')

class mapData(db.Model):
    __tablename__ = 'Map_Database'

    locationId = db.Column(db.Integer, primary_key=True)

    locationName = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False,default= datetime.datetime.utcnow())
    fogData = db.Column(db.Integer, nullable=False)
    temperatureData = db.Column(db.Integer, nullable=False)
    humidityData = db.Column(db.Integer, nullable=False)
    lightData = db.Column(db.Integer, nullable=False)

    def __init__ (self, locationName, latitude, longitude, dateTime,fogData, temperatureData,humidityData,lightData):
        self.locationName= locationName
        self.latitude= latitude
        self.longitude= longitude
        self.dateTime= dateTime
        self.fogData = fogData
        self.temperatureData = temperatureData
        self.humidityData = humidityData
        self.lightData = lightData

class APIData(db.Model):
    __tablename__ = 'API_Database'

    APIId = db.Column(db.Integer, primary_key=True)
    APICode = db.Column(db.String(80), nullable=False)

    def __init__ (self, APIId, APICode):
        self.APIId= APIId
        self.APICode= APICode

@maps.route('/map', methods=['POST','GET'])
def map_page():  
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":
        if request.method == 'POST':
            location = request.form.get("location")
            location_data = mapData.query.filter(mapData.locationName.like(location)).first()
            if location_data:
                start_coord = (location_data.latitude, location_data.longitude)
                folium_map = folium.Map(location=start_coord, zoom_start=24, tiles="OpenStreetMap")
                results = db.session.query(mapData).all()
                for item in results:
                    Popup = str(item.locationName) + " Fog:" + str(item.fogData) + " Temperature:" + str(item.temperatureData) + " Humidity:" + str(item.humidityData) + " Light:" + str(item.lightData)
                    folium.CircleMarker(location = [item.latitude, item.longitude],
                            radius = 50, popup = Popup ,fill=True).add_to(folium_map)
                    folium.Marker(location = [item.latitude, item.longitude],
                            radius = 25, popup = Popup ,fill=True).add_to(folium_map)
                folium_map.save('static/DataHTML.html')
                context = { "locationName": location_data.locationName,"fogData": location_data.fogData, "temperatureData": location_data.temperatureData,
                            "humidity": location_data.humidityData, "light":location_data.lightData }
                return render_template('MapPageHTML.html', context = context)
    
        start_coords = (13.067439, 80.237617)
        folium_map = folium.Map(location=start_coords, zoom_start=14, tiles="OpenStreetMap")
        results = db.session.query(mapData).all()
        for item in results:
            Popup = str(item.locationName) + " Fog:" + str(item.fogData) + " Temperature:" + str(item.temperatureData) + " Humidity:" + str(item.humidityData) + " Light:" + str(item.lightData)
            folium.CircleMarker(location = [item.latitude, item.longitude],
                radius = 25, popup = Popup ,fill=True ).add_to(folium_map)
        folium_map.save('static/DataHTML.html')
        return render_template('MapPageHTML.html')

    return redirect(url_for('login.login_page'))

@maps.route('/logout')
def logout_page(): 
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":  
        resp = make_response(redirect(url_for('login.login_page')))
        resp.set_cookie('Authentication', 'False')
        return resp
    return redirect(url_for('login.login_page'))