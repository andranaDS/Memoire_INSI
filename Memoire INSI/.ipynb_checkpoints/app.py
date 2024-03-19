from flask import Flask, render_template, request
import pandas as pd
import pickle

# Création de l'application flask
app = Flask(__name__)

model = pickle.load(open('model_sarima_fit.pkl', 'rb'))


def forecast(target_date):
    target_datetime = pd.to_datetime(target_date['date'], format='%d-%m-%Y')
    fitted_values = model.predict()
    last_index = fitted_values.index[-1]
    steps = int((target_datetime - last_index).days / 30)

    # Utiliser le modèle pour faire des prédictions
    forecast = model.forecast(steps=steps)

    return int(forecast[-1])


@app.route("/")
def index():
    return render_template('templates/index.html')


@app.route("/api/predictions", methods=['POST'])
def predictions():
    content = request.json
    results = forecast(content)
    return


# Execution de ce fichier
if __name__ == '__main__':
    app.run(debug=True)
