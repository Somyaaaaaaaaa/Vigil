# **VIGIL**

**Status: Operational**
**Classification: Personal Command & Intelligence Dashboard**

VIGIL is a high-fidelity tactical management system designed for complete oversight of daily operations. It combines execution tracking, behavioral analysis, and strategic planning within a unified, mission-oriented interface.

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

### **I. COMMAND (Dashboard)**

Central control node providing real-time situational awareness of active objectives, streaks, and system status.

### **II. DATA ACQUISITION (Tracking)**

* **Tasks:** Daily objective execution
* **Habits:** Behavioral consistency tracking

### **III. STRATEGY (Planning)**

* **Goals:** Long-term trajectory alignment
* **Routines:** Structured daily systems (SOPs)
* **Checklist:** Non-time-sensitive execution pool

### **IV. INTELLIGENCE (Insights)**

Processes behavioral data into actionable insights, identifying patterns, inefficiencies, and performance gaps.

---

## **ACCESS PROTOCOL**

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

Copy it and rename to `.env`, then fill in your credentials.

---

## **SECURITY NOTE**

* `.env` is not included in the repository
* Credentials must be configured locally
* Do not expose your Supabase keys publicly

---

## **INTELLECTUAL PROPERTY NOTICE**

**© 2026 VIGIL CORE. ALL RIGHTS RESERVED.**

The Vigil system, including its design language and structure, is an original work.

* Non-commercial use only
* Attribution required if shared
* Rebranding or redistribution without credit is not permitted
