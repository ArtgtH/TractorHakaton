import streamlit as st

import requests


def get_fox():
    r = requests.get('https://randomfox.ca/floof/')
    return r.json().get('image')


if __name__ == '__main__':
    st.image(get_fox())
