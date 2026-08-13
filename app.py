import os
from demoparser2 import DemoParser

def parse_uploaded_demo(uploaded_file, match_idx):
    """Принимает файл из интерфейса Streamlit, сохраняет на диск сервера и парсит"""
    # Создаем временный путь на сервере GitHub
    temp_path = f"/tmp/uploaded_match_{match_idx}.dem" if os.path.exists("/tmp") else f"uploaded_match_{match_idx}.dem"
    
    try:
        # Записываем загруженный файл на диск сервера небольшими кусками
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Запускаем быстрый парсер на Rust
        parser = DemoParser(temp_path)
        header = parser.parse_header()
        
        parsed_data = {
            "match_id": match_idx,
            "map": header.get("map_name", "Unknown"),
            "total_ticks": header.get("total_ticks", 0),
            
            # Собираем только самые важные логи игровых событий для ИИ
            "kills": parser.parse_ticks(["player_death"]),
            "damage": parser.parse_ticks(["player_hurt"]),
            "grenades": parser.parse_ticks(["smokegrenade_detonate", "flashbang_detonate", "hegrenade_detonate"]),
            "blind": parser.parse_ticks(["player_blind"]),
            "shots": parser.parse_ticks(["weapon_fire"])
        }
        return parsed_data

    except Exception as e:
        raise Exception(f"Ошибка парсинга файла: {str(e)}")
        
    finally:
        # Жестко удаляем файл, чтобы не забить оперативную память сервера
        if os.path.exists(temp_path):
            os.remove(temp_path)
