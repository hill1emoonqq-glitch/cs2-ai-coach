import streamlit as st
import json
from parser_logic import parse_uploaded_demo

st.set_page_config(page_title="CS2 Core Data Extractor", page_icon="🎯", layout="centered")

st.title("🎯 ИИ-Аналитик матчей CS2 (Экстрактор логов)")
st.subheader("Сбор честных параметров игры для ручного ИИ-аудита")

st.info("""
**Финальный режим:** Сайт больше не выдает шаблонные тренировки и фальшивое ЭЛО. 
Он извлекает чистую историю твоих дуэлей из файлов. Скопируй полученный JSON-код ниже и скинь ИИ в чат для помиллиметрового разбора.
""")

uploaded_files = st.file_uploader("Загрузи файлы демок (.dem):", type=["dem"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 7:
        st.warning("⚠️ Пожалуйста, выберите не более 7 файлов за один раз.")
    else:
        st.markdown(f"Выбрано файлов для анализа: **{len(uploaded_files)}**")
        
        if st.button("🚀 Извлечь честные логи матчей", type="primary", use_container_width=True):
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
                
            status_text.success("🎉 Логи матчей успешно извлечены без фальшивых цифр!")
            
            # Перевод данных в JSON-строку БЕЗ ОШИБОК
            final_json_string = json.dumps(all_matches_report, ensure_ascii=False, indent=2, default=str)
            
            st.success("✅ Твой объективный игровой отчет сформирован!")
            st.subheader("📋 Итоговый текст для копирования")
            st.markdown("Нажми кнопку копирования в правом верхнем углу блока ниже и отправь текст ИИ в чат:")
            st.code(final_json_string, language="json")
