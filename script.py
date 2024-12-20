import requests

# Kanal ID'leri ve isimleri
channels = [
    (406666682, "TRT 1 FHD"),
    (3531762195, "S-SPORT"),
    # Diğer kanal ID'lerinizi buraya ekleyin
]

# Hedef URL şablonu
url_template = "https://vavoo.to/play/{channel_id}/index.m3u8"

# Gerekli headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# Oturum oluştur (çerezler dahil)
session = requests.Session()
session.headers.update(headers)

# m3u dosyası için içerik
m3u_entries = ["#EXTM3U"]

for channel_id, channel_name in channels:
    # Hedef URL
    url = url_template.format(channel_id=channel_id)

    try:
        # İstek gönder (çerezleri kullanarak)
        response = session.get(url, allow_redirects=False)

        # "Location" başlığından gerçek m3u8 bağlantısını al
        if response.status_code == 302 and "Location" in response.headers:
            m3u8_link = response.headers["Location"]

            # m3u formatında giriş ekle
            m3u_entries.append(f"#EXTINF:-1, {channel_name}")
            m3u_entries.append(m3u8_link)
            print(f"Kanal eklendi: {channel_name} -> {m3u8_link}")
        else:
            print(f"Kanal eklenemedi: {channel_name} (ID: {channel_id}) - HTTP {response.status_code}")
    except Exception as e:
        print(f"Hata oluştu: {channel_name} (ID: {channel_id}) - {e}")

# m3u dosyasını yaz
with open("channels.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(m3u_entries))

print("channels.m3u dosyası oluşturuldu.")
