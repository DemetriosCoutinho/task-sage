import bcrypt
from .config import config
import psycopg2

def conectar_db():
    params = config()
    return psycopg2.connect(**params)

def add_user(username, password, user_type):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)",
                (username, hashed.decode('utf-8'), user_type)
            )

def login_user(username, password):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT password, user_type FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                hashed_password = result[0].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return result[1]  # Retorna o tipo de usuário
    return None

# CRUD para Projetos

def add_project(name, begin_date, end_date):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO projects (name, begin_date, end_date) VALUES (%s, %s, %s)",
                (name, begin_date, end_date)
            )

def remove_project(project_id):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))

def update_project(project_id, **kwargs):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            for column, value in kwargs.items():
                cursor.execute(f"UPDATE projects SET {column} = %s WHERE id = %s", (value, project_id))

# CRUD para Tarefas

def add_task(name, project_id, due_date, status):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (name, project_id, due_date, status) VALUES (%s, %s, %s, %s)",
                (name, project_id, due_date, status)
            )

def remove_task(task_id):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))

def update_task(task_id, **kwargs):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            for column, value in kwargs.items():
                cursor.execute(f"UPDATE tasks SET {column} = %s WHERE id = %s", (value, task_id))

def search_data(tabela):
    """Busca todos os dados de uma tabela especificada."""
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tabela}")
            result = cursor.fetchall()
    return result