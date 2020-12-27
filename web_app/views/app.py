import os

import folium
from flask import Flask, render_template, request

from forms import DataFilterForm
from forms import NavigatorForm

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/data', methods=['POST', 'GET'])
def data():
    theads = ['id', 'lat', 'lon', 'name']
    rows = [[1, 25, 26, 'q'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [2, 27, 28, 'e'],
            [3, 29, 30, 'w']]
    form = DataFilterForm()
    if request.method == 'POST':
        label = form.label.data
        left_top_lat = form.left_top_lat.data
        left_top_lon = form.left_top_lon.data
        right_bottom_lat = form.right_bottom_lat.data
        right_bottom_lon = form.right_bottom_lon.data
        print(label, left_top_lat, left_top_lon, right_bottom_lat, right_bottom_lon)

    return render_template('data.html', title='data', theads=theads, rows=rows, form=form)


@app.route('/', methods=['POST', 'GET'])
def index():
    form = NavigatorForm()
    if request.method == 'POST':
        start = form.start.data
        finish = form.finish.data
        print(start, finish)

    start_coords = (59.99083, 30.31835)
    folium_map = folium.Map(
        location=start_coords,
        zoom_start=17
    )

    locations = [(59.9873158, 30.3054728), (59.9876555, 30.3065391), (59.9876922, 30.3066544), (59.9877585, 30.3068666)]
    folium.PolyLine(locations=locations, color='red').add_to(folium_map)
    folium_map.save('templates/map.html')

    return render_template('index.html', title='navigator', form=form)


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/analytics')
def analytics():
    traffic_data = [["1", 22, "color: green"],
                    ["2", 35, "color: yellow"],
                    ["3", 12, "color: red"]]
    return render_template('analytics.html', title='analytics', data=traffic_data)


if __name__ == '__main__':
    app.run(debug=True)
