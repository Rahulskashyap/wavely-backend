from preferences import load_preferences


def get_language_prompt():

    prefs = load_preferences()

    language = prefs["preferences"]["language"]

    prompts = {
        "English": "Generate the podcast in English.",
        "Hindi": "Generate the podcast in Hindi.",
        "Kannada": "Generate the podcast in Kannada.",
        "Tamil": "Generate the podcast in Tamil.",
        "Telugu": "Generate the podcast in Telugu.",
        "Malayalam": "Generate the podcast in Malayalam.",
        "Marathi": "Generate the podcast in Marathi.",
        "Gujarati": "Generate the podcast in Gujarati.",
        "Bengali": "Generate the podcast in Bengali.",
        "Punjabi": "Generate the podcast in Punjabi.",
        "Odia": "Generate the podcast in Odia.",
        "Urdu": "Generate the podcast in Urdu."
    }

    return prompts.get(language, "Generate the podcast in English.")