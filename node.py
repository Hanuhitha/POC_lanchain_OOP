

from langchain_core.messages import HumanMessage
import codecs

class Node:
    def __init__(self, agent):
        self.agent = agent

    def __call__(self, state):
        query = state['query']
        messages = state['messages']
        next = state['next']
        file_path = state['file_path']

        output = self.agent.agent_chain.invoke(state)
        if self.agent.agent_name == "ROUTER":
            state['next'] = output.content.strip().upper()
            state['messages'] = [HumanMessage(content =query)]
        else:
            state['messages'] = [HumanMessage(content = output.content)]
        if self.agent.write_output:
            self.write_code(file_path, output.content)
        return state
    
    def write_code(self, file_path, ai_output):
        with codecs.open(file_path, 'w', encoding='utf-8') as file:
            status = file.write(ai_output)
            print("File written succesfully")
            









        
