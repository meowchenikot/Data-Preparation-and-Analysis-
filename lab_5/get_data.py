import os
import urllib.request
import pandas as pd
from io import StringIO

def download_and_clean():
    if os.path.exists('vhi_data.csv'):
        print("Файл vhi_data.csv вже існує! Завантаження скасовано.")
        return

    print("Починаємо завантаження даних з NOAA... Це займе пару секунд.")
    dfs = []
    
    for province_id in range(1, 28):
        url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1=1981&year2=2024&type=Mean"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                text = response.read().decode('utf-8')
                
            clean_lines = []
            for line in text.split('\n'):
                line = line.replace('<tt><pre>', '').replace('</pre></tt>', '').replace('<br>', '').strip()
                if line.endswith(','):
                    line = line[:-1]
                if line and line[0].isdigit():
                    clean_lines.append(line)
                    
            if not clean_lines:
                continue
                
            csv_data = StringIO('\n'.join(clean_lines))
            df = pd.read_csv(csv_data, sep=r'\s*,\s*', engine='python', header=None, 
                             names=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
            
            df['NOAA_ID'] = province_id
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
            df['VHI'] = pd.to_numeric(df['VHI'], errors='coerce')
            
            df = df[df['VHI'] != -1]
            df.dropna(subset=['Year', 'VHI'], inplace=True)
            dfs.append(df)
            print(f"Завантажено область {province_id}/27")
            
        except Exception as e:
            print(f"Помилка з областю {province_id}: {e}")

    df_raw = pd.concat(dfs, ignore_index=True)

    province_dict = {
        1: "Черкаська", 2: "Чернігівська", 3: "Чернівецька", 4: "Крим", 
        5: "Дніпропетровська", 6: "Донецька", 7: "Івано-Франківська", 8: "Харківська", 
        9: "Херсонська", 10: "Хмельницька", 11: "Київська", 12: "м. Київ", 
        13: "Кіровоградська", 14: "Луганська", 15: "Львівська", 16: "Миколаївська", 
        17: "Одеська", 18: "Полтавська", 19: "Рівненська", 20: "м. Севастополь", 
        21: "Сумська", 22: "Тернопільська", 23: "Закарпатська", 24: "Вінницька", 
        25: "Волинська", 26: "Запорізька", 27: "Житомирська"
    }
    
    df_raw['Region'] = df_raw['NOAA_ID'].map(lambda x: province_dict.get(x, "Unknown"))
    
    final_df = df_raw[['Year', 'Week', 'Region', 'VCI', 'TCI', 'VHI']]
    
    final_df.to_csv('vhi_data.csv', index=False)
    print("Файл vhi_data.csv успішно створено.")

if __name__ == "__main__":
    download_and_clean()