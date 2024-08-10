from models import create_chat_model, create_embedding_model
from agent import Agent
from agent_state import AgentState
from create_rag import CoderRag, SummaryRag
from langchain_core.output_parsers import JsonOutputParser
from PIL import Image
from node import Node
from prompts import (
    code_prompt_template,
    summary_prompt_template,
    decision_prompt_template,
    code_summarizer_prompt_template,
    audio_summary_prompt,
    router_parser,
    summary_parser,
    coder_parser,

)
from langgraph.graph import END, StateGraph, START
from tools import ToolAgent, text_to_audio
from langchain.tools.render import render_text_description




def save_graph(graph):
    try:
        # Get the image data
        img_data = graph.get_graph().draw_mermaid_png()
        
        # Save the image to a file
        with open('flow.png', 'wb') as f:
            f.write(img_data)
        
        print(f"Image saved successfully")
    except Exception as e:
        print(f"Error saving image: {e}")

# pipeline


def execute_graph():

    #  model init
    llm = create_chat_model()
    embeddings = create_embedding_model()

    # rags

    coder_db = CoderRag(
        source="Leetcode/1-100q",
        destination="./chroma_db_code",
        embeddings=embeddings,
    ).create_db()

    summary_db = SummaryRag(
        source="docs",
        destination="./chroma_db",
        embeddings=embeddings,
    ).create_db()

    #  retriver
    code_retriever = coder_db.as_retriever(
        search_type="similarity", search_kwargs={"k": 1}
    )

    summary_retriever = summary_db.as_retriever(
        search_type="similarity", search_kwargs={"k": 1}
    )

    #  defining agents (chain)

    router_agent = Agent(prompt=decision_prompt_template, llm=llm, agent_name="ROUTER")
    document_summary_agent = Agent(
        prompt=summary_prompt_template,
        llm=llm,
        agent_name="SUMMARIZER",
        retriever=summary_retriever,
        write_output=True,
    )
    coder_agent = Agent(
        prompt=code_prompt_template,
        llm=llm,
        agent_name="CODER",
        write_output=True,
        retriever=code_retriever,
    )
    code_summary_agent = Agent(
        prompt=code_summarizer_prompt_template,
        llm=llm,
        agent_name="CODE_SUMMARIZER",
        write_output=True,
    )

    audio_agent = ToolAgent(llm=llm,prompt=audio_summary_prompt,write_output=True,agent_name="AUDIO_SUMMARIZER",
                            parser=JsonOutputParser(),tools= [text_to_audio], rendered_tools=
                              render_text_description([text_to_audio]))

    # defining nodes

    router_node = Node(agent=router_agent, agent_parser=router_parser)

    summary_node = Node(agent=document_summary_agent, agent_parser=summary_parser)
    coder_node = Node(agent=coder_agent, agent_parser=coder_parser)
    code_summary_node = Node(agent=code_summary_agent, agent_parser=summary_parser)
    audio_summary_node = Node(agent=audio_agent, agent_parser=False)

    #  langraph
    graph = StateGraph(AgentState)

    graph.add_node("Summarizer", summary_node)
    graph.add_node("Coder", coder_node)
    graph.add_node("router", router_node)
    graph.add_node("Code_Summarizer", code_summary_node)
    graph.add_node("Audio_Summarizer", audio_summary_node)

    #  start edge
    graph.add_edge(START, "router")

    conditional_mapping = {"SUMMARIZER": "Summarizer", "CODER": "Coder", "END": END, "ROUTER":"router","CODE_SUMMARIZER": "Code_Summarizer", "AUDIO_SUMMARIZER":"Audio_Summarizer"}
    graph.add_conditional_edges("router", lambda x: x["next"], conditional_mapping)
    graph.add_conditional_edges("Summarizer", lambda x: x["next"], conditional_mapping)
    graph.add_conditional_edges("Coder", lambda x: x["next"], conditional_mapping)
    graph.add_conditional_edges("Code_Summarizer", lambda x: x["next"], conditional_mapping)
    graph.add_conditional_edges("Audio_Summarizer", lambda x: x["next"], conditional_mapping)

    
    graph_compiled = graph.compile()

    # save_graph(graph_compiled)
    # local testing code
    # start_state = {
    #     "query": """what is bert? Write a summary.
    # """
    # }

    # for s in graph_compiled.stream(start_state):
    #     if "__end__" not in s:
    #         print(s)
    #         print("----")
    #     else:
    #         final_state = s
    #         break

    return graph_compiled


execute_graph()

