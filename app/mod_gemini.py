# pip install --upgrade requests
# pip install requests[socks]

# import json
import requests
from config import URL_API_GEMINI, DEFAULT_MODEL_GEMINI
from keys import ACCESS_ID, API_KEY, VALUE_KEY, PROXY_HTTP, PROXY_SOCKS5H
from common import DictObj



# The Main Query to Google / Основной запрос к API и к Google:
def ask_gemini(request_data: dict) -> dict:

    """
    RU: Основной запрос API к Google через сторонний API Telegramm -> @myapi_aibot (для стран под санкциями)

    EN: The main API request to Google is via a third-party Telegram API -> @myapi_aimbot (for countries under sanctions)
    """

    dict_des = DictObj(request_data)
    question = dict_des.question
    system_content = dict_des.system_content or None
    tools = dict_des.tools or None
    tool_config = dict_des.tool_config or None
    model = dict_des.model or None
    dialog = dict_des.dialog or None

    headers = {
        API_KEY: VALUE_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    data = {
        # Content-Type: multipart/form-data
        'access_id': (None, ACCESS_ID),
        'user_content': (None, question),
        'model': (None, model or DEFAULT_MODEL_GEMINI),
        'system_content': (None, system_content),
        'tools': (None, tools),
        'tool_config': (None, tool_config),
        'assist_content': (None, dialog)
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


































    # # 0: Compression Raw Data / Сжатие сырых данных:
    # def gemi_0(self, request_data: dict) -> dict:
    #     return self.ask_gemini(question, system_content, model)

    # # 1: The Target Audience / Определение аудитории :
    # def gemi_1(self, question: str, system_content: str, model: str = None, dialog: str = None) -> dict:
    #     return self.ask_gemini(question, system_content, tools_1, tool_config_any, model)

    # # 2. Get Type Page / Тип страницы:
    # def gemi_2(self, question: str, system_content: str, model: str = None, dialog: str = None) -> dict:
    #     return self.ask_gemini(question, system_content, tools_2, tool_config_any, model)
    

    # """
    #     Анализ контекста и конкурентов, API поисковиков  - позже, подвопросом !!!!
    #     Задача: Изучить топ-5 конкурентов, их сильные/слабые стороны.
    #     Пример для ИИ:
    #     "Проанализируй тексты конкурентов по запросу 'доставка здорового питания Москва'. Какие выгоды они выделяют (экономия времени, пп-меню)? Какие возражения не закрывают (цена, вкус)?"
    # """


    # # 3. Get User's Goals / Цели пользователя:
    # def gemi_3(self, question: str, system_content: str, model: str = None, dialog: str = None) -> dict:
    #     return self.ask_gemini(question, system_content, tools_3, tool_config_any, model)

    # # 4. Keyword Collection / Сбор ключевых слов:
    # def gemi_4(self, question: str, system_content: str, model: str = None, dialog: str = None) -> dict:
    #     return self.ask_gemini(question, system_content, tools_4, tool_config_any, model)
    
    # # 5. Developing a plan / Разработка плана:
    # def gemi_5(self, question: str, system_content: str, model: str = None, dialog: str = None) -> dict:
    #     return self.ask_gemini(question, system_content, tools_5, tool_config_any, model)
    

    # # # Определение тональности и стиля коммуникации бренда для сайта:
    # # def gemi_6(self, question: str):
    # #     system_content = """
    # #         Выбрать основную манеру общения с аудиторией (экспертная, дружелюбная, официальная, вдохновляющая, нейтральная и т. д.) с учетом специфики бизнеса/ресурса и целевой аудитории.
    # #         Ключевые аспекты:
    # #         Уровень формальности (строгий/непринужденный)
    # #         Эмоциональная окраска (теплый/сдержанный/мотивирующий)
    # #         Степень экспертности (простое объяснение/узкоспециализированные термины)
    # #     """
    # #     return self.ask_gemini(question, system_content, tools_6, tool_config_any)



    # # 6. Writing a text / Написание текста:
    # def gemi_6(self, question: str, system_content: str, model: str = None, dialog: str = None) -> dict:
    #     return self.ask_gemini(question, system_content, tools_6, tool_config_any, model)




# 8. Проверка на ИИ-генерацию и исправление паттернов
# Задача: Убрать шаблонность, воду, неестественные обороты.
# Примеры для ИИ:

# "Общие фразы → Конкретика"

# Было: "Наш сервис предлагает высококачественные решения"

# Стало: "Чиним iPhone с гарантией 1 год — заменим экран за 30 минут"

# "ИИ-штампы → Естественность"

# Было: "В современном мире важно выбирать надежных партнеров"

# Стало: "92% клиентов возвращаются к нам — потому что даем честные сроки ремонта"

# "Вода → Факты"

# Было: "Мы используем инновационные технологии"

# Стало: "Применяем пайку BGA для ремонта видеокарт — это снижает риск перегрева на 40%."

# "Роботизированные CTA → Персонализация"

# Было: "Оставьте заявку на нашем сайте"

# Стало: "Закажите бесплатный выезд мастера — он диагностирует поломку за 10 минут и назовет цену до начала работ"

# Промпт для проверки:
# "Проанализируй этот текст на признаки ИИ-генерации: общие фразы, отсутствие конкретики, неестественные связки. Перепиши, добавив цифры, уникальные детали и разговорные элементы, как будто текст писал эксперт."


# 9. Комплексная проверка по чек-листу
# Пример для ИИ:
# *"Проверь текст по критериям:

# Есть ли H1, H2-H4 с ключами?

# Решены ли боли ЦА (п.3)?

# Нет ли штампов из п.8?

# CTA ведут к действию?

# Упомянуты ли УТП и возражения?"*


# 10. Результат
# Готовая страница, которая:

# Ранжируется в SEO.

# Увлекает и продает.

# Не выглядит как ИИ-генерация.

# Финал:
# *"Доработай текст, чтобы он звучал как написанный человеком-экспертом: добавь личный опыт ('Мы 10 лет чиним MacBook'), живые примеры ('Клиент Сергей сэкономил 15 000 руб, обратившись сразу к нам'), и сократи общие фразы."*

# Этот промпт дает ИИ четкие инструкции на каждом этапе, минимизируя "роботизированность" и усиливая продающую силу.





# print(ask_gemini("Привет как дела Вера?", "ты асистентка по имени Лера"))
# {'response': 'Привет! У меня все хорошо, спасибо, что спросил. Меня зовут Лера, а не Вера. Чем могу помочь?\n', 'expenses': 2.52e-05, 'used_tokens': 42}