import streamlit as st
import requests
st.title("Multi-Agent Travel Assistant")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit-travel-thread"

user_input = st.text_area("Enter your travel request")

if st.button("Plan Trip"):
    response = requests.post(
        "http://127.0.0.1:8000/plan-trip",
        json={
            "user_input": user_input,
            "thread_id": st.session_state.thread_id
        }
    )

    if response.status_code == 200:
        st.write(response.json()["final_response"])
    else:
        st.error("Something went wrong")