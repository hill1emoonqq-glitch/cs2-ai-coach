import streamlit as st
import json
from parser_logic import parse_uploaded_demo

st.set_page_config(page_title="CS2 AI Match Analyst", page_icon="🎯")

st.title("🎯 ИИ-Аналитик матчей CS2")
st.subheader("Объективная оценка скилла, расчет Premier Elo и персональный план тренировок")

st.info("""
**Никаких ссылок!** Теперь вы можете просто загрузить файлы демок, которые скачали через Steam.
Выберите один или несколько файлов формата `.dem` (или `.dem.bz2`), и система сразу проведет честный анализ 100+ параметров.
""")

st.markdown("### 📦 Загрузка файлов матчей")
# Кнопка загрузки, которая принимает до 7 файлов одновременно
uploaded_files = st.file_uploader(
    "Перетащите файлы демок сюда или нажмите кнопку 'Browse files':", 
    type=["dem", "bz2"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 7:
        st.warning("⚠️ Пожалуйста, выберите не более 7 файлов за один раз.")
    else:
        st.write(f"Выбрано файлов для анализа: **{len(uploaded_files)}**")
        
        if st.button("🚀 Начать глубокий ИИ-анализ", type="primary", use_container_width=True):
            all_matches_report = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(uploaded_files, 1):
                status_text.markdown(f"**⏳ Шаг {idx}/{len(uploaded_files)}:** Чтение и анализ структуры файла `{file.name}`...")
                
                try:
                    # Вызываем обновленную функцию парсинга
                    match_data = parse_uploaded_demo(file, idx)
                    all_matches_report.append(match_data)
                    st.toast(f"Файл {file.name} успешно обработан!", icon="✅")
                except Exception as e:
                    st.error(f"❌ Ошибка при обработке файла {file.name}: {e}")
                    
                progress_bar.progress(idx / len(uploaded_files))
                
            status_text.success("🎉 Все загруженные демки успешно обработаны без фальшивых цифр!")
            
            # Переводим результат в текст
            final_json_string = json.dumps(all_matches_report, ensure_ascii=False, indent=2)
            
            st.success("✅ Твой объективный игровой отчет сформирован!")
            st.subheader("📋 Данные для ИИ-Тренера")
            st.markdown("Скопируй сгенерированный ниже код и отправь его мне в чат вместе с промптом тренера:")
            st.code(final_json_string, language="json")
