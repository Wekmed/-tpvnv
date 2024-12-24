import os
import cloudscraper

# Kanal bilgileri
channels = [
   (406666682, "TRT 1 FHD"),
    (1130441933, "Kanal D FHD"),
    (351471337, "Show TV FHD"),
    (129909794, "ATV FHD"),
    (161305206, "NOW TV HD"),
    (2720556692, "Star TV FHD"),
    (1702470161, "TV8 FHD"),
    (2549900211, "TEVE 2 FHD"),
    (1908265816, "TV8.5 FHD"),
    (3239529951, "Dmax FHD"),
    (951448076, "TLC FHD"),
    (2579401878, "TRT HABER"),
    (3194104127, "NTV"),
    (960578312, "Szc TV"),
    (1470199900, "HaberTurk"),
    (3571625991, "Dinamik Kemal Sunal"),
    (2337350974, "Dinamik Aksiyon"),
    (1822425118, "Dinamik Animasyon"),
    (3830648039, "Dinamik Bilim Kurgu"),
    (1557465046, "Dinamik Fantastik"),
    (3270480503, "Ben 10"),
    (443724116, "Tom & Jerry"),
    (383348303, "Sirinler"),
    (2879086761, "Oscar Collerde"),
    (3029254675, "NICKELODEON"),
    (312904614, "TRT SPOR"),
    (2081577417, "TRT SPOR YILDIZ"),
    (1197336000, "BEIN SPORTS HABER"),
    (1352421053, "BEIN SPORTS 1"),
    (2851539143, "BEIN SPORTS 2"),
    (3410167560, "BEIN SPORTS 3"),
    (1872232768, "BEIN SPORTS 4"),
    (4000315601, "BEIN SPORTS 5"),
    (4071474743, "BEIN SPORTS MAX 1"),
    (3407936242, "BEIN SPORTS MAX 2"),
    (3531762195, "S-SPORT"),
    (3943651030, "S-SPORT 2"),
]

# URL şablonu
url_template = "https://vavoo.to/play/{channel_id}/index.m3u8"

# Cloudscraper ile HTTP isteği gönderme
scraper = cloudscraper.create_scraper()

# Çalışma dizini
output_dir = "./docs"

# GitHub Pages için m3u8 dosyalarını oluşturma
os.makedirs(output_dir, exist_ok=True)

for channel_id, channel_name in channels:
    url = url_template.format(channel_id=channel_id)

    try:
        # Gerçek m3u8 linkini al
        response = scraper.get(url, allow_redirects=False)
        if response.status_code == 302 and "Location" in response.headers:
            real_m3u8_link = response.headers["Location"]

            # m3u8 dosyasını oluştur
            channel_filename = channel_name.replace(" ", "").lower() + ".m3u8"
            file_path = os.path.join(output_dir, channel_filename)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,{channel_name}\n{real_m3u8_link}")
            print(f"{channel_name} için m3u8 dosyası oluşturuldu: {file_path}")

        else:
            print(f"Hata: {channel_name} için gerçek link alınamadı.")
    except Exception as e:
        print(f"İstek sırasında hata oluştu: {channel_name} - {e}")

print("Tüm kanallar için m3u8 dosyaları oluşturuldu.")
