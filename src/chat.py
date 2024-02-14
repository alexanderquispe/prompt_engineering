import streamlit as st, time


def echo_message(prompt):
    return f"Echo: {prompt}"


def chat_message(callback=echo_message):

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("question"):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        # time.sleep(1)
        response = callback(prompt)
        print(response)

        with st.chat_message("ai"):
            st.markdown(response, True)

        st.session_state.messages.append({"role": "ai", "content": response})
