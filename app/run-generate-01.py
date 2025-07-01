import json
from mod_gemini import ask_gemini


print("SYSTEM: Входные данные о желаемой странице (все ньюансы, чем больше тем лучше, цены, услуги или тематика):\n")
intro_data = input()
system_content = None #"""

#     Определи:
#     1.  Тема.
#     2.  Интент (commercial / informational / news / etc.).
#     3.  Цель страницы (продать / информировать / убедить / научить).
#     4.  Тактика письма (показать экономию / создать интригу / доказать экспертность).
#     5.  Тон (деловой / дружелюбный / срочный).

# """


tools = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "Собрать подходящие данные и вернуть в json.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "description": "Определить тему контента для страницы сайта",
                            "type": "string"
                        },
                        "intent": {
                            "description": "Определить тип сайта по контенту - комерческий, информационный, новостной (commercial / informational / news)",
                            "type": "string"
                        },
                        "goals": {
                            "description": "Определить цель повествования, что ожидается от читающего контент (sell / inform / convince / teach)",
                            "type": "string"
                        }
                    },
                    "required": ["topic", "intent", "goals"]
                }
            },
         ]
    }
])


tool_config = json.dumps({
    "function_calling_config": {
        "mode": "ANY"   # AUTO - может запустить функцию или ответить текстом (по умолчанию), ANY или ONE - принудительно вызовет, в любом случае, NONE - игнор, только текстом
    }
})


answer = ask_gemini(intro_data, system_content, tools, tool_config)
print("\n", answer) # answer["response"]


#автомастерская, низкие цены, тюниг, 2 мастера русские