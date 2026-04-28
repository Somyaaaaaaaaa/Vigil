# **VIGIL**

**Status: In development**
**Type: Personal productivity and tracking dashboard**

VIGIL is a personal system to manage tasks, habits, goals, and routines in one place. It focuses on tracking daily execution, building consistency, and giving useful insights into your behavior over time.

---

## **1. Code Architecture**

* `app.py` → Entry point, routing, authentication
* `database.py` → Supabase integration and all data operations

### **Modules**

* `home.py` → Dashboard, streak tracking, overview
* `analytics.py` → Scores, trends, behavioral insights
* `habits.py` → Daily logging system
* `tasks.py` → Task execution layer
* `goals.py` → Direction and long-term planning
* `routines.py` → Time-blocking and structure
* `checklist.py` → Quick, non-time-bound execution

### **Flow**

```
app.py → route → module → database.py → Supabase
```

---

## **2. Logical Architecture**

**Execution Layer**
→ Tasks, Checklist

**Consistency Layer**
→ Habits, Streaks

**Structure Layer**
→ Routines

**Direction Layer**
→ Goals

**Reflection Layer**
→ Notes

**Analysis Layer**
→ Analytics & Insights

---

## **OPERATIONAL MODULES**

### **I. Dashboard**

### **II. Tracking**

* **Tasks:** 
* **Habits:** 

### **III. Planning**

* **Goals:**
* **Routines:** 
* **Checklist:** 

### **IV. Insights**

---

## **ACCESS**

The system is protected by a password layer.

Before running the app, configure your environment:

### **Create a `.env` file**

```
APP_PASSWORD=your_password_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

If not configured, access will be denied.

---

## **DATABASE CONFIGURATION**

VIGIL uses **Supabase** for persistent storage.

### **Setup Steps:**

1. Create a Supabase project
2. Create required tables (tasks, goals, missions, habits, notes, etc.)
3. Add credentials to `.env` (see above)

---

## **DEPLOYMENT INSTRUCTIONS**

### **1. Clone Repository**

```
git clone https://github.com/Somyaaaaaaaaa/Vigil.git
cd Vigil
```

### **2. Install Dependencies**

```
pip install -r requirements.txt
```

### **3. Configure Environment**

Create `.env` file as described above.

### **4. Run Application**

```
streamlit run app.py
```

---

## **FOR CONTRIBUTORS / USERS**

A template file is provided:

```
.env.example
```

Copy it and rename to `.env` before filling in your credentials.

---

## **SECURITY NOTE**

* `.env` is not included in the repository
* Credentials must be configured locally

---

## **License**

**© 2026 VIGIL**

For personal and non-commercial use
Attribution required if shared
Do not redistribute without credit