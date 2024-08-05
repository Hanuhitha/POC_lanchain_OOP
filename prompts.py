
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# coder system prompt
code_sys_prompt = (
"You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python/JAVA. Don't explain the code, just generate the code block itself. Include main method with test cases"
"You might use the retrieved code for reference"
"\n"
)

# paper summary system prompt
qa_system_prompt = (
"You are an assistant for question-answering tasks"
"Use the following pieces of retrieved context to answer the question."
" If you don't know the answer, just say that you don't know."
"Use three sentences maximum and keep the answer concise."
"Do not answer anything except the retrieved content."
"\n"
)

# router prompt
decision_prompt = (
"""You are a language model designed to classify queries based on their type. Your task is to return "CODER" if the query is related to coding, "SUMMARIZER" if the query is a general question, and "END" if the previous messages indicate the question has already been answered. Here are the criteria:

1. **CODER**: The query contains keywords like "code," "program," "algorithm," "debug," or mentions specific programming languages or frameworks.
2. **SUMMARIZER**: The query does not fit the CODER criteria and is a general question or request for information.
3. **END**: The context from previous messages clearly indicates that the current question has already been answered.
4. If the conversation history is empty, choose between SUMMARIZER and CODER based on the nature of the query:
    - Choose SUMMARIZER if the query requires summarizing information or distilling key points.
    - Choose CODER if the query requires is a logical question that requires writing code.
5. If the conversation history is not empty, return END.
Given the following query and previous messages, determine the appropriate response:

### Previous Messages
{messages}

### Query
{query}

Respond with either "CODER," "SUMMARIZER," or "END."
"""
)

code_prompt_template = ChatPromptTemplate.from_messages([
    ("system", code_sys_prompt),
    MessagesPlaceholder("retrieved_code"),
    ("human", "{query}"),
])

#  actual prompt
summary_prompt_template = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("retrieved_docs"),
    ("human", "{query}"),
])


decision_prompt_template = ChatPromptTemplate.from_template(decision_prompt)