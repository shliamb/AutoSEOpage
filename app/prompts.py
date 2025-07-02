import json


# GEMINI:
tools_first = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "Собрать подходящие данные и вернуть в json. Без доболнительного форматирования, ничего лишнего. Никакой воды.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tema": {
                            "description": "Классифицируй страницу сайта по теме: search_engines, social_media, \
                                            e-commerce, news_media, entertainment, education, forums_communities, blogs, \
                                            business_corporate, government_non-profit, tools_utilities, gaming, adult_content, health_medical, travel_tourism",
                            "type": "string"
                        },
                        "type": {
                            "description": "Классифицируй страницу сайта по типу: commercial, informational, news, social_media, entertainment, educational, forums, tools",
                            "type": "string"
                        },
                        "attention": {
                            "description": "Опиши лучшие варианты удержания внимания на сайте читающего, не банальные и не нужно банальщины. Постарайся угадать что хочет читающий по данному вопросу.",
                            "type": "string"
                        },
                        "compressed": {
                            "description": "Конретизируй переданное описания желаемой страницы сайта в пункты, выдели важное. Подчеркни - плюсы и минусы.",
                            "type": "string"
                        }
                    },
                    "required": ["tema", "type", "attention", "compressed"]
                }
            },
         ]
    }
])

tool_config_any = json.dumps({
    "function_calling_config": {
        "mode": "ANY"   # AUTO - может запустить функцию или ответить текстом (по умолчанию), ANY или ONE - принудительно вызовет, в любом случае, NONE - игнор, только текстом
    }
})




# DEEPSEEK:

#