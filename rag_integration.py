from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Import the data preparation module that likely contains functions for generating and processing data.
from data_preparation import dataGenerator

# Define a class that integrates RAG functionality.
class ragIntegrator:

    # Define a static method that takes a prompt and generates a response using the RAG system.
    def ragOutput(prompt):

        #To generate clean data again data
        #Generator.clean_data()

        # Define a static method that takes a prompt and generates a response using the RAG system.
        split_docs = dataGenerator.split_data()

        # Initialize the ChatOpenAI model with GPT-4 and streaming capabilities.
        llm = ChatOpenAI(model_name='gpt-4', streaming=True, temperature=0)

        # Create an embeddings model using OpenAIEmbeddings for document vectorization.
        embeddings_model = OpenAIEmbeddings()

        # Create a searchable database of documents using the Chroma vector store.
        db = Chroma.from_documents(split_docs, OpenAIEmbeddings())

        # Define a template that structures how the AI assistant should respond.
        template = """
        Act as a AI Assistant for a travel agency and use the following pieces of context to answer the question at the end.
        If you don't know the answer, just try to answer from your own knowledge.
        Try to summarize the answer clear and concise.
        ______
        Context: {context}
        Question: {question}
        Helpful Answer:"""

        # Convert the template string into a PromptTemplate object.
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # Initialize the RetrievalQA chain which will retrieve documents and generate answers.
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .75, "k": 5}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
        # Return the output from the qa_chain, which processes the given prompt and generates a response.
        return qa_chain({"query": prompt})
