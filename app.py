from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request,  redirect, url_for, make_response
import datetime
import folium

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uzhfmxqswtarzz:6023a52de30ae3e4bcc60da220ded3e030c585d4c8fdc335ae2bbc598079b2d9@ec2-34-203-91-150.compute-1.amazonaws.com:5432/d6msipoere0v0b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class userData(db.Model):
    __tablename__ = 'User_Database'

    UserId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)

    def __init__ (self, UserId, Username, Password):
        self.UserId= UserId
        self.Username= Username
        self.Password = Password

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

def auth_login(username, password):
   username = str(username)
   password = str(password)
   token = userData.query.filter(userData.Username.like(username)).filter(userData.Password.like(password)).first()
   if token:
      return True
   return False

@app.route('/', methods =[ 'POST', 'GET'])
def login_page():
    if request.method == 'POST':
       # getting input with name = fname in HTML form
       username = request.form.get("username")
       password = request.form.get("password")
       resp = make_response(redirect(url_for('map_page')))
       if auth_login(username, password):
          resp.set_cookie('Authentication', 'True')
          return resp 
       resp.set_cookie('Authentication', 'False') 
       return render_template('LoginPageHTML.html')

    return render_template('LoginPageHTML.html')

@app.route('/map', methods=['POST','GET'])
def map_page():  
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":
        if request.method == 'POST':
            location = request.form.get("location")
            location = str(location)
            location_data = mapData.query.filter(mapData.locationName.like(location)).first()
            print("\n",location_data)
            if location_data:
                start_coord = (location_data.latitude, location_data.longitude)
                folium_map = folium.Map(location=start_coord, zoom_start=15, tiles="OpenStreetMap")
                results = db.session.query(mapData).all()
                for item in results:
                    Popup = str(item.locationName) + " Fog:" + str(item.fogData) + " Temperature:" + str(item.temperatureData) + " Humidity:" + str(item.humidityData) + " Light:" + str(item.lightData)
                    folium.CircleMarker(location = [item.latitude, item.longitude],
                            radius = 65, popup = Popup ,fill=True).add_to(folium_map)
                    folium.Marker(location = [item.latitude, item.longitude],
                            radius = 25, popup = Popup ,fill=True).add_to(folium_map)
                folium_map.save('static/DataHTML.html')
                context = { "locationName": location_data.locationName,"fogData": location_data.fogData, "temperatureData": location_data.temperatureData,
                            "humidity": location_data.humidityData, "light":location_data.lightData }
                return render_template('MapPageHTML.html', context = context)
            
            else:
                    location_data = mapData.query.filter(mapData.locationName.like('Kelambakkam')).first()
                    start_coord = (location_data.latitude, location_data.longitude)
                    folium_map = folium.Map(location=start_coord, zoom_start=15, tiles="OpenStreetMap")
                    results = db.session.query(mapData).all()
                    for item in results:
                        Popup = str(item.locationName) + " Fog:" + str(item.fogData) + " Temperature:" + str(item.temperatureData) + " Humidity:" + str(item.humidityData) + " Light:" + str(item.lightData)
                        folium.CircleMarker(location = [item.latitude, item.longitude],
                                radius = 65, popup = Popup ,fill=True).add_to(folium_map)
                        folium.Marker(location = [item.latitude, item.longitude],
                                radius = 25, popup = Popup ,fill=True).add_to(folium_map)
                    folium_map.save('static/DataHTML.html')
                    context = { "locationName": location_data.locationName,"fogData": location_data.fogData, "temperatureData": location_data.temperatureData,
                                "humidity": location_data.humidityData, "light":location_data.lightData }
                    return render_template('MapPageHTML.html', context = context)
                
        location_data = mapData.query.filter(mapData.locationName.like('Kelambakkam')).first()
        start_coord = (location_data.latitude, location_data.longitude)
        folium_map = folium.Map(location=start_coord, zoom_start=15, tiles="OpenStreetMap")
        results = db.session.query(mapData).all()
            
        for item in results:
            Popup = str(item.locationName) + " Fog:" + str(item.fogData) + " Temperature:" + str(item.temperatureData) + " Humidity:" + str(item.humidityData) + " Light:" + str(item.lightData)
            folium.CircleMarker(location = [item.latitude, item.longitude],
            radius = 65, popup = Popup ,fill=True).add_to(folium_map)
            folium.Marker(location = [item.latitude, item.longitude],
            radius = 25, popup = Popup ,fill=True).add_to(folium_map)
            folium_map.save('static/DataHTML.html')
            context = { "locationName": location_data.locationName,"fogData": location_data.fogData, "temperatureData": location_data.temperatureData,
                                "humidity": location_data.humidityData, "light":location_data.lightData }
            return render_template('MapPageHTML.html', context = context)
      
    return redirect(url_for('login_page'))

@app.route('/logout')
def logout_page(): 
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":  
        resp = make_response(redirect(url_for('login_page')))
        resp.set_cookie('Authentication', 'False')
        return resp
    return redirect(url_for('login_page'))

@app.route('/variables')
def variable_page():
    API_var = request.args.get('API', default = '****', type = str)
    locationName_var = request.args.get('location', default = 'Kelambakkam', type = str)
    fogData_var = request.args.get('fogData', default = 0, type = str)
    tempData_var = request.args.get('tempData', default = 0, type = str)
    humiData_var = request.args.get('humiData', default = 0, type = str)
    lightData_var = request.args.get('lightData', default = 0, type = str)
    
    locationName_var = str(locationName_var)
    fogData_var = int(fogData_var)
    tempData_var = int(tempData_var)
    humiData_var = int(humiData_var)
    lightData_var = int(lightData_var)
    
    Data = APIData.query.filter(APIData.APICode.like(API_var)).first()
    print("\n", Data, "API SUCCESSFULL")
    if Data:
        Data = mapData.query.filter(mapData.locationName.like(locationName_var)).first()
        print("\n", Data, "UPDATE SUCCESSFULL")
        if Data:
            resp = make_response(redirect(url_for('map_page')))
            Data.fogData = int(fogData_var)
            Data.temperatureData = int(tempData_var)
            Data.humidityData = int(humiData_var)
            Data.lightData = int(lightData_var)
            Data.dateTime = datetime.datetime.now()
            db.session.commit()
            return resp

    return redirect(url_for('map_page'))

if __name__ == '__main__':
    db.create_all()
    app.run()
