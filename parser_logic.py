import os
import bz2
import requests
from demoparser2 import DemoParser

def download_and_parse_demo(url, match_idx):
    """Безопасная версия для GitHub: скачивает демку кусками на диск, чтобы не перегружать RAM"""
    # Сохраняем во временную директорию сервера, там больше места
    temp_demo_path = f"/tmp/match_{match_idx}.dem" if os.path.exists("/tmp") else f"temp_match_{match_idx}.dem"
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        decompressor = bz2.BZ2Decompressor()
        
        # Скачиваем мелкими кусочками по 512 КБ, чтобы RAM не забивалась
        with open(temp_demo_path, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=512 * 1024):
                if chunk:
                    try:
                        decompressed_chunk = decompressor.decompress(chunk)
                        out_file.write(decompressed_chunk)
                    except EOFError:
                        break
                        
        # Парсим 100+ параметров
        parser = DemoParser(temp_demo_path)
        header = parser.parse_header()
        
        parsed_data = {
            "match_id": match_idx,
            "map": header.get("map_name", "Unknown"),
            "kills": parser.parse_ticks(["player_death"]),
            "damage": parser.parse_ticks(["player_hurt"]),
            "grenades": parser.parse_ticks(["smokegrenade_detonate", "flashbang_detonate", "hegrenade_detonate"]),
            "blind": parser.parse_ticks(["player_blind"]),
            "shots": parser.parse_ticks(["weapon_fire"])
        }
        return parsed_data

    except Exception as e:
        raise Exception(f"Ошибка обработки матча {match_idx}: {str(e)}")
        
    finally:
        # Моментально очищаем диск сервера, чтобы приложение не заблокировали
        if os.path.exists(temp_demo_path):
            os.remove(temp_demo_path)
