from langchain_core.messages import HumanMessage
import codecs


class Node:
    def __init__(self, agent, agent_parser, output_dir="./"):
        """Initializes the Node class

        Args:
            agent (Runnable): A user defined runnable agent
            agent_parser (_type_): A pydantic parser for the agent output
            output_dir (str, optional): path to store agent outputs. Defaults to './'.
        """
        self.agent = agent
        self.agent_parser = agent_parser
        self.output_dir = output_dir

    def __call__(self, state):
        """Call method to initiate the node

                Args:
                    state (AgentState): A state dict to exchange information between nodes.
        n
                Returns:
                    AgentState: state dict
        """
        query = state["query"]
        output = self.agent.agent_chain.invoke(state)
        try:
            output = self.agent_parser.parse(output.content)
        except Exception as e:
            # pydantic fails, return to the previous state.
            state['error'] = f'The output you gave last time had parsing error. Please follow the formatting guidelines. The error was : {e}'
            state['next'] = self.agent.agent_name # routing to self
            state['messages'] = state['messages'][:-1]
            return state
        if self.agent.agent_name == "ROUTER":
            state["next"] = output.decision.strip().upper()
            state["messages"] = [HumanMessage(content=query)]
        elif self.agent.agent_name == "CODER":
            state["messages"] = [HumanMessage(content="CODER : "+output.code)]
            if self.agent.write_output:
                code_file_path = self.output_dir + "code/" + output.filename
                state["code_file_path"] = code_file_path
                self.write_code(code_file_path, output.code)
            state['next'] = "CODE_SUMMARIZER"
        elif "SUMMARIZER" in self.agent.agent_name:
            state["messages"] = [HumanMessage(content="SUMMARIZER :"+output.summary)]
            if self.agent.write_output:
                summary_file_path = (
                    self.output_dir
                    + "summary/"
                    + output.filename.split(".")[0]
                    + ".txt"
                )
                state["summary_file_path"] = summary_file_path
                self.write_code(summary_file_path, output.summary)
           
            state['next'] = "ROUTER"
        return state

    def write_code(self, file_path, ai_output):
        """Method to write code to the  file storage

        Args:
            file_path (_type_): path to the file
            ai_output (_type_): output content to be written to the files
        """
        with codecs.open(file_path, "w", encoding="utf-8") as file:
            status = file.write(ai_output)
            print("File written succesfully")
