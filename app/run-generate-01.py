import json
from mod_gemini import ask_gemini


print("SYSTEM: Входные данные о желаемой странице (все ньюансы, чем больше тем лучше, цены, услуги или тематика):\n")
intro_data = input()
system_content = """

    Определи:
    1.  Тема.
    2.  Интент (commercial / informational / news / etc.).
    3.  Цель страницы (продать / информировать / убедить / научить).
    4.  Тактика письма (показать экономию / создать интригу / доказать экспертность).
    5.  Тон (деловой / дружелюбный / срочный).

"""

# 1
response_type = {"type": "text"}


# 2
response_type = json.dumps({
    "type": "json_schema",
    "json_schema": {
        "name": "mainset",
        "schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "description": "the theme of the future site page",
                    "type": "string"
                },
                "intent": {
                    "description": "commercial / informational / news / etc.",
                    "type": "string"
                },
                "goals": {
                    "description": "page objectives (sell / inform / convince / teach)",
                    "type": "string"
                }
            },
            "required": ["topic", "intent", "goals"]
        }
    }
})



answer = ask_gemini(intro_data, system_content, response_type)
print("\nAI:", answer["response"])