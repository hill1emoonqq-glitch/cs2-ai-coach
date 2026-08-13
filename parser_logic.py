import os
from demoparser2 import DemoParser

def parse_uploaded_demo(uploaded_file, match_idx):
    """Глубокий экстрактор: безошибочно собирает тики и события матча с диска"""
    temp_path = f"/tmp/uploaded_match_{match_idx}.dem" if os.path.exists("/tmp") else f"uploaded_match_{match_idx}.dem"
    
    try:
        # Записываем файл на диск сервера мелкими кусками
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        parser = DemoParser(temp_path)
        header = parser.parse_header()
        
        # Запрашиваем базовые поля тиков напрямую списком
        fields = ["tick", "X", "Y", "Z", "health", "player_name", "total_rounds_played"]
        ticks_df = parser.parse_ticks(fields)
        
        # Собираем логи игровых событий смертей (для подсчета K/D и HS)
        try:
            kills_df = parser.parse_events("player_death")
            kills_clean = kills_df.tail(100).to_dict(orient="records")
        except:
            kills_clean = []
            
        # Очищаем от пустых значений и берем последние тики для оптимизации объема
        ticks_clean = ticks_df.dropna(subset=["player_name"]).tail(400).to_dict(orient="records")
        
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
        # Жестко зачищаем диск сервера после каждого шага
        if os.path.exists(temp_path):
            os.remove(temp_path)
