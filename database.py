import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_mission(title, category, mode, time_value, duration):
    try:
        supabase.table("missions").insert({
            "title": title.strip(),
            "category": category,
            "mode": mode,
            "time_value": str(time_value),
            "duration": duration,
            "completed": False
        }).execute()
    except Exception as e:
        print("Error adding mission:", e)

def delete_mission(mission_id):
    try:
        supabase.table("missions") \
            .delete() \
            .eq("id", mission_id) \
            .execute()
    except Exception as e:
        print("Error deleting mission:", e)

def load_missions():
    try:
        response = supabase.table("missions").select("*").execute()
        return response.data
    except Exception as e:
        print("Error loading missions:", e)
        return []

def update_mission_status(mission_id, status):
    try:
        supabase.table("missions") \
            .update({"completed": bool(status)}) \
            .eq("id", mission_id) \
            .execute()
    except Exception as e:
        print("Error updating mission:", e)

def add_goal(title, category, mode, time_value, duration):
    try:
        supabase.table("goals").insert({
            "title": title.strip(),
            "category": category,
            "mode": mode,
            "time_value": str(time_value),
            "duration": duration,
            "completed": False
        }).execute()
    except Exception as e:
        print("Error adding goal:", e)

def delete_goal(goal_id):
    try:
        supabase.table("goals") \
            .delete() \
            .eq("id", goal_id) \
            .execute()
    except Exception as e:
        print("Error deleting goal:", e)

def load_goals():
    try:
        response = supabase.table("goals").select("*").execute()
        return response.data
    except Exception as e:
        print("Error loading goals:", e)
        return []
    
def update_goal_status(goal_id, status):
    try:
        supabase.table("goals") \
            .update({"completed": bool(status)}) \
            .eq("id", goal_id) \
            .execute()
    except Exception as e:
        print("Error updating goal:", e)
        
def save_goal_detail(goal_id, section, content):
    try:
        supabase.table("goal_details").upsert({
            "goal_id": goal_id,
            "section": section,
            "content": content
        }).execute()
    except Exception as e:
        print("Error saving goal detail:", e)

def load_goal_details(goal_id):
    try:
        response = supabase.table("goal_details") \
            .select("*") \
            .eq("goal_id", goal_id) \
            .execute()
        return response.data
    except Exception as e:
        print("Error loading goal details:", e)
        return []

def add_task(task, task_date, mission_id=None):
    try:
        supabase.table("tasks").insert({
            "task": task.strip(),
            "date": str(task_date),
            "mission_id": mission_id,
            "completed": False
        }).execute()
    except Exception as e:
        print("Error adding task:", e)


def load_tasks_by_date(task_date):
    try:
        response = supabase.table("tasks") \
            .select("*") \
            .eq("date", str(task_date)) \
            .execute()
        return response.data
    except Exception as e:
        print("Error loading tasks:", e)
        return []


def update_task_status(task_id, status):
    try:
        # Explicitly cast status to bool to ensure Supabase likes it
        supabase.table("tasks") \
            .update({"completed": bool(status)}) \
            .eq("id", task_id) \
            .execute()
    except Exception as e:
        print("Error updating task:", e)


def delete_task(task_id):
    try:
        supabase.table("tasks") \
            .delete() \
            .eq("id", task_id) \
            .execute()
    except Exception as e:
        print("Error deleting task:", e)

def save_habits(date, wake, sleep, water, steps, workout, screen, mood, energy, focus, meals, snacks, night_issue):
    try:
        supabase.table("habits").upsert({
            "date": date,
            "wake_time": wake,
            "sleep_time": sleep,
            "water": water,
            "steps": steps,
            "workout": workout,
            "screen_time": screen,
            "mood": mood,
            "energy": energy,
            "focus": focus,
            "meals": meals,
            "snacks": snacks,
            "night_issue": night_issue
        }).execute()
    except Exception as e:
        print("Error saving habits:", e)

def load_habits(date):
    try:
        response = supabase.table("habits").select("*").eq("date", date).execute()
        return response.data
    except Exception as e:
        print("Error loading habits:", e)
        return []

def add_wishlist(item):
    try:
        supabase.table("wishlist").insert({
            "item": item.strip(),
            "completed": False
        }).execute()
    except Exception as e:
        print("Error adding wishlist:", e)


def update_wishlist(item_id, status):
    try:
        supabase.table("wishlist") \
            .update({"completed": bool(status)}) \
            .eq("id", item_id) \
            .execute()
    except Exception as e:
        print("Error updating wishlist:", e)


def delete_wishlist(item_id):
    try:
        supabase.table("wishlist") \
            .delete() \
            .eq("id", item_id) \
            .execute()
    except Exception as e:
        print("Error deleting wishlist:", e)


def load_wishlist():
    try:
        response = supabase.table("wishlist").select("*").execute()
        return response.data
    except Exception as e:
        print("Error loading wishlist:", e)
        return []
    
def load_all_habits():
    try:
        response = supabase.table("habits").select("*").execute()
        return response.data
    except Exception as e:
        print("Error loading habits:", e)
        return []
    
def load_goal_details_all():
    try:
        response = supabase.table("goal_details").select("*").execute()
        return response.data
    except Exception as e:
        print("Error loading goal details:", e)
        return []
    
def add_routine(day, start_time, end_time, task):
    try:
        supabase.table("routines").insert({
            "day": day,
            "start_time": start_time,
            "end_time": end_time,
            "task": task.strip()
        }).execute()
    except Exception as e:
        print("Error adding routine:", e)

def load_routines():
    try:
        response = supabase.table("routines").select("*").execute()
        return response.data
    except Exception as e:
        print("Error loading routines:", e)
        return []
    
def add_note(date, note):
    try:
        supabase.table("notes").insert({
            "date": date,
            "note": note.strip()
        }).execute()
    except Exception as e:
        print("Error adding note:", e)

def load_all_notes():
    try:
        response = supabase.table("notes").select("*").execute()
        return response.data
    except Exception as e:
        print("Error loading notes:", e)
        return []
    

def add_habit_log(data):
    response = supabase.table("habits").insert({
        "date": data["date"],
        "wake_time": data["wake"],
        "sleep_time": data["sleep"],
        "water": data["water"],
        "steps": data["steps"],
        "workout": data["workout"],
        "screen_time": data["screen_time"],
        "mood": data["mood"],
        "energy": data["energy"],
        "focus": data["focus"],
        "meals": data["meals"],
        "snacks": data["snacks"],
        "night_issue": data["night_issue"]
    }).execute()

    return response

def delete_note(note_id):
    response = supabase.table("notes").delete().eq("id", note_id).execute()
    return response