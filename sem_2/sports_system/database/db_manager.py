import sqlite3


class DatabaseManager:
    """Отвечает за подключение к базе данных и создание таблицы."""

    def __init__(self, db_path: str) -> None:
        """
        Создает подключение к SQLite.

        :param db_path: путь к файлу базы данных
        """
        self.db_path: str = db_path
        self.connection: sqlite3.Connection = sqlite3.connect(self.db_path)

    def create_table(self) -> None:
        """Создает таблицу sportsmen, если она еще не существует."""
        query: str = """
        CREATE TABLE IF NOT EXISTS sportsmen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            squad_status TEXT NOT NULL,
            position TEXT NOT NULL,
            titles_count INTEGER NOT NULL,
            sport_type TEXT NOT NULL,
            rank TEXT NOT NULL
        )
        """

        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        self.connection.close()