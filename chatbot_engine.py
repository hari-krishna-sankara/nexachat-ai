from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("api_key"))

GROQ_MODEL = "openai/gpt-oss-20b"

history_file = "chat_history.json"


def get_groq_response(question, chat_history):

    messages = []

    # Add previous chat history
    for role, text in chat_history[-10:]:

        messages.append({
            "role": "user" if role == "You" else "assistant",
            "content": text
        })

    # Add current question
    messages.append({
        "role": "user",
        "content": question
    })

    try:

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            stream=True
        )

        return response

    except Exception as e:

        print("Error:", e)


def save_chat_history(history):

    with open(history_file, "w", encoding="utf-8") as f:

        json.dump(
            history,
            f,
            indent=4,
            ensure_ascii=False
        )


def load_chat_history():

    if os.path.exists(history_file):

        try:

            with open(history_file, "r", encoding="utf-8") as f:

                history = json.load(f)

            if all(
                isinstance(item, list) and len(item) == 2
                for item in history
            ):

                return history

            else:

                print("Warning: Invalid history format")
                return []

        except Exception as e:

            print("Warning: Could not load chat history:", e)
            return []

    return []


def display_chat_history(history):

    if not history:

        print("No Chat History")
        return

    print("\n========== Chat History ==========")

    for role, text in history:

        print(f"{role}: {text}")

    print("==================================\n")