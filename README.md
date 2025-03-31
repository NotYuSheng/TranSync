# 📄 Arabic-to-English XLSX Translator

A tool for batch-translating `.xlsx` spreadsheets from **Arabic to English** using a locally hosted LLM in **LM Studio**. It supports:

- ✅ Multi-sheet Excel files
- ✅ Cell-by-cell translation (only if Arabic is detected)
- ✅ Original formatting preserved (fonts, borders, colors, etc.)
- ✅ Translated sheet names
- ✅ Streamlit frontend for file uploads + downloads
- ✅ FastAPI backend for processing logic

---

## 🚀 Features

- Upload and translate multiple `.xlsx` files at once
- Only cells with Arabic text are translated
- Translated cells are formatted as:
  ```
  Original: [Arabic]
  Translated: [English]
  ```
- Preserves original Excel formatting using `openpyxl`
- Works entirely offline using [LM Studio](https://lmstudio.ai/)
- Easy to use via web UI or API

---

## 📆 Tech Stack

- **Python 3.10**
- **FastAPI** — backend API
- **Streamlit** — frontend UI
- **OpenAI SDK** — calls LM Studio over OpenAI-compatible API
- **openpyxl** — for cell-wise translation with formatting
- **Docker + Docker Compose** — for full containerization

---

## 🧑‍💻 Setup

### 1. Prerequisites

- [Docker](https://www.docker.com/)
- [LM Studio](https://lmstudio.ai/) running with a supported LLM (e.g., `Nous-Hermes-2-Mistral-7B-DPO-GGUF`)

> LM Studio must be running at `http://192.168.1.121:1234` (or update the URL in `translate.py`)

---

### 2. Clone the repo

```bash
git clone https://github.com/notyusheng/xlsx-translate.git
cd xlsx-translate
```

---

### 3. Start the app

```bash
docker compose up --build
```

- Streamlit UI: [http://localhost:8501](http://localhost:8501)
- FastAPI backend: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🗀️ Using the App

1. Open the Streamlit UI in your browser.
2. Upload one or more `.xlsx` files.
3. Click **Translate**.
4. Download the translated files with formatting and cell structure preserved.

---

## 🧠 How It Works

- Files are uploaded to the FastAPI backend
- Each `.xlsx` workbook is loaded via `openpyxl`
- The app:
  - Loops through each sheet
  - Translates Arabic cells using a local LLM
  - Translates sheet names if in Arabic
  - Writes values back to the workbook **without altering formatting**
- Files are returned for download via the frontend

---

## 💠 Customize

### Change LLM endpoint

Edit this line in `translate.py`:

```python
client = openai.OpenAI(
    base_url="http://192.168.1.121:1234/v1",
    api_key="lm-studio"
)
```

---

## 📂
