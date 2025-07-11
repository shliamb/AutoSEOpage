import json
import logging
logging.basicConfig(level=logging.INFO)
from mod_gemini import ask_gemini
from common import DictObj
from prompts import tool_config_any, gen_seo_text, system_check, system_con_gen_text, checking



# For Testing app data  Printing Information in Terminal:
# Удалить это гавно позже, когда видеть процесс уже не нужно будет
def out_info(data, who: str = None):
    in_who = f"{who}: " if who else ""

    if isinstance(data, dict):
        for key, value in data.items():
            logging.info(f"\n{key}: {value}")

    elif isinstance(data, list):
        logging.info(f"\n{in_who}{data}")

    elif isinstance(data, str):
        logging.info(f"\n{in_who}{data}")



# Saving Tokens and total cost:
def tok_cost(current_tokens: int, current_cost: float, answer: dict):

    if not isinstance(answer, dict):
        raise TypeError("Response must be a dictionary")

    try:
        tokens_used = answer["used_tokens"]
        expenses = answer["expenses"]
        
        if not isinstance(tokens_used, (int, float)) or not isinstance(expenses, (int, float)):
            raise TypeError("Token and expense values must be numeric")
            
        return current_tokens + int(tokens_used), current_cost + float(expenses)
    
    except KeyError as e:
        raise KeyError(f"Missing required key in response: {e}")




def request_gemini(data: dict) -> dict:
    """
    Отправляет запрос к Gemini API и возвращает ответ с информацией о токенах и стоимости.
    
    Args:
        data: Словарь с данными запроса, должен содержать 'total_cost' и 'tokens'
    
    Returns:
        Dict с ответом от Gemini или None в случае ошибки
    """

    if not isinstance(data, dict):
        logging.error("Invalid input: data must be a dictionary")
        return None

    total_cost, tokens = data.get("total_cost"), data.get("tokens")

    try:
        # Запрос к AI
        answer = ask_gemini(data)
        if not answer:
            logging.warning("Empty response from Gemini API")
            return None
        
        # Обновляем токены и цену
        updated_tokens, updated_cost = tok_cost(tokens, total_cost, answer)
        
        # Получаем основной ответ
        response_data = answer.get("response", {})
        if not response_data:
            logging.warning("No 'response' field in Gemini answer")
            return None
        
        # Добавляем метаинформацию
        response_data.update({
            "tokens": updated_tokens,
            "total_cost": updated_cost
        })
        
        return response_data
        
    except Exception as e:
        logging.error(f"Error in request_gemini: {e}")
        return None




MAX_ITERATIONS = 4

def main():
    """Генерирует SEO-текст для страницы сайта"""

    # Получение пользовательского запроса
    logging.info("RU: Дайте описание страницы сайта которую нужно сгенерировать:")
    logging.info("EN: Give a description of the site page that needs to be generated:\n")
    query = input().strip()

    if not query:
        logging.error("Пустой запрос")
        return None


    tokens, total_cost, dialog = 0, 0, []


    for iteration in range(1, MAX_ITERATIONS + 1):
        logging.info(f"Итерация {iteration}/max {MAX_ITERATIONS}")
        


        #### 1. Генерирует Текст:
        data_gen_text = {
            "question": query,
            "system_content": system_con_gen_text,
            "tools": gen_seo_text,
            "tool_config": tool_config_any,
            "model": "gemini-2.5-flash", #"gemini-2.0-flash", "gemini-2.5-flash"
            "dialog": json.dumps(dialog, ensure_ascii=False) if dialog else None,
            "tokens": tokens,
            "total_cost": total_cost
        }

        logging.info(f"\n!!!!!\n{data_gen_text}\n")

        # Запрос к ИИ:
        answer_gen_text = request_gemini(data_gen_text)
        if not answer_gen_text:
            return False
        
        an_class = DictObj(answer_gen_text)
        seo_text, keywords, description, title, tokens, total_cost = an_class.seo_text, an_class.keywords, an_class.description, an_class.title, an_class.tokens, an_class.total_cost

        # Добавление запроса пользователя в историю диалога:
        dialog.append({"user": query})

        # Добавление ответа ИИ в историю диалога:
        answer_ai = f"Полученный текст: {seo_text}, keywords: {json.dumps(keywords, ensure_ascii=False)}, description: {description}, title: {title}"
        dialog.append({"assistant": answer_ai})
        ####





        #### 2. Проверка и вердикт:
        data_check = {
            "question": answer_ai,
            "system_content": system_check,
            "tools": checking,
            "tool_config": tool_config_any,
            "model": "gemini-2.5-flash", #"gemini-2.0-flash", "gemini-2.5-flash"
            "dialog": json.dumps(dialog, ensure_ascii=False) if dialog else None,
            "tokens": tokens,
            "total_cost": total_cost
        }

        # Запрос к ИИ
        answer_check = request_gemini(data_check)
        if not answer_check:
            return False
        
        answ = DictObj(answer_check)
        acceptance, annotation, tokens, total_cost = answ.acceptance, answ.annotation, answ.tokens, answ.total_cost

        if acceptance:
            return {"Анотации": annotation, "Полученный текст": {seo_text}, "keywords": {json.dumps(keywords, ensure_ascii=False)}, "description": {description}, "title": {title}}


        # Добавление запроса пользователя/агента в историю диалога:
        dialog.append({"user": annotation})

        # Добавление ответа ИИ в историю диалога:
        dialog.append({"assistant": f"Полученный текст: {seo_text}, keywords: {json.dumps(keywords, ensure_ascii=False)}, description: {description}, title: {title}"})
        
        query = annotation
        
        ####




