import streamlit as st
import json
from parser_logic import parse_uploaded_demo

# Настройка страницы
st.set_page_config(
    page_title="CS2 AI Match Analyst",
    page_icon="🎯",
    layout="centered"
)

# Главный заголовок сайта
st.title("🎯 ИИ-Аналитик матчей CS2")
st.subheader("Объективная оценка скилла, расчет Premier Elo и персональный план тренировок")

# Информационная карточка
st.info("""
**📊 Честный ИИ-анализ без случайных чисел**

Вместо случайных цифр ты получишь объективную оценку, где твой текущий скилл строго равен реальному эло. 
ИИ рассчитает примерное финальное Premier-эло за матч. На основе анализа создается персональная двухчасовая тренировка. 
Ты получишь четкие фокусы для следующих матчей: на что именно обращать внимание и как побеждать.
""")

st.markdown("### 📦 Загрузка файлов матчей")

# Кнопка загрузки файлов
uploaded_files = st.file_uploader(
    "Перетащите файлы демок (.dem) сюда или нажмите кнопку 'Browse files':", 
    type=["dem"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 7:
        st.warning("⚠️ Пожалуйста, выберите не более 7 файлов за один раз во избежание перегрузки сервера.")
    else:
        st.markdown(f"Выбрано файлов для анализа: **{len(uploaded_files)}**")
        
        # Кнопка запуска анализа
        if st.button("🚀 Начать глубокий ИИ-анализ", type="primary", use_container_width=True):
            all_matches_report = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(uploaded_files, 1):
                status_text.markdown(f"**⏳ Шаг {idx}/{len(uploaded_files)}:** Чтение и анализ структуры файла `{file.name}`...")
                
                try:
                    match_data = parse_uploaded_demo(file, idx)
                    all_matches_report.append(match_data)
                    st.toast(f"Файл {file.name} успешно обработан!", icon="✅")
                except Exception as e:
                    st.error(f"❌ Ошибка при обработке файла {file.name}: {e}")
                    
                progress_bar.progress(idx / len(uploaded_files))
                
            status_text.success("🎉 Все загруженные демки успешно обработаны!")
            
            # Перевод данных в JSON-строку без ошибок
            final_json_string = json.dumps(all_matches_report, ensure_ascii=False, indent=2, default=str)
            
            st.success("✅ Твой объективный игровой отчет сформирован!")
            st.subheader("📋 Данные для ИИ-Тренера")
            st.markdown("Скопируй сгенерированный ниже код и отправь его мне в чат вместе с промптом тренера:")
            st.code(final_json_string, language="json")
