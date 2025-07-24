# SEO PageGen AI (Idea)

Прототип для генерации SEO-текстов через Gemini API.  
**Важно**: Это концепт, который можно развивать. [Готовый бот уже реализован здесь](https://t.me/gen_seo_text_bot).

<br>

## 🚀 Быстрый старт

```bash
git clone https://github.com/shliamb/AutoSEOpage.git
python -m venv venv
source venv/bin/activate  # .\venv\Scripts\activate на Windows
pip install -r requirements.txt
python run.
```
---

### 🔧 Как работает

1. **Ввод данных:** Описываете текст (тип страницы, ЦА, ключевые слова и т.д.)

2. **Этапы обработки:**

   - 📝 **Планировщик:** Создает структуру, семантическое ядро (сохраняет в JSON)

   - ✍️ **SEO-Писатель:** Генерирует заголовки, тело текста

   - 🔍 **Ревизор:** Проверяет соответствие критериям, запускает рерайт при необходимости

3. **Вывод:** Готовый текст в выбранном формате.
---

### ⚙️ Конфигурация (config.py)
```python
DEFAULT_MODEL_GEMINI = "gemini-2.5-flash"  # Доступно: "gemini-2.0", "gemini-2.5-pro"
MAX_ITERATIONS = 2                        # Лимит рерайтов
OUTPUT_FORMAT = "MARKDOWN"                # Варианты: "markdown", "html", "plain"
Требуется файл .env с API-ключом (шаблон в .env-test).
```
---

### 💡 In future:

```text
- audio multimodal input / output data
- file input
- multiagents work
- may be tebles?
```
---

<br>
<!-- --- -->
