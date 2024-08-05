

from models import create_chat_model, create_embedding_model
from agent import Agent
from agent_state import AgentState
from create_rag import CoderRag, SummaryRag
from node import Node
from prompts import code_prompt_template, summary_prompt_template,decision_prompt_template
from langgraph.graph import END, StateGraph, START

# pipeline

def main():

    #  model init
    llm= create_chat_model()
    embeddings = create_embedding_model()

    # rags

    coder_db = CoderRag( source= "/Users/sripad/Desktop/LLM/project/Leetcode/1-100q", destination= "./chroma_db_code",embeddings= embeddings ).create_db()
    
    summary_db = SummaryRag( source= "/Users/sripad/Desktop/LLM/docs", destination= "./chroma_db",embeddings= embeddings ).create_db()


    #  retriver 
    code_retriever = coder_db.as_retriever(search_type="similarity",
                             search_kwargs ={"k": 1})
    

    summary_retriever = summary_db.as_retriever(search_type="similarity",
                             search_kwargs ={"k": 1})  


    #  defining agents (chain)

    router_agent = Agent(prompt = decision_prompt_template,llm = llm, agent_name = 'ROUTER')
    summary_agent = Agent(prompt = summary_prompt_template,llm = llm, agent_name = 'SUMMARIZER', retriever=summary_retriever)
    coder_agent = Agent(prompt = code_prompt_template,llm = llm, agent_name = 'CODER', write_output=True, retriever=code_retriever)

    # defining nodes

    router_node = Node(agent = router_agent)
    summary_node= Node(agent = summary_agent)
    coder_node = Node(agent = coder_agent)

    #  langraph 

    graph = StateGraph(AgentState)

    graph.add_node("Summarizer", summary_node)
    graph.add_node("Coder", coder_node)
    graph.add_node("router", router_node)

    #  start edge
    graph.add_edge(START, "router")

    conditional_mapping  = {"SUMMARIZER" : "Summarizer", "CODER": "Coder", "END" : END }
    graph.add_conditional_edges("router", lambda x : x["next"], conditional_mapping)
    for node in ['Summarizer','Coder']:
        graph.add_edge(node, "router")

    graph_compiled = graph.compile()

    start_state = {"query" : " Given an array nums of n integers and an integer target, are there elements a, b, c, and d in nums such that a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target. Write in Python",
                   "file_path" : "test.py"}

    for s in graph_compiled.stream(start_state):
        if "__end__" not in s:
            print(s)
            print("----")



main()






    



















