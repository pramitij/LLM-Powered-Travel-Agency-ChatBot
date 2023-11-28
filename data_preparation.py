import pandas as pd
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import DataFrameLoader

class dataGenerator:

    def clean_data():
        # Define column names as strings (up to 100 columns)
        my_cols = [str(i) for i in range(100)]

        # Read the raw CSV file into a DataFrame
        df = pd.read_csv('cruise_data_raw.csv', names=my_cols, engine="python")

        # Concatenating non-null values from column '10' onwards, separated by commas
        df["10"] = df.apply(lambda row: ', '.join(row[10:].dropna().tolist()), axis=1)

        # Keeping only the first 11 columns
        df = df[[str(i) for i in range(11)]]

        # Set the first row as the header
        df = df.rename(columns=df.iloc[0]).loc[1:]

        # Extract start city from the 'portsCovered' column
        df['startCity'] = df['portsCovered'].apply(lambda x: x.split('|')[0])

        # Extract end city from the 'portsCovered' column
        df['endCity'] = df['portsCovered'].apply(lambda x: x.split('|')[-1])

        # Drop the 'starRating' and 'startEndCity' columns
        df = df.drop(['starRating', 'startEndCity'], axis=1)

        # Save the cleaned data to a new CSV file
        df.to_csv('cruise_data_clean.csv', index=False)

        # Define the columns we want to embed vs which ones we want in metadata
        columns_to_embed = ["bonusOffers"]
        columns_to_metadata = df.columns

        # Function to format a row of the DataFrame as page content
        def format_page_content(row):
            # Create a dictionary from the row using the defined metadata columns
            d = dict(zip(columns_to_metadata, row[columns_to_metadata]))
            # Join the dictionary into a string, with each key-value pair on a new line
            return "\n".join(f"{k.strip()}: {v.strip()}" for k, v in d.items() if isinstance(v, str))

        # Apply the formatting function to each row to create the 'page_content' column
        df['page_content'] = df.apply(lambda row: format_page_content(row), axis=1)
        # Save the DataFrame with the page content to a new CSV file
        df.to_csv('cruise_data_with_page_content.csv', index=False)


    def split_data():
        df = pd.read_csv('cruise_data_with_page_content.csv')
        df = df.rename(columns = {"Unnamed: 0" : "index"})
        loader = DataFrameLoader(df, page_content_column="page_content")
        docs = loader.load()

        text_splitter = CharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap  = 0,
            length_function = len,
            is_separator_regex = False,
        )
        split_docs = text_splitter.split_documents(docs)
        return split_docs




