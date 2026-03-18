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
    QVBoxLayout,
)

from models.enums import SportRank, SquadStatus
from models.sportsmen import Sportsman


class AddDialog(QDialog):
    """Диалоговое окно для добавления нового спортсмена."""

    def __init__(self) -> None:
        """Инициализирует окно добавления спортсмена."""
        super().__init__()

        self.setWindowTitle("Добавить спортсмена")
        self.resize(450, 300)

        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.info_label: QLabel = QLabel("Добавление нового спортсмена FC Bayern Munich")
        self.main_layout.addWidget(self.info_label)

        self.form_layout: QFormLayout = QFormLayout()
        self.main_layout.addLayout(self.form_layout)

        self.full_name_input: QLineEdit = QLineEdit()
        self.form_layout.addRow("ФИО спортсмена:", self.full_name_input)

        self.squad_status_input: QComboBox = QComboBox()
        self.squad_status_input.addItems([status.value for status in SquadStatus])
        self.form_layout.addRow("Состав:", self.squad_status_input)

        self.position_input: QLineEdit = QLineEdit()
        self.form_layout.addRow("Позиция:", self.position_input)

        self.titles_count_input: QSpinBox = QSpinBox()
        self.titles_count_input.setMinimum(0)
        self.titles_count_input.setMaximum(1000)
        self.form_layout.addRow("Количество титулов:", self.titles_count_input)

        self.sport_type_input: QLineEdit = QLineEdit()
        self.form_layout.addRow("Вид спорта:", self.sport_type_input)

        self.rank_input: QComboBox = QComboBox()
        self.rank_input.addItems([rank.value for rank in SportRank])
        self.form_layout.addRow("Разряд:", self.rank_input)

        self.buttons_layout: QHBoxLayout = QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)

        self.save_button: QPushButton = QPushButton("Сохранить")
        self.buttons_layout.addWidget(self.save_button)

        self.cancel_button: QPushButton = QPushButton("Отмена")
        self.buttons_layout.addWidget(self.cancel_button)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_sportsman_data(self) -> Sportsman | None:
        """
        Собирает данные из формы и возвращает объект Sportsman.

        :return: объект Sportsman или None, если данные некорректны
        """
        full_name: str = self.full_name_input.text().strip()
        squad_status: str = self.squad_status_input.currentText()
        position: str = self.position_input.text().strip()
        titles_count: int = self.titles_count_input.value()
        sport_type: str = self.sport_type_input.text().strip()
        rank: str = self.rank_input.currentText()

        if not full_name:
            QMessageBox.warning(self, "Ошибка", "Поле ФИО спортсмена не может быть пустым.")
            return None

        if not position:
            QMessageBox.warning(self, "Ошибка", "Поле позиции не может быть пустым.")
            return None

        if not sport_type:
            QMessageBox.warning(self, "Ошибка", "Поле вида спорта не может быть пустым.")
            return None

        sportsman: Sportsman = Sportsman(
            id=None,
            full_name=full_name,
            squad_status=squad_status,
            position=position,
            titles_count=titles_count,
            sport_type=sport_type,
            rank=rank,
        )

        return sportsman