import sys

from PySide6.QtWidgets import QApplication

from controllers.main_controller import MainController
from database.db_manager import DatabaseManager
from models.repository import SportsmanRepository
from models.sportsmen import Sportsman


def main() -> None:
    """Точка входа в программу."""
    app: QApplication = QApplication(sys.argv)

    db_manager: DatabaseManager = DatabaseManager("bayern_club.db")
    db_manager.create_table()

    repository: SportsmanRepository = SportsmanRepository(db_manager)

    sportsmen: list[Sportsman] = [
        Sportsman(None, "Harry Kane", "основной", "нападающий", 30, "football", "мастер спорта"),
        Sportsman(None, "Thomas Muller", "основной", "нападающий", 20, "football", "КМС"),
        Sportsman(None, "Manuel Neuer", "основной", "вратарь", 18, "football", "КМС"),
        Sportsman(None, "Leon Goretzka", "основной", "полузащитник", 12, "football", "2-й разряд"),
        Sportsman(None, "Bayern Guard", "запасной", "разыгрывающий", 7, "basketball", "3-й разряд"),
        Sportsman(None, "Bayern Center", "основной", "центровой", 9, "basketball", "КМС"),
        Sportsman(None, "Bayern Setter", "запасной", "связующий", 5, "volleyball", "3-й разряд"),
        Sportsman(None, "Bayern Striker", "основной", "нападающий", 11, "handball", "2-й разряд"),
        Sportsman(None, "Bayern Mid", "основной", "полузащитник", 14, "football", "КМС"),
        Sportsman(None, "Bayern Keeper", "запасной", "вратарь", 6, "football", "1-й юношеский"),
        Sportsman(None, "Bayern Guard 2", "основной", "разыгрывающий", 8, "basketball", "2-й разряд"),
        Sportsman(None, "Bayern Wing", "запасной", "крайний", 4, "handball", "3-й разряд"),
    ]

    repository.replace_all_sportsmen(sportsmen)

    controller: MainController = MainController(repository)
    controller.show()

    exit_code: int = app.exec()

    db_manager.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()