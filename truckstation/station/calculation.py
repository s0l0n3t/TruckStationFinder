import math

def haversine(lat1, lon1, lat2, lon2):
    # Dereceyi radyana çevir
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formülü
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Dünya yarıçapı (kilometre cinsinden)
    r = 6371
    return c * r

# Örnek Kullanım
lat1, lon1 = 41.2436, -87.8392  # Konum 1 (Manteno, IL)
lat2, lon2 = 38.9595, -85.8903  # Konum 2 (Seymour, IN)
distance = haversine(lat1, lon1, lat2, lon2)
print(f"Mesafe: {distance:.2f} km")  # Çıktı: ~338.53 km