import os
from demoparser2 import DemoParser

def parse_uploaded_demo(uploaded_file, match_idx):
    """Экстрактор: собирает чистые логи событий матча без кривых внутренних расчетов"""
    temp_path = f"/tmp/uploaded_match_{match_idx}.dem" if os.path.exists("/tmp") else f"uploaded_match_{match_idx}.dem"
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        parser = DemoParser(temp_path)
        header = parser.parse_header()
        
        # Собираем чистые логи смертей (кто, кого, куда, из чего, хедшот ли)
        try:
            kills_df = parser.parse_events("player_death")
            kills_clean = kills_df.tail(150).to_dict(orient="records")
        except:
            kills_clean = []
            
        # Собираем чистые логи нанесенного урона
        try:
            hurt_df = parser.parse_events("player_hurt")
            hurt_clean = hurt_df.tail(200).to_dict(orient="records")
        except:
            hurt_clean = []
            
        # Запрашиваем базовые тики для фиксации раундов и координат
        try:
            fields = ["tick", "X", "Y", "Z", "player_name", "total_rounds_played"]
            ticks_df = parser.parse_ticks(fields)
            ticks_clean = ticks_df.dropna(subset=["player_name"]).tail(500).to_dict(orient="records")
        except:
            ticks_clean = []
        
        return {
            "match_id": match_idx,
            "map": header.get("map_name", "Unknown"),
            "total_ticks": header.get("total_ticks", 0),
            "kills_log": kills_clean,
            "damage_log": hurt_clean,
            "position_ticks": ticks_clean
        }

    except Exception as e:
        raise Exception(f"Ошибка сбора данных: {str(e)}")
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
