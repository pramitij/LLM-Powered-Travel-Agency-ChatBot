
# Cruise-Finder: LLM Powered Travel Agency ChatBot

## Description
Cruise-Finder is an innovative chatbot designed to assist users in finding the best cruise packages and information for planning their next adventure. Utilizing advanced natural language processing technologies, this chatbot offers insightful recommendations and answers queries in real-time, enhancing the customer experience for travel planning.
Check out the Presentation for a deeper-dive into the tech stack.

## Contributors
- Pramithi Jagdish
- Aswin Shriram Thiagarajan

## Features
- **Intelligent Conversations**: Powered by OpenAI's GPT-4, the chatbot engages in natural, human-like conversations.
- **Context-Aware Responses**: Integrates RAG (Retrieval-Augmented Generation) for contextually relevant answers.
- **Streamlit Web Interface**: User-friendly web interface built with Streamlit for easy interaction.
- **Dynamic Data Handling**: Custom data integration for up-to-date information on cruise packages.

## Installation
To run Cruise-Finder on your local machine, follow these steps:

1. **Clone the Repository**:
    ```
    git clone [https://github.com/pramitij/LLM-Powered-Travel-Agency-ChatBot.git]
    ```
2. **Install Dependencies**:
    ```
    pip install streamlit openai pandas langchain
    ```
3. **Set Environment Variables**:
    - Set `OPENAI_API_KEY` with your OpenAI key for GPT-4 access.

4. **Run the Streamlit App**:
    ```
    streamlit run app.py
    ```

## Usage
After launching the app, simply type your query about cruise packages in the chat input box and press enter. The chatbot will respond with information and suggestions.

## Technologies Used
- **OpenAI GPT-4**: For generating human-like text responses.
- **Streamlit**: For creating the web application.
- **LangChain**: For integrating RAG with the chatbot.
- **Python**: Primary programming language used.

## How It Works
1. **User Input**: Users type queries related to cruise packages.
2. **RAG Processing**: The chatbot uses RAG to pull relevant context from a database of cruise information.
3. **GPT-4 Generation**: It then feeds this context to GPT-4 to generate a cohesive, informative response.
4. **Display Response**: The response is displayed in the Streamlit app, simulating a real-time conversation.
