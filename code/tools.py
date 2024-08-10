from langchain.tools import Tool, DuckDuckGoSearchResults
from langchain_core.tools import tool 
from langchain.tools.render import render_text_description
from langchain_core.output_parsers import JsonOutputParser

tools = [DuckDuckGoSearchResults]
rendered_tools = render_text_description(tools)

tool_prompt = ("""You are an assistant that has access to the following set of tools.
Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input : {query}, check if the {retrieved_docs} have enough information to answer 
the query. If no, make use of the most relevant tools from {rendered_tools}

return the name and input of the tool to use.
Return your response as a JSON blob with 'name' and 'arguments' keys.
The value associated with the 'arguments' key should be a dictionary of parameters.""")