import json



# GEMINI:


system_con_gen_text = """
    Задача:  
    Создай SEO-оптимизированный HTML-контент для страницы сайта. Выполняй следующие требования:

        1. Структура текста (в зависимости от типа страницы):  
            - Коммерческая (услуги, товары, лендинг): 500–1000 слов  
            - Информационная (блог, статья, гайд, обзор): 1000–2500 слов  
            - Новостная (анонс, короткая статья): 300–800 слов

        2. SEO-требования:  
            - Текст должен отвечать на основное намерение пользователя  
            - Собери релевантное семантическое ядро: ключевые слова (включая геозапросы, если применимо). Оформи в JSON, без дублей и нерелевантных слов  
            - Основное ключевое слово должно входить в ключевые фразы

        - Подготовь:
            - title — короткий, точный, SEO-оптимизированный заголовок (в JSON)  
            - description — мета-описание страницы по SEO-стандартам (в JSON)

        - Без спама, без слов типа «лучший», «надежный», «дешевый» и без обещаний  
        - Избегай «воды» — контент должен быть конкретным и полезным  
        - H1 обязателен — лаконичный, в тему  
        - Соблюдай SEO-структуру: заголовки h1–h3, логичная структура  
        - Укажи места для картинки и одного видео в тексте (в виде <img> и <video> с title и alt) — продумать контекст для мультимедиа

        3. Формат вывода:  
            - Основной текст — в HTML, только содержимое <body>, без <html>, <head> и стилей  
            - Ключевые слова, title и description — в JSON  
            - Не добавляй иконки, эмодзи и избыточное оформление

    Важно:  
    Придерживайся норм по SEO, структурной логики, релевантности и фактической пользы для пользователя.
"""


system_check = """
    Сделай ревью последнего написанного текста страницы сайта. Дай ответ True - текст удовлетворителен 
    или False - текст нужно переписать.
    Дай конкретные и точные недочеты и ошибки, что бы их возможно было исправить. Дай заметку что хорошо - оставить, 
    что поменять и только реалистичные задачи.
    Не придирайся по пустякам.
"""


gen_seo_text = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "На основе описания страницы сайта напиши SEO текст - seo_text, собери ключевые фразы -  keywords и напиши описание стриницы - description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "seo_text": {
                            "description": "Напиши SEO текст для страницы сайта",
                            "type": "string"
                        },
                        "keywords": {
                            "description": "Собери keywords связанные с основным запросом будущей страницы",
                            "type": "array", # list
                            "items": {
                                "type": "string"
                            }
                        },
                        "description": {
                            "description": "Сформируй описание страницы сайта для вставки в html страницы.",
                            "type": "string"
                        },
                        "title": {
                            "description": "Сформируй title страницы сайта для вставки в html страницы.",
                            "type": "string"
                        }
                    },
                    "required": ["seo_text", "keywords", "description", "title"]
                }
            },
         ]
    }
], ensure_ascii=False)

checking = json.dumps([
    {
        "function_declarations": [
            {
                "name": "mainset",
                "description": "Проверь последнюю версию SEO текста, keywords, description от assistant_1 и дай ответ в булевом варианте. Дай пояснения своего решения.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "acceptance": {
                            "description": "Дай ответ в boolean. True - если текст удовлетверителен и в целом нет ошибок. False - если есть ошибки и текст нужно переписать.",
                            "type": "boolean"
                        },
                        "annotation": {
                            "description": "Если есть замечания или серьезные проблемы с текстом, то дай тут поясниения и опиши как это исправить и что нужно изменить.",
                            "type": "string"
                        }
                    },
                    "required": ["acceptance", "annotation"]
                }
            },
         ]
    }
], ensure_ascii=False)

# tools_3 = json.dumps([
#     {
#         "function_declarations": [
#             {
#                 "name": "mainset",
#                 "description": "На основе данных определи и собери подходящие данные. Json. Ответ должен быть четким, структурированным и без лишней информации",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "goals": {
#                             "description": "Угадай, что хочет получить посетитель этой страницы. Какая у него цель?",
#                             "type": "string"
#                         },
#                         "fears": {
#                             "description": "Выяви его скрытые страхи и сомнения, которые мотивируют поиск. Перечисли по важности.",
#                             "type": "string"
#                         },
#                         "benefit": {
#                             "description": "Предложи способы воздействия через контент, чтобы снять сомнения и повысить конверсию.",
#                             "type": "string"
#                         }
#                     },
#                     "required": ["goals", "fears", "benefit"]
#                 }
#             },
#          ]
#     }
# ])


# tools_4 = json.dumps([
#     {
#         "function_declarations": [
#             {
#                 "name": "mainset",
#                 "description": "Собери ключевые слова будущей страницы в json. Только важные и связанные прямо со страницей. Ответ должен быть четким, структурированным и без лишней информации",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "keywords": {
#                             "description": "Собери keywords связанные с основным запросом будущей страницы",
#                             "type": "array", # list
#                             "items": {
#                                 "type": "string"
#                             }
#                         }
#                     },
#                     "required": ["keywords"]
#                 }
#             },
#          ]
#     }
# ])


# tools_5 = json.dumps([
#     {
#         "function_declarations": [
#             {
#                 "name": "mainset",
#                 "description": "Рекомендации и структурный план страницы сайта на основе полученных данных. Json. Ответ должен быть четким, структурированным и без лишней информации",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "plan_main": {
#                             "description": "Описание общего плана страницы сайта. Текст, заголовки, ссылки, скидки, адреса, фото, видео, подробности и рекомендации.",
#                             "type": "string"
#                         },
#                         "plan_text": {
#                             "description": "План текста по пунктам. Конкретный и логичный.",
#                             "type": "string"
#                         },
#                         "plan_href": {
#                             "description": "План/рекомендации контекстных гиперссылок",
#                             "type": "string"
#                         },
#                         "plan_ui": {
#                             "description": "План лучшего расположения элементов  и UI страницы",
#                             "type": "string"
#                         },
#                         "plan_media": {
#                             "description": "План и рекомендации картинок и видеороликов на старнице сайта",
#                             "type": "string"
#                         }
#                     },
#                     "required": ["plan_main", "plan_text", "plan_href", "plan_ui", "plan_media"]
#                 }
#             },
#          ]
#     }
# ])






# tools_6 = json.dumps([
#     {
#         "function_declarations": [
#             {
#                 "name": "mainset",
#                 "description": "Написать текст для страницы. Json.",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "main_content": {
#                             "description": "Напиши SEO текст по вводным параметрам.",
#                             "type": "string"
#                         },
#                         "description": {
#                             "description": "Напиши description для html страницы сайта",
#                             "type": "string"
#                         },
#                         "title": {
#                             "description": "Напиши title для html страницы сайта.",
#                             "type": "string"
#                         }
#                     },
#                     "required": ["main_content", "description", "title"]
#                 }
#             },
#          ]
#     }
# ])


tool_config_any = json.dumps({
    "function_calling_config": {
        "mode": "ANY"   # AUTO - может запустить функцию или ответить текстом (по умолчанию), ANY или ONE - принудительно вызовет, в любом случае, NONE - игнор, только текстом
    }
})




# DEEPSEEK:

#