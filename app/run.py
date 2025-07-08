# import json
from mod_gemini import Gemini



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



# Ключевые узлы, проверять другим через агента в jsone  отвечает True если все устроило, нет False - цикл повторно херачит пока не понравится,
# Добавляя в переписку агентскую недостатки и успешно выполненые аспекты..
# 


def main():

    tokens = 0
    total_cost = 0

    intro_queshen = """
        RU:
        Опишите максимально подробно, какой должна быть страница вашего сайта. Если это 
        коммерческая страница, укажите цены, перечень услуг, отзывы клиентов, точный адрес 
        (город, страна, ближайшая станция метро или ориентир). Расскажите о вашем коллективе, 
        офисе, рабочих подходах и опыте в данной сфере. Если страница информационная, четко 
        обозначьте ее цели: какую аудиторию вы хотите привлечь, какую проблему решить или какую 
        идею донести. Опишите вашу задумку, ключевые темы и структуру контента.:

        EN:
        Describe in as much detail as possible what your desired website page should look like. 
        If it's a commercial page, include prices, services, customer reviews, exact address 
        (city, country, nearest subway station or landmark). Provide details about your team, office, 
        work approach, and experience in the field. If it's an informational page, clearly define its 
        goals: what audience you want to attract, what problem to solve, or what idea to convey. Explain 
        your concept, key topics, and content structure.:

    """
    out_info(f"{intro_queshen}\n", "ai")


    raw = input()
    print("---------------")

    try:
        gemi = Gemini()


        # 0: Compression raw data / Сжатие сырых данных:
        system_content = """
            Оптимизируй текст: сократи, убери лишние символы, 
            переносы. Упрости структуру для удобства дальнейшего редактирования. 
        """
        answer_0 = gemi.gemi_0(raw, system_content)
        tokens, total_cost = tok_cost(tokens, total_cost, answer_0)
        clear_raw = answer_0.get("response")
        out_info(clear_raw, "compresed") # скомпрешеные входные данные


        # 1: The target audience / Определение аудитории :
        system_content = """
            На основе описания страницы сайта определи портрет целевой аудитории. 
            Проанализируй: 
            1. Демографию (средний возраст, доход, география, род занятий, уровень доверчивости, соотношение пола); 
            2. Возможные раздражающие факторы такой аудитории (что лучше избегать в тексте, возможно громких обещаний и агресивных фраз, оборотов или слов); 
            Ответ должен быть четким, структурированным и без лишней информации.
        """
        answer_1 = gemi.gemi_1(clear_raw, system_content)
        tokens, total_cost = tok_cost(tokens, total_cost, answer_1)
        response = answer_1.get("response")
        demographics = response.get("demographics") # Целевая аудитория
        anger =  response.get("anger") # Раздражающие факторы данной аудитории

        # out_info(demographics, "demographics")
        # out_info(anger, "anger")


        # 2. Get Type Page / Тип страницы:
        system_content = """
            На основе описания страницы сайта определи следующие пункты типа, формата и тематического фокуса страницы: 
            1. Определи тип страницы: коммерческая страница, информационная, новостная.
            2. Укажи стадию воронки: ознакомление, сравнение, конверсия, удержание.
            3. Сформулируй основную цель: информировать, убедить, продать, развлечь.
            4. Выдели ключевую тему/фокус одним предложением.
            Отвечай кратко, без лишних объяснений.
        """
        answer_2 = gemi.gemi_2(clear_raw, system_content)
        tokens, total_cost = tok_cost(tokens, total_cost, answer_2)
        response = answer_2.get("response")
        type_page = response.get("type_page") # Тип страницы
        funnel_stage = response.get("funnel_stage") # Стадия воронки
        main_goal = response.get("main_goal") # Основная цель страницы
        focus = response.get("focus") # Ключевая тема

        # out_info(type_page, "type_page")
        # out_info(funnel_stage, "funnel_stage")
        # out_info(main_goal, "main_goal")
        # out_info(focus, "focus")


        # 3. Get User's Goals / Цели пользователя страницы:
        system_content = """
            1. Угадай, что хочет получить посетитель этой страницы. Какая у него цель?
            2. Выяви его скрытые страхи и сомнения, которые мотивируют поиск. Перечисли по важности.
            3. Предложи способы воздействия через контент, чтобы снять сомнения и повысить конверсию.
            Отвечай кратко, по пунктам, без лишних объяснений.
        """

        custom_query = f"О странице: {clear_raw}\nАудитория: {demographics}\nТип страницы: {type_page}\nОсновная цель контента по отношению к читающему: {main_goal}\nКлючевая тема: {focus}" 
        #print(custom_query)

        answer_3 = gemi.gemi_3(custom_query, system_content)
        tokens, total_cost = tok_cost(tokens, total_cost, answer_3)
        response = answer_3.get("response")
        goals = response.get("goals") # Угаданные цели посетителя сайта
        fears = response.get("fears") # Страхи посетителя, из за которых он все еще ищет
        benefit = response.get("benefit") # Решения текстом

        # out_info(goals, "goals")
        # out_info(fears, "fears")
        # out_info(benefit, "benefit")


        # 4. Keyword Collection / Сбор ключевых слов:
        system_content = (
            "Сбор ключевых слов (SEO-ядро):"
            "Определи основные ключевые запросы для страницы (включая высоко- и низкочастотные)."
            "Добавь длинные хвосты (long-tail) — более конкретные и менее конкурентные фразы."
            #"Учитывай разные интенты пользователей (например: «купить», «сравнить», «как сделать», «отзывы»)."
            "Приоритет гео-запросам в коммерческих и новостных сайтах: если есть адрес/город — делай ответ максимально конкретным, с привязкой к локации."
            "Держи список четким: только релевантные слова без дублей и мусора."
        )

        custom_query = f"О странице: {clear_raw}\n"
        #print(custom_query)

        answer_4 = gemi.gemi_4(custom_query, system_content)
        tokens, total_cost = tok_cost(tokens, total_cost, answer_4)
        response = answer_4.get("response")
        keywords = response.get("keywords") # Список ключевых слов страницы

        # out_info(keywords, "keywords")



        # 5. Developing a plan / Разработка плана:
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

        custom_query = f"О странице: {clear_raw}\n"
        #print(custom_query)

        answer_5 = gemi.gemi_5(custom_query, system_content)
        tokens, total_cost = tok_cost(tokens, total_cost, answer_5)

        response = answer_5.get("response")
        plan_main = response.get("plan_main")
        plan_text = response.get("plan_text")
        plan_href = response.get("plan_href")
        plan_ui = response.get("plan_ui")
        plan_media = response.get("plan_media")

        # out_info(plan_main, "plan_main")
        # out_info(plan_text, "plan_text")
        # out_info(plan_href, "plan_href")
        # out_info(plan_ui, "plan_ui")
        # out_info(plan_media, "plan_media")


        # 6. Writing a text / Написание текста:
        system_content = f"""
            Написать SEO текст для страницы сайта. 
            Колличество слов должно соотвествовать категории страницы сайта - {type_page},
            Целевая аудитория сайта - {demographics},
            Внутренние страхи такой удитории - {anger},
            Основная цель страницы - {main_goal},
            Ключевая тема текста - {focus},
            Возможные желания читателя от страницы - {goals},
            Основные страхи читателя, которые движат им - {fears},
            Возможные подходы решений его страхов в тексте - {benefit},
            Ключевые слова, которые желательно использовать в SEO тексте - {keywords},
            План для написания текста - {plan_text}
        """
        print(f"\n{system_content}\n")

        custom_query = f"О странице: {clear_raw}\n"
        #print(custom_query)

        answer_6 = gemi.gemi_6(custom_query, system_content)
        tokens, total_cost = tok_cost(tokens, total_cost, answer_6)

        response = answer_6.get("response")
        main_content = response.get("main_content")
        description = response.get("description")
        title = response.get("title")

        out_info(main_content, "main_content")
        out_info(description, "description")
        out_info(title, "title")


        return {"complete": True, "used_tokens": tokens, "total_cost": total_cost}
    
    except Exception as e:
        out_info(f"Error: {e}", "System")
        return False


answer = main()
print(answer)


# Страница по ремонту телефона Poco x3 Pro. В них есть производственный брак - перегрев и отвал процессора. Я частный мастер по ремонту. Даю гарантию. Самый дешевый ремонт подобного дифекта по Москве. Даю гарантии. Ремонтирую на потоке. Улучшаю охлаждение при помощи качественных термопрокладок - предотвращая подобную проблему снова. Реболл - 4500р. Гарантия 3 месяца.
