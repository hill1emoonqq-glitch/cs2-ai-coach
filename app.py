import streamlit as st
import json
import os
import bz2
from parser_logic import parse_uploaded_demo

# Настройка страницы
st.set_page_config(page_title="CS2 Core Data Extractor", page_icon="🎯", layout="centered")

st.title("🎯 ИИ-Аналитик матчей CS2 (Экстрактор логов)")
st.subheader("Сбор честных параметров игры для ручного ИИ-аудита")

st.info("""
**Финальный режим:** Сайт принимает файлы как в формате архива `.bz2` (прямо из Steam), так и распакованные `.dem`. 
Система сама всё распакует, соберет параметры и подготовит файл для ИИ!
""")

# ИСПРАВЛЕНО: Теперь в type разрешены и dem, и bz2 файлы!
uploaded_files = st.file_uploader(
    "Перетащите файлы демок (.dem или .dem.bz2) сюда:", 
    type=["dem", "bz2"], 
    accept_multiple_files=True
)

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
                    # Если файл загружен в формате .bz2, распаковываем его на сервере перед парсингом
                    if file.name.endswith(".bz2"):
                        status_text.markdown(f"**📦 Распаковка архива {idx}/{len(uploaded_files)}...**")
                        temp_dem_name = f"extracted_match_{idx}.dem"
                        
                        # Безопасная распаковка bz2 мелкими кусками на диск сервера
                        decompressor = bz2.BZ2Decompressor()
                        with open(temp_dem_name, "wb") as f_out:
                            # Читаем загруженный bz2 файл блоками
                            file_bytes = file.read()
                            decompressed_data = decompressor.decompress(file_bytes)
                            f_out.write(decompressed_data)
                        
                        # Передаем распакованный файл в парсер, подменив объект загрузки
                        class MockFile:
                            def __init__(self, path): self.path = path
                            def getbuffer(self):
                                with open(self.path, "rb") as f: return f.read()
                        
                        mock_file = MockFile(temp_dem_name)
                        match_data = parse_uploaded_demo(mock_file, idx)
                        
                        # Чистим временный распакованный файл
                        if os.path.exists(temp_dem_name):
                            os.remove(temp_dem_name)
                    else:
                        # Если файл уже чистый .dem, парсим напрямую
                        match_data = parse_uploaded_demo(file, idx)
                        
                    all_matches_report.append(match_data)
                    st.toast(f"Файл {file.name} успешно обработан!", icon="✅")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка при обработке файла {file.name}: {e}")
                    
                progress_bar.progress(idx / len(uploaded_files))
                
            status_text.success("🎉 Логи матчей успешно извлечены без фальшивых цифр!")
            
            # Перевод данных в JSON-строку БЕЗ ОШИБОК
            final_json_string = json.dumps(all_matches_report, ensure_ascii=False, indent=2, default=str)
            
            st.success("✅ Твой объективный игровой отчет полностью сформирован!")
            st.markdown("### 📥 Шаг 3: Скачай отчет для ИИ")
            
            st.download_button(
                label="📥 Скачать файл отчета (cs2_report.json)",
                data=final_json_string,
                file_name="cs2_report.json",
                mime="application/json",
                use_container_width=True
            )
