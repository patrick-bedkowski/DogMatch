# -*- coding: utf-8 -*-
"""
@author: dogmatch.team.co
"""

import numpy as np
import pickle
import streamlit as st
import json

import functions as f


# Load the recommender model
def load_model():
    with open("./src/recommender/model.pkl", "rb") as file:
        return pickle.load(file)


# Load the breed code to name mapping
def load_code_to_breed():
    with open("./src/recommender/code_to_breed.json", "r") as file:
        return json.load(file)


def randomize_inputs():
    st.session_state.user_input = np.random.randint(
        1, 6, size=len(fields)
    ).tolist()


def reset_inputs():
    st.session_state.user_input = [3] * len(fields)


# Recommend the breed based on user input
def recommend():
    recommender = load_model()
    code_to_breed = load_code_to_breed()
    prediction = recommender.predict([st.session_state.user_input])[0]
    breed = code_to_breed.get(str(prediction), "Unknown")

    if breed != "Unknown":
        st.session_state.breed_image_url = f.get_breed_image_url(breed)

        breed = breed[:-1]  # convert to singular form (remove "s" at the end)
        st.session_state.recommendation = f"Recommended breed is: \"{breed}\""
        st.session_state.error_message = ""
    else:
        st.session_state.breed_image_url = ""
        st.session_state.recommendation = ""
        st.session_state.error_message = "An error occurred"


def main():
    global fields

    # st.set_page_config(layout="wide")
    st.set_page_config(page_title="DogMatch", page_icon="🐕")
    # st.sidebar.header("Recommend")

    # Streamlit UI
    title = """
    <div style="background-color:tomato;">
    <h2 style="color:white;text-align:center;">DogMatch</h2>
    </div>
    """
    st.markdown(title, unsafe_allow_html=True)

    # css = """
    # <style>
    # .stApp {
    #     max-width: 1000px;
    #     margin: 0 auto;
    # }
    # </style>
    # """
    # st.markdown(css, unsafe_allow_html=True)

    # Input fields
    fields = f.get_traits()

    # Initialize session state for input values if not present
    if "user_input" not in st.session_state:
        st.session_state.user_input = [3] * len(fields)
    if "recommendation" not in st.session_state:
        st.session_state.recommendation = ""
    if "error_message" not in st.session_state:
        st.session_state.error_message = ""
    if "breed_image_url" not in st.session_state:
        st.session_state.breed_image_url = ""

    with st.container():
        title = """
        <br>
        <h3 style="color:white;text-align:center;">Cechy psa</h3>
        """
        st.markdown(title, unsafe_allow_html=True)

        # Input collection with sliders arranged in columns
        col_1, col_2, col_3, col_4 = st.columns(4)
        for i, field in enumerate(fields):
            col_index = i // 4
            user_input = [col_1, col_2, col_3, col_4][col_index].slider(
                field, 1, 5, st.session_state.user_input[i]
            )
            st.session_state.user_input[i] = user_input

        # Buttons with callbacks
        st.button("Reset", on_click=reset_inputs)
        st.button("Losowo (DEV)", on_click=randomize_inputs)
        st.button("Rekomenduj", on_click=recommend)

        # Placeholders
        recommendation_placeholder = st.empty()
        error_placeholder = st.empty()
        breed_image = st.empty()

        # Display the recommendation or error message
        if st.session_state.recommendation:
            recommendation_placeholder.success(st.session_state.recommendation)
        if st.session_state.error_message:
            error_placeholder.error(st.session_state.error_message)
        if st.session_state.breed_image_url:
            breed_image.image(st.session_state.breed_image_url)


if __name__ == "__main__":
    main()