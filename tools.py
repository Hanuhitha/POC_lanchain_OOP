from langchain_core.tools import tool 

from gtts import gTTS
from agent import Agent
from operator import itemgetter
from langchain_core.prompts import PromptTemplate

@tool
def text_to_audio(text:str, filename:str):
    "Method to convert the given text into audio"
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("audio/" + filename)
    return {'audio_file_path':"audio/"+filename}


class ToolAgent:
    def __init__(self, prompt, llm, agent_name, tools,rendered_tools,write_output=False, parser=False):
        
        self.prompt = prompt 
        self.llm =  llm
        self.parser = parser
        self.agent_name = agent_name
        self.write_output = write_output
        self.tools = tools
        self.rendered_tools = rendered_tools
        self.prompt = PromptTemplate(
            template=self.prompt,
            input_variables=["query"],
            partial_variables={
                               "format_tools":self.rendered_tools},
        )
        self.agent_chain = self.create_chain()

    def create_chain(self):
        # rendered_tools = self.rendered_tools 
        return self.prompt | self.llm| self.parser | self.tool_chain
        

    def tool_chain(self, model_output):
        tool_map = {tool.name: tool for tool in self.tools}
        try:
            chosen_tool = tool_map[model_output["name"]]
        except:
            return 
        return itemgetter("arguments") | chosen_tool



