import re
import os
import json
import logging
from datetime import datetime
logging.basicConfig(level=logging.INFO)
from mod_gemini import ask_gemini
from config import MAX_ITERATIONS, DEFAULT_MODEL_GEMINI, OUTPUT
from common import DictObj
from prompts import tool_config_any, gen_seo_text, system_check, system_con_gen_text, checking, system_plan, gen_plan




def request_gemini(data: dict) -> dict:

    if not isinstance(data, dict):
        logging.error("Invalid input: data must be a dictionary")
        return None

    try:
        # Запрос к AI
        answer = ask_gemini(data)
        if not answer:
            logging.warning("Empty response from Gemini API")
            return None
        
        # Получаем основной ответ
        response_data = answer.get("response")
        if not response_data:
            logging.warning("No 'response' field in Gemini answer")
            return None
        
        # Добавляем метаинформацию
        response_data.update({
            "tokens": answer.get("used_tokens"),
            "total_cost": answer.get("expenses")
        })
        
        return response_data
        
    except Exception as e:
        logging.error(f"Error in request_gemini: {e}")
        return None



def clear_dash(text):
    return re.sub(r'[—–]', '-', text)  # заменяет как "—" (длинное тире), так и "–" (среднее тире)



def save_file(
    annotation: str,
    seo_text: str,
    keywords: str,
    description: str,
    title: str,
    tokens: int,
    total_cost: float
) -> bool:
    """
    Сохраняет сгенерированный SEO-контент в текстовый файл.
    
    Args:
        annotation: Аннотации проверяющего ИИ
        seo_text: Сгенерированный SEO-текст
        keywords: Ключевые слова
        description: Описание страницы
        title: Заголовок страницы
        tokens: Количество потраченных токенов
        total_cost: Общая стоимость генерации
    
    Returns:
        bool: True если файл успешно сохранен, False в противном случае
    """
    try:
        # Создаем директорию если её нет
        os.makedirs(OUTPUT, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(OUTPUT, f"gen_seo_text_{timestamp}.txt")
        
        # Используем f-строки для лучшей читаемости
        content = f"""Результат генерации контента ИИ ({DEFAULT_MODEL_GEMINI}):

1. Текст:
{seo_text}
------------------------------------------------------

2. Описание страницы (description):
{description}
------------------------------------------------------

3. Заголовок страницы в браузере (title):
{title}
------------------------------------------------------

4. Ключевые слова (keywords):
{keywords}
------------------------------------------------------

5. Аннотации проверяющего ИИ:
{annotation}
------------------------------------------------------

6. Токенов всего потрачено: {tokens}, Стоимость всего: {total_cost:.4f}$
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logging.info(f"Файл успешно сохранен: {filename}")
        return True
        
    except OSError as e:
        logging.error(f"Ошибка при работе с файлом: {e}")
        return False
    except Exception as e:
        logging.error(f"Неожиданная ошибка при сохранении файла: {e}")
        return False


def main():

    # Получение пользовательского запроса
    logging.info("RU: Дайте описание страницы сайта которую нужно сгенерировать:")
    logging.info("EN: Give a description of the site page that needs to be generated:\n")
    query = input().strip()

    if not query:
        logging.error("Empty request")
        return None


    tokens, total_cost, i, dialog = 0, 0, 1, []



    

    #### 1. Составление плана и другой статы:
    data_gen_text = {
        "question": query,
        "system_content": system_plan,
        "tools": gen_plan,
        "tool_config": tool_config_any,
        "model": DEFAULT_MODEL_GEMINI, #"gemini-2.0-flash", #"gemini-2.0-flash", "gemini-2.5-flash"
        "dialog": json.dumps(dialog, ensure_ascii=False) if dialog else None,
    }

    logging.info(f"Составляю план страницы")

    # Запрос к ИИ:
    answer_gen_text = request_gemini(data_gen_text)
    if not answer_gen_text:
        return False
    
    an_class = DictObj(answer_gen_text)
    plan, tokens, total_cost = an_class.plan, an_class.tokens + tokens, an_class.total_cost + total_cost

    # Добавление запроса пользователя в историю диалога:
    dialog.append({"user": query}) 

    # Добавление ответа ИИ в историю диалога:
    answer_plan = f"План и другие данные для написания текста: {plan}"
    dialog.append({"assistant_1": answer_plan})

    logging.info(answer_plan)
    #logging.info(f"\n!!!!!\ndialog: {dialog}\n")
    ####




    while True:

        #### 2. Генерирует Текст:
        data_gen_text = {
            "question": query,
            "system_content": f"{system_con_gen_text} + \n\nПлан и другие данные для написания текста: {plan}",
            "tools": gen_seo_text,
            "tool_config": tool_config_any,
            "model": DEFAULT_MODEL_GEMINI, #"gemini-2.0-flash", #"gemini-2.0-flash", "gemini-2.5-flash"
            "dialog": json.dumps(dialog, ensure_ascii=False) if dialog else None,
        }

        logging.info(f"Составляю текст страницы. Попытка {i} из возможных {MAX_ITERATIONS}")
        #logging.info(f"\n!!!!!\ndata_gen_text:{data_gen_text}\n")

        # Запрос к ИИ:
        answer_gen_text = request_gemini(data_gen_text)
        if not answer_gen_text:
            return False
        
        an_class = DictObj(answer_gen_text)
        seo_text, keywords, description, title, tokens, total_cost = an_class.seo_text, an_class.keywords, an_class.description, an_class.title, an_class.tokens + tokens, an_class.total_cost + total_cost

        # Добавление запроса пользователя в историю диалога:
        dialog.append({"user": query}) 

        # Добавление ответа ИИ в историю диалога:
        answer_ai = f"Полученный текст: {seo_text}, keywords: {json.dumps(keywords, ensure_ascii=False)}, description: {description}, title: {title}"
        dialog.append({"assistant_2": answer_ai})

        logging.info(answer_ai + f"\nпопытка: {i}")
        ####





        #### 3. Проверка и вердикт:
        data_check = {
            "question": answer_ai,
            "system_content": f"{system_check} + \nТак же проверить, соотвествует ли результат, первоночальному плану и входным данным: {plan}",
            "tools": checking,
            "tool_config": tool_config_any,
            "model": DEFAULT_MODEL_GEMINI, #"gemini-2.0-flash", #"gemini-2.0-flash", "gemini-2.5-flash"
            "dialog": json.dumps(dialog, ensure_ascii=False) if dialog else None,
        }

        logging.info(f"Проверяю полученный результат на соотвествие поставленной задачи")

        # Запрос к ИИ
        answer_check = request_gemini(data_check)
        if not answer_check:
            return False
        
        answ = DictObj(answer_check)
        acceptance, annotation, tokens, total_cost = answ.acceptance, answ.annotation, answ.tokens + tokens, answ.total_cost + total_cost

        seo_text = clear_dash(seo_text)
        keywords = json.dumps(keywords, ensure_ascii=False)

        if acceptance:
            if not save_file(annotation, seo_text, keywords, description, title, tokens, total_cost):
                logging.error("Error save file 54")
                return False
            return {"Текст прошел проверку. Анотации по нему": annotation, "Полученный текст": {seo_text}, "keywords": {keywords}, "description": {description}, "title": {title}, "tokens": tokens, "total_cost": total_cost}



        # Добавление запроса пользователя/агента в историю диалога:
        dialog.append({"user": answer_ai})

        # Добавление ответа ИИ в историю диалога:
        dialog.append({"assistant_3": f"Текст принят или нет: {acceptance}, Анотации по нему: {annotation}"})
        
        query = annotation
        logging.info(f"Текст не прошел проверку и будет снова переписан: {annotation}")
        
        if i == MAX_ITERATIONS:
            if not save_file(annotation, seo_text, keywords, description, title, tokens, total_cost):
                logging.error("Error save file 54")
                return False
            logging.info(f"Закончились предусмотренные попытки на переписывание текста. Возвращаю последний результат")
            return {"Текст не прошел модерацию агента, но попытки переписывания закончились, вот последний результат: Анотации": annotation, "Полученный текст": {seo_text}, "keywords": {keywords}, "description": {description}, "title": {title}, "tokens": tokens, "total_cost": total_cost}

        
        i += 1
        ####




if __name__ == "__main__":
    try:
        result = main()
        if result:
            logging.info(f"\nРезультат: {result}")
        else:
            logging.error("Не удалось получить результат")
    except KeyboardInterrupt:
        logging.info("Прервано пользователем")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")






# Страница по ремонту телефона Poco x3 Pro. В них есть производственный брак - перегрев и отвал процессора. Я частный мастер по ремонту. Даю гарантию. Самый дешевый ремонт подобного дифекта по Москве. Даю гарантии. Ремонтирую на потоке. Улучшаю охлаждение при помощи качественных термопрокладок - предотвращая подобную проблему снова. Реболл - 4500р. Гарантия 3 месяца.





