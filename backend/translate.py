import openai
import pandas as pd
import re

# LLM client
client = openai.OpenAI(
    base_url="http://192.168.1.121:1234/v1",
    api_key="lm-studio"
)

def contains_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+', text))

def translate_text(text: str) -> str:
    if not isinstance(text, str) or not text.strip() or not contains_arabic(text):
        return text

    prompt = f"""You are an expert Arabic to English translator.
Translate the following Arabic text into fluent English. Do not explain. Do not add any notes.
Only output the translated sentence.

Arabic: {text}
English:"""

    try:
        response = client.chat.completions.create(
            model="lm-studio",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        translation = response.choices[0].message.content.strip()
        print(f"\n🟡 Original: {text}\n🟢 Translated: {translation}")
        return f"Original: {text}\nTranslated: {translation}"
    except Exception as e:
        print(f"❌ Error translating: {e}")
        return text

def translate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    translated_df = df.copy()

    for row_idx in range(df.shape[0]):
        for col_idx in range(df.shape[1]):
            val = df.iat[row_idx, col_idx]
            if isinstance(val, str) and contains_arabic(val):
                translated_df.iat[row_idx, col_idx] = translate_text(val)

    return translated_df

def translate_workbook(sheet_dict: dict) -> dict:
    translated_sheets = {}

    for sheet_name, df in sheet_dict.items():
        translated_df = translate_dataframe(df)

        # Translate the sheet name if it contains Arabic
        if contains_arabic(sheet_name):
            translated_name_raw = translate_text(sheet_name)
            translated_name = translated_name_raw.replace("Original:", "").replace("Translated:", "").strip()
            print(f"📝 Sheet name translated: {sheet_name} → {translated_name}")
        else:
            translated_name = sheet_name

        # Excel sheet names have a 31-character limit and must not contain some characters
        translated_name = translated_name[:31].replace('/', '-').replace('\\', '-').replace('*', '-').replace('?', '-').replace('[', '(').replace(']', ')')

        translated_sheets[translated_name] = translated_df

    return translated_sheets
