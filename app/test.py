

# class DictObj:
#     def __init__(self, data: dict):
#         self.__dict__.update(data)  # Добавляем все ключи как атрибуты
    
#     def __repr__(self):
#         return f"DictObj({self.__dict__})"

# # Пример использования
# data = {"question": "Как дела?", "answer": 42, "unknown_field": True}
# obj = DictObj(data)

# print(obj.question)  # "Как дела?"
# print(obj.answer)    # 42
# print(obj.unknown_field)  # True
# print(obj)  # DictObj({'question': 'Как дела?', 'answer': 42, 'unknown_field': True})







# from types import SimpleNamespace
# data = {"question": "Запрос", "tokens": 100}
# obj = SimpleNamespace(**data)

# print(obj.question)  # "Запрос"
# print(obj.tokens)    # 100








# from typing import NamedTuple

# class Quest(NamedTuple):
#     question: str
#     system_content: str
#     tools: str
#     tool_config: str
#     model: str
#     dialog: str
#     tokens: str
#     total_cost: str

# data_gen_text = {
#     "question": "запрос",
#     "system_content": "text system content",
#     "tools": "gen_seo_text",
#     "tool_config": "tool_config_any", 
#     "model": "gemini-2.5-flash",
#     "dialog": "dialog",
#     "tokens": "tokens",
#     "total_cost": "total_cost",
#     "test": "44"
# }

# p = Quest(**data_gen_text)
# print(p.question)  # 10






def main():
    """Генерирует SEO-текст для страницы сайта"""
    
    # Получение пользовательского запроса
    logging.info("\nRU: Дайте описание страницы сайта которую нужно сгенерировать:")
    logging.info("EN: Give a description of the site page that needs to be generated:\n")
    query = input().strip()
    
    if not query:
        logging.error("Пустой запрос")
        return None
    
    # Инициализация состояния
    state = {
        "tokens": 0,
        "total_cost": 0,
        "dialog": []
    }
    
    MAX_ITERATIONS = 2
    
    for iteration in range(1, MAX_ITERATIONS + 1):
        logging.info(f"Итерация {iteration}/{MAX_ITERATIONS}")
        
        try:
            result = generate_seo_content(query, state)
            if not result:
                logging.error(f"Ошибка на итерации {iteration}")
                return None
                
            # Обновляем состояние
            state.update(result)
            
            # Добавляем в историю диалога
            update_dialog_history(state["dialog"], query, result)
            
        except Exception as e:
            logging.error(f"Ошибка на итерации {iteration}: {e}")
            return None
    
    return format_final_result(state)


def generate_seo_content(query, state):
    """Генерирует SEO-контент через API"""
    
    request_data = {
        "question": query,
        "system_content": system_con_gen_text,
        "tools": gen_seo_text,
        "tool_config": tool_config_any,
        "model": "gemini-2.0-flash",
        "dialog": json.dumps(state["dialog"]) if state["dialog"] else None,
        "tokens": state["tokens"],
        "total_cost": state["total_cost"]
    }
    
    response = request_gemini(request_data)
    if not response:
        return None
    
    return parse_ai_response(response)


def parse_ai_response(response):
    """Парсит ответ от AI"""
    try:
        answ = DictObj(response)
        return {
            "seo_text": answ.seo_text,
            "keywords": answ.keywords,
            "description": answ.description,
            "title": answ.title,
            "tokens": answ.tokens,
            "total_cost": answ.total_cost
        }
    except AttributeError as e:
        logging.error(f"Ошибка парсинга ответа: {e}")
        return None


def update_dialog_history(dialog, query, result):
    """Обновляет историю диалога"""
    dialog.append({"user": query})
    dialog.append({
        "assistant": f"Полученный текст: {result['seo_text']}, "
                    f"keywords: {json.dumps(result['keywords'], ensure_ascii=False)}, "
                    f"description: {result['description']}, "
                    f"title: {result['title']}"
    })


def format_final_result(state):
    """Форматирует финальный результат"""
    return {
        "answer": state.get("seo_text", ""),
        "tokens": state["tokens"],
        "total_cost": state["total_cost"]
    }


# Основной вызов
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


