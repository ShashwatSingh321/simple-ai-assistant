import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

# Safety limit: maximum model rounds for one user question
MAX_STEPS = 5

messages.append(
    {
        "role": "system",
        "content": (
            "Act like a very humble agent and respond "
            "always under 10 words."
        )
    }
)

# Chat loop starts here
while True:
    user_input = input("\nShashwat: ")

    if user_input.strip().lower() in [
        "exit", "quit", "bye", "goodbye"
    ]:
        print("Assistant: Goodbye!")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Chained tool calling
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS
        )

        msg = response.choices[0].message

        # The model has finished and doesn't need another tool
        if not msg.tool_calls:
            break

        # Preserve the assistant's tool-call request
        messages.append(msg)

        # Execute every tool requested in this round
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = {}

            try:
                func_args = json.loads(
                    tool_call.function.arguments or "{}"
                )

                fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result = fn(**func_args)

            except Exception as e:
                result = (
                    f"Error while running {func_name}: {e}"
                )

            # Return the tool result to the model
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

    else:
        # Ran out of steps without receiving a final answer
        fallback = (
            "Sorry, I could not finish this within "
            "the step limit."
        )

        messages.append(
            {
                "role": "assistant",
                "content": fallback
            }
        )

        print("Assistant: " + fallback)
        continue

    # Save and display the final model response
    messages.append(
        {
            "role": "assistant",
            "content": msg.content or ""
        }
    )

    print("Assistant: " + (msg.content or ""))
