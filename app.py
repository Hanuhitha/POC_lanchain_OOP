import streamlit as st
from main import execute_graph


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


graph = execute_graph()
st.title("Langchain Smart Q/A chat")
code_language = st.selectbox("code language", ["python", "Java", "CPP", "None"])
query = st.text_area("Enter your question:")
if code_language != "None":
    query = query + f". Write code in {code_language} programming language"

current_state = None
if st.button("Submit"):
    if query:
        with st.status("Processing user query"):
            try:
                for s in graph.stream({"query": query}):
                    current_state = list(s.keys())[0]
                    if "__end__" not in s:
                        st.write(current_state)
                    else:
                        st.write(current_state)
                        break
            except:
                st.error("error occured! Cannot process request. Retry with different prompt.")
        try:
            current_state_dict = s[current_state]
            code_file_path = s[current_state]["code_file_path"]
            
            
            code_file = read_file(code_file_path)
            st.code(code_file)

            summary = read_file(s[current_state]["summary_file_path"])
            
            st.success("Done!")
            st.text(summary)
        except:
            st.error(s)
