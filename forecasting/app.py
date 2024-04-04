import json
import re
from sklearn.ensemble import IsolationForest
import joblib

import pandas as pd
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, fields

from flasgger import APISpec, Swagger, swag_from

from mail_messages.broker import send_email_to_user

import logging

import pickle

model = joblib.load("isolation_forest.joblib")
task_2_data_index = pd.read_csv("task_2_data_index.csv")
task1_df = pd.read_csv("task_2_data.csv")
task1_df = task1_df.drop(columns=['Unnamed: 0'])
df_weekly = pd.read_csv("df_weekly.csv")
df_monthly = pd.read_csv("df_monthly.csv")

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

app = Flask(__name__)
api = Api(app, version='1.0', title='Tractor API', description='API для получения оценки состояния трактора')

swagger = Swagger(app)


def test(data):
    data_for_pred = task1_df.sample(5)
    logger.info(data.columns)

    res = model.predict(data_for_pred)

    otvet = ''
    for i, a in enumerate(res):
        otvet += 'Запись номер ' + str(i)
        if a == -1:
            otvet += ' аномалия/n'
        else:
            otvet += ' не аномалия/n'

    """
    функция, которая заменяет поиск аномалий по csv файлу

    :return: result - какое-то сообщение, которое мы дальше вернем в UI, id - id трактора
    """
    return otvet


def test1():
    """
    Расчет аномалий для машины(количество и относительная частота аномалий в данных)

    :return: [{id: str, anomaly_timestamps_cnt: int, anomaly_ratio: float}]
    где id - ID машины, anomaly_timestamps_cnt - число аномалий для машины,
    anomaly_ratio - относительная частота аномалий
    """
    global task1_df

    i_forest_predict = model.predict(task1_df)

    task1_df["label"] = i_forest_predict
    task1_df["label"] = task1_df["label"].apply(
        lambda x: 0 if x == 1 else 1
    )

    data_concated = pd.concat(
        [task1_df, task_2_data_index],
        axis=1
    )

    data_anomaly_for_all_timestamps = data_concated.groupby(
        "tractor"
    ).agg({"label": "sum"})

    data_all_timestamps = data_concated.groupby(
        "tractor"
    ).agg({"label": "count"})

    data_timestaps_merged = data_anomaly_for_all_timestamps.merge(
        data_all_timestamps, on="tractor"
    )

    data_timestaps_merged.columns = [
        "anomaly_timestamps_cnt",
        "all_timestamps_cnt"
    ]

    data_timestaps_merged["anomaly_ratio"] = data_timestaps_merged["anomaly_timestamps_cnt"] / \
                                             data_timestaps_merged["all_timestamps_cnt"]

    data_timestaps_merged = data_timestaps_merged.reset_index()

    answer_list = []

    for example in data_timestaps_merged.to_dict("records"):
        answer_list.append(
            {
                "id": example["tractor"],
                "anomaly_timestamps_cnt": example["anomaly_timestamps_cnt"],
                "anomaly_ratio": example["anomaly_ratio"]
            }
        )

    return answer_list


def get_predict_for_time_sample(
        tractor_id: str, data: pd.DataFrame,
        time_sample_type: str
) -> dict[str, str]:
    logger.info(data.columns)
    data_for_train = data[
        data["tractor"] == tractor_id
        ].drop(
        columns=[
            "Дата и время",
            "tractor"
        ]
    )

    logger.info((len(data_for_train)))

    clf = IsolationForest(
        random_state=42
    ).fit(
        data_for_train
    )

    i_forest_predict = clf.predict(data_for_train)

    data_for_train["label"] = i_forest_predict

    i_forest_predict_last = i_forest_predict[-1]

    answer_string = "машина рекомендуется к проверке" if i_forest_predict_last == -1 else "машина в порядке"

    if time_sample_type == "w":
        answer_string = "По данным за последнюю неделю " + answer_string
    elif time_sample_type == "m":
        answer_string = "По данным за последний месяц " + answer_string

    return {tractor_id: answer_string}


def test2(ids):
    """
    функция, которая оценивает поломки по id

    :return: {w: [{id: result}], m: [{id: result}]} где m - месяц, w - неделя,
    id - ID машины, result - результат для отдельной машины
    """

    answers_week = {
        "w": [],
        "m": []
    }

    for example_id in ids:

        logger.info(example_id)

        answers_week["w"].append(get_predict_for_time_sample(
            example_id,
            df_weekly,
            "w"
        ))

        answers_week["m"].append(get_predict_for_time_sample(
            example_id,
            df_monthly,
            "m"
        ))

    return answers_week


def check_mail(mail):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, mail):
        return True
    else:
        return False


# model_for_breakdown = api.models(
#     'Data', {
#     'ids': fields.String(description='id тракторов'),
#     'mail': fields.String(description='mail для отправки сообщений')}
# )


@api.route('/api/tractor_breakdown')
class TractorBreakdown(Resource):

    @api.doc(description='Получаем id тракторов в json, отдаем результат работы модели и ошибку с email, если такая есть')
    def get(self):
        ids = request.args.getlist('ids')

        logger.info(ids)

        res = test2(ids)

        error = None

        email = request.args.get('mail')
        if email and check_mail(email):
            topic = 'Проверка поломок тракторов'
            res = send_email_to_user(email, res, topic)
        elif email:
            error = 'invalid email'
        else:
            error = 'request without email'

        return jsonify({'result': res, 'error': error})


@api.route('/api/tractor_anom')
class TractorAnom(Resource):

    @api.doc(description='Получаем df в json с данными трактора, отдаем результат работы модели и ошибку с email, если такая есть')
    def post(self):

        data = pd.read_json(request.json['json'])

        res = test(data)

        try:
            email = (request.json['mail'])
            if email and check_mail(email):
                topic = f'Результат проверки аномалий по CSV файлу'
                send_email_to_user(email, res, topic)
        except Exception as e:
            error = 'request without email'
        else:
            if res == 'success':
                error = None
            else:
                error = 'invalid email'

        return jsonify({'result': res, 'error': error})

    @api.doc(description='Получаем df в json с данными трактора, отдаем результат работы модели и ошибку с email, если такая есть')
    def get(self):

        ids = request.args.getlist('ids')

        res = test1()

        error = None

        email = request.args.get('mail')
        if email and check_mail(email):
            topic = 'Проверка аномалий тракторов'
            res = send_email_to_user(email, res, topic)
        elif email:
            error = 'invalid email'
        else:
            error = 'request without email'

        return jsonify({'result': res, 'error': error})


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5555)
