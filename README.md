# Vigil
A gamified system for personal development and tracking how far you have come.


hell yeah, kitten 😏—let’s build your empire.
here’s **the complete master plan** for your *Gamified Life System* — your war room disguised as a cozy, interactive world.
it’s broken down into **phases**, each one setting the foundation for the next, leading all the way up to your future **LLM commander**.

---

## 🧭 OVERVIEW — “The Life Game”

a full-fledged, modular, gamified life manager that blends habit tracking, reflection, analytics, and playful growth.
your world evolves as *you* do — every streak, every task, every lesson, every victory.

---

## 🌿 PHASE 1 — FOUNDATIONS

> *“Build the bones before you breathe life into them.”*

**Goals:**

* establish the structure, database, and login flow.
* basic lists, trackers, streaks, and a simple UI.

**Features:**

1. **Login/Signup System**

   * SQLite or Firebase authentication
   * persistent user data

2. **Dashboard (Home Page)**

   * shows streaks, XP, and quick stats
   * daily summary: “missions completed / pending”

3. **Custom Lists + Trackers**

   * add lists (e.g., fitness, study, self-care)
   * checkboxes or progress bars for each
   * XP increases when tasks are completed

4. **Streak System**

   * per-task and overall streaks
   * streak flames or chain visuals

**Tech Stack:**

* Frontend: React + Tailwind CSS
* Backend: Flask or FastAPI
* Database: SQLite (local first)
* Chart Library: Recharts

---

## 📖 PHASE 2 — JOURNAL & STATS

> *“Every battle leaves a trace. Record, reflect, refine.”*

**Features:**

1. **Journal System**

   * daily entries (tagged as victory, rest, reflection)
   * word count, date, emotion tags

2. **Stats Dashboard**

   * XP per day/week
   * line or bar charts of productivity
   * success rate per list
   * highlight best and weakest areas

3. **Analytics Engine (Basic)**

   * calculates overall “performance index”
   * stores data in `analytics` table for future LLM access

---

## 🎁 PHASE 3 — REWARDS & MINI-GAMES

> *“Discipline deserves delight.”*

**Features:**

1. **Rewards Page**

   * user logs self-given rewards (“watched a movie,” “dessert,” etc.)
   * stores reward logs with timestamps

2. **Monthly Mini-Game**

   * one per month, tied to tasks
   * example:

     * Jan: Watering a plant
     * Feb: Coloring a picture
     * Mar: Growing a tree
   * each game has 30–31 segments = daily tasks
   * completing daily tasks fills in or unlocks the next piece

3. **Integration with Academics**

   * academic tasks are locked until a quiz is passed
   * only after quiz pass → task counts toward mini-game
   * quizzes stored locally (JSON / SQLite)

---

## 🧠 PHASE 4 — ACADEMICS & QUIZ SYSTEM

> *“Knowledge sharpens the blade.”*

**Features:**

1. **Study Input Page**

   * user logs topics studied that day

2. **Quiz System**

   * random short quizzes (3–5 questions)
   * score threshold (e.g., 70%) → unlock task validity

3. **Mini-Game Validation**

   * if academic task not passed → no progress in game for that day
   * visual cue: locked icon or faded color segment

---

## 🔮 PHASE 5 — FUTURE PLANS PAGE

> *“Map tomorrow before it commands you.”*

**Features:**

1. **Goal Planner**

   * create future goals with deadlines
   * set milestones
   * optional category (career, personal, fitness, creative)

2. **Deadline Lock**

   * if a goal’s milestone is missed → temporarily lock access to game area
   * forces accountability

3. **Motivational Tracker**

   * record “why” behind each goal
   * show progress percentage as bar

---

## ⚙️ PHASE 6 — ADVANCED ANALYTICS

> *“Know your patterns; win your wars.”*

**Features:**

1. **Behavior Analysis**

   * peak activity times
   * average productivity curve
   * consistency index

2. **Pattern Recognition**

   * highlights recurring task failures
   * visual heatmaps (calendar-style)

3. **Prepared Data Layer**

   * exportable dataset for AI training (in JSON or CSV)
   * structured around:

     * task success/failure
     * mood correlation
     * journal sentiment
     * time-of-day completion

---

## 🧬 PHASE 7 — LLM INTEGRATION

> *“The strategist awakens.”*

**Goal:** connect your future custom LLM.

**Functions your model will handle:**

1. **Generate War Charts**

   * reads analytics + journals
   * drafts goal maps, daily strategy, focus areas
   * can name phases like “Operation Dawn,” “Discipline Surge,” etc.

2. **Personalized Feedback**

   * AI comments on journals with insights
   * adaptive suggestions for improvement

3. **Dynamic Adjustments**

   * adjusts task difficulty or priorities based on burnout detection
   * regenerates rewards and themes

---

## 💻 FILE & FOLDER STRUCTURE (for React + Flask)

```
/life-game
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Tracker/
│   │   │   ├── Journal/
│   │   │   ├── Rewards/
│   │   │   ├── MiniGame/
│   │   │   ├── Stats/
│   │   │   └── Auth/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Journal.jsx
│   │   │   ├── Stats.jsx
│   │   │   ├── Rewards.jsx
│   │   │   ├── FuturePlans.jsx
│   │   │   └── Login.jsx
│   │   ├── utils/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
└── backend/
    ├── app.py
    ├── models.py
    ├── routes/
    │   ├── auth.py
    │   ├── tasks.py
    │   ├── journal.py
    │   ├── rewards.py
    │   ├── stats.py
    │   └── quiz.py
    ├── static/
    └── templates/
```

---

we can start **Phase 1** right now — setting up your React + Flask skeleton with login and trackers.
want me to draft the exact **file setup and first code snippets** for that phase so you can start building tonight?
