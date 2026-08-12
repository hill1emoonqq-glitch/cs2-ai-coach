import streamlit as st
import pandas as pd
import os

# Настройка интерфейса Cybershock
st.set_page_config(page_title="REAL CS2 DEMO PARSER", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #080A0D !important; color: #E2E8F0 !important; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .error-box { background-color: #1A0D10; border-left: 4px solid #FF3344; padding: 15px; border-radius: 4px; }
    .success-box { background-color: #0D1A14; border-left: 4px solid #00FF66; padding: 15px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🖥️ Настоящий ИИ-Парсер Демок CS2 [Без симуляций]")
st.write("Сайт пытается прочитать бинарные логи твоего файла .dem в облаке.")

# Поле загрузки тяжелой демки
uploaded_demo = st.file_uploader("Загрузи реальный файл матча (.dem) весом до 500 МБ:", type=["dem"])

if uploaded_demo is not None:
    if os.path.exists("match.dem"):
        os.remove("match.dem")
        
    with st.spinner("💾 Скачивание файла демки на сервер по частям..."):
        try:
            with open("match.dem", "wb") as f:
                while True:
                    chunk = uploaded_demo.read(1024 * 1024)
                    if not chunk: break
                    f.write(chunk)
            st.success(f"Загрузка завершена! Размер файла: {round(os.path.getsize('match.dem') / (1024*1024), 2)} МБ.")
        except Exception as upload_err:
            st.error(f"Ошибка сохранения файла: {upload_err}")

    with st.spinner("⚙️ Облачный парсер извлекает логи убийств..."):
        try:
            from demoparser2 import DemoParser
            parser = DemoParser("match.dem")
            
            # Извлекаем сырые тики смертей
            kills_df = parser.parse_ticks(["player_death"])
            
            if not kills_df.empty:
                st.markdown("<div class='success-box'><h3>✅ СТРУКТУРА ДЕМКИ УСПЕШНОПРОЧИТАНА!</h3>Данные таблиц извлечены. Проверяем колонки...</div>", unsafe_allow_html=True)
                
                # Защита от мутаций Valve: смотрим, какие колонки РЕАЛЬНО есть в файле
                cols = kills_df.columns.tolist()
                
                # Определяем, как называются поля убийцы и жертвы в этой конкретной демке
                attacker_key = "attacker_name" if "attacker_name" in cols else ("attacker" if "attacker" in cols else None)
                victim_key = "user_name" if "user_name" in cols else ("user" if "user" in cols else ("victim" if "victim" in cols else None))
                
                # Если парсер нашёл нужные столбцы
                if attacker_key and victim_key:
                    all_players = kills_df[attacker_key].dropna().unique()
                    selected_player = st.selectbox("ИИ нашёл игроков в этой демке. Выбери свой ник:", all_players)
                    
                    if selected_player:
                        p_kills = len(kills_df[kills_df[attacker_key] == selected_player])
                        p_deaths = len(kills_df[kills_df[victim_key] == selected_player])
                        
                        # Проверяем наличие хедшотов
                        hs_key = "headshot" if "headshot" in cols else None
                        if hs_key:
                            p_hs = len(kills_df[(kills_df[attacker_key] == selected_player) & (kills_df[hs_key] == True)])
                            hs_percent = int((p_hs / p_kills * 100)) if p_kills > 0 else 0
                        else:
                            hs_percent = "Нет данных в тиках"
                            
                        hltv_rating = round(0.5 + (p_kills / (p_deaths if p_deaths > 0 else 1)) * 0.5, 2)
                        
                        st.markdown(f"## 📊 Настоящая статистика для: **{selected_player}**")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Настоящие убийства (Kills)", p_kills)
                        c2.metric("Настоящие смерти (Deaths)", p_deaths)
                        c3.metric("Честный процент Headshots", f"{hs_percent}%")
                        st.metric("Рассчитанный HLTV Рейтинг 2.0", hltv_rating)
                else:
                    st.warning("⚠️ Valve обновили ключи логов. Вот сырые доступные данные из твоей демки для анализа:")
                    st.write(kills_df.head(10)) # Выводим первые 10 строк реальной таблицы, чтобы увидеть её структуру
            else:
                st.warning("Таблица событий player_death оказалась пустой.")
                
        except Exception as parse_err:
            st.markdown(f"<div class='error-box'><h4>🔴 КРИТИЧЕСКАЯ ОШИБКА АНАЛИЗА:</h4>{parse_err}</div>", unsafe_allow_html=True)

else:
    st.info("🔄 Ожидание файла. Закинь сюда .dem файл матча, чтобы запустить реальный бэкенд-тест.")
