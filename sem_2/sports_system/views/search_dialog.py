from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
    QAbstractItemView,
)

from models.sportsmen import Sportsman
from models.repository import SportsmanRepository
from views.widgets.pagination_widget import PaginationWidget


class SearchDialog(QDialog):
    """Диалоговое окно для поиска спортсменов с выводом результатов."""

    def __init__(self, repository: SportsmanRepository, sports: list[str], ranks: list[str]) -> None:
        """
        Инициализирует окно поиска.

        :param repository: репозиторий для работы с данными
        :param sports: список уникальных видов спорта
        :param ranks: список уникальных разрядов
        """
        super().__init__()

        self.repository: SportsmanRepository = repository
        self.current_results: list[Sportsman] = []
        self.current_page: int = 1
        self.page_size: int = 10

        self.setWindowTitle("Поиск спортсменов")
        self.resize(1000, 650)

        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.info_label: QLabel = QLabel("Поиск спортсменов FC Bayern Munich")
        self.main_layout.addWidget(self.info_label)

        self.search_type_combo: QComboBox = QComboBox()
        self.search_type_combo.addItems(
            [
                "По ФИО или виду спорта",
                "По диапазону титулов",
                "По ФИО или разряду",
            ]
        )
        self.main_layout.addWidget(self.search_type_combo)

        self.stacked_widget: QStackedWidget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self._create_name_or_sport_page(sports)
        self._create_titles_range_page()
        self._create_name_or_rank_page(ranks)

        self.buttons_layout: QHBoxLayout = QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)

        self.search_button: QPushButton = QPushButton("Найти")
        self.buttons_layout.addWidget(self.search_button)

        self.clear_button: QPushButton = QPushButton("Очистить")
        self.buttons_layout.addWidget(self.clear_button)

        self.close_button: QPushButton = QPushButton("Закрыть")
        self.buttons_layout.addWidget(self.close_button)

        self.results_label: QLabel = QLabel("Результаты поиска")
        self.main_layout.addWidget(self.results_label)

        self.results_table: QTableWidget = QTableWidget()
        self.results_table.setColumnCount(7)
        self.results_table.setHorizontalHeaderLabels(
            [
                "ID",
                "ФИО спортсмена",
                "Состав",
                "Позиция",
                "Титулы",
                "Вид спорта",
                "Разряд",
            ]
        )
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.main_layout.addWidget(self.results_table)

        self.pagination_widget: PaginationWidget = PaginationWidget()
        self.main_layout.addWidget(self.pagination_widget)

        self.search_type_combo.currentIndexChanged.connect(self.stacked_widget.setCurrentIndex)
        self.search_button.clicked.connect(self.perform_search)
        self.clear_button.clicked.connect(self.clear_results)
        self.close_button.clicked.connect(self.reject)

        self.pagination_widget.first_page_clicked.connect(self.go_to_first_page)
        self.pagination_widget.previous_page_clicked.connect(self.go_to_previous_page)
        self.pagination_widget.next_page_clicked.connect(self.go_to_next_page)
        self.pagination_widget.last_page_clicked.connect(self.go_to_last_page)
        self.pagination_widget.page_size_changed.connect(self.change_page_size)

        self.pagination_widget.update_info(1, 1, 0)

    def _create_name_or_sport_page(self, sports: list[str]) -> None:
        """
        Создает страницу поиска по ФИО или виду спорта.

        :param sports: список видов спорта
        """
        page = QWidget()
        layout: QFormLayout = QFormLayout()
        page.setLayout(layout)

        self.name_input_1: QLineEdit = QLineEdit()
        layout.addRow("ФИО спортсмена:", self.name_input_1)

        self.sport_input: QComboBox = QComboBox()
        self.sport_input.addItem("")
        self.sport_input.addItems(sports)
        layout.addRow("Вид спорта:", self.sport_input)

        self.stacked_widget.addWidget(page)

    def _create_titles_range_page(self) -> None:
        """Создает страницу поиска по диапазону титулов."""
        page = QWidget()
        layout: QFormLayout = QFormLayout()
        page.setLayout(layout)

        self.min_titles_input: QSpinBox = QSpinBox()
        self.min_titles_input.setMinimum(0)
        self.min_titles_input.setMaximum(1000)
        layout.addRow("Минимум титулов:", self.min_titles_input)

        self.max_titles_input: QSpinBox = QSpinBox()
        self.max_titles_input.setMinimum(0)
        self.max_titles_input.setMaximum(1000)
        self.max_titles_input.setValue(1000)
        layout.addRow("Максимум титулов:", self.max_titles_input)

        self.stacked_widget.addWidget(page)

    def _create_name_or_rank_page(self, ranks: list[str]) -> None:
        """
        Создает страницу поиска по ФИО или разряду.

        :param ranks: список разрядов
        """
        page = QWidget()
        layout: QFormLayout = QFormLayout()
        page.setLayout(layout)

        self.name_input_2: QLineEdit = QLineEdit()
        layout.addRow("ФИО спортсмена:", self.name_input_2)

        self.rank_input: QComboBox = QComboBox()
        self.rank_input.addItem("")
        self.rank_input.addItems(ranks)
        layout.addRow("Разряд:", self.rank_input)

        self.stacked_widget.addWidget(page)

    def perform_search(self) -> None:
        """Выполняет поиск по выбранным параметрам."""
        search_data: dict = self.get_search_data()

        if search_data["search_type"] == "name_or_sport":
            if not search_data["full_name"] and not search_data["sport_type"]:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Нужно заполнить хотя бы ФИО спортсмена или вид спорта."
                )
                return

            self.current_results = self.repository.search_by_name_or_sport(
                search_data["full_name"],
                search_data["sport_type"],
            )

        elif search_data["search_type"] == "titles_range":
            if search_data["min_titles"] > search_data["max_titles"]:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Минимальное количество титулов не может быть больше максимального."
                )
                return

            self.current_results = self.repository.search_by_titles_range(
                search_data["min_titles"],
                search_data["max_titles"],
            )

        elif search_data["search_type"] == "name_or_rank":
            if not search_data["full_name"] and not search_data["rank"]:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Нужно заполнить хотя бы ФИО спортсмена или разряд."
                )
                return

            self.current_results = self.repository.search_by_name_or_rank(
                search_data["full_name"],
                search_data["rank"],
            )

        self.current_page = 1
        self.update_results_table()

        if not self.current_results:
            QMessageBox.information(
                self,
                "Результат поиска",
                "По заданным параметрам записи не найдены."
            )

    def update_results_table(self) -> None:
        """Обновляет таблицу результатов поиска с учетом пагинации."""
        total_records: int = len(self.current_results)
        total_pages: int = max(1, (total_records + self.page_size - 1) // self.page_size)

        if self.current_page > total_pages:
            self.current_page = total_pages

        start_index: int = (self.current_page - 1) * self.page_size
        end_index: int = start_index + self.page_size
        page_items: list[Sportsman] = self.current_results[start_index:end_index]

        self.results_table.setRowCount(len(page_items))

        for row_index, sportsman in enumerate(page_items):
            self.results_table.setItem(row_index, 0, QTableWidgetItem(str(sportsman.id)))
            self.results_table.setItem(row_index, 1, QTableWidgetItem(sportsman.full_name))
            self.results_table.setItem(row_index, 2, QTableWidgetItem(sportsman.squad_status))
            self.results_table.setItem(row_index, 3, QTableWidgetItem(sportsman.position))
            self.results_table.setItem(row_index, 4, QTableWidgetItem(str(sportsman.titles_count)))
            self.results_table.setItem(row_index, 5, QTableWidgetItem(sportsman.sport_type))
            self.results_table.setItem(row_index, 6, QTableWidgetItem(sportsman.rank))

        self.pagination_widget.update_info(self.current_page, total_pages, total_records)

    def clear_results(self) -> None:
        """Очищает результаты поиска."""
        self.current_results = []
        self.current_page = 1
        self.results_table.setRowCount(0)
        self.pagination_widget.update_info(1, 1, 0)

    def go_to_first_page(self) -> None:
        """Переходит на первую страницу результатов."""
        self.current_page = 1
        self.update_results_table()

    def go_to_previous_page(self) -> None:
        """Переходит на предыдущую страницу результатов."""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_results_table()

    def go_to_next_page(self) -> None:
        """Переходит на следующую страницу результатов."""
        total_records: int = len(self.current_results)
        total_pages: int = max(1, (total_records + self.page_size - 1) // self.page_size)

        if self.current_page < total_pages:
            self.current_page += 1
            self.update_results_table()

    def go_to_last_page(self) -> None:
        """Переходит на последнюю страницу результатов."""
        total_records: int = len(self.current_results)
        total_pages: int = max(1, (total_records + self.page_size - 1) // self.page_size)
        self.current_page = total_pages
        self.update_results_table()

    def change_page_size(self, page_size: int) -> None:
        """
        Изменяет количество записей на странице.

        :param page_size: новый размер страницы
        """
        self.page_size = page_size
        self.current_page = 1
        self.update_results_table()

    def get_search_data(self) -> dict:
        """
        Возвращает данные формы поиска.

        :return: словарь с параметрами поиска
        """
        search_type_index: int = self.search_type_combo.currentIndex()

        if search_type_index == 0:
            return {
                "search_type": "name_or_sport",
                "full_name": self.name_input_1.text().strip(),
                "sport_type": self.sport_input.currentText().strip(),
            }

        if search_type_index == 1:
            return {
                "search_type": "titles_range",
                "min_titles": self.min_titles_input.value(),
                "max_titles": self.max_titles_input.value(),
            }

        return {
            "search_type": "name_or_rank",
            "full_name": self.name_input_2.text().strip(),
            "rank": self.rank_input.currentText().strip(),
        }