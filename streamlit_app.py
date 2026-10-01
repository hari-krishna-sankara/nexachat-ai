import streamlit as st

from chatbot_engine import get_groq_response


st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖"
)


st.title("🤖 NexaChat AI Chatbot")
st.caption("Powered by Groq")


# Create separate chat history for each session
if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# Display previous messages
for role, text in st.session_state.chat_history:

    if role == "You":

        with st.chat_message("user"):
            st.markdown(text)

    else:

        with st.chat_message("assistant"):
            st.markdown(text)


# Chat input
user_input = st.chat_input("Type your message...")


if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)


    # Get response
    response_stream = get_groq_response(
        user_input,
        st.session_state.chat_history[-10:]
    )


    if response_stream:

        full_response_content = ""

        with st.chat_message("assistant"):

            response_placeholder = st.empty()

            for chunk in response_stream:

                if chunk.choices[0].delta.content is not None:

                    content = chunk.choices[0].delta.content

                    full_response_content += content

                    response_placeholder.markdown(
                        full_response_content
                    )


        # Save conversation only in this user's session
        st.session_state.chat_history.append(
            ["You", user_input]
        )

        st.session_state.chat_history.append(
            ["Bot", full_response_content]
        )


    else:

        st.error("Sorry, something went wrong.")
