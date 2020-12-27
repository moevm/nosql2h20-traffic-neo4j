import folium
import numpy as np
from flask import Blueprint, render_template, request

from web_app.extensions import csrf_protect

from .forms import AnalyticsFilterForm, DataFilterForm, NavigatorForm

traffic_bp = Blueprint("traffic", __name__)


@csrf_protect.exempt
@traffic_bp.route("/data", methods=["POST", "GET"])
def data():
    theads = ["id", "lat", "lon", "name", "name1"]
    rows = [
        [1, 25, 26, "q", "2"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [2, 27, 28, "e", "3"],
        [3, 29, 30, "w", "4"],
    ]
    form = DataFilterForm()
    if request.method == "POST" and form.validate():
        label = form.label.data
        lat0 = form.lat0.data
        lon0 = form.lon0.data
        lat1 = form.lat1.data
        lon1 = form.lon1.data
        print(label, lat0, lon0, lat1, lon1)

    return render_template("data.html", title="data", theads=theads, rows=rows, form=form)


@csrf_protect.exempt
@traffic_bp.route("/", methods=["POST", "GET"])
def index():
    locations = [
        (59.9873158, 30.3054728),
        (59.9876555, 30.3065391),
        (59.9876922, 30.3066544),
        (59.9877585, 30.3068666),
    ]

    form = NavigatorForm()
    if request.method == "POST" and form.validate():
        start = form.start.data
        finish = form.finish.data
        print(start, finish)

    start_coords = np.mean(locations, axis=0)
    folium_map = folium.Map(location=start_coords, zoom_start=17)
    folium.PolyLine(locations=locations, color="red").add_to(folium_map)
    folium_map.save("map.html")

    return render_template("index.html", title="navigator", form=form)


@csrf_protect.exempt
@traffic_bp.route("/map")
def map():
    return render_template("map.html")


@csrf_protect.exempt
@traffic_bp.route("/analytics", methods=["POST", "GET"])
def analytics():
    traffic_data = [
        ["1", 22, "color: green"],
        ["2", 35, "color: yellow"],
        ["3", 12, "color: red"],
    ]
    form = AnalyticsFilterForm()
    if request.method == "POST" and form.validate():
        date = form.date._value()
        lat0 = form.lat0.data
        lon0 = form.lon0.data
        lat1 = form.lat1.data
        lon1 = form.lon1.data
        print(date, lat0, lon0, lat1, lon1)

    return render_template(
        "analytics.html", title="analytics", data=traffic_data, form=form
    )
