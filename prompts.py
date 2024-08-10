from langchain_core.prompts import PromptTemplate
from pydantics_store import Router, Coder, Summarizer, Audio
from langchain.output_parsers import PydanticOutputParser
from tools import text_to_audio


# coder system prompt


code_prompt = (
"""You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python/JAVA/CPP. Don't explain the code, just generate the code block itself.

You might use the retrieved code for reference.
{retrieved_code}

Query:
{query}

Format instructions:
{format_instructions}

Take a look at the error {error} that you made last time to get better result now.

Generate code based on the query. Respond ONLY with the code in the JSON format specified by the format instructions. Do not include explanations or additional text.
Avoid using OOP.
STRICTLY FOLLOW FORMATTING INSTRUCTIONS.


"""
)



# Question answer prompt
qa_prompt = """

You are a question-answering assistant. Use the provided context to answer the query.

Query:
{query}

Format instructions:
{format_instructions}

"Additionally, review the previous error message to ensure the output is formatted correctly, if required:
{error}"

Context:
{retrieved_docs}
"""

# router prompt
decision_prompt = (
"""
You are a router. You route to nodes based on the query you receive. You can route to one of the three options.
Option 1 : CODER
Option 2 : SUMMARIZER
Option 3 : END


Choose END if {code_file_path} has a file path. Choose END if  {summary_file_path} has a file path.

Choose END  if message history has code in it.
Choose END if the message history has summary in it.
If the messages have message from CODER or SUMMARIZER, Choose END.
query : {query}
message history : {messages}
format instructions : {format_instructions}

STRICTLY Adhere to format instructions. Do not return any pretext to the output.
"""

)





#  CODE summarizer prompt
code_summarizer_prompt = """ You are a code summarizer. Elaborate any code found in the previous messages in detail.

Previous Messages:
{messages}

Format instructions:
{format_instructions}

"Additionally, review the previous error message to ensure the output is formatted correctly, if required:
{error}"

Rules:
1. Summarize only code from the previous messages.
2. Provide a elaborate summary of the code's purpose and functionality.
3. Include a filename for the summary, using .txt extension.
4. Respond ONLY with a JSON object containing 'summary' and 'filename' fields.
5. If no code is present, set summary to "No code found" and filename to "empty.txt".

Summarize following these rules. Do not include any text outside the JSON object."""



audio_summary_prompt = (
    """
    You are an agent with access to the following tools:
    {format_tools}

    If the messages have SUMMARIZER data, then only you need to generate audio summary.
    Else, do not choose the tool.
    Generate a filename depending on the context.

    Select the tool based on the input message history. 
    {messages}
    The output MUST be json with formatting instructions given below:

    Given the user input, return the name and input of the tool to use.
    Return your response as a JSON blob with 'name' and 'arguments' keys.
    The value associated with the 'arguments' key should be a dictionary of parameters

    Past errors:
    {error}
    
    STRICTLY ADHERE TO THE FORMATIING RULES. DO NOT GIVE ANYTHING OTHER THAN THE JSON OUTPUT.
    The output will be parsed using JsonOutputParser() package from langchain. Be sure to generate
    the output such that it works with the JsonOutputParser()

    """

)

# Initializing pydantic parsers for each nodes
router_parser = PydanticOutputParser(pydantic_object=Router)
coder_parser = PydanticOutputParser(pydantic_object=Coder)
summary_parser = PydanticOutputParser(pydantic_object=Summarizer)
audio_parser = PydanticOutputParser(pydantic_object=Audio)


code_prompt_template = PromptTemplate(
    template=code_prompt,
    input_variables=["query", "retrieved_code"],
    partial_variables={"format_instructions": coder_parser.get_format_instructions()},
)

summary_prompt_template = PromptTemplate(
    template=qa_prompt,
    input_variables=["query", "retrieved_docs"],
    partial_variables={"format_instructions": summary_parser.get_format_instructions()},
)

decision_prompt_template = PromptTemplate(
    template=decision_prompt,
    input_variables=["query", "messages"],
    partial_variables={"format_instructions": router_parser.get_format_instructions()},
)

code_summarizer_prompt_template = PromptTemplate(
    template=code_summarizer_prompt,
    input_variables=["messages"],
    partial_variables={"format_instructions": summary_parser.get_format_instructions()},
)


