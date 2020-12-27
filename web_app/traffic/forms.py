from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, SubmitField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import Length, NumberRange


class NavigatorForm(FlaskForm):
    start = StringField(
        "start", validators=[Length(min=1, max=50, message="field cannot be empty")]
    )
    finish = StringField(
        "finish", validators=[Length(min=1, max=50, message="field cannot be empty")]
    )
    go = SubmitField("go")


class DataFilterForm(FlaskForm):
    label = SelectField(
        "label", choices=[("Bulding", "Bulding"), ("WayNode", "WayNode"), ("Way", "Way")]
    )
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
