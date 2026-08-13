import streamlit as st
import json
from parser_logic import parse_uploaded_demo

# Настройка страницы
st.set_page_config(page_title="CS2 Demo Data Extractor", page_icon="🎯")

st.title("🎯 ИИ-Аналитик матчей CS2 (Экстрактор данных)")
st.subheader("Извлечение сухих параметров из файлов демок для ИИ-Тренера")

st.info("""
**Инструкция:** Загрузи сюда свои файлы демок (.dem). Сайт за пару секунд вытащит из них чистые 
игровые логи (убийства, урон, выстрелы). Скопируй полученный текст ниже и отправь его ИИ в чат 
вместе со второй частью инструкции, чтобы получить поминутный разбор!
""")

# Кнопка загрузки файлов
uploaded_files = st.file_uploader(
    "Перетащите файлы демок (.dem) сюда:", 
    type=["dem"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 7:
        st.warning("⚠️ Пожалуйста, выберите не более 7 файлов за один раз.")
    else:
        st.markdown(f"Выбрано файлов для анализа: **{len(uploaded_files)}**")
        
        if st.button("🚀 Извлечь чистые логи матчей", type="primary", use_container_width=True):
            all_matches_report = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(uploaded_files, 1):
                status_text.markdown(f"**⏳ Чтение файла {idx}/{len(uploaded_files)}:** `{file.name}`...")
                try:
                    match_data = parse_uploaded_demo(file, idx)
                    all_matches_report.append(match_data)
                    st.toast(f"Файл {file.name} успешно обработан!", icon="✅")
                except Exception as e:
                    st.error(f"❌ Ошибка при обработке файла {file.name}: {e}")
                    
                progress_bar.progress(idx / len(uploaded_files))
                
            status_text.success("🎉 Данные успешно извлечены!")
            
            # Перевод данных в JSON-строку БЕЗ ОШИБОК
            final_json_string = json.dumps(all_matches_report, ensure_ascii=False, indent=2, default=str)
            
            st.subheader("📋 Итоговый текст для копирования")
            st.markdown("Нажми кнопку копирования в правом верхнем углу блока ниже и отправь текст ИИ:")
            st.code(final_json_string, language="json")
