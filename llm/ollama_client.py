import ollama
import tools.registry


import ollama
import tools.registry

def get_response(messages: list[ollama.Message]) -> ollama.Message:
    """
    Prompt the model and stream its thinking and response.
    """
    stream = ollama.chat(
        model="llama3.2:3b",
        messages=messages,
        tools=tools.registry.tools,
        stream=True
    )

    thinking_started = False
    response_started = False

    thinking = ""
    content = ""
    tool_calls = []

    for chunk in stream:
        # Stream thinking
        if chunk.message.thinking:
            if not thinking_started:
                print("\nArchie is thinking:\n")
                thinking_started = True

            print(chunk.message.thinking, end="", flush=True)
            thinking += chunk.message.thinking

        # Stream normal response
        if chunk.message.content:
            if not response_started:
                print("\n\nArchie:\n")
                response_started = True

            print(chunk.message.content, end="", flush=True)
            content += chunk.message.content

        # Collect tool calls
        if chunk.message.tool_calls:
            tool_calls.extend(chunk.message.tool_calls)

    print()

    return ollama.Message(
        role="assistant",
        content=content,
        thinking=thinking,
        tool_calls=tool_calls
    )
