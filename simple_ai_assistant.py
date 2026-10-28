# standard library imports
import os

# Third-party imports
from openai import OpenAI
from dotenv import load_dotenv

# Local modules
from utilities.tools import TOOLS, run_tool
from utilities.utilities import log

load_dotenv() # by default looks for .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

# Safety limit: the max number of model rounds for ONE user question
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
            # The complex logic is now handled inside run_tool
            result = run_tool(tool_call)

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

        print("🤖 Assistant: " + fallback)
        continue

    # Save and display the final model response
    messages.append(
        {
            "role": "assistant",
            "content": msg.content or ""
        }
    )

    print("🤖 Assistant: " + (msg.content or ""))