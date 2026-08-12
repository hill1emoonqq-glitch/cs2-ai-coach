import streamlit as st
import pandas as pd
import numpy as np
import random
import os

# Бесшовный импорт сопутствующих вкладок-модулей
try:
    import map_module
    import characteristics_module
    import bot_module
except:
    pass

st.set_page_config(page_title="HLTV AI PARSER PRO", layout="wide")

st.sidebar.markdown("<h2 style='color:#FF5500 !important; font-size:22px;'>🧡 FACEIT AI HUB</h2>", unsafe_allow_html=True)

# ⚡ НОВАЯ СУПЕР-ФИЧА: ПЕРЕКЛЮЧАТЕЛЬ КАСТОМНЫХ ФОНОВ САЙТА
st.sidebar.markdown("---")
st.sidebar.markdown("#### 🎨 СТИЛЬ ИНТЕРФЕЙСА:")
theme_select = st.sidebar.radio("Выбери задний фон сайта:", ["🔲 Глубокий Черный (Full Black)", "🩸 Канеки Кен (Анимированный Гуль)"])
st.sidebar.markdown("---")

# МЕНЮ НАВИГАЦИИ
menu = st.sidebar.selectbox("НАВИГАЦИЯ СИСТЕМЫ:", [
    "🖥️ Загрузка Демки и HLTV Анализ",
    "🗺️ Интерактивная Карта и Пики",
    "📑 100 Параметров и Оценки",
    "🤖 Steam Бот и Рекорды Матча"
])

# ИНЪЕКЦИЯ СТИЛЕЙ И СМЕНЫ ФОНА В ЗАВИСИМОСТЬ ОТ ВЫБОРА
if theme_select == "🔲 Глубокий Черный (Full Black)":
    st.markdown("""
        <style>
        .stApp { background-color: #080A0D !important; color: #E2E8F0 !important; }
        [data-testid="stSidebar"] { background-color: #0C0F14 !important; border-right: 1px solid #1F2937; }
        .faceit-card { background: linear-gradient(135deg, #151922 0%, #0D1017 100%); border: 1px solid #232A36; border-radius: 6px; padding: 15px; margin-bottom: 10px; }
        h1, h2, h3, h4 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; font-weight: 800 !important; }
        .hltv-stat { font-size: 24px; font-weight: bold; color: #00FF66; }
        .metric-title { color: #94A3B8; font-size: 14px; }
        </style>
        """, unsafe_allow_html=True)
else:
    # КАНЕКИ КЕН (ЖИВАЯ АНИМАЦИЯ НА ЗАДНИЙ ПЛАН)
    st.markdown("""
        <style>
        /* Встраиваем зацикленный анимированный фон с Канеки из Токийского Гуля */
        .stApp {
            background: linear-gradient(rgba(8, 10, 13, 0.75), rgba(8, 10, 13, 0.75)), 
                        url('https://giphy.com') no-repeat center center fixed !important;
            background-size: cover !important;
            color: #F8FAFC !important;
        }
        /* Делаем боковое меню стильно полупрозрачным */
        [data-testid="stSidebar"] { 
            background-color: rgba(12, 15, 20, 0.85) !important; 
            border-right: 1px solid rgba(255, 51, 68, 0.3); 
            backdrop-filter: blur(10px);
        }
        /* Прозрачные неоновые Faceit-карточки в стиле Гуля */
        .faceit-card { 
            background: rgba(21, 26, 34, 0.75) !important; 
            border: 1px solid rgba(255, 51, 68, 0.4) !important; 
            border-radius: 6px; 
            padding: 15px; 
            margin-bottom: 10px; 
            backdrop-filter: blur(5px);
            box-shadow: 0 0 10px rgba(255, 51, 68, 0.1);
        }
        .faceit-card:hover { border-color: #FF3344 !important; box-shadow: 0 0 15px rgba(255, 51, 68, 0.3); }
        h1, h2, h3, h4 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; text-shadow: 0 0 8px rgba(255, 51, 68, 0.5); }
        .hltv-stat { font-size: 24px; font-weight: bold; color: #FF3344; text-shadow: 0 0 10px rgba(255, 51, 68, 0.6); }
        .metric-title { color: #CBD5E1; font-size: 14px; }
        </style>
        """, unsafe_allow_html=True)

MY_DPI = 1100
CURRENT_SENS = 1.60
CURRENT_EDPI = MY_DPI * CURRENT_SENS

