import mysql.connector

from mysql.connector import Error
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date

DB_CONFIG = {
    "host": "192.168.1.60",
    "port": 3306,
    "user": "root",
    "password": "rootpassword",
    "database": "task_app"
}


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def write_task_to_data(task_data: BaseModel):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = '''
            INSERT INTO tasks (title, description, due_date, priority) VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(query, (task_data.title, task_data.description, task_data.due_date, task_data.priority))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error writing to MySQL: {e}")
        raise


def read_task_all_data() -> List[Dict]:
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = 'SELECT * FROM tasks'
        cursor.execute(query)
        tasks = cursor.fetchall()
        cursor.close()
        connection.close()
        return tasks
    except Error as e:
        print(f"Error reading from MySQL: {e}")
        raise


def get_task_id_data(task_id: int) -> Optional[Dict]:
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = '''SELECT * FROM tasks WHERE id = %s'''
        cursor.execute(query, (task_id,))
        task = cursor.fetchone()
        cursor.close()
        connection.close()
        return task
    except Error as e:
        print(f"Error reading task by ID from MySQL: {e}")
        raise


def get_task_id_len() -> int:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = '''SELECT COUNT(*) FROM tasks '''
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count
    except Error as e:
        print(f"Error reading count from MySQL: {e}")
        raise


def update_task_data(task_id: int, task_data: BaseModel):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = '''
            UPDATE tasks SET title = %s, description = %s, due_date = %s, priority = %s
            WHERE id = %s 
        '''
        cursor.execute(query, (task_data.title, task_data.description, task_data.due_date, task_data.priority, task_id))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error update task in MySQL: {e}")
        raise


def delete_task_data_by_id(task_id: int):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = '''DELETE FROM tasks WHERE id = %s'''
        cursor.execute(query, (task_id,))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error deleting task in MySQL: {e}")
        raise