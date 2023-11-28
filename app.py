import os
import openai
import streamlit as st
from rag_integration import ragIntegrator as rag

# Set the model to be used for the ChatOpenAI model
MODEL = 'gpt-4'

# Retrieve your OpenAI API key from an environment variable for security purposes
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set the title of Streamlit app
st.title("Cruise-Finder: Travel Agency ChatBot")

# Check if the 'openai_model' is set in the session state, if not, initialize it.
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL

# Initialize a list of messages in the session state to store the conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "user", "content": "Hello! Welcome to our Cruise Finder Chatbot. I can help you find the best cruise packages and information to plan your next big adventure."}]

# Loop through the messages in the session state and display them in the Streamlit chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input from the Streamlit chat input box
if prompt := st.chat_input("Type Message.."):
    # Add the user's message to the session state to maintain the conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create a placeholder for the assistant's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Invoke the RAG integrator to get a response based on the user's prompt relavent to custom data
        result = rag.ragOutput(prompt)

        # Format the RAG response to be compatible with Streamlit's markdown
        rag_response = result['result'].replace("$", "\$").replace("\n", "  \n")

        # Use the OpenAI ChatCompletion API to generate a response, including the context from RAG
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                    {"role": "system", "content": rag_response},  # The initial context provided by RAG
                    *[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages  # The conversation history
                    ],
                ],
            stream=True,
        ):
            # Check if the chat completion is still processing
            if response.choices[0].finish_reason == None:

                    # Append the incremental response to the full response
                    full_response += (response.choices[0].delta.content or "")
                    # Display the response as it's being generated
                    message_placeholder.markdown(full_response + "▌")

        # Once the full response is generated, display it in the chat
        message_placeholder.markdown(full_response)

    # Add the assistant's full response to the session state to maintain the conversation history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

