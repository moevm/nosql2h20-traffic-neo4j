from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, IntegerField, SubmitField
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import Length, NumberRange, Optional


class NavigatorForm(FlaskForm):
    start_street = StringField(
        "start", validators=[Length(min=1, max=50, message="field cannot be empty")]
    )
    finish_street = StringField(
        "finish", validators=[Length(min=1, max=50, message="field cannot be empty")]
    )
    start_number = StringField(
        "start", validators=[Length(min=1, max=50, message="field cannot be empty")]
    )
    finish_number = StringField(
        "finish", validators=[Length(min=1, max=50, message="field cannot be empty")]
    )
    go = SubmitField("go")


class DataFilterForm(FlaskForm):
    label = SelectField(
        "label", choices=[("Building", "Building"), ("WayNode", "WayNode"), ("Way", "Way")]
    )
    lat0 = FloatField(
        "lat0",
        validators=[
            NumberRange(min=0.0, max=100.0, message="value must be in range [0, 100]"),
            Optional()
        ],
    )
    lon0 = FloatField(
        "lon0",
        validators=[
            NumberRange(min=0.0, max=100.0, message="value must be in range [0, 100]"),
            Optional()
        ],
    )
    lat1 = FloatField(
        "lat1",
        validators=[
            NumberRange(min=0.0, max=100.0, message="value must be in range [0, 100]"),
            Optional()
        ],
    )
    lon1 = FloatField(
        "lon1",
        validators=[
            NumberRange(min=0.0, max=100.0, message="value must be in range [0, 100]"),
            Optional()
        ],
    )
    node_id1 = IntegerField("id1", validators=[
        NumberRange(min=0.0, message="value must be greater or equal to zero"),
        Optional()
    ])
    node_id2 = IntegerField("id2", validators=[
        NumberRange(min=0.0, message="value must be greater or equal to zero"),
        Optional()
    ])
    housenumber = StringField("house number", validators=[Optional()])
    street = StringField("street name", validators=[Optional()])
    filter = SubmitField("filter")


class ImportForm(FlaskForm):
    Import = FileField("Upload file", validators=[FileRequired()])


class ExportForm(FlaskForm):
    Export = SubmitField("export")


class AnalyticsFilterForm(FlaskForm):
    date = DateTimeLocalField("time", format="%d.%m.%Y %H:%M")
    lat0 = FloatField(
        "lat0",
        validators=[
            NumberRange(min=0.0, max=100.0, message="value must be in range [0, 100]")
        ],
    )
    lon0 = FloatField(
        "lon0",
        validators=[
            NumberRange(min=0.0, max=100.0, message="value must be in range [0, 100]")
        ],
    )
    lat1 = FloatField(
        "lat1",
        validators=[
            NumberRange(min=0.0, max=100.0, message="value must be in range [0, 100]")
        ],
    )
    lon1 = FloatField(
        "lon1",
        validators=[
            NumberRange(min=0.0, max=100.0, message="value must be in range [0, 100]")
        ],
    )
    filter = SubmitField("filter")
