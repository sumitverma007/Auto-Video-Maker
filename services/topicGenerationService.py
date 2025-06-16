# Get API key
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def get_openai_response(prompt: str, topic: str):
    full_prompt = f"Topic: {topic}\n\n{prompt}"

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7
        )

        return json.loads(
            response.choices[0].message.content
        )
        # return json.dumps({
        #     "response": response.choices[0].message.content
        # }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)