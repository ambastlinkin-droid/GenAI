import os
from dotenv import load_dotenv
from google import genai
from utils.config import SYSTEM_PROMPT

load_dotenv()

class LLMClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        # ── Fix 1: exact message the test expects ──────────────
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=self.api_key)

    def call_api(self, user_query):
    # ── Use .format() to inject user query ────────────────────
        full_prompt = SYSTEM_PROMPT.format(user_query=user_query)

        response = self.client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
        )

        if not response or not response.text:
            return "didn't receive a valid response"

        return response.text.strip()


def answer_student_query(query):
    try:
        client = LLMClient()
        return client.call_api(query)

    except ValueError as e:
        return f"Configuration Error: {str(e)}"

    # ── Fix 3: exact prefix the test expects ───────────────────
    except Exception as e:
        return f"encountered an error: {str(e)}"


def main():
    """Main function to demonstrate the movies recommendation assistant."""
    print("Movies Recommendation Assistant")
    print("=" * 50)

    sample_queries = [
        "I want to watch a good action movie tonight",
        "Recommend me something funny",
        "What's a good sci-fi movie?",
        "I'm in the mood for horror",
        "Whats the weather like today?"
    ]

    for query in sample_queries:
        print(f"\nQuery: {query}")
        response = answer_student_query(query)
        print(f"Response: {response}")
        print("-" * 40)


if __name__ == "__main__":
    main()