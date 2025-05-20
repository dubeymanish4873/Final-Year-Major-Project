from llm_model import generate_response
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import streamlit as st
from langchain.document_loaders import UnstructuredURLLoader, TextLoader, CSVLoader, PyPDFLoader

st.title("Research Tool")
st.sidebar.title("Article URLs")
main_placeholder = st.empty()

# Initialize session state for data_dict if not present
if 'data_dict' not in st.session_state:
    st.session_state.data_dict = {
        'instruction': '',
        'input': '',
        'output': ''
    }

# Input URLs
urls = st.sidebar.text_input("URL")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt", "pdf", "csv"])
process_data_clicked = st.sidebar.button("Process Data")

if process_data_clicked:
    all_texts = []

    if urls:
        st.success("URL uploaded successfully.")
        loader = UnstructuredURLLoader([urls])  # wrap in list
        main_placeholder.text("Loading URL Content......")
        data = loader.load()
        documents_text = "\n\n".join([dt.page_content for dt in data])
        all_texts.append(documents_text)

    if uploaded_file:
        st.success("URL uploaded successfully.")
        main_placeholder.text("Loading file content...")
        file_path = f"temp_uploaded_file.{uploaded_file.name.split('.')[-1]}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension == "pdf":
            loader = PyPDFLoader(file_path)
        elif file_extension == "csv":
            loader = CSVLoader(file_path)
        elif file_extension == "txt":
            loader = TextLoader(file_path)
        else:
            st.error("Unsupported file type.")
            loader = None

        if loader:
            file_data = loader.load()
            file_text = "\n\n".join([dt.page_content for dt in file_data])
            all_texts.append(file_text)

    # Merge all collected texts
    combined_text = "\n\n".join(all_texts)
    print(combined_text)
    st.success("Merged all collected texts")

    if combined_text.strip():
        st.session_state.data_dict["input"] = combined_text
        main_placeholder.text("Data processing complete.")
    else:
        main_placeholder.text("No data was loaded.")

    # st.session_state.data_dict.update({"input": documents_text})

# Input question
query = main_placeholder.text_input("Prompt:")

if query:
    st.session_state.data_dict.update({
        "instruction": str(query),
        "output": ""
    })
    st.header("Answer")
    response = generate_response(st.session_state.data_dict)
    st.write(response)
