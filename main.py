from agent.orchestrator import run_agent
from ollama import Message

def main() -> None:

    # Introduce and set ground conventions for AI
    messages = [
        Message(
            role="system",
            content="""
            You are Archie, a local AI assistant.

            RESPONSE GUIDELINES:
            - Be concise and direct.
            - Avoid unnecessary explanations and repetition.
            - Prefer short answers unless more detail is requested.
            - Use bullet points when appropriate.
            - Do not sacrifice accuracy for brevity.
            - For complex tasks, explain your reasoning clearly.

            When a tool returns a file or directory path, use that exact
            path in subsequent tool calls.

            Never guess, reconstruct, or shorten paths returned by tools.
            Do not replace absolute paths with relative paths.
            """
        )
    ]

    print("Assistant active.")

    while True:
        user_input = input("> ")

        if user_input == "quit":
            break

        if not user_input:
            continue

        messages.append(Message(
            role="user",
            content=user_input
        ))


        print("Archie: ", end="", flush=True)

        answer = run_agent(messages)

        print(answer)
        print()

        print(messages)


if __name__ == '__main__':
    main()
