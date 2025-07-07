# Task Manager 📌

**TaskManager** is a Django-based web application designed to organize and track work within an IT company.  
It enables efficient assignment, monitoring, and management of tasks during the development process.

Admins have full control over users, projects, and all tasks, while users can manage their own tasks  
and stay informed about their responsibilities and company environment.

## 💻 Tech Stack

---
- Python3.13🐍 
- Django5.2🌐
- SQLite (dev) / PostgreSQL (prod)🛢️
- Bootstrap5 + Custom CSS🎨
- Logic-enabled HTML Templates🧾
- Coverage.py (for testing)✅

## 🌟 Features 

---
- Role-based access (Admin / User)
- Customized admin panel
- Task management with assignment, status control, priority and deadlines
- Full CRUD for Admin (Users, Projects, Tasks)
- Limited CRUD for Users (Create/update/delete own tasks, mark as completed)
- Advanced filtering & search:
  - Tasks: by name, status, priority, task-type, project, assigned to me, created by me
  - Projects: by name
  - Users: by username, position, project
- Authentication system (Login / Logout / Registration)
- Interactive and user-friendly interface with custom UI for:
  - Home page
  - My Profile page
  - Project, Task, and Worker management pages
- Test coverage to ensure code reliability and maintainability

## 🧱 Database Schema

---
![schema.png](screenshots/schema.png)
## 🛠 Installation

---
> ⚠️ **Prerequisites:**  
Make sure you have **python 3.13** and **pip** installed on your system.  
You can check with:
>```bash
>python --version
>pip --version
>```
<br>

1. **Clone the repository:**
```bash
   git clone https://github.com/sosunovych-andrii/task-manager.git
````
2. Create and activate a virtual environment:
```bash
  python -m venv venv
  source venv/bin/activate    # For macOS/Linux
  # OR
  venv\Scripts\activate       # For Windows
```
3. Install dependencies:
```bash
  pip install -r requirements.txt
```
4. Apply migrations:
```bash
  python manage.py migrate
```
5. Run the development server:
```bash
  python manage.py runserver
  # Then open http://127.0.0.1:8000/ in your browser
```

## 🔐 Demo Login Credentials

---
Explore the application using the following demo accounts:

| Role   | Username | Password    |
|--------|----------|-------------|
| Admin  | `admin`  | `ytrewq123` |
| User   | `user`   | `ytrewq123` |

> ⚠️ You can also create your own account via registration form.

## 📸 Screenshots

---
<details>
<summary>🔽 Click to expand Admin Interface</summary>
  <img src="screenshots/img.png"/>
  <img src="screenshots/img_2.png"/>
  <img src="screenshots/img_1.png"/>
  <img src="screenshots/img_3.png"/>
  <img src="screenshots/img_4.png"/>
  <img src="screenshots/img_5.png"/>
  <img src="screenshots/img_6.png"/>
  <img src="screenshots/img_7.png"/>
  <img src="screenshots/img_8.png"/>
  <img src="screenshots/img_9.png"/>
  <img src="screenshots/img_10.png"/>
  <img src="screenshots/img_11.png"/>
  <img src="screenshots/img_12.png"/>
  <img src="screenshots/img_13.png"/>
  <img src="screenshots/img_14.png"/>
  <img src="screenshots/img_15.png"/>
</details>
<details>
<summary>🔽 Click to expand User Interface</summary>
  <img src="screenshots/img_16.png"/>
  <img src="screenshots/img_17.png"/>
  <img src="screenshots/img_18.png"/>
  <img src="screenshots/img_19.png"/>
  <img src="screenshots/img_20.png"/>
  <img src="screenshots/img_21.png"/>
  <img src="screenshots/img_22.png"/>
  <img src="screenshots/img_23.png"/>
  <img src="screenshots/img_24.png"/>
  <img src="screenshots/img_25.png"/>
  <img src="screenshots/img_26.png"/>
  <img src="screenshots/img_27.png"/>
</details>
