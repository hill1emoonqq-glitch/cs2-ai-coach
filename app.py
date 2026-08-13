import streamlit as st
import json
# Импортируем функцию безопасного парсинга из parser_logic.py
from parser_logic import download_and_parse_demo

# Настройка внешнего вида страницы сайта
st.set_page_config(
    page_title="CS2 AI Match Analyst",
    page_icon="🎯",
    layout="centered"
)

# Главный заголовок сайта в стиле УТП
st.title("🎯 ИИ-Аналитик матчей CS2")
st.subheader("Объективная оценка скилла, расчет Premier Elo и персональный план тренировок")

# Красивая карточка с описанием того, что получит пользователь
st.info("""
**Вместо случайных цифр ты получишь объективную оценку, где твой текущий скилл строго равен реальному эло.** 
ИИ рассчитает примерное финальное Premier-эло за матч. На основе анализа создается персональная двухчасовая тренировка. 
Ты получишь четкие фокусы для следующих матчей: на что именно обращать внимание и как побеждать.
""")

st.markdown("""
### 📋 Инструкция:
1. Зайди в свой профиль Steam -> Игры -> Личная статистика CS2 -> Премьер матчи.
2. Скопируйте прямую ссылку на скачивание нужного матча (кнопка *«Скачать демо»*).
3. Вставь до 7 ссылок (в формате `.dem.bz2`) в поле ниже, каждую с новой строки.
""")

# Удобное поле для ввода текстовых ссылок
urls_input = st.text_area(
    "Вставь ссылки на демо-файлы сюда:", 
    height=180,
    placeholder="https://valve.net\nhttps://valve.net"
)

# Кнопка запуска
if st.button("🚀 Запустить честный ИИ-анализ", type="primary", use_container_width=True):
    # Очищаем строки от пробелов и убираем пустые переносы
    urls = [url.strip() for url in urls_input.split("\n") if url.strip()]
    
    if not urls:
        st.error("❌ Пожалуйста, введите хотя бы одну ссылку на демо-файл из Steam.")
    elif len(urls) > 7:
        st.warning("⚠️ Система оптимизирована для анализа не более 7 матчей за один раз во избежание перегрузки.")
    else:
        all_matches_report = []
        
        # Создаем интерактивные элементы загрузки
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Запускаем цикл обработки каждой ссылки
        for idx, url in enumerate(urls, 1):
            status_text.markdown(f"**⏳ Шаг {idx}/{len(urls)}:** Скачивание матча и извлечение 100+ параметров пакетов...")
            
            try:
                # Наш безопасный движок парсит данные без забивания RAM
                match_data = download_and_parse_demo(url, idx)
                all_matches_report.append(match_data)
                st.toast(f"Матч №{idx} успешно обработан!", icon="✅")
            except Exception as e:
                st.error(f"❌ Ошибка при обработке ссылки №{idx}: {e}")
                
            # Двигаем полоску прогресса вперед
            progress_bar.progress(idx / len(urls))
            
        status_text.success("🎉 Все доступные матчи успешно обработаны без фальшивых цифр!")
        
        # Превращаем собранный лог в текстовый JSON формат
        final_json_string = json.dumps(all_matches_report, ensure_ascii=False, indent=2)
        
        st.success("✅ Твой объективный игровой отчет сформирован!")
        
        # Раздел вывода результатов
        st.subheader("📋 Данные для ИИ-Тренера")
        st.markdown("Скопируй сгенерированный ниже код и отправь его мне в чат вместе с промптом тренера для получения 2-часового плана тренировок:")
        
        # Виджет Streamlit с автоматической кнопкой "Скопировать" в правом верхнем углу
        st.code(final_json_string, language="json")
