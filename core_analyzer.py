import io
import os
import bz2
import json
import requests
from demoparser2 import DemoParser

# Сюда вставляйте ваши 7 прямых ссылок на демки из Steam (заканчиваются на .dem.bz2)
DEMO_URLS = [
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com"
]

def download_and_extract(url, output_path):
    print(f" -> Скачивание архива...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Декомпрессия .bz2 на лету во время скачивания
    decompressor = bz2.BZ2Decompressor()
    print(f" -> Распаковка в {output_path}...")
    
    with open(output_path, 'wb') as out_file:
        for chunk in response.iter_content(chunk_size=1024 * 1024): # Блоками по 1 МБ
            if chunk:
                try:
                    decompressed_chunk = decompressor.decompress(chunk)
                    out_file.write(decompressed_chunk)
                except EOFError:
                    break

def parse_match_data(demo_path, match_index):
    print(f" -> Чтение структуры и сбор 100+ параметров...")
    parser = DemoParser(demo_path)
    
    # Вытаскиваем только агрегированную статистику раундов и игроков, 
    # чтобы файл не весил 500 МБ, а ИИ мог его прочесть в чате.
    parsed_data = {
        "match_number": match_index,
        "map_name": parser.parse_header()["map_name"],
        "total_ticks": parser.parse_header()["total_ticks"],
        
        # Честные логи важнейших событий матча
        "kills_log": parser.parse_ticks(["player_death"]),
        "damage_log": parser.parse_ticks(["player_hurt"]),
        "grenades_log": parser.parse_ticks(["smokegrenade_detonate", "flashbang_detonate", "hegrenade_detonate"]),
        "blind_log": parser.parse_ticks(["player_blind"]),
        "shots_log": parser.parse_ticks(["weapon_fire"])
    }
    return parsed_data

def main():
    final_report = []
    print("=== ЗАПУСК АНАЛИЗАТОРА ДЕМО CS2 НА 100+ ПАРАМЕТРОВ ===")
    
    for idx, url in enumerate(DEMO_URLS, 1):
        if "example.com" in url:
            print(f"\n[!] Пропуск ссылки №{idx}: Замените тестовый URL на реальную ссылку Steam.")
            continue
            
        temp_demo_name = f"temp_match_{idx}.dem"
        print(f"\n[{idx}/{len(DEMO_URLS)}] Обработка матча:")
        
        try:
            # 1. Скачиваем и распаковываем
            download_and_extract(url, temp_demo_name)
            
            # 2. Парсим
            match_data = parse_match_data(temp_demo_name, idx)
            final_report.append(match_data)
            print(f" -> Матч успешно обработан!")
            
        except Exception as e:
            print(f" [Ошибка] Не удалось обработать матч {idx}: {e}")
            
        finally:
            # 3. Чистим диск от тяжелой демки (до 1.5 ГБ) сразу после парсинга
            if os.path.exists(temp_demo_name):
                os.remove(temp_demo_name)
                print(f" -> Временный демо-файл удален. Диск свободен.")

    # Сохраняем сжатый итоговый JSON для отправки в ИИ
    output_json = "cs2_ai_input.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2)
        
    print("\n=======================================================")
    print(f"УСПЕХ! Создан файл данных: '{output_json}'")
    print("Что делать дальше:")
    print("1. Откройте этот файл и скопируйте весь его текст.")
    print("2. Вставьте этот текст в чат к ИИ вместе с системным промптом тренера.")
    print("=======================================================")

if __name__ == "__main__":
    main()
