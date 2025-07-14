from keys import HOST



URL_API_GEMINI = f"http://{HOST}/api/gemini/"
DEFAULT_MODEL_GEMINI = "gemini-2.5-flash"  # gemini-2.5-flash   gemini-2.0-flash


MAX_ITERATIONS = 2 # Сколько раз переписывать текст разрешено
OUTPUT_FORMAT = "MARKDOWN" #"в HTML, только содержимое <body>, без <html>, <head> и стилей " # MARKDOWN  Просто текст
