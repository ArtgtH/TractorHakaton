import json

import streamlit as st
import pandas as pd
import requests


if __name__ == '__main__':

	if st.session_state['name'] == 'Worker':

		st.sidebar.header('Страница отслеживания аномалий по .CSV')

		st.sidebar.subheader('Необходимо загрузить файлик с данными телеметрии в поле, ответ будет выведен \
		на этой же странице после поля ввода')

		file = st.file_uploader(label='Загрузите данные о тракторе в виде CSV', type='csv')
		mail = st.text_input(label='Введите почту для отправки результата (опционально)')
		send = st.button(label='отправить данные')

		if send:

			if file is not None:
				st.success('успешно загружено, ожидайте результатов')

				file = pd.read_csv(file, delimiter=';')

				file = file.to_json(orient='records')

				if mail:
					data = {'mail': mail, 'json': file}
				else:
					data = {"json": file}

				r = requests.request(method='POST', url='http://api:5555/api/tractor_anom', json=data)

				if r.status_code == 200:

					res = json.loads(r.text)

					error = res.get('error')
					result = res.get('result')

					for elem in result.split('/n'):
						st.write(
							elem
						)

					if error == 'invalid email':
						st.error('Invalid email')
