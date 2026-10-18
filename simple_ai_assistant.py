import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # by default looks for .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

while True:

    user_input = input("\nShashwat:")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    print("Assistant: " + response.choices[0].message.content)
    print(response.choices[0].message.role)