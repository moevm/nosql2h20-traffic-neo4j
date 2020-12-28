

from datetime import datetime
from functools import reduce

import folium
import numpy as np
from flask import Blueprint, render_template, request
from folium import LatLngPopup
from neomodel import Q

from web_app.db.models import Building
from web_app.db.models import Way
from web_app.db.models import WayNode
from web_app.extensions import csrf_protect
from .forms import AnalyticsFilterForm, DataFilterForm, NavigatorForm

traffic_bp = Blueprint("traffic", __name__)


@csrf_protect.exempt
@traffic_bp.route("/data", methods=["POST", "GET"])
def data():
    theads = []
    rows = []
    form = DataFilterForm()
    if request.method == "POST" and form.validate():
        label = form.label.data
        lat = sorted([form.lat0.data, form.lat1.data])
        lon = sorted([form.lon0.data, form.lon1.data])

        if label == 'Building':
            theads = Building.properties()
            nodes = Building.nodes.filter(Q(lat__gte=lat[0]), Q(lat__lte=lat[1]), Q(lon__gte=lon[0]), Q(lon__lte=lon[1]))
            rows = [list(node.__dict__.values()) for node in nodes]
        elif label == 'WayNode':
            theads = WayNode.properties()
            nodes = WayNode.nodes.filter(Q(lat__gte=lat[0]), Q(lat__lte=lat[1]), Q(lon__gte=lon[0]), Q(lon__lte=lon[1]))
            rows = [list(node.__dict__.values()) for node in nodes]
        else:
            theads = Way.properties()
            ways = Way.filter(lat, lon)
            rows = [list(way.__dict__.values()) for way in ways]
            for row in rows:
                row[2] = np.around(row[2], decimals=1)
    return render_template("data.html", title="data", theads=theads, rows=rows, form=form)


@csrf_protect.exempt
@traffic_bp.route("/", methods=["POST", "GET"])
def index():
    colors = {1: 'green', 2: 'yellow', 3: 'red'}
    speeds = {1: 60, 2: 40, 3: 20}
    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    np.random.seed(np.mod(hash(date), 10**9))

    folium_map = folium.Map(location=(59.9503, 30.3367), zoom_start=12)

    form = NavigatorForm()
    if request.method == "POST":
        start_street = form.start_street.data
        start_number = form.start_number.data
        finish_street = form.finish_street.data
        finish_number = form.finish_number.data

        start_street = start_street.lower().replace('ул.', 'улица').replace('пр-т', 'проспект')
        finish_street = finish_street.lower().replace('ул.', 'улица').replace('пр-т', 'проспект')

        start_building = Building.find_by_adress(street=start_street, number=start_number)
        start_node = WayNode.match(lat=start_building.lat, lon=start_building.lon)

        finish_building = Building.find_by_adress(street=finish_street, number=finish_number)
        finish_node = WayNode.match(lat=finish_building.lat, lon=finish_building.lon)

        k=5
        paths, distances = WayNode.kShortestPaths(id0=start_node.id, id1=finish_node.id, k=k)
        L = np.max([len(distance) for distance in distances])
        part = np.random.randint(3, 10)
        heuristics = []
        levels = np.random.randint(1, 4, size=(k, part))
        for distance, level in zip(distances, levels):
            heuristic = 0
            for i, d in enumerate(distance):
                heuristic += d / speeds[level[i // ((L // part) + 1)]]
            heuristics.append(heuristic)
        _, idx = min((val, idx) for (idx, val) in enumerate(heuristics))

        L = len(distances[idx])
        levels = levels[idx]
        levels = np.repeat(levels, L // part, axis=0)
        levels = np.resize(levels, (k, L))
        locations = [(node.lat, node.lon) for node in paths[idx]]
        for i in range(L // part):
            folium.PolyLine(locations=locations[part * i: part * (i+1)+1], color=colors[levels[idx][i * part]]).add_to(folium_map)
    folium_map.save("web_app/templates/map.html")

    return render_template("index.html", title="navigator", form=form)


@csrf_protect.exempt
@traffic_bp.route("/map")
def map():
    return render_template("map.html")


@csrf_protect.exempt
@traffic_bp.route("/analytics", methods=["POST", "GET"])
def analytics():
    traffic_data = [
        ["1", 0, "color: green"],
        ["2", 0, "color: yellow"],
        ["3", 0, "color: red"],
    ]
    form = AnalyticsFilterForm()
    if request.method == "POST":
        date = form.date._value()
        np.random.seed(np.mod(hash(date), 10**9))

        lat = sorted([form.lat0.data, form.lat1.data])
        lon = sorted([form.lon0.data, form.lon1.data])
        nodes = WayNode.nodes.filter(Q(lat__gte=lat[0]), Q(lat__lte=lat[1]), Q(lon__gte=lon[0]), Q(lon__lte=lon[1]))

        traffic_dist = []
        for idx in range(2):
            traffic_dist.append(np.random.randint(1, len(nodes) - np.sum(traffic_dist) - 5 + idx))
        traffic_dist.append(len(nodes) - 1 - np.sum(traffic_dist))
        traffic_data = [
            ["1", traffic_dist[0], "color: green"],
            ["2", traffic_dist[1], "color: yellow"],
            ["3", traffic_dist[2], "color: red"],
        ]

    return render_template("analytics.html", title="analytics", data=traffic_data, form=form)
