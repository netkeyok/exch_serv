import sqlite3
import os

# Определение пути к корневой директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_NAME = "local_database.db"

# Определение пути к базе данных в корне проекта
DB_PATH = os.path.join(BASE_DIR, DB_NAME)


def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS document_numbers (
            prefix TEXT PRIMARY KEY,
            current_number INTEGER NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def generate_document_number(prefix, wh_id):
    # Инициализация базы данных при отсутствии
    if not os.path.exists(DB_PATH):
        initialize_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Проверка текущего номера для данного префикса
    cursor.execute(
        "SELECT current_number FROM document_numbers WHERE prefix = ?", (prefix,)
    )
    row = cursor.fetchone()

    if row is None:
        # Если префикс не существует, инициализируем его с 1
        current_number = 1
        cursor.execute(
            "INSERT INTO document_numbers (prefix, current_number) VALUES (?, ?)",
            (prefix, current_number),
        )
    else:
        # Если префикс существует, инкрементируем номер
        current_number = row[0] + 1
        cursor.execute(
            "UPDATE document_numbers SET current_number = ? WHERE prefix = ?",
            (current_number, prefix),
        )

    conn.commit()
    conn.close()

    # Возвращаем новый номер документа с двумя префиксами
    return f"{prefix}{wh_id}{current_number:08d}"


if __name__ == "__main__":
    pass
    # Примеры использования
    # print(generate_document_number("INV", "WH01"))  # Например, "INVWH0100000001"
    # print(generate_document_number("PO", "WH02"))   # Например, "POWH0200000001"
    # print(generate_document_number("INV", "WH01"))  # Например, "INVWH0100000002"
