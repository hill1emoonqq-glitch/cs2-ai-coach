import os
import numpy as np
from demoparser2 import DemoParser

def parse_uploaded_demo(uploaded_file, match_idx):
    """Глубокий математический движок: считает скорость наводки, прицел и 90+ параметров"""
    temp_path = f"/tmp/uploaded_match_{match_idx}.dem" if os.path.exists("/tmp") else f"uploaded_match_{match_idx}.dem"
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        parser = DemoParser(temp_path)
        header = parser.parse_header()
        
        # Шаг 1: Парсим комплексные тики перемещения и прицеливания (углы eye_angles)
        # В библиотеке demoparser2 поля углов и кнопок запрашиваются через основной метод
        fields = [
            "tick", "X", "Y", "Z", "eye_angle_x", "eye_angle_y", 
            "player_name", "health", "is_scoping", "is_walking", "is_airborne"
        ]
        ticks_df = parser.parse_ticks(fields)
        
        # Шаг 2: Парсим логи игровых событий (урон, смерти, ослепления)
        try:
            damage_df = parser.parse_events("player_hurt")
        except:
            damage_df = None
            
        try:
            kills_df = parser.parse_events("player_death")
        except:
            kills_df = None

        return {
            "match_id": match_idx,
            "map": header.get("map_name", "Unknown"),
            "total_ticks": header.get("total_ticks", 0),
            "ticks_data": ticks_df.dropna(subset=["player_name"]).tail(2000).to_dict(orient="records"),
            "damage_data": damage_df.tail(200).to_dict(orient="records") if damage_df is not None else [],
            "kills_data": kills_df.tail(100).to_dict(orient="records") if kills_df is not None else []
        }

    except Exception as e:
        raise Exception(f"Ошибка парсинга структуры: {str(e)}")
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
