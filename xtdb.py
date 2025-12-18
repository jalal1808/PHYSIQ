import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "knowledge_base.db"

# Excel file paths
DOCTORS_XLSX = "data/doctors.xlsx"
EXERCISES_XLSX = "data/exercises.xlsx"
FOOD_XLSX = "data/food.xlsx"

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        designation TEXT,
        speciality TEXT,
        location TEXT,
        fee REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_name TEXT,
        muscle TEXT,
        equipment TEXT,
        rating REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_item TEXT,
        category TEXT,
        calories REAL,
        protein REAL,
        carbs REAL,
        fat REAL,
        fiber REAL,
        weight_loss_rating INTEGER,
        weight_gain_rating INTEGER,
        primary_goal TEXT
    )
    """)

    conn.commit()

def load_doctors(conn):
    df = pd.read_excel(DOCTORS_XLSX)
    df.to_sql("doctors", conn, if_exists="append", index=False)

def load_exercises(conn):
    df = pd.read_excel(EXERCISES_XLSX)
    df.columns = ["exercise_name", "muscle", "equipment", "rating"]
    df.to_sql("exercises", conn, if_exists="append", index=False)

def load_food(conn):
    df = pd.read_excel(FOOD_XLSX)
    df.columns = [
        "food_item", "category", "calories", "protein",
        "carbs", "fat", "fiber",
        "weight_loss_rating", "weight_gain_rating", "primary_goal"
    ]
    df.to_sql("food", conn, if_exists="append", index=False)

def main():
    conn = sqlite3.connect(DB_PATH)

    create_tables(conn)
    load_doctors(conn)
    load_exercises(conn)
    load_food(conn)

    conn.close()
    print("Excel data successfully loaded into SQLite")

if __name__ == "__main__":
    main()

