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


        # 1: Compression raw data / Сжатие сырых данных:
        system_content = """
            Оптимизируй текст: сократи, убери лишние символы, 
            переносы. Упрости структуру для удобства дальнейшего редактирования. 
        """
        answer_0 = gemi.gemi_0(raw, system_content)
        tokens, total_cost = tok_cost(tokens, total_cost, answer_0)
        clear_raw = answer_0.get("response")
        out_info(clear_raw, "compresed") # скомпрешеные входные данные


        # 2: The target audience / Определение аудитории :
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
        demographics = response.get("demographics")
        anger =  response.get("anger")
        out_info(demographics, "demographics") # Целевая аудитория
        out_info(anger, "anger") # Раздражающие факторы данной аудитории


        # 3. Get Type Page / Тип страницы:
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
        type_page = response.get("type_page")
        funnel_stage = response.get("funnel_stage")
        main_goal = response.get("main_goal")
        focus = response.get("focus")
        out_info(type_page, "type_page") # Тип страницы
        out_info(funnel_stage, "funnel_stage") # Стадия воронки
        out_info(main_goal, "main_goal") # Основная цель
        out_info(focus, "focus") # Ключевая тема


        # answer_3 = gemi.gemi_3(raw + str(answer_2.get("response")))
        # out_dict(answer_3.get("response"))

        # answer_4 = gemi.gemi_4(raw + str(answer_3.get("response")))
        # out_list(answer_4.get("response"))

        # answer_5 = gemi.gemi_5(raw + str(answer_1.get("response")) + str(answer_2.get("response")) + str(answer_3.get("response")))
        # out_dict(answer_5.get("response"))

        # answer_6 = gemi.gemi_6(raw + str(answer_5.get("response")))
        # out_dict(answer_6.get("response"))

        return {"complete": True, "used_tokens": tokens, "total_cost": total_cost}
    
    except Exception as e:
        out_info(f"Error: {e}", "System")
        return False


answer = main()
print(answer)


# Страница по ремонту телефона Poco x3 Pro. В них есть производственный брак - перегрев и отвал процессора. Я частный мастер по ремонту. Даю гарантию. Самый дешевый ремонт подобного дифекта по Москве. Даю гарантии. Ремонтирую на потоке. Улучшаю охлаждение при помощи качественных термопрокладок - предотвращая подобную проблему снова. Реболл - 4500р. Гарантия 3 месяца.
