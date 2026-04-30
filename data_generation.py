from faker import Faker
import random
import csv
import psycopg2
from datetime import timedelta

conn = psycopg2.connect(
    host='localhost',
    port='5433',
    database='trainy_db',
    user='postgres',
    password='0000'
)
cursor = conn.cursor()
fake = Faker('ru_RU')

# generate and copy data to 'users'

def generate_users():
    users = []
    ROLE = ['administrator', 'user_logged', 'user_logged', 'user_logged', 'user_logged', 'user_logged', 'user_logged']
    for _ in range(200):
        users.append({
            'email': fake.email(),
            'password': fake.password(),
            'full_name': fake.name(),
            'role': random.choice(ROLE),
            'phone_number': fake.phone_number()
        })

    with open('users.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['email', 'password', 'full_name', 'role', 'phone_number'])
        writer.writeheader()
        writer.writerows(users)

    print('Users generated!')


def copy_users():
    generate_users()
    cursor.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
    with open('users.csv', 'r', encoding='utf-8') as f:
        cursor.copy_expert("""
            COPY users(email, password, full_name, role, phone_number)
            FROM STDIN
            WITH (FORMAT CSV, HEADER true, DELIMITER ',')
        """, f)

    conn.commit()
    print('Users copied!')



# generate and copy data to 'trains'

def generate_trains():
    trains = []
    train_names = ["Ласточка", "Сапсан", "Стриж", "Красная стрела", "Мегаполис", "Двухэтажный", 
              "Невский экспресс", "Россия", "Волга", "Урал", "Кавказ", "Арктика", "Башкортостан", 
              "Лотос", "Жигули", "Вятка", "Оренбуржье", "Поморье", "Томич", "Черноморец", 
              "Сахалин", "Алтай", "Ямал", "Карелия", "Мордовия", "Смена", "Полярная стрела", 
              "Гранд Экспресс", "Лев Толстой", "Премиум", "Алтай", "Янтарь", "Воркута", "Сура", 
              "Саяны", "Кама", "Поволжье", "Южный Урал", "Воронеж", "Белогорье", "Тихий Дон", 
              "Кубань", "Океан", "Гилюй", "Соловей", "Юность", "Чувашия", "Московия", "Сыктывкар", 
              "Ульяновск", "Рыбинск", "Николаевский экспресс", "Александр Невский", 
              "Императорская Россия", "Таврия", "Рускеальский экспресс", "Демидовский экспресс", 
              "Поезд Деда Мороза", "Славянский экспресс", "Северная Пальмира"]
    
    distance_type = ["local", "long_distance", "commuter"]
    speed_type = ["passenger", "express", "high_speed", "very_high_speed"]

    for train in train_names:
        trains.append({
            'train_number': random.randint(100,999),
            'train_name': train,
            'distance_type': random.choice(distance_type),
            'speed_type': random.choice(speed_type)
        })

    with open('trains.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['train_number', 'train_name', 'distance_type', 'speed_type'])
        writer.writeheader()
        writer.writerows(trains)
    print('Trains generated!')

def copy_trains():
    generate_trains()
    cursor.execute("TRUNCATE TABLE trains RESTART IDENTITY CASCADE;")
    with open('trains.csv', 'r', encoding='utf-8') as f:
        cursor.copy_expert("""
            COPY trains(train_number, train_name, distance_type, speed_type)
            FROM STDIN
            WITH (FORMAT CSV, HEADER true, DELIMITER ',')
        """, f)
    conn.commit()
    print('Trains copied!')


# generate and copy data to 'trips'
def generate_trips():
    trips = []
    status = ['scheduled', 'boarding', 'departed', 'completed', 'delayed', 'cancelled']
    for _ in range(200):
        trips.append({
            'train_id': random.randint(1, 60),
            'status': random.choice(status),
            'base_price': random.randrange(600, 20000, 100)
        })

    with open('trips.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['train_id', 'status', 'base_price'])
        writer.writeheader()
        writer.writerows(trips)

    print('Trips generated!')

    cursor.execute("TRUNCATE TABLE trips RESTART IDENTITY CASCADE;")
    with open('trips.csv', 'r', encoding='utf-8') as f:
        cursor.copy_expert("""
            COPY trips(train_id, status, base_price)
            FROM STDIN
            WITH (FORMAT CSV, HEADER true, DELIMITER ',')
        """, f)
    conn.commit()
    print('Trips copied!')


# generate and copy data to 'stations'

def generate_stations():
    station_names = [
    "Артышта II", "Бабаево", "Балезино", "Белореченская", "Вековка",
    "Владимир", "Вязьма", "Горячий Ключ", "Данилов", "Дербент",
    "Дружинино", "Инзер", "Иртышское", "Карталы I", "Мариинск",
    "Междуреченск", "Пенза I", "Пенза III", "Рыбное", "Рязань II",
    "Свирь", "Сухиничи-Главные", "Сызрань I", "Узуново", "Черепаново",
    "Катайск", "Катуар", "Каучук", "Кафтино", "Кача",
    "Качалино", "Качканар", "Кашин", "Кашира-Пассажирская", "Кашира-Товарная",
    "Кашпир", "Кая", "Каяла", "Каясан", "Кварса",
    "Кедровка", "Кедровый", "Кедрозеро", "Кежемская", "Рудня",
    "Ружино", "Рузаевка", "Рукополь", "Ручей", "Рыбинск-Пассажирский",
    "Рябцево", "Ряжск-1", "Рязань-1", "Савкино", "Сагджему",
    "Сакмарская", "Салтыковка", "Салым", "Сальск", "Самара",
    "Самолуково", "Учум", "Ушман", "Ушумун", "Уяр",
    "Фалёнки", "Фаянсовая", "Февральск", "Филаретовка", "Филоново",
    "Фирсово", "Фоминская", "Форель", "Фурманов", "Хабайдак",
    "Хабаровск-1", "Хабары", "Одинцово", "Баковка", "Сколково",
    "Немчиновка", "Сетунь", "Рабочий Посёлок", "Кунцевская", "Славянский бульвар",
    "Фили", "Тестовская", "Беговая", "Белорусская", "Савёловская"
    ]

    cities = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Челябинск", "Красноярск", "Самара", "Уфа",
    "Ростов-на-Дону", "Краснодар", "Омск", "Воронеж", "Пермь",
    "Волгоград", "Саратов", "Тюмень", "Тольятти", "Ижевск",
    "Барнаул", "Ульяновск", "Иркутск", "Хабаровск", "Ярославль",
    "Владивосток", "Махачкала", "Томск", "Оренбург", "Кемерово",
    "Новокузнецк", "Рязань", "Астрахань", "Набережные Челны", "Пенза",
    "Липецк", "Киров", "Тула", "Чебоксары", "Калининград",
    "Курск", "Улан-Удэ", "Ставрополь", "Магнитогорск", "Севастополь",
    "Сочи", "Иваново", "Брянск", "Тверь", "Белгород",
    "Сургут", "Владимир", "Чита", "Нижний Тагил", "Архангельск",
    "Смоленск", "Курган", "Калуга", "Грозный", "Вологда",
    "Владикавказ", "Саранск", "Тамбов", "Якутск", "Мурманск",
    "Петрозаводск", "Кострома", "Новороссийск", "Комсомольск-на-Амуре", "Химки",
    "Симферополь", "Сыктывкар", "Нижневартовск", "Шахты", "Дзержинск",
    "Орёл", "Армавир", "Энгельс", "Ангарск", "Благовещенск",
    "Северодвинск", "Бийск", "Королёв", "Прокопьевск", "Мытищи",
    "Рыбинск", "Люберцы", "Южно-Сахалинск", "Норильск", "Петропавловск-Камчатский"
    ]

    stations = []
    codes = list(range(1001, len(station_names) + 1001))

    for i in range(len(station_names)):
        stations.append({
            'station_name': station_names[i],
            'city': cities[i],
            'code': codes[i]
        })

    cursor.execute("TRUNCATE TABLE stations RESTART IDENTITY CASCADE;")
    with open('stations.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['station_name', 'city', 'code'])
        writer.writeheader()
        writer.writerows(stations)

    with open('stations.csv', 'r', newline='', encoding='utf-8') as f:
        cursor.copy_expert("""
            COPY stations(station_name, city, code)
            FROM STDIN
            WITH (FORMAT CSV, HEADER true, DELIMITER ',')
        """, f)
    conn.commit()

    print('Stations generated!')

# generate and copy data to 'passengers'

def generate_passengers():
    passengers = []
    user_names = []
    pass_numbers = []
    doc_type = ['passport', 'international_passport', 'birth_certificate', 
                'military_id', 'foreign_citizen_passport', 'temporary_identity_card']

    with open('users.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            user_names.append(row['full_name'])
            pass_numbers.append(row['phone_number'])

    for i in range(200):
        passengers.append({
            'user_id': i+1,
            'full_name': user_names[i],
            'document_type': random.choice(doc_type),
            'document_number': random.randint(123456789, 987654321),
            'birthday': fake.date_this_year(),
            'phone_number': pass_numbers[i],
            'is_default': True
        })

    cursor.execute("TRUNCATE TABLE passengers RESTART IDENTITY CASCADE;")
    conn.commit()

    with open('passengers.csv', 'w+', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['user_id', 'full_name', 'document_type', 
                                                'document_number', 'birthday', 'phone_number', 'is_default'])
        writer.writeheader()
        writer.writerows(passengers)

    with open('passengers.csv', 'r', newline='', encoding='utf-8') as f:
        cursor.copy_expert("""
            COPY passengers(user_id, full_name, document_type, document_number, birthday, phone_number, is_default)
            FROM STDIN
            WITH (FORMAT CSV, HEADER true, DELIMITER ',')
        """, f)
    conn.commit()

    print('Passengers generated!')


# generate and copy data to 'carriages'
def generate_carriages():
    carriages = []
    carriage_types = ['seated', 'reserved', 'general', 'compartment', 'luxury', 'soft', 'international4', 'international3']

    for _ in range(10000):
        carriages.append({
            'trip_id': random.randint(1, 200),
            'carriage_number': random.randint(12345, 98765),
            'carriage_type': random.choice(carriage_types),
            'total_seats': random.randint(20, 70)
        })

    cursor.execute("TRUNCATE TABLE carriages RESTART IDENTITY CASCADE;")
    with open('carriages.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['trip_id', 'carriage_number', 'carriage_type', 'total_seats'])
        writer.writeheader()
        writer.writerows(carriages)

    with open('carriages.csv', 'r', newline='', encoding='utf-8') as f:
        cursor.copy_expert("""
            COPY carriages(trip_id, carriage_number, carriage_type, total_seats)
            FROM STDIN
            WITH (FORMAT CSV, HEADER true, DELIMITER ',')
        """, f)
    conn.commit()

    print('Carriages generated!')



def generate_seats():
    seats = []
    with open('carriages.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            for j in range(int(row['total_seats'])):
                seats.append({
                    'carriage_id': i+1,
                    'seat_number': j+1,
                    'is_available': random.choice((True, False)),
                    'price': random.randrange(500, 10000, 50)
                })

    with open('seats.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['carriage_id', 'seat_number', 'is_available', 'price'])
        writer.writeheader()
        writer.writerows(seats)

    with open('seats.csv', 'r', encoding='utf-8') as f:
        cursor.copy_expert("""
            COPY seats(carriage_id, seat_number, is_available, price)
            FROM STDIN
            WITH (FORMAT CSV, HEADER true, DELIMITER ',')
        """, f)
    conn.commit()
    print("Seats generated!")


def generate_trip_stops():
    trip_stops = []

    for i in range(200):

        current_time = fake.date_time_this_year()

        station_ids = random.sample(range(1,90), 10)

        # generate arrival/departure datetime with 3-7 hours delta and 10-20 mins dwell/layover
        for j in range(10):
            pairs = []

            current_time += timedelta(hours=(random.randint(3,7)))
            arrival_time = current_time

            gap = random.choice([10, 15, 20])
            departure_time = arrival_time + timedelta(minutes=gap)

            arrival_string = arrival_time.strftime('%d.%m.%Y %H:%M')
            departure_string = departure_time.strftime('%d.%m.%Y %H:%M')

            pairs.append(arrival_string)
            pairs.append(departure_string)

            trip_stops.append({
                'trip_id': i+1,
                'station_id': station_ids[j],
                'stop_order': j+1,
                'arrival_time': pairs[0],
                'departure_time': pairs[1]
            })

    with open('trip_stops.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['trip_id', 'station_id', 'stop_order', 'arrival_time', 'departure_time'])
        writer.writeheader()
        writer.writerows(trip_stops)

    with open('trip_stops.csv', 'r', encoding='utf-8') as f:
        cursor.copy_expert("""
            COPY trip_stops(trip_id, station_id, stop_order, arrival_time, departure_time)
            FROM STDIN
            WITH (FORMAT CSV, HEADER true, DELIMITER ',')
        """, f)
    conn.commit()
    print("Trip_stops generated!")

generate_trip_stops()
