import requests
import re

# Web sitesinden bein-sports içeren linkleri çekme
def fetch_bein_links(base_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        # Web sitesine istek gönder
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        # Bein Sports içeren m3u8 linklerini ara
        m3u8_links = re.findall(r"https?://[^\s]+\.m3u8", response.text)
        return [link for link in m3u8_links if "bein-sports" in link]
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
        return []

# Var olan M3U dosyasını güncelleme
def update_m3u_file(file_path, new_links):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

# Her bein-sports linkini yeni linklerle değiştir
updated_lines = []
for line in lines:
    # bein-sports-1'den bein-sports-10'a kadar olan linkleri kontrol et
    if any(f"bein-sports-{i}" in line for i in range(1, 11)):  
        for new_link in new_links:
            # Her bir new_link'i kontrol et
            for i in range(1, 11):  # bein-sports-1'den bein-sports-10'a kadar
                if f"bein-sports-{i}" in new_link:
                    line = f"{new_link}\n"  # Linki güncelle
                    break  # Bir kez eşleşme bulduğunda diğerlerini kontrol etme
    updated_lines.append(line)  # Güncellenmiş satırı listeye ekle

        # Güncellenen dosyayı yaz
        with open(file_path, 'w') as file:
            file.writelines(updated_lines)
        print(f"{file_path} başarıyla güncellendi.")
    except FileNotFoundError:
        print(f"{file_path} dosyası bulunamadı.")

if __name__ == "__main__":
    # Bein Sports linklerini çekeceğimiz site
    base_url = "https://www.atomsportv366.top/"

    # Güncellenecek M3U dosyası
    m3u_file_path = "index.m3u"

    print("Bein Sports linkleri çekiliyor...")
    bein_links = fetch_bein_links(base_url)

    if bein_links:
        print(f"Bulunan Bein Sports linkleri: {len(bein_links)}")
        update_m3u_file(m3u_file_path, bein_links)
    else:
        print("Hiç Bein Sports linki bulunamadı.")
