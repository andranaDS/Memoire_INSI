from datetime import timedelta
from random import randrange
from datetime import datetime

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)

    return start + timedelta(seconds=random_second)


# Affichage des mesures de metriques
def display_metrics(train, train_prediction, test, test_prediction):
    # Mesures de performances sur l'ensemble d'entrainement
    train_mae = mean_absolute_error(train, train_prediction)
    train_mse = mean_squared_error(train, train_prediction)
    train_rmse = mean_squared_error(train, train_prediction, squared=False)
    train_r2 = r2_score(train, train_prediction)

    # Mesures de performances sur l'ensemble de test
    test_mae = mean_absolute_error(test, test_prediction)
    test_mse = mean_squared_error(test, test_prediction)
    test_rmse = mean_squared_error(test, test_prediction, squared=False)
    test_r2 = r2_score(test, test_prediction)

    # Création d'un Dataframe pour afficher les mesures de performance
    perf_df = pd.DataFrame({
        'Métriques:': ['MAE', 'MSE', 'RMSE', 'R²'],
        'Ensemble d\'entrainenemt:': [train_mae, train_mse, train_rmse, train_r2],
        'Ensemble de test:': [test_mae, test_mse, test_rmse, test_r2]
    })

    return perf_df

# Conversion de date de type string en format 'Y-m'
def to_month(str_date):
    # Convertir la chaîne en objet datetime
    date_obj = datetime.strptime(str_date, '%Y-%m-%d')

    # Formater la date
    formatted_date = date_obj.strftime('%m-%Y')

    return formatted_date 


def forecast(model, target_date):
    target_datetime = datetime.strptime(target_date,'%Y-%m-%d')
    fitted_values = model.predict()
    last_index = fitted_values.index[-1]
    steps = int((target_datetime - last_index).days / 30)

    # Utiliser le modèle pour faire des prédictions
    forecast = model.forecast(steps=steps)

    return int(forecast.iloc[-1])