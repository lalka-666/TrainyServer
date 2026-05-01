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


# write data in csv file and copy it to database
def copy_table(table_name: str, data: list[dict]): 
    columns = list(data[0].keys())

    with open(f'{table_name}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)

    cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
    conn.commit()

    with open(f'{table_name}.csv', 'r', encoding='utf-8') as f:
        cursor.copy_expert(f"""
            COPY {table_name}({', '.join(map(str, columns))})
            FROM STDIN
            WITH (FORMAT CSV, HEADER true, DELIMITER ',')
        """, f)

    conn.commit()
    print(f'{table_name} copied!')


def generate_users():
    users = []
    ROLE = ['administrator', 'user_logged', 'user_logged', 'user_logged', 
            'user_logged', 'user_logged', 'user_logged']
    for _ in range(200):
        users.append({
            'email': fake.email(),
            'password': fake.password(),
            'full_name': fake.name(),
            'role': random.choice(ROLE),
            'phone_number': fake.phone_number()
        })
    
    copy_table("users", users)
    print('Users generated!')


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

    copy_table("trains", trains)
    print('Trains generated!')


def generate_trips():
    trips = []
    status = ['scheduled', 'boarding', 'departed', 
              'completed', 'delayed', 'cancelled']
    for _ in range(200):
        trips.append({
            'train_id': random.randint(1, 60),
            'status': random.choice(status),
            'base_price': random.randrange(600, 20000, 100)
        })

    copy_table("trips", trips)
    print('Trips generated!')


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

    copy_table("stations", stations)
    print('Stations generated!')


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

    copy_table("passengers", passengers)
    print('Passengers generated!')


def generate_carriages():
    carriages = []
    carriage_types = ['seated', 'reserved', 'general', 'compartment', 
                      'luxury', 'soft', 'international4', 'international3']

    for _ in range(10000):
        carriages.append({
            'trip_id': random.randint(1, 200),
            'carriage_number': random.randint(12345, 98765),
            'carriage_type': random.choice(carriage_types),
            'total_seats': random.randint(20, 70)
        })

    copy_table("carriages", carriages)
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

    copy_table("seats", seats)
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

    copy_table("trip_stops", trip_stops)
    print("Trip_stops generated!")
