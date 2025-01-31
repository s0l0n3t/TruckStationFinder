from pymongo import MongoClient
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
import re
import random

# MongoDB Bağlantısı
def get_mongo_collection():
    client = MongoClient("localhost", 27017)
    db = client.trackstation
    return db['stationdb']

# Adres Temizleme Fonksiyonu
def clean_address(address):
    pattern = r"\b([A-Z]{1,3}-?\d+)\b"
    match = re.search(pattern, address)
    return match.group(0) if match else None

# Şehir için Rastgele Koordinat Üret
def generate_random_coordinates(base_lat, base_lon, radius_km=10):
    offset_lat = random.uniform(-radius_km/111, radius_km/111)
    offset_lon = random.uniform(-radius_km/(111*abs(base_lat)), radius_km/(111*abs(base_lat)))
    return base_lat + offset_lat, base_lon + offset_lon

# Ana İşlem (Sadece latitude ve longitude güncellenecek)
def process_stations():
    collection = get_mongo_collection()
    stations = list(collection.find())
    
    locator = Nominatim(user_agent="geoapi", timeout=25)
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    
    for station in tqdm(stations, desc="Koordinatlar Güncelleniyor"):
        try:
            original_address = station.get("Address", "")
            city = station.get("City", "").strip()
            state = station.get("State", "").strip()
            cleaned_address = clean_address(original_address)
            
            # Gerekli alan kontrolü
            if not cleaned_address or not city or not state:
                continue

            # 1. AŞAMA: Tam adresle deneme
            full_address = f"{cleaned_address}, {city}, {state}, USA"
            location = geocode(full_address)
            
            if not location:
                # 2. AŞAMA: Sadece şehir ve eyaletle deneme
                city_location = locator.geocode(f"{city}, {state}, USA", exactly_one=True)
                if city_location:
                    base_lat, base_lon = city_location.latitude, city_location.longitude
                    latitude, longitude = generate_random_coordinates(base_lat, base_lon)
                else:
                    # 3. AŞAMA: Fallback rastgele koordinat (eyalet bazlı)
                    state_location = locator.geocode(f"{state}, USA", exactly_one=True)
                    if state_location:
                        base_lat, base_lon = state_location.latitude, state_location.longitude
                        latitude, longitude = generate_random_coordinates(base_lat, base_lon, 100)
                    else:
                        latitude, longitude = None, None
            else:
                latitude, longitude = location.latitude, location.longitude

            # SADECE latitude ve longitude güncellenecek
            collection.update_one(
                {"_id": station["_id"]},
                {"$set": {
                    "latitude": latitude,
                    "longitude": longitude
                }}
            )

        except Exception as e:
            print(f"Hata (ID={station['_id']}): {str(e)}")

if __name__ == "__main__":
    process_stations()
    print("Tüm işlemler tamamlandı!")