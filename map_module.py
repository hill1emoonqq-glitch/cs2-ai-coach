import streamlit as st
import pandas as pd
import numpy as np
import random

def show_page():
    st.title("🗺️ Интерактивная Карта Моментов и Анализ Пиков")
    st.write("ИИ-визуализация пространственных логов демки. Разбор векторов дуэлей и типов перемещения.")

    # Выбор карты для отображения координатной сетки
    selected_map = st.selectbox("Выбери карту для наложения логов координат:", ["de_mirage", "de_inferno", "de_ancient", "de_anubis"])
    
    st.markdown("---")
    st.markdown(f"### 📍 Интерактивная 2D-Карта Позиционирования ({selected_map})")
    st.write("Красные точки — твои смерти (десинхронизация осей), Зеленые — твои фраги и Entry-киллы.")

    # Генерируем случайную, но реалистичную для 1920x1440 координатную сетку фраг-зоны
    # Имитируем реальный парсинг координат X и Y из демки
    np.random.seed(42)
    frag_count = random.randint(15, 25)
    death_count = random.randint(10, 18)
    
    # Координаты для Mirage (Мидл, А-плент, Б-аппсы)
    frag_x = np.random.uniform(-1500, 1500, frag_count)
    frag_y = np.random.uniform(-1000, 1200, frag_count)
    
    death_x = np.random.uniform(-1300, 1400, death_count)
    death_y = np.random.uniform(-900, 1100, death_count)

    # Создаем DataFrame для встроенной интерактивной карты Streamlit
    # Масштабируем под координаты карты CS2
    df_frags = pd.DataFrame({'x': frag_x, 'y': frag_y, 'Тип': 'Твой Фраг'})
    df_deaths = pd.DataFrame({'x': death_x, 'y': death_y, 'Тип': 'Твоя Смерть'})
    df_map_data = pd.concat([df_frags, df_deaths])

    # Отрисовываем интерактивный Scatter-график (заменяет статичную картинку)
    # Игрок может зумить, двигать и кликать на точки!
    st.scatter_chart(
        df_map_data,
        x='x',
        y='y',
        color='Тип',
        size=80,
        height=450,
        use_container_width=True
    )
    st.caption("💡 Подсказка ИИ: Наведи мышь на точку или прокрути колесико, чтобы приблизить конкретную зону (Мидл / Плент) и увидеть вектор смещения твоей модели.")

    # --- АНАЛИЗ ТИПОВ ИСПОЛЬЗОВАННЫХ ПИКОВ ---
    st.markdown("---")
    st.markdown("### 🏹 АНАЛИТИКА ПИКОВ И ВЫЛЕТОВ ИЗ-ЗА УГЛОВ")
    st.write("Статистика того, как именно ты пересекал линию обзора врага при выходе из-за укрытий стены:")

    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("<div style='background-color:#12161A; padding:15px; border-radius:4px; border-left:4px solid #FF5500;'><h4>🏃‍♂️ Широкий стрейф (4:3 Max Velocity)</h4><b>Реализовано: 18 раз</b><br>Эффективность дуэлей: 72%<br><span style='color:#00FF66;'>ИИ-Вердикт: Идеально используешь визуальную скорость растянутого разрешения 4:3. Враги на дальних дистанциях мажут.</span></div>", unsafe_allow_html=True)
        
    with col_p2:
        st.markdown("<div style='background-color:#12161A; padding:15px; border-radius:4px; border-left:4px solid #FF3344;'><h4>🎯 Выход на префайре (Wall Alignment)</h4><b>Реализовано: 12 раз</b><br>Эффективность дуэлей: 33%<br><span style='color:#FF3344;'>ИИ-Вердикт: Ошибка! Из-за eDPI 1760 ты вылетаешь слишком далеко от ребра стены ( Wall Clearance = 42 пикселя). Твой прицел режет пустоту, давая врагу время на размен.</span></div>", unsafe_allow_html=True)
        
    with col_p3:
        st.markdown("<div style='background-color:#12161A; padding:15px; border-radius:4px; border-left:4px solid #3B82F6;'><h4>🛡️ Пассивный прием (Angle Advantage)</h4><b>Реализовано: 9 раз</b><br>Эффективность дуэлей: 55%<br><span style='color:#3B82F6;'>ИИ-Вердикт: Допустимо. Ты держишь грамотную высоту каски, но прижимаясь в упор к стене, выдаешь свое плечо на 120 мс раньше.</span></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏅 ЗОНА РЕКОРДОВ НА ЭТОЙ КАРТЕ")
    st.success(f"🏆 **Личный рекорд побит!** На карте `{selected_map}` в этой катке ты показал самое минимальное время гашения остаточной скорости при Counter-Strafing — всего **12 тиков** до чистой остановки. Это твой лучший результат за последние 15 матчей в базе памяти!")
