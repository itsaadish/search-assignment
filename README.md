# search-clothing


Welcome to **Clothing Search**, a full-stack web application that enables users to search for clothing items using an interactive and user-friendly interface.



## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone <github-repo-link>

###Go to main folder

### 2️⃣ Frontend Setup (React)
```bash
cd clothing-search-frontend
npm install
npm start
```
Your frontend server will start at **http://localhost:3000**.
Add your open api key in utils.py file in core folder inside backed
### 3️⃣ Backend Setup (Django)
#### Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Apply Migrations & Start Server
```bash
python manage.py migrate
python manage.py makemigrations
python manage.py runserver localhost:3100
```
Your backend server will run at **http://localhost:3100**.

---

## 📂 Project Structure
```
clothing-search/
├── backend/               # Django Backend
│   ├── manage.py          # Django Management Script
│   ├── settings.py        # Django Configuration
│   ├── ...
│
├── clothing-search-frontend/  # React Frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── ...
│
└── README.md             # Project Documentation
```

---

## 💡 Technologies Used
- **Frontend**: React, JavaScript, CSS
- **Backend**: Django, Python
- **Database**: SQLite (as per configuration)
- **Package Management**: npm, pip

---

## 🤝 Contributing
We welcome contributions! Feel free to submit issues or pull requests to improve the project.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🎯 Future Improvements
- ✅ Implement authentication & user profiles
- ✅ Add an AI-powered recommendation system
- ✅ Enhance mobile responsiveness

Let's build something amazing together! 🚀

