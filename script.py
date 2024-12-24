import cloudscraper
import os

# Kanal ID'leri ve isimleri
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
    # Diğer kanal ID'leri ve isimlerini buraya ekleyin
]

# URL şablonu
url_template = "https://vavoo.to/play/{channel_id}/index.m3u8"

# Cloudscraper oluştur
scraper = cloudscraper.create_scraper()

# HTTP Başlıkları
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
}

# M3U dosyasını oluşturma
m3u_entries = ["#EXTM3U"]

# Kanallar için işlemleri başlat
for channel_id, channel_name in channels:
    url = url_template.format(channel_id=channel_id)

    try:
        # İstek gönder ve yönlendirme başlığını al
        response = scraper.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 302 and "Location" in response.headers:
            m3u8_link = response.headers["Location"]

            # GitHub.io URL'si oluştur
            github_url = f"https://{os.environ['GITHUB_REPOSITORY_OWNER']}.github.io/{channel_name.replace(' ', '').lower()}.m3u8"
            
            # m3u dosyasına yeni linki ekle
            m3u_entries.append(f"#EXTINF:-1, {channel_name}")
            m3u_entries.append(github_url)

            print(f"Kanal eklendi: {channel_name} -> {github_url}")
        else:
            print(f"Kanal eklenemedi: {channel_name} (ID: {channel_id}) - HTTP {response.status_code}")
    except Exception as e:
        print(f"Hata oluştu: {channel_name} (ID: {channel_id}) - {e}")

# M3U dosyasını yazma
with open("channels_vavoo.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(m3u_entries))

print("channels_vavoo.m3u dosyası başarıyla güncellendi.")
