import os
from demoparser2 import DemoParser

def parse_uploaded_demo(uploaded_file, match_idx):
    """Глубокий экстрактор: правильно собирает тики и события матча без синтаксических ошибок"""
    temp_path = f"/tmp/uploaded_match_{match_idx}.dem" if os.path.exists("/tmp") else f"uploaded_match_{match_idx}.dem"
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        parser = DemoParser(temp_path)
        header = parser.parse_header()
        
        # Передаем список нужных полей напрямую в метод, как требует библиотека
        fields = ["tick", "X", "Y", "Z", "health", "player_name", "total_rounds_played"]
        ticks_df = parser.parse_ticks(fields)
        
        # Дополнительно берем логи смертей, чтобы зафиксировать оружие и хедшоты
        try:
            kills_df = parser.parse_events("player_death")
            kills_clean = kills_df.tail(100).to_dict(orient="records")
        except:
            kills_clean = []
            
        # Форматируем и уменьшаем размер для ИИ-чата
        ticks_clean = ticks_df.dropna(subset=["player_name"]).tail(300).to_dict(orient="records")
        
        parsed_data = {
            "match_id": match_idx,
            "map": header.get("map_name", "Unknown"),
            "total_ticks": header.get("total_ticks", 0),
            "player_ticks_sample": ticks_clean,
            "kills_sample": kills_clean
        }
        return parsed_data

    except Exception as e:
        raise Exception(f"Ошибка глубокого парсинга: {str(e)}")
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
