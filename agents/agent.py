# agent.py
import json
import time
from agents.memory import LastMemories, LastTokens, RelevantMemories
from llm import generate_text, generate_text_with_function_call, gpt4_model, gpt35_model, gpt35_16k_model
from utils import Logger

SYSTEM_MESSAGE = """You are a helpful assistant. You are trying to solve the Goal. Keep track of your thought process in the [SCRATCHPAD], use the following format to record your thoughts:

Goal: the goal you must solve
Thought: you should always think about what to do
Action: the action to take, should be one of available [TOOLS]
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Action: final_answer
Final Answer: the final answer to the original input question.
"""

THINK_INSTRUCTIONS = """You are currently in the 'Thought' Step. 
Based on the thought process in the [SCRATCHPAD], think about the steps to resolve the Goal, consider the available [TOOLS]. Explain your reasoning and declare the tool to use at the end. Answer in one or two sentences."""

FINAL_ANSWER_INSTRUCTIONS = """You are currently in the 'Final Answer' Step.
Based only in the thought process and results in the [SCRATCHPAD], create a highly detailed and accurate answer to solve the Goal. You can use Markdown format. Be clear and concise."""

class Agent:
    def __init__(self, tools):
        self.tools = tools
        self.log = Logger()
        self.memory = RelevantMemories()

    def get_tools_schema(self):
        final_answer_schema = {
            "name": "final_answer", 
            "description": "Use this tool when you have all necessary information to resolve the Goal or no additional tools are required.", 
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
        tools_schema = [tool.get_schema() for tool in self.tools]
        tools_schema.append(final_answer_schema)        
        return tools_schema
    
    def get_tools_schema_str(self):
        return json.dumps(self.get_tools_schema())
    
    def execute_chain_of_thought(self, goal: str, max_iterations: int=5):
        start_time = time.time()
        self.memory.add_to_memory("user", goal)
        self.relevant_memories = self.memory.get_relevant_memories(goal)
        self.goal = goal
        self.scratchpad = "Goal: " + self.goal
        self.log.info(f"Goal: {self.goal}", verbose=True)
        final_answer = ""

        for iteration in range(max_iterations):

            thought = self.think()
            self.log.info(f"Thought: {thought}", verbose=True)
            self.scratchpad += f"\nThought: {thought}"
            
            chosen_tool = self.select_tool()
            self.log.info(f"Action: {chosen_tool}", verbose=True)
            self.scratchpad += f"\nAction: {chosen_tool}"
            
            if chosen_tool is None or chosen_tool.get("name","") == 'final_answer':
                final_answer = self.final_answer()
                self.scratchpad += f"\nFinal Answer: {final_answer}"
                break

            observation = self.act(chosen_tool)
            self.log.info(f"Observation: {observation}", verbose=True)
            self.scratchpad += f"\nObservation: {observation}"

        else:
            final_answer = self.final_answer()
            self.scratchpad += f"\nFinal Answer: {final_answer}"

        self.memory.add_to_memory("assistant", final_answer)
        time_taken = time.time() - start_time

        minutes, seconds = divmod(time_taken, 60)
        log_str = f"Time Spent:\n{int(minutes)} minutes and {seconds:.2f} seconds\n"
        self.log.info(f"Final Answer: {final_answer}", verbose=True)
        self.log.info(log_str)

        return final_answer

    def think(self):
        system_message = {"role": "system", "content": f"{SYSTEM_MESSAGE}\n{THINK_INSTRUCTIONS}"} 
        prompt = f"[HISTORY]\nHere is the conversation history between you and the user:\n{self.relevant_memories}\n\n"
        prompt += f"[TOOLS]\n{self.get_tools_schema()}\n\n[GOAL]\n{self.goal}\n\n[SCRATCHPAD]\n{self.scratchpad}\nThought:"
        result = generate_text(prompt, model=gpt4_model, messages=[system_message], stop=["Action:", "Final Answer:"])
        return result

    def select_tool(self):
        functions = self.get_tools_schema()
        prompt = f"[HISTORY]\nHere is the conversation history between you and the user:\n{self.relevant_memories}\n\n"  
        prompt += f"[SCRATCHPAD]\n{self.scratchpad}"
        result = generate_text_with_function_call(prompt, model=gpt4_model, functions=functions)
        return result

    def act(self, input_json):
        func_name = input_json.get("name", "")
        if not func_name:
            return "ERROR: Unable to parse tool function from action input."
        args_dict = input_json.get("arguments", {})
        if not args_dict:
            return "ERROR: Unable to parse tool arguments from action input."

        if isinstance(args_dict, str):
            try:
                args_dict = json.loads(args_dict)
            except Exception as e:
                return f"ERROR: Unable to parse tool arguments from action input: {e}"

        tool = None
        for t in self.tools:
            if t.func.__name__ == func_name:
                tool = t
                break
        if not tool:
            return f"ERROR: No tool found with func_name '{func_name}'"
        
        try:
            result = tool.execute(**args_dict)
        except Exception as e:
            return f"ERROR: Failed executing {func_name}: {e}"

        return result

    def final_answer(self):
        system_message = {"role": "system", "content": f"{SYSTEM_MESSAGE}\n{FINAL_ANSWER_INSTRUCTIONS}"}        
        prompt = f"[HISTORY]\nHere is the conversation history between you and the user:\n{self.relevant_memories}\n\n"  
        prompt += f"[GOAL]\n{self.goal}\n\n[SCRATCHPAD]\n{self.scratchpad}\nFinal Answer:"
        result = generate_text(prompt, model=gpt35_16k_model, messages=[system_message])
        return result