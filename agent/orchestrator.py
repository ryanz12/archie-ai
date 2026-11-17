from llm.ollama_client import get_response
from tools.registry import available_functions
from ollama import Message
from typing import Any

def execute_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    tool = available_functions.get(tool_name)

    if tool is None:
        return {"success": False, "error": "Unknown tool"}

    if tool["requires_permission"]:
        print(f"\nArchie wants to use {tool_name}")
        print(f"Arguments: {arguments}")

        approval = input("Allow this action? (y/n): ").strip().lower()

        if approval != "y":
            return {
                "success": False,
                "error": "User denied permission. The action was not executed"
            }

    try:
        result = tool["function"](**arguments)

        # Additional confirmation
        if isinstance(result, dict) and result.get("require_confirmation"):
            print(f"\nArchie: {result['message']}")

            approval = input("Allow? (y/n): ").strip().lower()

            if approval != "y":
                return {"success": False, "error": "User denied confirmation."}

            arguments["overwrite"] = True
            result = tool["function"](**arguments)

        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def run_agent(messages: list[Message]) -> str:
    """
    Take list of messages, prompt AI until no more tool calls
    are present, then return the message
    """
    max_iterations = 10

    for _ in range(max_iterations):
        response = get_response(messages)

        messages.append(response)

        tool_calls = response.tool_calls

        if not tool_calls:
            return response.content or ""

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments

            result = execute_tool(function_name, arguments)

            messages.append(Message(
                role="tool",
                tool_name=function_name,
                content=str(result)
            ))

    return "I have reeached the maximum number of tool calls"
