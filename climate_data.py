from flask import Flask, request, render_template
import requests


app = Flask(__name__)


API_KEY = '194ff5e75473e82e8f67e9c6478707a5'  # Reemplaza con tu API Key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'


# Ruta principal con pestañas
@app.route('/')
def home():
   return render_template('index.html')


# Función para obtener datos del clima
def fetch_weather(city):
   params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
   response = requests.get(BASE_URL, params=params)
   return response.json() if response.status_code == 200 else None


# Ruta para obtener el clima general de una ciudad
@app.route('/general', methods=['GET', 'POST'])
def general_weather():
   if request.method == 'POST':
       city = request.form.get('city')
       city_data = fetch_weather(city)
      
       if city_data:
           weather_info = {
               'name': city_data['name'],
               'temp': city_data['main']['temp'],
               'feels_like': city_data['main']['feels_like'],
               'temp_min': city_data['main']['temp_min'],
               'temp_max': city_data['main']['temp_max'],
               'humidity': city_data['main']['humidity'],
               'wind_speed': city_data['wind']['speed'],
               'description': city_data['weather'][0]['description'],
               'icon': city_data['weather'][0]['icon']
           }
           return render_template('general_result.html', **weather_info)
       else:
           error = "City not found or error fetching weather data."
           return render_template('general_result.html', error=error)
  
   return render_template('general_form.html')


# Ruta para comparar clima entre dos ciudades
@app.route('/compare', methods=['GET', 'POST'])
def compare_weather():
   if request.method == 'POST':
       city1 = request.form.get('city1')
       city2 = request.form.get('city2')
       preference = request.form.get('preference')


       city1_data = fetch_weather(city1)
       city2_data = fetch_weather(city2)


       best_city = None
       if city1_data and city2_data:
           weather1 = city1_data['weather'][0]['main'].lower()
           weather2 = city2_data['weather'][0]['main'].lower()
          
           weather_map = {
               'sunny': ['clear', 'few clouds'],
               'rainy': ['rain', 'drizzle'],
               'snowy': ['snow'],
               'cloudy': ['clouds', 'overcast clouds'],
               'clear': ['clear']
           }
          
           if weather1 in weather_map.get(preference, []):
               best_city = {'name': city1, 'temp': city1_data['main']['temp'], 'weather': weather1, 'icon': city1_data['weather'][0]['icon']}
           elif weather2 in weather_map.get(preference, []):
               best_city = {'name': city2, 'temp': city2_data['main']['temp'], 'weather': weather2, 'icon': city2_data['weather'][0]['icon']}


       if best_city:
           message = f"The best city for {preference} weather is {best_city['name']}!"
           return render_template('compare_result.html', best_city=best_city, message=message)
       else:
           error = "Neither city matches your preference. Try checking the weather manually."
           return render_template('compare_result.html', error=error)


   return render_template('compare_form.html')


# Ruta para seleccionar el clima en Europa
@app.route('/select_weather', methods=['GET', 'POST'])
def select_weather():
   if request.method == 'POST':
       preference = request.form.get('preference')
       cities = ['London', 'Paris', 'Berlin', 'Madrid', 'Rome', 'Athens']  # Ejemplo de ciudades en Europa
       best_city = None


       for city in cities:
           data = fetch_weather(city)
           if data:
               weather = data['weather'][0]['main'].lower()
               if preference in ['sunny', 'rainy', 'snowy', 'cloudy', 'clear']:
                   weather_map = {
                       'sunny': ['clear', 'few clouds'],
                       'rainy': ['rain', 'drizzle'],
                       'snowy': ['snow'],
                       'cloudy': ['clouds', 'overcast clouds'],
                       'clear': ['clear']
                   }
                   if weather in weather_map[preference]:
                       best_city = {'name': city, 'temp': data['main']['temp'], 'weather': weather, 'icon': data['weather'][0]['icon']}
                       break


       return render_template('select_weather_result.html', best_city=best_city, preference=preference)
  
   return render_template('select_weather_form.html')


if __name__ == '__main__':
   app.run(debug=True)