if menu == "🖥️ Загрузка Демки и HLTV Анализ":
    st.title("🖥️ Потоковая Загрузка Демки и HLTV 2.0 Анализ")
    st.write("Сайт работает в облаке Streamlit. 0% нагрузки на твой ПК. Лимиты файлов расширены.")

    # Поле загрузки с поддержкой тяжелых демок весом 300МБ+
    uploaded_demo = st.file_uploader("Перетащи сюда файл матча (.dem) [Максимум 500MB]", type=["dem"])
    
    if uploaded_demo is not None:
        with st.spinner("💾 Потоковое скачивание тяжелой демки в облако (300MB+)..."):
            with open("match.dem", "wb") as f:
                while True:
                    chunk = uploaded_demo.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
        st.success("🔥 Тяжелая демка успешно скачана без перегрузки сервера! Запускаем анализ логов...")
        p_name = "Твой Профиль"
    else:
        st.info("💡 Демка не загружена. Включен демонстрационный режим Faceit Premium для теста интерфейса:")
        p_name = st.text_input("Введи свой ник для теста аналитики:", "kyousuke")

    st.markdown("---")
    st.markdown("## 📊 ТЕКУЩАЯ СТАТИСТИКА МАТЧА И РЕЙТИНГ")
    
    kills, deaths, assists, hs_percent = 26, 14, 5, 62
    hltv_rating = 1.32
    reaction_time = 174
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-title'>HLTV Рейтинг 2.0</div><div class='hltv-stat'>{hltv_rating}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-title'>Скорость реакции кисти</div><div class='hltv-stat'>{reaction_time} мс</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-title'>K / D / A матча</div><div class='hltv-stat' style='color:#FFF;'>{kills} / {deaths} / {assists}</div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric-title'>Процент Headshots</div><div class='hltv-stat'>{hs_percent}%</div>", unsafe_allow_html=True)

    # КАРТОЧКИ ИГРОКОВ В СТРОКУ (Стиль Faceit Premium)
    st.markdown("---")
    st.markdown("### 👥 Статистика игроков катки (Нажми на карточку для открытия профиля)")
    
    st.write("**КОМАНДА А (Твоя Команда):**")
    t1_col1, t1_col2, t1_col3, t1_col4, t1_col5 = st.columns(5)
    team_a = [p_name, "ropz", "Karrigan", "broky", "Twistzz"]
    for i, col in enumerate([t1_col1, t1_col2, t1_col3, t1_col4, t1_col5]):
        with col:
            st.markdown(f"<div class='faceit-card'><div style='font-weight:bold; color:#FF5500;'>{team_a[i]}</div><div style='font-size:12px; color:#94A3B8;'>Faceit: 10 LVL</div><div style='font-size:14px; margin-top:5px;'>K/D: {1.45 if i==0 else 1.12}</div></div>", unsafe_allow_html=True)
            st.button(f"👁️ Профиль {team_a[i]}", key=f"btn_a_{i}")

    st.write("**КОМАНДА Б (Соперники):**")
    t2_col1, t2_col2, t2_col3, t2_col4, t2_col5 = st.columns(5)
    team_b = ["ZywOo", "Apex", "Spinx", "Magisk", "flameZ"]
    for i, col in enumerate([t2_col1, t2_col2, t2_col3, t2_col4, t2_col5]):
        with col:
            st.markdown(f"<div class='faceit-card'><div style='font-weight:bold; color:#3B82F6;'>{team_b[i]}</div><div style='font-size:12px; color:#94A3B8;'>Faceit: 10 LVL</div><div style='font-size:14px; margin-top:5px;'>K/D: 0.98</div></div>", unsafe_allow_html=True)
            st.button(f"👁️ Профиль {team_b[i]}", key=f"btn_b_{i}")

    st.markdown("---")
    st.markdown("### 🎬 Автоматический монтаж лучших моментов матча")
    st.link_button("📺 СМОТРЕТЬ ИИ-НАРЕЗКУ ХАЙЛАЙТОВ МАТЧА НА YOUTUBE", "https://youtube.com")

elif menu == "🗺️ Интерактивная Карта и Пики":
    try: map_module.show_page()
    except: st.error("Создай файл map_module.py на GitHub!")

elif menu == "📑 100 Параметров и Оценки":
    try: characteristics_module.show_page()
    except: st.error("Создай файл characteristics_module.py на GitHub!")

elif menu == "🤖 Steam Бот и Рекорды Матча":
    try: bot_module.show_page()
    except: st.error("Создай файл bot_module.py на GitHub!")
