from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from io import BytesIO
import pandas as pd
import os
from translate import translate_workbook

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate-xlsx/")
async def translate_multiple_xlsx(files: List[UploadFile] = File(...)):
    output_paths = []

    for file in files:
        try:
            if not file.filename.endswith(".xlsx"):
                print(f"⏭️ Skipped non-xlsx file: {file.filename}")
                continue

            contents = await file.read()
            excel_file = BytesIO(contents)

            # Read all sheets
            sheet_dict = pd.read_excel(excel_file, engine="openpyxl", sheet_name=None, header=None)

            print(f"📄 Loaded workbook: {file.filename} with {len(sheet_dict)} sheet(s)")
            translated_dict = translate_workbook(sheet_dict)

            output_dir = "./data/output"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, file.filename.replace(".xlsx", "_translated.xlsx"))

            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for sheet_name, df in translated_dict.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

            print(f"✅ Saved translated file: {output_path}")
            output_paths.append({
                "original_filename": file.filename,
                "translated_filename": os.path.basename(output_path)
            })

        except Exception as e:
            print(f"❌ Error processing {file.filename}: {e}")

    return {"results": output_paths}
