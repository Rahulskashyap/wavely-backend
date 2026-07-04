import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_highlights(news_text):
    prompt = f"""
You are an AI news editor.

From the following news, generate exactly 5 short bullet point highlights.

Rules:
- Maximum 15 words each.
- No numbering.
- No markdown.
- Keep them engaging.
- Use the same language as the news text.

News:

{news_text}
"""

    response = model.generate_content(prompt)

    highlights = []

    for line in response.text.split("\n"):
        line = line.strip()

        line = line.lstrip("-•* ").strip()
        if line:
            highlights.append(line)

    return highlights[:5]