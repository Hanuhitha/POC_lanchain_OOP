import streamlit as st


def read_python_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# query = "Given an array nums of n integers and an integer target, are there elements a, b, c, and d in nums such that a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target. Write in Python"
python_file_path = '/Users/sripad/Desktop/POC_lanchain_OOP/test.py'
with open(python_file_path, 'r') as file:
    python_code = file.read()


st.title('Output')
query = st.text_area('Enter your question:')

# st.code(python_code, language='python')


if st.button('Submit'):
     if query:
          with st.spinner('Loading file...'):
            try:
                # Read the Python file
                python_code = read_python_file(python_file_path)
                # Display the query
                st.write(f"Your question: {query}")
                # Display the Python code with syntax highlighting
                st.code(python_code, language='python')
            except Exception as e:
                st.error(f"Error reading file: {e}")



