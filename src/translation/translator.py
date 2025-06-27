from transformers import pipeline

# Charge une seule fois le modèle de traduction
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")

def translate_caption(caption: str) -> str:
    result = translator(caption, max_length=60)
    return result[0]["translation_text"]