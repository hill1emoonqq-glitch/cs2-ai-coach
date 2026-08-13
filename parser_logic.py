import os
from demoparser2 import DemoParser

def parse_uploaded_demo(uploaded_file, match_idx):
    """Глубокий экстрактор: вытаскивает точные координаты, оружие, хедшоты и урон по миллиметрам"""
    temp_path = f"/tmp/uploaded_match_{match_idx}.dem" if os.path.exists("/tmp") else f"uploaded_match_{match_idx}.dem"
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        parser = DemoParser(temp_path)
        header = parser.parse_header()
        
        # ИСПРАВЛЕНО: используем аргумент selected_columns вместо columns
        # 1. Вытаскиваем детальные логи убийств (с оружием, хедшотами и координатами)
        kills_df = parser.parse_ticks([
            "player_death"
        ], selected_columns=[
            "tick", "attacker_name", "attacker_steamid", 
            "user_name", "user_steamid", "weapon", "headshot",
            "attacker_x", "attacker_y", "attacker_z",
            "user_x", "user_y", "user_z"
        ])
        
        # 2. Вытаскиваем детальные логи урона (куда попал, сколько снёс)
        damage_df = parser.parse_ticks([
            "player_hurt"
        ], selected_columns=[
            "tick", "attacker_name", "user_name", "dmg_health", "hitgroup", "weapon"
        ])

        # Фильтруем пустые значения и берем последние события матча для ИИ-анализа
        kills_clean = kills_df.dropna(subset=["attacker_name", "user_name"]).tail(150).to_dict(orient="records")
        damage_clean = damage_df.dropna(subset=["attacker_name", "user_name"]).tail(300).to_dict(orient="records")
        
        parsed_data = {
            "match_id": match_idx,
            "map": header.get("map_name", "Unknown"),
            "total_ticks": header.get("total_ticks", 0),
            "kills_detailed": kills_clean,
            "damage_detailed": damage_clean
        }
        return parsed_data

    except Exception as e:
        raise Exception(f"Ошибка глубокого парсинга: {str(e)}")
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
