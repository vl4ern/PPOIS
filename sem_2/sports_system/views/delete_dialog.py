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
    QVBoxLayout,
)


class DeleteDialog(QDialog):
    """Диалоговое окно для удаления спортсменов."""

    def __init__(self, sports: list[str], ranks: list[str]) -> None:
        """
        Инициализирует окно удаления.

        :param sports: список уникальных видов спорта
        :param ranks: список уникальных разрядов
        """
        super().__init__()

        self.setWindowTitle("Удалить спортсменов")
        self.resize(500, 320)

        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.info_label: QLabel = QLabel("Удаление спортсменов FC Bayern Munich")
        self.main_layout.addWidget(self.info_label)

        self.delete_type_combo: QComboBox = QComboBox()
        self.delete_type_combo.addItems(
            [
                "Удалить по ФИО или виду спорта",
                "Удалить по диапазону титулов",
                "Удалить по ФИО или разряду",
            ]
        )
        self.main_layout.addWidget(self.delete_type_combo)

        self.stacked_widget: QStackedWidget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self._create_name_or_sport_page(sports)
        self._create_titles_range_page()
        self._create_name_or_rank_page(ranks)

        self.buttons_layout: QHBoxLayout = QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)

        self.delete_button: QPushButton = QPushButton("Удалить")
        self.buttons_layout.addWidget(self.delete_button)

        self.cancel_button: QPushButton = QPushButton("Отмена")
        self.buttons_layout.addWidget(self.cancel_button)

        self.delete_type_combo.currentIndexChanged.connect(self.stacked_widget.setCurrentIndex)
        self.delete_button.clicked.connect(self._validate_and_accept)
        self.cancel_button.clicked.connect(self.reject)

    def _create_name_or_sport_page(self, sports: list[str]) -> None:
        """
        Создает страницу удаления по ФИО или виду спорта.

        :param sports: список видов спорта
        """
        page = QDialog()
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
        """Создает страницу удаления по диапазону титулов."""
        page = QDialog()
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
        Создает страницу удаления по ФИО или разряду.

        :param ranks: список разрядов
        """
        page = QDialog()
        layout: QFormLayout = QFormLayout()
        page.setLayout(layout)

        self.name_input_2: QLineEdit = QLineEdit()
        layout.addRow("ФИО спортсмена:", self.name_input_2)

        self.rank_input: QComboBox = QComboBox()
        self.rank_input.addItem("")
        self.rank_input.addItems(ranks)
        layout.addRow("Разряд:", self.rank_input)

        self.stacked_widget.addWidget(page)

    def _validate_and_accept(self) -> None:
        """Проверяет корректность данных перед удалением."""
        delete_data: dict = self.get_delete_data()

        if delete_data["delete_type"] == "name_or_sport":
            if not delete_data["full_name"] and not delete_data["sport_type"]:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Нужно заполнить хотя бы ФИО спортсмена или вид спорта."
                )
                return

        elif delete_data["delete_type"] == "titles_range":
            if delete_data["min_titles"] > delete_data["max_titles"]:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Минимальное количество титулов не может быть больше максимального."
                )
                return

        elif delete_data["delete_type"] == "name_or_rank":
            if not delete_data["full_name"] and not delete_data["rank"]:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Нужно заполнить хотя бы ФИО спортсмена или разряд."
                )
                return

        self.accept()

    def get_delete_data(self) -> dict:
        """
        Возвращает данные, введенные пользователем в зависимости от режима удаления.

        :return: словарь с параметрами удаления
        """
        delete_type_index: int = self.delete_type_combo.currentIndex()

        if delete_type_index == 0:
            return {
                "delete_type": "name_or_sport",
                "full_name": self.name_input_1.text().strip(),
                "sport_type": self.sport_input.currentText().strip(),
            }

        if delete_type_index == 1:
            return {
                "delete_type": "titles_range",
                "min_titles": self.min_titles_input.value(),
                "max_titles": self.max_titles_input.value(),
            }

        return {
            "delete_type": "name_or_rank",
            "full_name": self.name_input_2.text().strip(),
            "rank": self.rank_input.currentText().strip(),
        }