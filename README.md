# Dinner Management – Backend

מערכת שרת לניהול הושבת אנשים בדינר / אירוע, בנויה כארכיטקטורת **Microservices** ב־Python, עם הפרדה ברורה בין שכבת API, שכבת Business Logic ושכבת Database Gateway.

המערכת מיועדת לעבוד מול פרונט (React/Vite) ומאפשרת:
- ניהול מוזמנים (People) כולל טעינה מקובץ CSV.
- ניהול שולחנות (Tables) כולל מיקום באולם, צורה, מגדר, מספר כיסאות וסיבוב.
- ניהול משתמשים והרשאות (Users) עם JWT.
- הדפסת מדבקות LABEL לכל משתתף ישוב.
- חיבור ל־MongoDB (מקומי או Atlas).
- תקשורת בין שירותים באמצעות **ZeroMQ (REQ/REP)**.

---

## ארכיטקטורה גבוהה

הפרויקט מחולק לשלושה שירותים נפרדים:

1. **API Gateway** – תיקייה: `dinner_managment_api_gateway`  
   - חשיפת REST API ב־HTTP באמצעות FastAPI.  
   - טיפול ב־CORS.  
   - אימות והרשאות בעזרת JWT Middleware.  
   - תקשורת לשירות Business Logic באמצעות ZeroMQ (Client).  
   - הדפסת מדבקות בעזרת `pywin32` למדפסת בשם `LABEL` (Windows בלבד).

2. **Business Logic** – תיקייה: `dinner_managment_business_logic`  
   - מכיל את הלוגיקה העסקית של המערכת:  
     - חוקים לגבי הושבה, סנכרון בין אנשים לשולחנות וכו'.  
     - ולידציה ותרגום בין בקשות HTTP לבין פעולות על בסיס הנתונים.  
   - נפתח כשרת ZeroMQ (Server) מול ה־API Gateway.  
   - פועל כ־Client ZeroMQ מול ה־Database Gateway.

3. **Database Gateway** – תיקייה: `dinner_managment_database_gateway`  
   - אחראי על תקשורת מול MongoDB.  
   - מכיל את מודלי הנתונים (Pydantic) עבור:  
     - `PersonModel`  
     - `TableModel`  
     - `UserModel`  
   - מאזין בבקשות ZeroMQ מה־Business Logic, ומבצע CRUD ב־MongoDB.

תרשים זרימה קצר:

React Client  <--HTTP-->  API Gateway  <--ZMQ-->  Business Logic  <--ZMQ-->  Database Gateway  <-->  MongoDB

---

## טכנולוגיות עיקריות

- **שפה**: Python  
- **Web Framework**: FastAPI (ב־API Gateway)  
- **תקשורת בין שירותים**: ZeroMQ (pyzmq)  
- **מסד נתונים**: MongoDB (מקומי או Atlas)  
- **אימות והרשאות**: JWT (ספריית PyJWT)  
- **מודלים וסכמות**: Pydantic  
- **הדפסה למדבקה** (Windows בלבד): pywin32 ו־GDI  

---

## מבנה הפרויקט

dinner_managment_server/
  dinner_managment_api_gateway/
    requirements.txt
    src/
      .env
      main.py
      api/
      globals/
      infrastructures/
        factory.py
      models/
  dinner_managment_business_logic/
    requirements.txt
    src/
      .env
      main.py
      api/
      globals/
      infrastructures/
        factory.py
      models/
  dinner_managment_database_gateway/
    requirements.txt
    src/
      .env
      main.py
      api/
      globals/
      infrastructures/
        factory.py
      models/

כל שירות הוא פרויקט Python עצמאי עם `requirements.txt`, קוד מקור ב־`src/` וקובץ `main.py` שמפעיל את השירות דרך מחלקת `Factory`.

---

## דרישות מקדימות (Prerequisites)

- Python 3.10 ומעלה (מומלץ 3.10/3.11).  
- גישה ל־MongoDB:  
  - או MongoDB Atlas (Cluster בענן).  
  - או MongoDB מקומי (`mongodb://127.0.0.1:27017/`).  
- מערכת הפעלה:  
  - **Windows** מומלץ (במיוחד לצורך הדפסת מדבקות באמצעות pywin32).  
  - שאר המערכת (ללא הדפסה) יכולה תאורטית לרוץ גם על Linux, אבל קוד ההדפסה מותאם ל־Windows בלבד.  
- רצוי להריץ כל שירות ב־Terminal / CMD נפרד.

---

## קובצי `.env` ופרמטרים חשובים

בכל אחד משלושת השירותים יש קובץ `src/.env`.  
מומלץ **לא לשמור סיסמאות אמיתיות בגיט** ולהחליף את השדות לערכים שלך.

