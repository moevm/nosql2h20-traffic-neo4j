from datetime import datetime
import io

import folium
import os
import numpy as np
from flask import Blueprint, flash, render_template, request, redirect, current_app
from flask import send_from_directory
from neomodel import Q
from werkzeug.utils import secure_filename

from web_app.db.models import Building, Way, WayNode
from web_app.extensions import csrf_protect

from neomodel import db

from .forms import AnalyticsFilterForm, DataFilterForm, NavigatorForm, ImportForm, ExportForm

import docker
import tarfile

traffic_bp = Blueprint("traffic", __name__)


def copy_from_container(src, dst):
    client = docker.from_env()
    name, src = src.split(':')
    container = client.containers.get(name)

    bits, stat = container.get_archive(src)

    file_obj = io.BytesIO()
    for chunk in bits:
        file_obj.write(chunk)

    file_obj.seek(0)

    tar = tarfile.open(mode='r', fileobj=file_obj)
    tar.extractall(os.path.dirname(dst))
    os.chmod(dst, 777)


def copy_to_container(src, dst):
    client = docker.from_env()
    name, dst = dst.split(':')
    container = client.containers.get(name)

    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(srcname)
    finally:
        tar.close()

    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)


@csrf_protect.exempt
@traffic_bp.route("/export", methods=["POST", "GET"], endpoint='export_db')
def export_db():
    query = (
        "CALL apoc.export.json.all(\"/all.json\",{})"
    )

    results, _ = db.cypher_query(query=query)

    root_dir = os.path.dirname(os.getcwd())
    path = root_dir
    full_path = os.path.join(path, 'all.json')

    copy_from_container('neo4j:/var/lib/neo4j/import/all.json', full_path)

    return send_from_directory(path, 'all.json', as_attachment=True)


@csrf_protect.exempt
@traffic_bp.route("/import", methods=["POST", "GET"], endpoint='import_db')
def import_db():
    form = ImportForm()

    if request.method == 'POST' and form.validate_on_submit():
        f = form.Import.data

        filename = secure_filename(f.filename)
        if not os.path.isdir(current_app.config['UPLOAD_FOLDER']):
            os.mkdir(current_app.config['UPLOAD_FOLDER'])

        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        copy_to_container(os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
                          'neo4j:/var/lib/neo4j/import/all.json')

        query = (
            "CALL apoc.import.json(\"/all.json\",{})"
        )

        results, _ = db.cypher_query(query=query)

        flash('Import successful')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ), 'error')

    return redirect(request.referrer)


@csrf_protect.exempt
@traffic_bp.route("/data", methods=["POST", "GET"])
def data():
    theads = []
    rows = []
    form = DataFilterForm()
    import_form = ImportForm()
    export_form = ExportForm()
    if request.method == "POST" and form.validate():
        label = form.label.data
        if form.lat0.data is None or form.lat1.data is None:
            lat = None
        else:
            lat = sorted([form.lat0.data, form.lat1.data])

        if form.lon0.data is None or form.lon1.data is None:
            lon = None
        else:
            lon = sorted([form.lon0.data, form.lon1.data])

        if form.node_id1.data is None or form.node_id2.data is None:
            ids = None
        else:
            ids = sorted([form.node_id1.data, form.node_id2.data])

        housenumber = form.housenumber.data

        street = form.street.data

        if label == "Way":
            theads = Way.properties()
            if lat is None:
                lat = [0, 100]
            if lon is None:
                lon = [0, 100]

            ways = Way.filter(lat, lon)
            rows = [list(way.__dict__.values()) for way in ways]
            for row in rows:
                row[2] = np.around(row[2], decimals=1)
        else:
            if label == "WayNode":
                theads = WayNode.properties()
                nodes = WayNode.nodes
            else:
                theads = Building.properties()
                nodes = Building.nodes
                if housenumber:
                    nodes = nodes.filter(
                        Q(housenumber__exact=housenumber)
                    )
                if street:
                    nodes = nodes.filter(
                        Q(street__exact=street)
                    )
            if lat:
                nodes = nodes.filter(
                    Q(lat__gte=lat[0]),
                    Q(lat__lte=lat[1])
                )
            if lon:
                nodes = nodes.filter(
                    Q(lon__gte=lon[0]),
                    Q(lon__lte=lon[1]),
                )
            if ids:
                nodes = nodes.filter(
                    Q(id__gte=ids[0]),
                    Q(id__lte=ids[1])
                )
            rows = [list(node.__dict__.values()) for node in nodes]

    return render_template("data.html", title="data", theads=theads, rows=rows, form=form,
                           import_form=import_form, export_form=export_form)


@csrf_protect.exempt
@traffic_bp.route("/", methods=["POST", "GET"])
def index():
    colors = {1: "green", 2: "yellow", 3: "red"}
    speeds = {1: 60, 2: 40, 3: 20}
    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    np.random.seed(np.mod(hash(date), 10 ** 9))

    folium_map = folium.Map(location=(59.9503, 30.3367), zoom_start=12)

    form = NavigatorForm()
    if request.method == "POST":
        start_street = form.start_street.data
        start_number = form.start_number.data
        finish_street = form.finish_street.data
        finish_number = form.finish_number.data

        start_street = (
            start_street.lower().replace("ул.", "улица").replace("пр-т", "проспект")
        )
        finish_street = (
            finish_street.lower().replace("ул.", "улица").replace("пр-т", "проспект")
        )
        try:
            start_building = Building.find_by_adress(
                street=start_street, number=start_number
            )
            start_node = WayNode.match(lat=start_building.lat, lon=start_building.lon)

            finish_building = Building.find_by_adress(
                street=finish_street, number=finish_number
            )
            finish_node = WayNode.match(lat=finish_building.lat, lon=finish_building.lon)
        except IndexError:
            flash("Error! Address or house number was not found.")
            return render_template("index.html", title="navigator", form=form)
        k = 5
        paths, distances = WayNode.kShortestPaths(
            id0=start_node.id, id1=finish_node.id, k=k
        )
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
            folium.PolyLine(
                locations=locations[part * i : part * (i + 1) + 1],
                color=colors[levels[idx][i * part]],
            ).add_to(folium_map)
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
    if request.method == "POST" and form.validate():
        date = form.date._value()
        np.random.seed(np.mod(hash(date), 10 ** 9))

        lat = sorted([form.lat0.data, form.lat1.data])
        lon = sorted([form.lon0.data, form.lon1.data])
        nodes = WayNode.nodes.filter(
            Q(lat__gte=lat[0]), Q(lat__lte=lat[1]), Q(lon__gte=lon[0]), Q(lon__lte=lon[1])
        )

        traffic_dist = []
        for idx in range(2):
            traffic_dist.append(
                np.random.randint(1, len(nodes) - np.sum(traffic_dist) - 5 + idx)
            )
        traffic_dist.append(len(nodes) - 1 - np.sum(traffic_dist))
        traffic_data = [
            ["1", traffic_dist[0], "color: green"],
            ["2", traffic_dist[1], "color: yellow"],
            ["3", traffic_dist[2], "color: red"],
        ]

    return render_template(
        "analytics.html", title="analytics", data=traffic_data, form=form
    )
