import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, MarianTokenizer, MarianMTModel
from typing import Union


def create_models(lang_hotel: str = "ka", lang_guest: str = "en") -> Union[tuple[tuple[AutoTokenizer, AutoModelForSeq2SeqLM], tuple[AutoTokenizer, AutoModelForSeq2SeqLM]], str]:
    supported_language_pairs: list[tuple[str, str]] = [("en", "ka"), ("ka", "en"), ("en", "ru"), ("ru", "en")]
    if (lang_hotel, lang_guest) not in supported_language_pairs:
        return "<unsupported_language_pair>"

    # for translation to Georgian, only English to Georgian model exists and only that model name contains "synthetic": opus-mt-synthetic-en-ka
    model_name_h2g = f"Helsinki-NLP/opus-mt-{"synthetic-en" if lang_guest == "ka" else lang_hotel}-{lang_guest}"
    model_name_g2h = f"Helsinki-NLP/opus-mt-{"synthetic-en" if lang_hotel == "ka" else lang_guest}-{lang_hotel}"

    tokenizer_hotel = AutoTokenizer.from_pretrained(model_name_h2g)
    model_hotel = AutoModelForSeq2SeqLM.from_pretrained(model_name_h2g)

    tokenizer_guest = AutoTokenizer.from_pretrained(model_name_g2h)
    model_guest = AutoModelForSeq2SeqLM.from_pretrained(model_name_g2h)

    return (tokenizer_hotel, model_hotel), (tokenizer_guest, model_guest)


def translate(msg: str, tokenizer: MarianTokenizer, model: MarianMTModel) -> str:
    inputs = tokenizer(msg, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs)

    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translated_text