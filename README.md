# LMWN_ASSIGN Machine Learning Engineer
รัน ใน venv 
- python -m venv env
- env/scripts/activate

Build docker-compose
- Docker-compose build 
- Docker-compose up

หลังจาก Docker-compose up จะสามารถเข้า localhost ได้ 
![up](https://github.com/Ferryjeerakit/LMWN_ASSIGN/assets/153589125/a7b675a9-df79-4fa1-a517-973362629713)

โดยเราสามารถรับ method get,post ได้ผ่าน http://127.0.0.1:5000/recommend/u00000 โดยสามารถสาง parameter ไปแล้วรับกับมาเป็น json ได้ครับ
โดยสามารถดู Test-performance ได้ จากตัว performance_report.pdf ครับ

**ตัว database server ผมเลือกใช้เป็น mysql**
- docker exec -it workspace-db-1 bash
- mysql -uroot -p
- password: banana

  ในส่วนของ database ถ้า databaseไม่ได้สร้างtableขึ้นมาสามารถ import จาก .sql ที่ผมแนบไว้ให้ได้ครับ
