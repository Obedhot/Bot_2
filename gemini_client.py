import google.generativeai as genai

from config import settings


def build_personality_prompt() -> str:
    return (
        f"You are {settings.bot_name}, a person who loves coding, science, and logic. "
        f"You speak in {settings.bot_language}. Your real name is {settings.bot_real_name}. "
        "Write short, relevant, friendly chat replies with occasional humor. "
        "Do not claim to be human or the account owner, and do not insult or threaten anyone. "
        "If the message is unclear, draft a brief clarifying question."
    )


def build_chat_session():
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add your key to the local .env file.")

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(
        model_name=settings.gemini_model,
        generation_config={
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 512,
            "response_mime_type": "text/plain",
        },
    )
    return model.start_chat()
