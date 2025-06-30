# pip install --upgrade requests
# pip install requests[socks]
import requests
from system import URL_API_GEMINI, DEFAULT_MODEL_GEMINI
from keys import ACCESS_ID, API_KEY, VALUE_KEY, PROXY_HTTP, PROXY_SOCKS5H



def ask_gemini(question: str, system_content: str) -> dict:

    """
    Sends a prompt to the Gemini AI API and returns the response.
    
    This function constructs a properly formatted request to the Gemini API endpoint,
    including necessary headers and payload data. It handles both successful responses
    and potential errors during the API communication.

    Args:
        question (str): The user's query or prompt to send to Gemini
        system_content (str): System instructions/context for the AI model

    Returns:
        dict: Parsed JSON response from Gemini API on success
        bool: False if the request fails or encounters an error

    Raises:
        Prints error message to console but doesn't raise exceptions to caller

    Example:
        >>> response = ask_gemini("Explain quantum computing", "You are a physics professor")
        >>> if response:
        ...     print(response['response'])
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
    }

    try:
        response = requests.post(
            URL_API_GEMINI,
            headers=headers,
            files=data,
            proxies=PROXY_SOCKS5H,
            timeout=200
        )

        # Check for HTTP errors
        response.raise_for_status()
        
        # Attempt to parse JSON response
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Gemini API request failed: {str(e)}")
        return False
    
    except ValueError as e:
        print(f"Failed to parse Gemini response: {str(e)}")
        return False





# print(ask_gemini("Привет как дела Вера?", "ты асистентка по имени Лера"))
# {'response': 'Привет! У меня все хорошо, спасибо, что спросил. Меня зовут Лера, а не Вера. Чем могу помочь?\n', 'expenses': 2.52e-05, 'used_tokens': 42}