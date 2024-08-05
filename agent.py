from langchain.schema.runnable import RunnableLambda

class Agent:
    def __init__(self, prompt,llm, agent_name, write_output=False, retriever=False):
        self.prompt = prompt 
        self.llm =  llm
        self.retriever = retriever
        self.agent_name = agent_name
        self.agent_chain = self.create_chain()
        self.write_output = write_output


    def retrieve_data(self,data):
        query =  data['query']
        retrieved_doc = self.retriever.invoke(query)
        if self.agent_name.upper() == 'CODER':
            retrieved_code = [x.metadata['code'] for x in retrieved_doc]
            data['retrieved_code'] = retrieved_code
        retrieved_doc = [x.page_content for x in retrieved_doc]
        data['retrieved_docs'] = retrieved_doc
        return data
    
    def create_chain(self):
        if self.agent_name.upper() == 'ROUTER':
            agent_chain = self.prompt | self.llm
            return agent_chain
        chain_runnable = RunnableLambda(self.retrieve_data)
        agent_chain = chain_runnable | self.prompt | self.llm
        return agent_chain








        