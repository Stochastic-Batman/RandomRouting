import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# En -> Ka is opus-mt-synthetic-en-ka
supported_languages = ["en", "ru", "ka"]
from_lang = "ru"
to_lang = "ka"

tokenizer = AutoTokenizer.from_pretrained(f"Helsinki-NLP/opus-mt-{from_lang}-{to_lang}")
model = AutoModelForSeq2SeqLM.from_pretrained(f"Helsinki-NLP/opus-mt-{from_lang}-{to_lang}")

msg = "Как дела?"
msg = "Мы прико́льно отдохну́ли на да́че."
msg = "Он притвори́лся спя́щим."
msg = "How's it going?"
msg = "როგორ ხარ?"

inputs = tokenizer(msg, return_tensors="pt")
with torch.no_grad():
    outputs = model.generate(**inputs)


translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(translated_text)