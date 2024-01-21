import pandas as pd
import requests
import time
#แก้ไปใช้ request.parquet ถ้าใช้ userfull table
df = pd.read_parquet('requestfix.parquet')

# เก็มค่า ms
response_times = []

# Start timer
start_time = time.time()

for index, row in df.iterrows():
    user_id = row['user_id']

    # รับ param จาก df
    params = {
        "latitude" : row['latitude'], 
        "longitude" : row['longitude'],
        "max_dis" : row['max_dis'],
        "size" : row['size'],
        "sort_dist" : row['sort_dis']
    }

    try:
        # Send a POST 
        response = requests.post(f'http://127.0.0.1:5000/recommend/{user_id}', json=params)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

        # Assuming the response is in JSON format, parse it
        data = response.json()

        # เก็บค่าเป็น milisec
        response_times.append(response.elapsed.total_seconds() * 1000)

        # ถ้า list ว่างแปลว่าไม่มัร้านอาหารที่อยู่ใน max_dis ที่ตั้ง
        if not data.get('restaurants'):
            print(f"This userID {user_id} has no restaurant near")

    except Exception as err:
        print(f"An error occurred for user {user_id}: {err}")
    else:
        # result
        print("User ID:", user_id)
        print("Status code:", response.status_code)
        print("Response:", data)

#calculate request per sec
end_time = time.time()

total_time = end_time - start_time
requests_per_second = len(df) / total_time

print("requests per second:", requests_per_second)

# หา AVG ms
average_response_time = sum(response_times) / len(response_times)
print("Average Response Time:", average_response_time, "ms")
