from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, DateField
from datetime import datetime

class EnergyForm(FlaskForm):
    date = DateField('Entrez une date', [validators.DataRequired()])
    submit = SubmitField('Prédire')