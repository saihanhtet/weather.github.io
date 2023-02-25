from flask import Flask, render_template, request
from weather import Weather

app = Flask(__name__)  # initialise application

# configurations of function


@app.route('/', methods=['POST', 'GET'])  # route configure
def index():
    # listen for the request from form in html template
    if request.method == 'POST':
        # get the city from form input in html template
        city = request.form['name']
        weather = Weather(city).new(sentence=False)  # get the weather results
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']  # dict list for wind directions
        # converting wind degree to wind direction
        ix = round(weather[12] / (360. / len(dirs)))
        direction = dirs[ix % len(dirs)]
        # context is the give the access to weather data inside the html template
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
        # call the template you want to show.
        return render_template('index.html', context=context)
    else:
        # data is to check where data is empty or not and if empty results not show.
        context = {
            "data": False
        }
        return render_template('index.html', context=context)


if __name__ == '__main__':
    import webbrowser  # import webbrowser package to open in browser
    # open the website in browser with link
    webbrowser.open('http://127.0.0.1:5000/')
    # debug should be false to open with webbrowser debug run twice
    app.run(debug=False)
