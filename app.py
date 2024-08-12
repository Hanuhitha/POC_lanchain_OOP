import streamlit as st
from main import execute_graph


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

if __name__ == "__main__":
    graph = execute_graph()
    st.title("Langchain Smart Q/A system")
    code_language = st.selectbox("code language", ["python", "Java", "CPP", "None"])
    query = st.text_area("Enter your question:")
    if code_language != "None":
        query = f"""{query}. Write code in {code_language} programming language. """
    else:
        query =   f"""Write a summary for {query}"""

    current_state = None
    if st.button("Submit"):
        if query:
            with st.status("Thinking.."):
                try:
                    for s in graph.stream({"query": query}):
                        current_state = list(s.keys())[0]
                        if "__end__" not in s:
                            st.write(f'Entering : {current_state} node')
                        else:
                            st.write(f'Entering : {current_state} node')
                            break
                except:
                    st.error("error occured! Cannot process request. Retry with different prompt.")
            try:
                current_state_dict = s[current_state]
                code_file_path = s[current_state]["code_file_path"]
                summary_file_path = s[current_state]["summary_file_path"]
                audio_file_path = s[current_state]["audio_file_path"]
                
                if code_file_path:
                
                    code_file = read_file(code_file_path)
                    st.header("Generated Code")
                    st.code(code_file)
                if summary_file_path:
                    summary = read_file(summary_file_path)
                    st.header("Generated Summary")
                    summary = [x + "\n" if not (i+1)%15 else x for i,x in enumerate(summary.split(" "))]
                    st.text(" ".join(summary))
                    
                if audio_file_path:
                    st.header("Audio Summary")
                    st.audio(audio_file_path)
                    
                    
            except:
                st.error("LLM unable to process the request")
                st.error(s)
