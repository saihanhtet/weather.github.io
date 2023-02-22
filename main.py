from flask import Flask, render_template, request
from dotenv import load_dotenv
from weather import Weather
import random

app = Flask(__name__)  # initialise application

# configurations


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        city = request.form['name']
        weather = Weather(city).new(sentence=False)
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(weather[12] / (360. / len(dirs)))
        direction = dirs[ix % len(dirs)]
        context = {
            'city': weather[0],
            'temp': weather[1],
            'description': weather[2],
            'windtype': weather[3],
            'windspeed': weather[4],
            'pressure': weather[5],
            'humidity': weather[6],
            'temp_max': weather[7],
            'temp_min': weather[8],
            'icon': f'icons/{weather[9]}.png',
            'feel': weather[10],
            'status': weather[11],
            'windeg': direction,
            'town': weather[13],
            'township': weather[13].split(',')[0],
            'data': True
        }
        return render_template('index.html', context=context)
    else:
        context = {
            "data": False
        }
        return render_template('index.html', context=context)


# features


if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
