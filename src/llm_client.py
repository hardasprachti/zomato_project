import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER    = os.getenv("LLM_PROVIDER", "groq")
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))
MAX_TOKENS  = int(os.getenv("LLM_MAX_TOKENS", 1024))

def get_recommendation(system_prompt, user_prompt):
    if PROVIDER == "gemini":
        return _call_gemini(system_prompt, user_prompt)
    elif PROVIDER == "openai":
        return _call_openai(system_prompt, user_prompt)
    elif PROVIDER == "anthropic":
        return _call_anthropic(system_prompt, user_prompt)
    elif PROVIDER == "groq":
        return _call_groq(system_prompt, user_prompt)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {PROVIDER}")

def _call_gemini(system_prompt, user_prompt):
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_prompt,
        generation_config={"temperature": TEMPERATURE, "max_output_tokens": MAX_TOKENS}
    )
    response = model.generate_content(user_prompt)
    return response.text

def _call_openai(system_prompt, user_prompt):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content

def _call_anthropic(system_prompt, user_prompt):
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text

def _call_groq(system_prompt, user_prompt):
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    model = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content
