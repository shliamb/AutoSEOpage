import json



# GEMINI:
tools_1 = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "На основе описания страницы сайта определи и собери подходящие данные целевой аудитории в json. Ответ должен быть четким, структурированным и без лишней информации",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "demographics": {
                            "description": "Проанализируй и внеси демографические данные",
                            "type": "string"
                        },
                        "anger": {
                            "description": "Проанализируй и внеси возможные раздражающие факторы аудитории",
                            "type": "string"
                        }
                    },
                    "required": ["demographics", "anger"]
                }
            },
         ]
    }
])

tools_2 = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "На основе описания страницы сайта определи и собери подходящие данные. Json. Ответ должен быть четким, структурированным и без лишней информации",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type_page": {
                            "description": "Определи тип страницы: коммерческая страница, информационная, новостная",
                            "type": "string"
                        },
                        "funnel_stage": {
                            "description": "Укажи стадию воронки: ознакомление, сравнение, конверсия, удержание",
                            "type": "string"
                        },
                        "main_goal": {
                            "description": "Сформулируй основную цель: информировать, убедить, продать, развлечь",
                            "type": "string"
                        },
                        "focus": {
                            "description": "Выдели ключевую тему/фокус одним предложением",
                            "type": "string"
                        }
                    },
                    "required": ["type_page", "funnel_stage", "main_goal", "focus"]
                }
            },
         ]
    }
])

tools_3 = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "На основе данных определи и собери подходящие данные. Json. Ответ должен быть четким, структурированным и без лишней информации",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "goals": {
                            "description": "Угадай, что хочет получить посетитель этой страницы. Какая у него цель?",
                            "type": "string"
                        },
                        "fears": {
                            "description": "Выяви его скрытые страхи и сомнения, которые мотивируют поиск. Перечисли по важности.",
                            "type": "string"
                        },
                        "benefit": {
                            "description": "Предложи способы воздействия через контент, чтобы снять сомнения и повысить конверсию.",
                            "type": "string"
                        }
                    },
                    "required": ["goals", "fears", "benefit"]
                }
            },
         ]
    }
])


tools_4 = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "Собери ключевые слова будущей страницы в json. Только важные и связанные прямо со страницей. Ответ должен быть четким, структурированным и без лишней информации",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "description": "Собери keywords связанные с основным запросом будущей страницы",
                            "type": "array", # list
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["keywords"]
                }
            },
         ]
    }
])


tools_5 = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "Рекомендации и структурный план страницы сайта на основе полученных данных. Json. Ответ должен быть четким, структурированным и без лишней информации",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plan_main": {
                            "description": "Описание общего плана страницы сайта. Текст, заголовки, ссылки, скидки, адреса, фото, видео, подробности и рекомендации.",
                            "type": "string"
                        },
                        "plan_text": {
                            "description": "План текста по пунктам. Конкретный и логичный.",
                            "type": "string"
                        },
                        "plan_href": {
                            "description": "План/рекомендации контекстных гиперссылок",
                            "type": "string"
                        },
                        "plan_ui": {
                            "description": "План лучшего расположения элементов  и UI страницы",
                            "type": "string"
                        },
                        "plan_media": {
                            "description": "План и рекомендации картинок и видеороликов на старнице сайта",
                            "type": "string"
                        }
                    },
                    "required": ["plan_main", "plan_text", "plan_href", "plan_ui", "plan_media"]
                }
            },
         ]
    }
])


tools_6 = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "Выбрать основную манеру общения с аудиторией. Json. Ответ должен быть четким, структурированным и без лишней информации",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ton": {
                            "description": "Определение тональности и стиля коммуникации бренда для сайта",
                            "type": "string"
                        }
                    },
                    "required": ["ton"]
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