import openai
import pandas as pd
import re

# LLM client
client = openai.OpenAI(
    base_url="http://192.168.1.1:1234/v1",
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
        return translation

    except Exception as e:
        print(f"❌ Error translating: {e}")
        return text

def translate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    translated_df = df.copy()
    original_columns = list(df.columns)

    for col_idx, col in enumerate(original_columns):
        col_str = str(col) if col is not None else f"col_{col_idx}"
        translated_col = f"{col_str}_translated"

        if translated_col in translated_df.columns:
            print(f"⚠️ Column '{translated_col}' already exists. Skipping.")
            continue

        translated_values = []
        needs_translation = False

        for val in df[col]:
            if isinstance(val, str) and contains_arabic(val):
                translation = translate_text(val)
                translated_values.append(translation)
                needs_translation = True
            else:
                translated_values.append(None)

        if needs_translation:
            print(f"📝 Inserting translated column after '{col_str}'")
            print(f"✅ Column '{translated_col}' will contain {sum(v is not None for v in translated_values)} translated cells.")

            try:
                insert_position = translated_df.columns.get_loc(col) + 1
                translated_df.insert(insert_position, translated_col, translated_values)
            except Exception as e:
                print(f"❌ Failed to insert column after '{col}': {e}")
                continue

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
