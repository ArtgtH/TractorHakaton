import json

import streamlit as st

import requests


if __name__ == '__main__':

	if st.session_state['name'] == 'Worker':

		st.sidebar.header('Страница отслеживания аномалий')
		st.sidebar.subheader('Вывод отчета по всем машинам')

		mail = st.text_input(label='Введите почту для отправки результата (опционально)')

		send = st.button(label='отправить запрос')

		if send:

			st.success('ожидайте результатов')

			tractors = '1,1,2,2,3,4,5'

			tractors = tractors.split(',')

			url = 'http://api:5555/api/tractor_anom'

			if mail:
				params = {'ids': tractors, 'mail': mail}

			else:
				params = {'ids': tractors}

			r = requests.get(url, params=params)

			if r.status_code == 200:
				res = json.loads(r.text)

				error = res.get('error')
				result = res.get('result')

				for item in result:
					id_val = item.get('id')
					anomaly_ratio_val = item.get('anomaly_ratio')
					anomaly_timestamps_cnt_val = item.get('anomaly_timestamps_cnt')
					st.text_area(
						f'ID {id_val}',
						f"""
						Anomaly Ratio {anomaly_ratio_val}\n
						Anomaly Timestamps {anomaly_timestamps_cnt_val}
						"""
					)

				st.write(
					result
				)

				if error == 'invalid email':
					st.error('Invalid email')
