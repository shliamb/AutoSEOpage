import json
from mod_gemini import ask_gemini
from prompts import tool_config_any, gen_seo_text, checking



# For Testing app data  Printing Information in Terminal:
def out_info(data, who: str = None):
    in_who = f"{who}: " if who else ""

    if isinstance(data, dict):
        for key, value in data.items():
            print(f"\n{key}: {value}")

    elif isinstance(data, list):
        print(f"\n{in_who}{data}")

    elif isinstance(data, str):
        print(f"\n{in_who}{data}")


# Saving Tokens and total cost:
def tok_cost(tokens, total_cost, answer):
    tokens += answer.get("used_tokens")
    total_cost += answer.get("expenses")
    return tokens, total_cost





def gemini_gen_text(raw: str, dialog: list, tokens: int, total_cost: int) -> tuple:

    try:
        request_data = {
            "question": raw,
            "system_content": """
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
            """,
            "tools": gen_seo_text,
            "tool_config": tool_config_any, 
            "model": "gemini-2.5-flash", #"gemini-2.0-flash", "gemini-2.5-flash"
            "dialog": json.dumps(dialog) if dialog else None
        }

        # Запрос к Ai
        answer = ask_gemini(request_data)
        # Токены и цена
        tokens, total_cost = tok_cost(tokens, total_cost, answer)
        answer_gemini = answer.get("response")

        seo_text = answer_gemini.get("seo_text")
        keywords = answer_gemini.get("keywords")
        description = answer_gemini.get("description")
        title = answer_gemini.get("title")

        # В историю общения ответ ии
        dialog.append({"assistant_1": f"Текст: {seo_text}, keywords: {json.dumps(keywords, ensure_ascii=False)}, description: {description}, title: {title}"})

        out_info(seo_text, "seo_text")
        out_info(keywords, "keywords") 
        out_info(description, "description")
        out_info(title, "title") 

        return answer_gemini, dialog, tokens, total_cost

    except Exception as e:
        out_info(f"Error: {e}", "System 1")
        return False




def gemini_check(dialog: list, tokens: int, total_cost: int) -> tuple:

    try:
        request_data = {
            "question": "Проверь последнюю версию SEO текста, keywords, description от assistant_1",
            "system_content": """
                Сделай ревью последнего написанного текста страницы сайта. Дай ответ True - текст удовлетворителен 
                или False - текст нужно переписать.
                Дай конкретные и точные недочеты и ошибки, что бы их возможно было исправить. Дай заметку что хорошо - оставить, 
                что поменять и только реалистичные задачи.
                Не придирайся по пустякам.
            """,
            "tools": checking,
            "tool_config": tool_config_any, 
            "model": "gemini-2.5-flash", #"gemini-2.0-flash", "gemini-2.5-flash"
            "dialog": json.dumps(dialog) if dialog else None
        }

        # Запрос к Ai
        answer = ask_gemini(request_data)

        # print("--------------")
        # print(answer)
        # print("--------------")

        # Токены и цена
        tokens, total_cost = tok_cost(tokens, total_cost, answer)
        answer_gemini = answer.get("response")

        acceptance = answer_gemini.get("acceptance")
        annotation = answer_gemini.get("annotation")

        # В историю общения ответ ии
        #dialog.append({"assistant_2": f"Решение assistant_2 о принятии или браковке текста: {acceptance}, Описание проблем и пути их решения: {annotation}"})


        out_info(acceptance, "acceptance")
        out_info(annotation, "annotation") 

        return answer_gemini, dialog, tokens, total_cost

    except Exception as e:
        out_info(f"Error: {e}", "System 2")
        return False

# [{"user": "Привет, меня зовут Алекс."}, {"assistant": "Очень приятно Алекс, я Ева."}, {"user": "Мне 40 лет."}, {"assistant": "Ты в самом расвете сил!"}]






        # return {"complete": True, "used_tokens": tokens, "total_cost": total_cost}
    
    # except Exception as e:
    #     out_info(f"Error: {e}", "System")
    #     return False



def main():
    """Запуск цепочки запросов"""
    intro_queshen = "\nRU: Дайте описание страницы сайта которую нужно сгенерировать:\nEN: Give a description of the site page that needs to be generated:\n"
    out_info(f"{intro_queshen}", "")
    raw = input()
    dialog = [{"user": raw}]
    tokens = 0
    total_cost = 0

    i = 1

    while True:

        print(f"Генерация текста {i} ----------")

        answer_gen_text_seo, dialog, tokens, total_cost = gemini_gen_text(raw, dialog, tokens, total_cost)

        print(f"Переделка {i} ----------")

        answer, dialog, tokens, total_cost = gemini_check(dialog, tokens, total_cost)

        acceptance = answer.get("acceptance")
        annotation = answer.get("annotation")

        if acceptance:
            print("\n")
            return {"answer": answer_gen_text_seo, "tokens": tokens, "total_cost": total_cost}

        i += 1

        if i > 3:
            print("\n")
            return {"answer": answer_gen_text_seo, "tokens": tokens, "total_cost": total_cost}
        
        raw = annotation


answer = main()
print(answer)






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