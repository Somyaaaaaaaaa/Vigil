## **STEP 0 — PREPARE YOUR ENVIRONMENT**

1. **Install VS Code** (if not already).
2. **Install Node.js** (needed for React frontend).

   * check: `node -v` in terminal
3. **Install Python 3** (for Flask backend).

   * check: `python --version`
4. **Install pip** (Python package manager).

---

## **STEP 1 — CREATE THE FOLDER STRUCTURE**

1. Open VS Code.
2. Create a main folder called `VIGIL`.
3. Inside `VIGIL`, create two folders: `frontend` and `backend`.

   ```
   VIGIL/
     frontend/
     backend/
   ```
4. Open VS Code terminal in `VIGIL` folder.

---

## **STEP 2 — SET UP BACKEND (FLASK + SQLITE)**

1. Navigate to `backend`:

   ```bash
   cd backend
   ```
2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```
3. Activate it:

   * Windows: `venv\Scripts\activate`
   * Mac/Linux: `source venv/bin/activate`
4. Install Flask and SQLAlchemy:

   ```bash
   pip install flask flask_sqlalchemy flask_cors
   ```
5. Create **files** inside `backend`:

   * `app.py`
   * `models.py`
   * `routes/` folder with `auth.py` and `tasks.py`

we’ll put the backend code (from my last message) into these files.

6. **Run your Flask server:**

   ```bash
   python app.py
   ```

   * you should see `Running on http://127.0.0.1:5000/`

---

## **STEP 3 — SET UP FRONTEND (REACT + TAILWIND)**

1. Open a new terminal in `VIGIL/frontend`.
2. Create a React app:

   ```bash
   npx create-react-app .
   ```
3. Install Tailwind:

   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```
4. Configure Tailwind (`tailwind.config.js`):

   ```js
   content: ["./src/**/*.{js,jsx,ts,tsx}"],
   theme: { extend: {} },
   plugins: [],
   ```
5. Import Tailwind in `src/index.css`:

   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```
6. Start React dev server:

   ```bash
   npm start
   ```

   * opens at `http://localhost:3000/`

---

## **STEP 4 — CONNECT FRONTEND & BACKEND**

1. Install Axios in frontend:

   ```bash
   npm install axios react-router-dom
   ```
2. Create components:

   * `Auth/` → `Login.jsx` and `Signup.jsx`
   * `Tracker/` → `Tracker.jsx`
3. Use Axios to call Flask endpoints (`/signup`, `/login`, `/tasks`).
4. Test API calls with Postman first (optional).

---
