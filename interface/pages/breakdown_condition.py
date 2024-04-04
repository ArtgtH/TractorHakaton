import json

import requests
import streamlit as st


if __name__ == '__main__':

	if st.session_state['name'] == 'Worker':

		st.sidebar.header('Страница отслеживания состояний тракторов по ID (без пробелов)')
		st.sidebar.subheader('Введите ID тракторов через запятую для получения информации об их состоянии')

		tractors = st.text_input(label='Введите ID тракторов')

		mail = st.text_input(label='Введите почту для отправки результата (опционально)')

		send = st.button(label='отправить данные')

		if send:

			st.success('ожидайте результатов')

			tractors = tractors.split(',')

			url = 'http://api:5555/api/tractor_breakdown'

			if mail:
				params = {'ids': tractors, 'mail': mail}

			else:
				params = {'ids': tractors}

			r = requests.get(url, params=params)

			if r.status_code == 200:

				res = json.loads(r.text)

				error = res.get('error')
				result = dict(res.get('result'))

				for id in (result.get('m')):
					st.write(
						f"""
						ID {list(id.keys())[0]} : {list(id.values())[0]}
						"""
					)

				if error == 'invalid email':
					st.error('Invalid email')
