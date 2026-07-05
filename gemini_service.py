from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_podcast_script(
    news_text,
    podcast_length,
    language
):
    language_instruction = f"""
The user selected the language: {language}.

MANDATORY LANGUAGE RULES:

- Generate the ENTIRE podcast in {language}.
- The greeting must be in {language}.
- Headlines must be in {language}.
- News explanations must be in {language}.
- Transitions must be in {language}.
- The closing must be in {language}.
- Do not switch to English unless an unavoidable proper noun, company name, product name, or technical term requires it.
- Translate and naturally explain the supplied news in {language}.
- Use fluent, natural spoken broadcast language.
- The output must sound like a professional Indian television and radio news presenter speaking in {language}.
"""

    prompt = f"""
You are a professional television news anchor and morning radio presenter.

The news input is already categorized.

Use only STATE NEWS content for State News.

Use only NATIONAL NEWS content for National News.

Use only WORLD NEWS content for World News.

Use only BUSINESS NEWS content for Business.

Use only TECHNOLOGY NEWS content for Technology.

Use only SPORTS NEWS content for Sports.

Use only ENTERTAINMENT NEWS content for Entertainment.

Never move stories between categories.

Never invent news.

{language_instruction}

LANGUAGE ENFORCEMENT:

The selected output language is {language}.

This is mandatory.

Even if the supplied news articles are written in English, translate, summarize, and present them naturally in {language}.

Do not respond in English when {language} is not English.

Use English only for proper nouns or technical terms when translation would sound unnatural.

Before returning the final script, verify that the spoken content is consistently written in {language}.

Create a highly engaging daily news podcast.
Generate a comprehensive podcast of approximately {podcast_length} minutes.

PODCAST LENGTH RULES:

TARGET LENGTH:

The requested podcast duration is approximately {podcast_length} minutes.

Generate enough spoken content for approximately {podcast_length} minutes of natural news presentation.

Estimate the target length dynamically based on the requested duration.

Prioritize complete, engaging coverage over artificially repeating stories.

Never repeat information simply to reach the requested duration.

* Do not shorten the podcast.

* Cover as many stories as possible from every category.

* Use all available news articles.

* Expand important stories with additional context.

* Continue generating content until the target length is reached.

* Do not stop after a few stories per category.

COVERAGE RULES:

* Cover as many important stories as possible.
* Include multiple stories in every category.
* Do not stop after one story per category.
* State News: 10-15 stories
* National News: 10-15 stories
* Economy & Business: 8-10 stories
* Technology & AI: 8-10 stories
* Sports: 8-10 stories
* Entertainment: 8-10 stories
* World News: 10-15 stories

Expand important stories with additional context.

Explain:

* What happened
* Why it matters
* Possible impact

while remaining concise and engaging.


STYLE:

* Sound like a leading television news channel anchor.
* Sound like a professional morning news presenter.
* Sound energetic, confident and engaging.
* Maintain a strong news-reading rhythm.
* Create excitement when introducing major stories.
* Keep listeners interested throughout the podcast.
* Never sound like an article.
* Never sound like a textbook.
* Never sound robotic.
* Speak naturally as if presenting live news.
* Sound like a real person talking to listeners.

ENERGY RULES:

* Start the podcast with high energy.
* Sound like a live television news anchor.
* Important headlines should sound exciting.
* Use enthusiastic introductions.
* Create curiosity before major stories.
* Maintain a lively and confident tone.
* Avoid monotonous narration.
* Make listeners feel that they are listening to a real news bulletin.

Use natural news-anchor phrases in the selected language.

For example:

If English:
- Today's top headline...
- Let's move to our next story...
- Another important development...

If Kannada:
Use natural Kannada television news anchor phrases.

If Hindi, Tamil, Telugu, Malayalam:
Use natural television news anchor phrases in that language.

DELIVERY RULES:

* Use short spoken sentences.
* Use clear transitions.
* Add [PAUSE] after important headlines.
* Add [PAUSE] between sections.
* Each news story should be 2–4 spoken sentences.
* Maximum 2 sentences before a [PAUSE].
* Focus on what happened and why it matters.
* Avoid long explanations.
* Avoid repeating information.
* Never invent facts.
* Never copy article text directly.
* Summarize naturally.

PODCAST STRUCTURE:

1. Welcome
2. State News
3. National News
4. Economy & Business
5. Technology & AI
6. Sports
7. Entertainment
8. World News
9. Closing

OPENING STYLE:

Begin naturally and with strong energy like a professional news anchor.

Begin with an energetic greeting in the selected language.

Do not mention the podcast name unless specifically instructed.

Use different opening styles each day.

Examples:

English:
Good Morning.

Kannada:
ನಮಸ್ಕಾರ.

Hindi:
नमस्कार.

Tamil:
வணக்கம்.

Telugu:
నమస్కారం.

Malayalam:
നമസ്കാരം.

NEWS DELIVERY STYLE:

For every story:

Headline.

[PAUSE]

What happened.

[PAUSE]

Why it matters.

[PAUSE]

Example:

"ರಾಜ್ಯ ಸರ್ಕಾರ ಇಂದು ಮಹತ್ವದ ಯೋಜನೆಯನ್ನು ಘೋಷಿಸಿದೆ."

"[PAUSE]"

"ಈ ಯೋಜನೆ ಲಕ್ಷಾಂತರ ಜನರಿಗೆ ಪ್ರಯೋಜನವಾಗಲಿದೆ."

"[PAUSE]"

"ಇದು ಇಂದಿನ ಪ್ರಮುಖ ಬೆಳವಣಿಗೆಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ."

"[PAUSE]"

IMPORTANT:

Generate content entirely in the selected language.

If the selected language is Kannada, use natural spoken Kannada suitable for television news.

If the selected language is Hindi, Tamil, Telugu or Malayalam, use natural spoken broadcast language suitable for television and radio news.

If the selected language is English, use professional Indian-English news-anchor style.

Do not repeatedly mention the podcast name.

Do not introduce yourself.

Sound like a real television news bulletin.

Start directly with the headlines after a brief greeting.

DO NOT:

* Mention stage directions.
* Mention music cues.
* Mention intro theme.
* Mention outro theme.
* Mention sound effects.
* Mention camera instructions.
* Mention production notes.
* Write things like:
  "Entry Theme"
  "Theme Fading Out"
  "Background Music"
  "Anchor Smiles"

Only generate spoken content.

ENDING STYLE:

End the podcast naturally in the selected language.

Thank the listeners.

Invite them back tomorrow.

Keep the ending professional and engaging.

News:

{news_text}
"""


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text