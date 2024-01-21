from flask import Flask, jsonify, request
import pickle
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import h3
import mysql.connector



app = Flask(__name__)

config = {
    'user': 'root',
    'password': 'banana',
    'host': 'db',
    'port': '3306',
    'database': 'dat'
}

#รับข้อมูลจาก mysql
def restaurant_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM `restaurant`')
    results_res = cursor.fetchall()
    cursor.close()
    connection.close()

    restaurant_df = pd.DataFrame(results_res)
    return restaurant_df

def usersmall_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM `usersmall`')
    results_usersmall = cursor.fetchall()
    cursor.close()
    connection.close()

    usersmall_df = pd.DataFrame(results_usersmall)
    return usersmall_df

#เอาไว้ใช้ถ้าจะใช้ userfull_data
# def userfull_data():
#     connection = mysql.connector.connect(**config)
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute('SELECT * FROM `userfull`')
#     results_userfull = cursor.fetchall()
#     cursor.close()
#     connection.close()

#     usersfull_df = pd.DataFrame(results_userfull)
#     return userfull_df


#หน้าหลัก
@app.route("/")
def index():
    return "Hello World!"


#get,post ข้อมูลผ่านตัวนี้
@app.route("/recommend/<user_id>", methods=['GET','POST'])
def recommend(user_id):
    # รับ param body json
    params = request.get_json()
    latitude = float(params.get('latitude'))
    longitude = float(params.get('longitude'))
    max_dis = int(params.get('max_dis',5000))
    size = int(params.get('size', 20)) 
    sort_dist = int(params.get('sort_dist', 1))

    if latitude is None or longitude is None:
        return jsonify({"error": "Missing parameter"}), 400

    with open("model.pkl", "rb") as f:
        model: NearestNeighbors = pickle.load(f)


    # load user and restaurant data โหลดเก่าใช้ไฟล์
    #user_df = pd.read_parquet("user.small.parquet")
    #restaurant_df = pd.read_parquet("restaurant.parquet").set_index("index")
        
    #user_df = userfull_data() #เอาไว้ใช้ถ้าจะใช้ fulldata
    user_df = usersmall_data()
    restaurant_df = restaurant_data().set_index("index")

  
    # find nearest neighbors to be recommend restaurants
    difference, ind = model.kneighbors(
        user_df[user_df["user_id"] == user_id].drop(columns="user_id"), n_neighbors=size
    )

    # get restaurant id from restaurant indices returned from the model
    recommend_df = restaurant_df.loc[ind[0]]

    # set distance as restaurant score
    recommend_df["difference"] = difference[0]

    # กัน float เอ๋อ
    recommend_df['latitude_float'] = recommend_df['latitude'].astype(float)
    recommend_df['longitude_float'] = recommend_df['longitude'].astype(float)

    #คำนวณค่า great circle displacement ใช้ h3
    recommend_df['displacement'] = recommend_df.apply(lambda row: h3.point_dist((latitude, longitude), (row['latitude_float'], row['longitude_float']), unit='m'), axis=1)
    recommend_df = recommend_df[recommend_df['displacement'] <= max_dis]

    #sort 
    if sort_dist == 1:
        recommend_df = recommend_df.sort_values(by='displacement')
    else:
        recommend_df = recommend_df.sort_values(by='difference')

    #latitide,longtitude เอาออกได้  มีไว้เผื่อลองเอาไปคำนวณกับตัว param ว่าตรงตามที่ใช้ h3 มั้ย
    return jsonify({"restaurants": recommend_df[["restaurant_id", "difference", "displacement", "latitude", "longitude"]].to_dict(orient="records")})
    #return jsonify({"restaurants": recommend_df[["restaurant_id", "difference", "displacement",]].to_dict(orient="records")})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
