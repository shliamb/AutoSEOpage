from keys import HOST


# General:
MAX_ITERATIONS = 2 # Сколько раз переписывать текст разрешено
OUTPUT_FORMAT = "в текст без оформления вообще" #"в HTML, только содержимое <body>, без <html>, <head> и стилей " # MARKDOWN  Просто текст

# Gemini:
URL_API_GEMINI = f"http://{HOST}/api/gemini/"
DEFAULT_MODEL_GEMINI = "gemini-2.0-flash"  # gemini-2.5-flash   gemini-2.0-flash

# Folders:
INPUT = "./input/"
OUTPUT = "./output/"