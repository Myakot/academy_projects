import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

def fetch_task(worker_id, db_url):
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.callproc('fetch_task', (worker_id,))
    task_id = cur.fetchone()[0]
    conn.commit()  # Фиксируем транзакцию здесь
    conn.close()
    return task_id

def complete_task(task_id, db_url):
    logging.info(f"Completing task {task_id}")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.callproc('complete_task', (task_id,))
    result = cur.fetchone()
    logging.info(f"Result of complete_task procedure: {result}")
    if result:
        logging.info(f"Result of complete_task procedure is not empty")
    else:
        logging.info(f"Result of complete_task procedure is empty")
    conn.commit()
    conn.close()
    return result[0] if result else None

def create_task(task_name, db_url):
    logging.info(f"Creating task {task_name}")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task_name, status) VALUES (%s, 'pending')", (task_name,))
    conn.commit()
    conn.close()

db_url = "postgresql://user:password@server/test_db"

task_name = "Новая задача"
create_task(task_name, db_url)

worker_id = 1
task_id = fetch_task(worker_id, db_url)
if task_id is None:
    logging.info("Нет доступных задач")
else:
    result = complete_task(task_id, db_url)
    if result:
        logging.info(f"Задача {task_id} выполнена")
    else:
        logging.info(f"Задача {task_id} не выполнена")
