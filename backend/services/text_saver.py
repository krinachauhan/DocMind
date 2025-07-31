import os

TEXT_OUTPUT_FOLDER = "data/text"

def save_text_to_file(file_id: str, text: str) -> str:
    os.makedirs(TEXT_OUTPUT_FOLDER, exist_ok=True)
    path = os.path.join(TEXT_OUTPUT_FOLDER, f"{file_id}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path
