from datetime import datetime
from functools import reduce

import folium
import numpy as np
from flask import Blueprint, render_template, request
from neomodel import Q

from web_app.db.models import Building
from web_app.db.models import Way
from web_app.db.models import WayNode
from web_app.db.util import find_by_address
from web_app.extensions import csrf_protect
from .forms import AnalyticsFilterForm, DataFilterForm, NavigatorForm

traffic_bp = Blueprint("traffic", __name__)


@csrf_protect.exempt
@traffic_bp.route("/data", methods=["POST", "GET"])
def data():
    theads = []
    rows = []
    form = DataFilterForm()
    if request.method == "POST":
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
    date = datetime.now()
    seed = np.mod(hash(date), 10**9)
    np.random.seed(np.mod(hash(date), 10**9))

    folium_map = folium.Map(location=(59.9503, 30.3367), zoom_start=12)

    form = NavigatorForm()
    if request.method == "POST":
        start_street = form.start_street.data
        start_number = form.start_number.data
        finish_street = form.finish_street.data
        finish_number = form.finish_number.data

        start_building = find_by_address(street=start_street, number=start_number)
        start_node = WayNode.match(lat=start_building.lat, lon=start_building.lon)

        finish_building = find_by_address(street=finish_street, number=finish_number)
        finish_node = WayNode.match(lat=finish_building.lat, lon=finish_building.lon)

        paths, distances = WayNode.kShortestPaths(id0=start_node.id, id1=finish_node.id)

        locations = [(node.lat, node.lon) for node in paths[0]]
        part = np.random.randint(3, 10)
        for i in range(len(locations) // part):
            folium.PolyLine(locations=locations[part * i: part * (i+1)+1], color=colors[np.random.randint(1, 4)]).add_to(folium_map)

    folium_map.save("web_app/templates/map.html")

    return render_template("index.html", title="navigator", form=form)


@csrf_protect.exempt
@traffic_bp.route("/map")
def map():
    return render_template("map.html")


@csrf_protect.exempt
@traffic_bp.route("/analytics", methods=["POST", "GET"])
def analytics():
    form = AnalyticsFilterForm()
    if request.method == "POST":
        date = form.date._value()
        np.random.seed(np.mod(hash(date), 10**9))

        lat = sorted([form.lat0.data, form.lat1.data])
        lon = sorted([form.lon0.data, form.lon1.data])
        nodes = WayNode.nodes.filter(Q(lat__gte=lat[0]), Q(lat__lte=lat[1]), Q(lon__gte=lon[0]), Q(lon__lte=lon[1]))
        sum = reduce(lambda a, x: a + x, [len(node.forward.all()) for node in nodes])

        traffic_dist = []
        for idx in range(2):
            traffic_dist.append(np.random.randint(1, sum - np.sum(traffic_dist) - 4 + idx))
        traffic_dist.append(sum - np.sum(traffic_dist))
        traffic_data = [
            ["1", traffic_dist[0], "color: green"],
            ["2", traffic_dist[1], "color: yellow"],
            ["3", traffic_dist[2], "color: red"],
        ]

    return render_template(
        "analytics.html", title="analytics", data=traffic_data, form=form
    )