### משתני סביבה משותפים

דוגמה:

MONGO_USERNAME=<your_mongo_username>
MONGO_PASSWORD=<your_mongo_password>
MONGO_CLUSTER=<your_cluster>.mongodb.net
DATABASE_NAME=dinner_db
MONGO_URI=mongodb+srv://${MONGO_USERNAME}:${MONGO_PASSWORD}@${MONGO_CLUSTER}/${DATABASE_NAME}?retryWrites=true&w=majority
MONGODB_URL=mongodb://127.0.0.1:27017/

JWT_SECRET=<strong_random_secret>
JWT_ALGORITHM=HS256
JWT_EXP_DELTA_SECONDS=3600

API_GATEWAY_PORT=8000
BUSINESS_LOGIC_PORT=8001
DATABASE_GATEWAY_PORT=8002

LOCAL_HOST=127.0.0.1
BUSINESS_LOGIC_HOST=127.0.0.1
DATABASE_GATEWAY_HOST=127.0.0.1
ZMQ_SERVER_HOST=127.0.0.1
LOCAL_PORT=8002

---

## התקנה והרצה – צעד אחר צעד

### 1. שכפול הפרויקט וכניסה לתיקייה הראשית

git clone <url-of-this-repo>
cd dinner_managment_server

### 2. יצירת Virtualenv והתקנת תלויות לכל שירות

#### API Gateway

cd dinner_managment_api_gateway
python -m venv venv
venv\Scripts\activate  # ב-Windows
pip install -r requirements.txt

#### Business Logic

cd ../dinner_managment_business_logic
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

#### Database Gateway

cd ../dinner_managment_database_gateway
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

### 3. עדכון קובצי `.env`

בכל אחת מתיקיות `src/.env` בשירותים:  
- לעדכן פרטי MongoDB  
- לעדכן JWT_SECRET חזק  
- לוודא שהפורטים וה־HOSTS מתאימים לסביבת הפיתוח שלך.

### 4. סדר הפעלה מומלץ

1. Database Gateway (ראשון)
   - cd dinner_managment_database_gateway
   - venv\Scripts\activate
   - python src/main.py

2. Business Logic
   - cd dinner_managment_business_logic
   - venv\Scripts\activate
   - python src/main.py

3. API Gateway
   - cd dinner_managment_api_gateway
   - venv\Scripts\activate
   - python src/main.py

לאחר מכן אפשר לגשת ל־API דרך:

http://127.0.0.1:8000

---

## סקירה קצרה של מודלי הנתונים

### Person

- id  
- name  
- phone (אופציונלי, עם ולידציה)  
- table_number  
- gender  
- is_reach_the_dinner  
- seat_near_friend  
- is_married, family, seat_with_family  
- special_request  
- city, street, floor, apartment_number  
- status, invitation_confirmed, contact_person  
- add_manual (נוסף ידנית / מקובץ)  
- is_active (מחיקה רכה)  
- date_created  

### Table

- id  
- people_list (מזהי אנשים)  
- position (x,y)  
- chairs (ברירת מחדל 12)  
- table_number  
- rotation (זווית במעלות)  
- gender (male/female)  
- shape (rectangle/circle/square/vip/reserva/bima)  
- is_active  
- date_created  

### User

- id  
- name  
- username  
- password (שמורה מוצפנת ב-DB Layer)  
- role (`admin` / `user`)  
- is_active  
- date_created  

---

## רמות ה-API (בגדול)

- `/auth` – התחברות וניהול משתמשים.  
- `/person` – CRUD על אנשים + ייבוא מקובץ CSV + הושבה/הורדה משולחן.  
- `/table` – CRUD על שולחנות + הוספה/הסרה של אנשים + עדכון מיקום באולם + ייבוא CSV.  
- `/print` – הדפסת מדבקות (Windows בלבד, מדפסת בשם LABEL).  

המסלולים המדויקים מוגדרים בקבצי ה-Router תחת `api/routers`.

---

## המשך פיתוח

- הוספת בדיקות (pytest / unittest).  
- הוספת Docker Compose לכל השירותים.  
- הוספת תיעוד OpenAPI מפורט ב-FastAPI.  
- שיפור לוגים וטיפול בשגיאות.  

---

## סיכום

זהו שרת Backend מודולרי ומופרד היטב לניהול הושבת אנשים באירוע.  
ניתן בקלות להרחיב את החוקים העסקיים, להוסיף סוגי דוחות, או לחבר ממשק נוסף (מובייל, מערכת ניהול אחרת) דרך ה-API Gateway.
