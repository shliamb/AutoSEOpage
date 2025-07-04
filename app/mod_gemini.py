# pip install --upgrade requests
# pip install requests[socks]
# import json
import requests
from config import URL_API_GEMINI, DEFAULT_MODEL_GEMINI
from keys import ACCESS_ID, API_KEY, VALUE_KEY, PROXY_HTTP, PROXY_SOCKS5H
from prompts import tools_1, tools_2, tools_3, tools_4, tools_5, tools_6, tool_config_any



class Gemini:
    def __init__(self):
        """Инициализация Gemini клиента."""

    # The Main Query to Google / Основной запрос к API и к Google:
    def ask_gemini(self, question: str, system_content: str, tools: str = None, tool_config: str = None) -> dict:

        """
        RU: Основной запрос API к Google через сторонний API Telegramm -> @myapi_aibot (для стран под санкциями)

        EN: The main API request to Google is via a third-party Telegram API -> @myapi_aimbot (for countries under sanctions)
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

    # 1: Compression raw data / Сжатие сырых данных:
    def gemi_0(self, question: str, system_content: str) -> dict:
        return self.ask_gemini(question, system_content)

    # 2: The target audience / Определение аудитории :
    def gemi_1(self, question: str, system_content: str) -> dict:
        return self.ask_gemini(question, system_content, tools_1, tool_config_any)

    # 3. Get Type Page / Тип страницы:
    def gemi_2(self, question: str, system_content: str) -> dict:
        return self.ask_gemini(question, system_content, tools_2, tool_config_any)
    

    # Анализ контекста и конкурентов, API поисковиков  - позже
    # Задача: Изучить топ-5 конкурентов, их сильные/слабые стороны.
    # Пример для ИИ:
    # "Проанализируй тексты конкурентов по запросу 'доставка здорового питания Москва'. Какие выгоды они выделяют (экономия времени, пп-меню)? Какие возражения не закрывают (цена, вкус)?"


    # Цель читающего, что он хочет:
    def gemi_3(self, question: str):
        system_content = """
            На основе данных определи следующие пункты: 
            1. Определи что хочет получить пользователь на этой странице, какова его цель
            2. Выяви его скрытые страхи и возражения, конкретные примеры страхов для темы которые могут влиять на его решения и действия
            3. Предложи варианты, как превратить эти страхи в выгоды в тексте, что бы дать ему то чего он хочет
            Отвечай кратко, без лишних объяснений.
        """
        return self.ask_gemini(question, system_content, tools_3, tool_config_any)


    # Сбор ключевых слов (SEO-ядро)::
    def gemi_4(self, question: str):
        system_content = (
            "Сбор ключевых слов (SEO-ядро):"
            "Определи основные ключевые запросы для страницы (включая высоко- и низкочастотные)."
            "Добавь длинные хвосты (long-tail) — более конкретные и менее конкурентные фразы."
            #"Учитывай разные интенты пользователей (например: «купить», «сравнить», «как сделать», «отзывы»)."
            "Приоритет гео-запросам в коммерческих и новостных сайтах: если есть адрес/город — делай ответ максимально конкретным, с привязкой к локации."
            "Держи список четким: только релевантные слова без дублей и мусора."
        )
        return self.ask_gemini(question, system_content, tools_4, tool_config_any)
    

    # Разработка плана/сценария + CTA:
    def gemi_5(self, question: str):
        system_content = """
            Разработка плана/сценария + CTA:
            Создай четкую структуру с вовлекающим началом и логичным развитием.
            Захвати внимание: используй сильный крючок (интрига, вопрос, неожиданный факт или эмоциональный образ).
            Развивай логику: проблема → решение → выгоды (можно через сторителлинг, данные или экспертные мнения).
            Добавь доказательства: реальные примеры, кейсы, цитаты или статистику для доверия.
            Включи 3 варианта CTA (основной, альтернативный, срочный) – например:
            Основной: «Скачать инструкцию сейчас»
            Альтернативный: «Подписаться на обновления»
            Срочный: «Зарегистрируйтесь до [дата], чтобы получить бонус».
            Без воды: только конкретика, понятные шаги и выгоды для читателя.
        """
        return self.ask_gemini(question, system_content, tools_5, tool_config_any)
    

    # Определение тональности и стиля коммуникации бренда для сайта:
    def gemi_6(self, question: str):
        system_content = """
            Выбрать основную манеру общения с аудиторией (экспертная, дружелюбная, официальная, вдохновляющая, нейтральная и т. д.) с учетом специфики бизнеса/ресурса и целевой аудитории.
            Ключевые аспекты:
            Уровень формальности (строгий/непринужденный)
            Эмоциональная окраска (теплый/сдержанный/мотивирующий)
            Степень экспертности (простое объяснение/узкоспециализированные термины)
        """
        return self.ask_gemini(question, system_content, tools_6, tool_config_any)





















# print(ask_gemini("Привет как дела Вера?", "ты асистентка по имени Лера"))
# {'response': 'Привет! У меня все хорошо, спасибо, что спросил. Меня зовут Лера, а не Вера. Чем могу помочь?\n', 'expenses': 2.52e-05, 'used_tokens': 42}