# pip install --upgrade requests
# pip install requests[socks]
import json
import requests
from system import URL_API_GEMINI, DEFAULT_MODEL_GEMINI
from keys import ACCESS_ID, API_KEY, VALUE_KEY, PROXY_HTTP, PROXY_SOCKS5H



def ask_gemini(question: str, system_content: str, tools: str, tool_config: str) -> dict:

    """
    Отправляет запрос в Gemini API.
    Sends request to Gemini API.

    Args:
        question (str): Вопрос / User question
        system_content (str): Системный промпт / System prompt

    Returns:
        dict/bool: JSON ответ или False / JSON response or False
    """
    
    headers = {
        API_KEY: VALUE_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    data = {
        # Content-Type: multipart/form-data
        'access_id': (None, ACCESS_ID),
        'user_content': (None, question),
        'model': (None, DEFAULT_MODEL_GEMINI),
        'system_content': (None, system_content),
        'tools': (None, tools),
        'tool_config': (None, tool_config),
    }

    try:
        response = requests.post(
            URL_API_GEMINI,
            headers=headers,
            files=data,
            proxies=PROXY_SOCKS5H,
            timeout=200
        )

        response.raise_for_status()
        return response.json()
    
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Gemini API error: {e}")
        return False





























# print(ask_gemini("Привет как дела Вера?", "ты асистентка по имени Лера"))
# {'response': 'Привет! У меня все хорошо, спасибо, что спросил. Меня зовут Лера, а не Вера. Чем могу помочь?\n', 'expenses': 2.52e-05, 'used_tokens': 42}