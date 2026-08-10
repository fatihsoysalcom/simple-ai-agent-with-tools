import os
from typing import Dict, Any

# Assume we have a simple LLM interface (replace with actual LLM call in production)
# For this example, we'll mock its behavior.
def mock_llm(prompt: str) -> str:
    print(f"\n--- LLM Input ---\n{prompt}\n--- LLM Output ---")
    if "what is the weather in" in prompt.lower():
        return "The weather in Istanbul is sunny and 25 degrees Celsius."
    elif "calculate" in prompt.lower():
        try:
            # Very basic calculation parsing
            expression = prompt.split("calculate")[-1].strip().split("=")[0].strip()
            result = eval(expression)
            return f"The result of {expression} is {result}."
        except Exception as e:
            return f"Could not calculate. Error: {e}"
    else:
        return "I am a simple AI agent. I can tell you the weather or perform basic calculations."

# Define available tools
def get_weather(location: str) -> str:
    # In a real scenario, this would call a weather API
    print(f"\n--- Tool: get_weather called with location: {location} ---")
    return mock_llm(f"what is the weather in {location}")

def calculate_expression(expression: str) -> str:
    # In a real scenario, this would execute code or use a calculator
    print(f"\n--- Tool: calculate_expression called with expression: {expression} ---")
    return mock_llm(f"calculate {expression}")

# Agent's thought process and tool selection logic
def agent_executor(user_query: str) -> str:
    # Step 1: LLM decides what to do based on the user query
    initial_thought_prompt = f"User query: {user_query}\n\nBased on the user query, decide if you need to use a tool. If so, specify the tool name and its arguments. If not, respond directly. Available tools: get_weather(location), calculate_expression(expression)"
    llm_response = mock_llm(initial_thought_prompt)

    # Step 2: Parse LLM response to determine action
    if "get_weather" in llm_response:
        # Extract arguments for get_weather
        try:
            location_arg = llm_response.split("get_weather(")[-1].split(")")[0].strip().strip("'"')
            tool_result = get_weather(location_arg)
        except Exception as e:
            tool_result = f"Error calling get_weather: {e}"
    elif "calculate_expression" in llm_response:
        # Extract arguments for calculate_expression
        try:
            expression_arg = llm_response.split("calculate_expression(")[-1].split(")")[0].strip().strip("'"')
            tool_result = calculate_expression(expression_arg)
        except Exception as e:
            tool_result = f"Error calling calculate_expression: {e}"
    else:
        # If no tool is identified, the LLM might have already generated a direct answer
        tool_result = llm_response

    # Step 3: LLM synthesizes the final answer using the tool result (or direct response)
    final_answer_prompt = f"User query: {user_query}\n\nTool result (if any): {tool_result}\n\nSynthesize a final answer for the user."
    final_answer = mock_llm(final_answer_prompt)

    return final_answer

if __name__ == "__main__":
    print("--- Simple AI Agent Demo ---")
    print("You can ask about the weather or ask to calculate something.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Agent: Goodbye!")
            break
        
        response = agent_executor(user_input)
        print(f"Agent: {response}")
