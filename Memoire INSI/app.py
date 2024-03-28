from flask import Flask, render_template, session, redirect, url_for, request
from models.utils import to_month, forecast
from Form.Energy import EnergyForm
import pickle


# Création de l'application flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-hard-secret-key'

model_dmd = pickle.load(open('models/model_tot_nb_dmd_sarimax_fit.pkl', 'rb'))
model_egy = pickle.load(open('models/model_tot_energy_sarimax_fit.pkl', 'rb'))

@app.route("/", methods=['GET', 'POST'])
def index():
    form = EnergyForm()

    form.date.render_kw = {
        'class': 'form-control datepicker',
        'required': 'required',
        'placeholder': '00/00/0000'
    }

    form.submit.render_kw = {
        'type': 'submit',
        'class': 'btn btn-primary'
    }
    
    if form.validate_on_submit() and request.method == 'POST':
        session['date'] = request.form['date']
        session['month'] = to_month(request.form['date'])

        return redirect(url_for('prediction'))

    return render_template('index.html', form=form)


@app.route("/prediction")
def prediction():
    results_dmd = forecast(model_dmd, session['date'])
    results_egy = forecast(model_egy, session['date']) * 1_000  # Pour avoir l'unité en MW
    results_egy = f"{results_egy:.2f}"
    return render_template('prediction.html', results_dmd=int(results_dmd), results_egy=results_egy)


# Execution de ce fichier
if __name__ == '__main__':
    app.run(debug=True)
