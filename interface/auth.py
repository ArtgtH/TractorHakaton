import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit as st


def initialize_session_state():
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None


if __name__ == '__main__':
    initialize_session_state()
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    st.sidebar.header('РОЛИ')
    st.sidebar.subheader('')

    st.sidebar.subheader('Рабочий')
    st.sidebar.write("""
    Username: Worker\n
    Password: Worker1234
    """)
    st.sidebar.subheader('')

    authenticator.login()

    if st.session_state["authentication_status"]:

        st.header('Привет дорогой пользователь')
        st.subheader('Выберите одну из функций ниже')
        st.page_link('pages/anom_by_csv.py', label='Отслеживание аномалий по загруженному CSV')
        st.page_link('pages/anom_by_id.py', label='Отслеживание аномалий машин по ID')
        st.page_link('pages/breakdown_condition.py', label='Отслеживание поломки машин по ID')

        authenticator.logout()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
