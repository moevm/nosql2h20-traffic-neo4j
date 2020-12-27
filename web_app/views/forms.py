from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms import DateTimeField
from wtforms import FloatField
from wtforms import SubmitField
from wtforms import SelectField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class NavigatorForm(FlaskForm):
    start = FloatField('start')
    finish = FloatField('finish')
    go = SubmitField('go')


class DataFilterForm(FlaskForm):
    label = SelectField('label', choices=['Bulding', 'WayNode', 'Way'])
    left_top_lat = FloatField('left top lat')
    left_top_lon = FloatField('left top lon')
    right_bottom_lat = FloatField('right bottom lat')
    right_bottom_lon = FloatField('right bottom lon')
    filter = SubmitField('filter')


class AnalyticsFilterForm(FlaskForm):
    date = DateField('date', format='%d.%m.%y',
                          render_kw={'placeholder': '01.01 for June 20, 2015'})
