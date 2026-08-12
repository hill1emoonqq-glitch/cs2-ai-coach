import streamlit as st
import random

def show_page():
    st.title("🤖 Модуль управления Steam-Ботом и Рекордами")
    st.write("Синхронизация с аккаунтом Steam. Настройка автоматических уведомлений после каток и архивация глобальных рекордов.")

    st.markdown("### 🔌 СТАТУС ПОДКЛЮЧЕНИЯ ИИ-БОТА")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        steam_id = st.text_input("Введи свой SteamID64 для привязки бота:", "76561198000000000")
    with col_b2:
        bot_status = st.selectbox("Статус уведомлений бота:", ["Включен (Авто-отчет)", "Отключен"])

    if st.button("🤖 СИМУЛИРОВАТЬ ОТВЕТ БОТА ПОСЛЕ МАТЧА"):
        st.success("🤖 Сообщение успешно сгенерировано и улетело на твой Steam-аккаунт!")
        st.markdown(f"""
        <div style='background-color:#161C24; padding:20px; border-radius:6px; border: 1px solid #FF5500; font-family: monospace;'>
            <b style='color:#FF5500;'>[🤖 CS2 AI Coach Bot]:</b> Катка завершена! Демка автоматически спарсена облаком.<br><br>
            Привет, <b>Gamer</b>! Я оценил твою игру. Твой HLTV рейтинг в этом матче составил: <span style='color:#00FF66; font-weight:bold;'>1.32</span>.<br><br>
            🏆 <b>ГЛАВНЫЕ РЕКОРДЫ ЭТОГО МАТЧА:</b><br>
            • 🎯 <b>Аим-Рекорд:</b> Время разворота на 180° составило рекордные <b>82 мс</b>! Это уровень Тир-1 Про (Параметр №11).<br>
            • 🔀 <b>Рекорд Трекинга:</b> Роботизированный мульти-трансфер прицела в упоре Б-плента выполнен без единого лишнего пикселя.<br>
            • 💰 <b>Экономика:</b> Закупка во фризтайме выполнена за <b>0.95 секунды</b> — абсолютная доминация по скорости на сервере.<br><br>
            ⚠️ <b>КРИТИЧЕСКИЙ СБОЙ ПО ХАРАКТЕРИСТИКАМ:</b><br>
            • Твой eDPI 1760 выдал оверфлик по оси X в 74% дуэлей на дистанции! Прицел трясется при зуме AWP. Снижай сенсу до <b>1.45</b>!<br><br>
            🔗 <a href='#' style='color:#3B82F6; font-weight:bold;'>КЛИКНИ СЮДА, ЧТОБЫ ПЕРЕЙТИ НА САЙТ И ПОСМОТРЕТЬ ВСЕ РЕКОРДЫ И 100 ПАРАМЕТРОВ</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏆 ТВОЙ ГЛОБАЛЬНЫЙ ЗАЛ СЛАВЫ (РЕКОРДЫ НА КАРТАХ)")
    
    col_rec1, col_rec2, col_rec3 = st.columns(3)
    with col_rec1:
        st.markdown("<div style='background-color:#0D1017; padding:15px; border-radius:4px; border-left:4px solid #00FF66;'><h4 style='margin:0; font-size:16px;'>🎯 РЕКОРД АИМА (Aim Botz)</h4><p style='font-size:24px; font-weight:bold; color:#FFF; margin:5px 0;'>165 мс</p><span style='font-size:12px; color:#94A3B8;'>Минимальное время до первого выстрела (TTFS)</span></div>", unsafe_allow_html=True)
    with col_rec2:
        st.markdown("<div style='background-color:#0D1017; padding:15px; border-radius:4px; border-left:4px solid #00FF66;'><h4 style='margin:0; font-size:16px;'>🏃‍♂️ РЕКОРД СТРЕЙФА (de_mirage)</h4><p style='font-size:24px; font-weight:bold; color:#FFF; margin:5px 0;'>12 тиков</p><span style='font-size:12px; color:#94A3B8;'>Идеальная остановка Counter-Strafing</span></div>", unsafe_allow_html=True)
    with col_rec3:
        st.markdown("<div style='background-color:#0D1017; padding:15px; border-radius:4px; border-left:4px solid #00FF66;'><h4 style='margin:0; font-size:16px;'>💣 РЕКОРД КЛАТЧЕЙ (de_inferno)</h4><p style='font-size:24px; font-weight:bold; color:#FFF; margin:5px 0;'>1v4 TAKE</p><span style='font-size:12px; color:#94A3B8;'>100% изоляция дуэлей под прессингом</span></div>", unsafe_allow_html=True)
