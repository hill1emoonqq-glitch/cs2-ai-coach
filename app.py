import streamlit as st
import json
from parser_logic import parse_uploaded_demo
from openai import OpenAI

# Настройка страницы
st.set_page_config(page_title="CS2 AI Match Analyst", page_icon="🎯")

st.title("🎯 Автономный ИИ-Аналитик CS2")
st.subheader("Честный расчет Premier Elo, разбор ошибок и план тренировок в один клик")

st.info("""
**Как это работает:** Загрузи файлы демок (.dem), которые ты скачал из Steam. 
Сайт сам извлечет более 100 скрытых параметров игры, передаст их ИИ-тренеру DeepSeek и сразу выведет готовый вердикт на эту страницу.
""")

# Поле для ввода ключа DeepSeek
api_key = st.text_input("🔑 Введи свой DeepSeek API Key:", type="password")
st.caption("Получить ключ и бесплатный баланс можно на сайте: https://deepseek.com")

st.markdown("### 📦 Шаг 1: Загрузка файлов матчей")
uploaded_files = st.file_uploader(
    "Перетащи файлы демок (.dem) сюда:", 
    type=["dem"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 7:
        st.warning("⚠️ Пожалуйста, выберите не более 7 файлов за один раз во избежание перегрузки сервера.")
    else:
        st.markdown(f"Выбрано файлов для анализа: **{len(uploaded_files)}**")
        
        st.markdown("### 🚀 Шаг 2: Запуск анализа")
        if st.button("🔥 Начать глубокий ИИ-анализ", type="primary", use_container_width=True):
            if not api_key:
                st.error("❌ Сначала введи свой DeepSeek API Key в поле выше, чтобы подключить ИИ-тренера!")
            else:
                all_matches_report = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 1. ПАРСИНГ ДЕМОК
                for idx, file in enumerate(uploaded_files, 1):
                    status_text.markdown(f"**⏳ Парсинг матча {idx}/{len(uploaded_files)}:** Сбор 100+ параметров из логов `{file.name}`...")
                    try:
                        match_data = parse_uploaded_demo(file, idx)
                        all_matches_report.append(match_data)
                        st.toast(f"Матч {file.name} успешно распарсен!", icon="✅")
                    except Exception as e:
                        st.error(f"❌ Ошибка парсинга файла {file.name}: {e}")
                        
                    progress_bar.progress(idx / len(uploaded_files))
                
                status_text.success("🎉 Все загруженные демки успешно распарсены! Данные готовы.")
                
                # Переводим логи матчей в строку
                final_json_string = json.dumps(all_matches_report, ensure_ascii=False, indent=2, default=str)
                
                # 2. ОТПРАВКА В ИИ (DEEPSEEK)
                with st.spinner("🤖 ИИ-Тренер DeepSeek изучает логи твоих матчей и составляет план тренировок..."):
                    try:
                        # Подключаемся к серверу DeepSeek
                        client = OpenAI(
                            api_key=api_key,
                            base_url="https://deepseek.com"
                        )
                        
                        prompt = f"""
                        Ты — профессиональный ИИ-аналитик и главный тренер по CS2 уровня Tier-1 команд. Твоя задача — провести жесткий, объективный и детальный аудит матчей на основе реальных данных из парсера демо-файла. Забудь про случайные числа, банальные советы и угадывание. Анализируй только предоставленный JSON-отчет.

                        Используй свою встроенную базу знаний по всем картам и всем режимам (Premier, Сompetitive, Wingman, DM).

                        Выдай структурированный ответ строго по следующим блокам:

                        1. 🎯 ОБЪЕКТИВНЫЙ РАСЧЕТ PREMIER ELO
                        - Рассчитай точный эквивалент Premier Elo за эти матчи на основе предоставленных метрик.
                        - Напиши текущий скилл-рейт игрока (например: 14,350 Elo, уровень Faceit 7). Объясни цифру на основе сухой статистики.

                        2. 📊 АНАЛИЗ ПО 100+ ПАРАМЕТРАМ (Главные аномалии)
                        Выдели критические проблемы и сильные стороны на основе данных: стрельба, эффективность гранат (Utility), позиционирование и тайминги разменов.

                        3. ⏳ ПЕРСОНАЛЬНАЯ 2-ЧАСОВАЯ ТРЕНИРОВКА
                        Составь пошаговое детальное расписание на 120 минут, нацеленное строго на исправление худших метрик из этих матчей. Укажи конкретные карты из мастерской, режимы и задачи (Aim, Prefire, Utility, DM).

                        4. 👁️ ЧЕТКИЕ ФОКУСЫ НА СЛЕДУЮЩИЕ МАТЧИ
                        Дай 3 тактических фокуса. На что именно обращать внимание в следующих играх, чтобы побеждать. Никакой воды.

                        Вот реальные данные моих матчей для анализа:
                        {final_json_string}
                        """
                        
                        # Запрос к быстрой и мощной модели deepseek-chat
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "user", "content": prompt}
                            ],
                            stream=False
                        )
                        
                        # Выводим ответ ИИ на страницу сайта
                        st.markdown("---")
                        st.subheader("📋 ВЕРДИКТ ИИ-ТРЕНЕРА И ПЛАН ТРЕНИРОВОК")
                        st.markdown(response.choices[0].message.content)
                        st.balloons()
                        
                    except Exception as ai_error:
                        st.error(f"❌ Ошибка при обращении к ИИ: {ai_error}. Проверь правильность API-ключа DeepSeek.")
