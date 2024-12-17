import requests
import re

def find_m3u8_links_from_homepage(base_url):
    """Ana sayfadan 'bein-sports' içeren m3u8 linklerini bulur."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Ana sayfaya istek gönder
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()

        # m3u8 linklerini ara
        m3u8_links = re.findall(r"https?://[^\s]+\.m3u8", response.text)

        # Bein Sports içeren linkleri filtrele
        bein_sports_links = [link for link in m3u8_links if "bein-sports" in link]

        return bein_sports_links

    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
        return []

def update_m3u_file(file_path, new_links):
    """M3U dosyasındaki Bein Sports linklerini günceller."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Güncelleme işlemi
        updated_lines = []
        for line in lines:
            # Sadece bein-sports linklerini kontrol et
            if "bein-sports" in line and line.strip().endswith(".m3u8"):
                current_link = line.strip()
                # Yeni link var mı, kontrol et
                updated_link = next((new_link for new_link in new_links if current_link.split("/")[-1] in new_link), current_link)
                if current_link != updated_link:
                    print(f"Değiştiriliyor: {current_link} -> {updated_link}")
                updated_lines.append(updated_link + "\n")
            else:
                updated_lines.append(line)

        # Dosyayı güncelle
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(updated_lines)

        print("M3U dosyası başarıyla güncellendi!")

    except FileNotFoundError:
        print(f"Hata: {file_path} bulunamadı!")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    # Ana sayfa URL'si
    base_url = "https://www.atomsportv367.top/"

    # M3U dosyasının yolu
    file_path = "index.m3u"

    # Ana sayfadan Bein Sports linklerini al
    bein_sports_links = find_m3u8_links_from_homepage(base_url)

    # Bulunan linklerle M3U dosyasını güncelle
    if bein_sports_links:
        update_m3u_file(file_path, bein_sports_links)
    else:
        print("Hiç Bein Sports yayın linki bulunamadı.")
