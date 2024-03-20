# LMWN_ASSIGN Machine Learning Engineer
รัน ใน venv 
- python -m venv env
- env/scripts/activate

Build docker-compose
- Docker-compose build 
- Docker-compose up

หลังจาก Docker-compose up จะสามารถเข้า localhost ได้ 
![up](https://github.com/Ferryjeerakit/LMWN_ASSIGN/assets/153589125/a7b675a9-df79-4fa1-a517-973362629713)

โดยเราสามารถรับ method get,post ได้ผ่าน http://127.0.0.1:5000/recommend/u00000 โดยสามารถส่ง parameter ไปแล้วรับกับมาเป็น json ได้ครับ
โดยสามารถดู Test-performance ได้ จากตัว performance_report.pdf ครับ
![postman](https://github.com/Ferryjeerakit/LMWN_ASSIGN/assets/153589125/ec7fc567-a348-401a-819a-1c7304e69c29)


**ในส่วนโปรแกรมผมได้สร้าง Docker container ที่จะประกอบด้วย**
ตัวโปรแกรมที่จะรัน Flask และตัว mysql server</br></br> 
#**ตัวโปรแกรม**
- ผมให้รับ param จาก mysql table -> user,restaurant
- จากนั้นนำข้อมูลไปใช้ในโมเดล nearest
- ในส่วนของ great circle displacement ผมใช้ h3 รับ param latiude,logitude จาก user และเอามาคำนวณกับ restaurant (ทดสอบแล้วตรงตามระยะ meter)
- user สามารถส่ง param lat,long,size,max_dis,sort_dis เพื่อกำหนด result ได้ โดยถ้าค่าเป็น null จะใส่เป็น default ที่กำหนดไว้
  ![param](https://github.com/Ferryjeerakit/LMWN_ASSIGN/assets/153589125/4e77ce11-e6d6-4c85-8e28-cc4909264b63)
- หลังจาก รับค่าแล้วจะ return เป็น json ให้
  


#**ตัว database server ผมเลือกใช้เป็น mysql**
- docker exec -it workspace-db-1 bash
- mysql -uroot -p
- password: banana
![sql](https://github.com/Ferryjeerakit/LMWN_ASSIGN/assets/153589125/4ed67526-7e5c-4020-ae48-56aa2736fc11)

  ในส่วนของ database ถ้า databaseไม่ได้สร้างtableขึ้นมาสามารถ import จาก .sql ที่ผมแนบไว้ให้
