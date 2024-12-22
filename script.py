import cloudscraper

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
    (884766068, "Dinamik Bilim Kurgu"),
    (1557465046, "Dinamik Fantastik"),
    (3270480503, "Ben 10"),
    (4100185659, "Tom & Jerry"),
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
    # Diğer kanal ID'lerinizi buraya ekleyin 
]

# URL şablonu
url_template = "https://vavoo.to/play/{channel_id}/index.m3u8"

# Cloudscraper oluştur
scraper = cloudscraper.create_scraper()

# HTTP Başlıkları
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
}

# Mevcut M3U dosyasını oku (varsa)
m3u_file = "channels_vavoo.m3u"
existing_entries = {}

try:
    with open(m3u_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF"):
                channel_name = lines[i].split(",")[-1].strip()
                if i + 1 < len(lines) and lines[i + 1].startswith("http"):
                    # EXTINF satırını ve altındaki URL'yi kaydet
                    existing_entries[channel_name] = (lines[i].strip(), lines[i + 1].strip())
except FileNotFoundError:
    print(f"{m3u_file} dosyası bulunamadı, yeni bir dosya oluşturulacak.")

# Yeni M3U içeriklerini oluştur
m3u_entries = ["#EXTM3U"]

for channel_id, channel_name in channels:
    url = url_template.format(channel_id=channel_id)

    try:
        # İstek gönder ve yönlendirme başlığını al
        response = scraper.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 302 and "Location" in response.headers:
            m3u8_link = response.headers["Location"]

            if channel_name in existing_entries:
                extinf_line, old_link = existing_entries[channel_name]
                if old_link == m3u8_link:
                    # Değişiklik yok, eski değerleri ekle
                    m3u_entries.append(extinf_line)
                    m3u_entries.append(old_link)
                else:
                    # Yeni link ile güncelle
                    m3u_entries.append(extinf_line)
                    m3u_entries.append(m3u8_link)
                    print(f"Kanal güncellendi: {channel_name} -> {m3u8_link}")
            else:
                # Yeni kanal ekleniyor
                m3u_entries.append(f"#EXTINF:-1, {channel_name}")
                m3u_entries.append(m3u8_link)
                print(f"Kanal eklendi: {channel_name} -> {m3u8_link}")
        else:
            print(f"Kanal eklenemedi: {channel_name} (ID: {channel_id}) - HTTP {response.status_code}")
    except Exception as e:
        print(f"Hata oluştu: {channel_name} (ID: {channel_id}) - {e}")

# M3U dosyasını yazma
with open(m3u_file, "w", encoding="utf-8") as f:
    f.write("\n".join(m3u_entries))

print("channels_vavoo.m3u dosyası başarıyla güncellendi.")