if __name__ == "__main__":
    try:
        result = main()
        if result:
            logging.info(f"Результат: {result}")
        else:
            logging.error("Не удалось получить результат")
    except KeyboardInterrupt:
        logging.info("Прервано пользователем")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")






# Страница по ремонту телефона Poco x3 Pro. В них есть производственный брак - перегрев и отвал процессора. Я частный мастер по ремонту. Даю гарантию. Самый дешевый ремонт подобного дифекта по Москве. Даю гарантии. Ремонтирую на потоке. Улучшаю охлаждение при помощи качественных термопрокладок - предотвращая подобную проблему снова. Реболл - 4500р. Гарантия 3 месяца.













                # - Напиши SEO текст для страницы сайта. Объем текста в зависимости от типа страницы:
                #     1. Коммерческая страница (услуги, товары, лендинг) - Оптимальный объем: 500 – 1000 слов,
                #     2. Информационная страница (блог, статья, гайд, обзор) - 1000 – 2500 слов,
                #     3. Новостная страница (короткие анонсы, статьи) - 300 – 800 слов.
                # - Текст должен отвечать на запрос пользователя.
                # - Собери основные ключевые слова (SEO-ядро) в json. Держи список четким: только релевантные слова без дублей и мусора. Гео-запросы по возможности. 
                # - Ключевые слова должны содержать основное ключевое слово.
                # - Сформулируй описание страницы description отдельно в json. По всем правилам SEO.
                # - Сформулируй название страницы title отдельно в json. По всем правилам SEO.
                # - Не используй спам, обещания, употребления гипер слов - самый лучший, надежный, дешевый.
                # - Соблюдай правила SEO построения текста, наличие h1 обязательно. Локаничный h1.
                # - Обозначь в html место картинки и видео ролика и добавив в них нужные мето теги типа title и alt.
                # - Избегайте "воды" – текст должен быть информативным.
                # - Убери любое форматирование, значки и иконки.
                # - SEO текст должен быть оформлен в формате html, но только то что внутри <body> без остального.




        # # 0: Compression raw data / Сжатие сырых данных:
        # system_content = """
        #     Оптимизируй текст: сократи, убери лишние символы, 
        #     переносы. Упрости структуру для удобства дальнейшего редактирования. 
        # """
        # answer_0 = airequest.gemi_0(raw, system_content)
        # tokens, total_cost = tok_cost(tokens, total_cost, answer_0)
        # clear_raw = answer_0.get("response")
        # out_info(clear_raw, "compresed") # скомпрешеные входные данные


        # # 1: The target audience / Определение аудитории :
        # system_content = """
        #     На основе описания страницы сайта определи портрет целевой аудитории. 
        #     Проанализируй: 
        #     1. Демографию (средний возраст, доход, география, род занятий, уровень доверчивости, соотношение пола); 
        #     2. Возможные раздражающие факторы такой аудитории (что лучше избегать в тексте, возможно громких обещаний и агресивных фраз, оборотов или слов); 
        #     Ответ должен быть четким, структурированным и без лишней информации.
        # """
        # answer_1 = airequest.gemi_1(clear_raw, system_content)
        # tokens, total_cost = tok_cost(tokens, total_cost, answer_1)
        # response = answer_1.get("response")
        # demographics = response.get("demographics") # Целевая аудитория
        # anger =  response.get("anger") # Раздражающие факторы данной аудитории

        # out_info(demographics, "demographics")
        # out_info(anger, "anger")


        # # 2. Get Type Page / Тип страницы:
        # system_content = """
        #     На основе описания страницы сайта определи следующие пункты типа, формата и тематического фокуса страницы: 
        #     1. Определи тип страницы: коммерческая страница, информационная, новостная.
        #     2. Укажи стадию воронки: ознакомление, сравнение, конверсия, удержание.
        #     3. Сформулируй основную цель: информировать, убедить, продать, развлечь.
        #     4. Выдели ключевую тему/фокус одним предложением.
        #     Отвечай кратко, без лишних объяснений.
        # """
        # answer_2 = airequest.gemi_2(clear_raw, system_content)
        # tokens, total_cost = tok_cost(tokens, total_cost, answer_2)
        # response = answer_2.get("response")
        # type_page = response.get("type_page") # Тип страницы
        # funnel_stage = response.get("funnel_stage") # Стадия воронки
        # main_goal = response.get("main_goal") # Основная цель страницы
        # focus = response.get("focus") # Ключевая тема

        # out_info(type_page, "type_page")
        # out_info(funnel_stage, "funnel_stage")
        # out_info(main_goal, "main_goal")
        # out_info(focus, "focus")


        # # 3. Get User's Goals / Цели пользователя страницы:
        # system_content = """
        #     1. Угадай, что хочет получить посетитель этой страницы. Какая у него цель?
        #     2. Выяви его скрытые страхи и сомнения, которые мотивируют поиск. Перечисли по важности.
        #     3. Предложи способы воздействия через контент, чтобы снять сомнения и повысить конверсию.
        #     Отвечай кратко, по пунктам, без лишних объяснений.
        # """

        # custom_query = f"О странице: {clear_raw}\nАудитория: {demographics}\nТип страницы: {type_page}\nОсновная цель контента по отношению к читающему: {main_goal}\nКлючевая тема: {focus}" 
        # #print(custom_query)

        # answer_3 = airequest.gemi_3(custom_query, system_content)
        # tokens, total_cost = tok_cost(tokens, total_cost, answer_3)
        # response = answer_3.get("response")
        # goals = response.get("goals") # Угаданные цели посетителя сайта
        # fears = response.get("fears") # Страхи посетителя, из за которых он все еще ищет
        # benefit = response.get("benefit") # Решения текстом

        # out_info(goals, "goals")
        # out_info(fears, "fears")
        # out_info(benefit, "benefit")


        # # 4. Keyword Collection / Сбор ключевых слов:
        # system_content = (
        #     "Сбор ключевых слов (SEO-ядро):"
        #     "Определи основные ключевые запросы для страницы (включая высоко- и низкочастотные)."
        #     "Добавь длинные хвосты (long-tail) — более конкретные и менее конкурентные фразы."
        #     #"Учитывай разные интенты пользователей (например: «купить», «сравнить», «как сделать», «отзывы»)."
        #     "Приоритет гео-запросам в коммерческих и новостных сайтах: если есть адрес/город — делай ответ максимально конкретным, с привязкой к локации."
        #     "Держи список четким: только релевантные слова без дублей и мусора."
        # )

        # custom_query = f"О странице: {clear_raw}\n"
        # #print(custom_query)

        # answer_4 = airequest.gemi_4(custom_query, system_content)
        # tokens, total_cost = tok_cost(tokens, total_cost, answer_4)
        # response = answer_4.get("response")
        # keywords = response.get("keywords") # Список ключевых слов страницы

        # out_info(keywords, "keywords")



        # # 5. Developing a plan / Разработка плана:
        # system_content = """
        #     Разработка плана/сценария + CTA:
        #     Создай четкую структуру с вовлекающим началом и логичным развитием.
        #     Захвати внимание: используй сильный крючок (интрига, вопрос, неожиданный факт или эмоциональный образ).
        #     Развивай логику: проблема → решение → выгоды (можно через сторителлинг, данные или экспертные мнения).
        #     Добавь доказательства: реальные примеры, кейсы, цитаты или статистику для доверия.
        #     Включи 3 варианта CTA (основной, альтернативный, срочный) – например:
        #     Основной: «Скачать инструкцию сейчас»
        #     Альтернативный: «Подписаться на обновления»
        #     Срочный: «Зарегистрируйтесь до [дата], чтобы получить бонус».
        #     Без воды: только конкретика, понятные шаги и выгоды для читателя.
        # """

        # custom_query = f"О странице: {clear_raw}\n"
        # #print(custom_query)

        # answer_5 = airequest.gemi_5(custom_query, system_content)
        # tokens, total_cost = tok_cost(tokens, total_cost, answer_5)

        # response = answer_5.get("response")
        # plan_main = response.get("plan_main")
        # plan_text = response.get("plan_text")
        # plan_href = response.get("plan_href")
        # plan_ui = response.get("plan_ui")
        # plan_media = response.get("plan_media")

        # out_info(plan_main, "plan_main")
        # out_info(plan_text, "plan_text")
        # out_info(plan_href, "plan_href")
        # out_info(plan_ui, "plan_ui")
        # out_info(plan_media, "plan_media")


        # # 6. Writing a text / Написание текста:
        # system_content = f"""
        #     Написать SEO текст для страницы сайта. 
        #     Колличество слов должно соотвествовать категории страницы сайта - {type_page},
        #     Целевая аудитория сайта - {demographics},
        #     Внутренние страхи такой удитории - {anger},
        #     Основная цель страницы - {main_goal},
        #     Ключевая тема текста - {focus},
        #     Возможные желания читателя от страницы - {goals},
        #     Основные страхи читателя, которые движат им - {fears},
        #     Возможные подходы решений его страхов в тексте - {benefit},
        #     Ключевые слова, которые желательно использовать в SEO тексте - {keywords},
        #     План для написания текста - {plan_text}
        # """
        # print(f"\n{system_content}\n")

        # custom_query = f"О странице: {clear_raw}\n"
        # #print(custom_query)

        # answer_6 = airequest.gemi_6(custom_query, system_content)
        # tokens, total_cost = tok_cost(tokens, total_cost, answer_6)

        # response = answer_6.get("response")
        # main_content = response.get("main_content")
        # description = response.get("description")
        # title = response.get("title")

        # out_info(main_content, "main_content")
        # out_info(description, "description")
        # out_info(title, "title")