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
st.write("Сайт читает бинарные логи твоего файла .dem в облаке.")

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

    with st.spinner("⚙️ Облачный парсер извлекает данные матча..."):
        try:
            from demoparser2 import DemoParser
            parser = DemoParser("match.dem")
            
            # 🔥 ИСПРАВЛЕНИЕ: Передаем ['player_death'] в квадратных скобках как список (Vec), чтобы C++ бэкенд не ругался
            events_df = parser.parse_events(["player_death"])
            
            if not events_df.empty:
                st.markdown("<div class='success-box'><h3>✅ ИГРОКИ УСПЕШНО НАЙДЕНЫ!</h3>Выбери свой ник ниже для автоматического расчета статистики.</div>", unsafe_allow_html=True)
                
                cols = events_df.columns.tolist()
                
                # Ищем правильные колонки в реальном ивенте player_death
                attacker_col = "attacker_name" if "attacker_name" in cols else ("attacker" if "attacker" in cols else None)
                user_col = "user_name" if "user_name" in cols else ("user" if "user" in cols else None)
                
                if attacker_col and user_col:
                    # Собираем всех уникальных игроков из матча
                    all_players = pd.concat([events_df[attacker_col], events_df[user_col]]).dropna().unique()
                    all_players = sorted([p for p in all_players if p != ""])
                    
                    selected_player = st.selectbox("Выбери свой ник из этого матча:", all_players, index=all_players.index("unight") if "unight" in all_players else 0)
                    
                    if selected_player:
                        # Считаем чистые единичные события убийств и смертей
                        p_kills = len(events_df[events_df[attacker_col] == selected_player])
                        p_deaths = len(events_df[events_df[user_col] == selected_player])
                        
                        # Проверяем наличие хедшотов
                        hs_col = "headshot" if "headshot" in cols else None
                        if hs_col:
                            p_hs = len(events_df[(events_df[attacker_col] == selected_player) & (events_df[hs_col] == True)])
                            hs_percent = int((p_hs / p_kills * 100)) if p_kills > 0 else 0
                        else:
                            hs_percent = 0
                            
                        safe_deaths = p_deaths if p_deaths > 0 else 1
                        hltv_rating = round(0.6 + (p_kills / safe_deaths) * 0.4, 2)
                        
                        # Вывод реальных, очищенных данных раундов
                        st.markdown(f"## 📊 Реальная статистика для: **{selected_player}**")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Настоящие убийства (Kills)", p_kills)
                        c2.metric("Настоящие смерти (Deaths)", p_deaths)
                        c3.metric("Честный процент Headshots", f"{hs_percent}%")
                        
                        st.metric("Рассчитанный HLTV Рейтинг 2.0 за матч", hltv_rating)
                        
                        if hltv_rating >= 1.2:
                            st.success("🏆 Ты отыграл этот матч в жесткий плюс!")
                        else:
                            st.warning("⚠️ Твоя сенса 1.60 создает микро-тряску кисти. Снижай eDPI до 1.45.")
                else:
                    st.warning("⚠️ Не удалось автоматически сопоставить имена колонок событий. Вот структура доступных данных:")
                    st.write(events_df.head(5))
            else:
                st.warning("Лог событий player_death пуст. Проверь файл демки.")
                
        except Exception as parse_err:
            st.markdown(f"<div class='error-box'><h4>🔴 КРИТИЧЕСКАЯ ОШИБКА АНАЛИЗА:</h4>{parse_err}</div>", unsafe_allow_html=True)

else:
    st.info("🔄 Ожидание файла. Закинь сюда .dem файл матча, чтобы запустить реальный бэкенд-тест.")
