# -*- coding: utf-8 -*-
"""
@author: dogmatch.team.co
"""

import streamlit as st

import functions as f


def add_dog():
    if st.session_state.name:
        st.session_state.success_message = "Dodano psa"
        st.session_state.error_message = ""

        # TODO: actual adding to DB
    else:
        st.session_state.success_message = ""
        st.session_state.error_message = "Wprowadź imię"


def main():

    # st.title("Page two")

    # st.set_page_config(layout="wide")
    st.set_page_config(page_title="DogMatch", page_icon="🐕")

    # Streamlit UI
    title = """
    <div style="background-color:tomato;">
    <h2 style="color:white;text-align:center;">DogMatch</h2>
    </div>
    """
    st.markdown(title, unsafe_allow_html=True)

    if "name" not in st.session_state:
        st.session_state.name = ""
    if "success_message" not in st.session_state:
        st.session_state.success_message = ""
    if "error_message" not in st.session_state:
        st.session_state.error_message = ""

    st.session_state.breed = st.selectbox(
        'Rasa',
        f.get_breeds()
    )

    st.session_state.name = st.text_input(
        label="Imię"
    )

    st.session_state.photo = st.file_uploader(
        label="Zdjęcie", type=["png", "jpg", "bmp", "tiff"]
    )

    st.button("Dodaj", on_click=add_dog)

    success_placeholder = st.empty()
    error_placeholder = st.empty()

    if st.session_state.success_message:
        success_placeholder.success(st.session_state.success_message)
    if st.session_state.error_message:
        error_placeholder.error(st.session_state.error_message)


if __name__ == "__main__":
    main()