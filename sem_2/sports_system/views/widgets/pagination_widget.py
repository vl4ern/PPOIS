from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)


class PaginationWidget(QWidget):
    """Универсальный виджет пагинации."""

    first_page_clicked = Signal()
    previous_page_clicked = Signal()
    next_page_clicked = Signal()
    last_page_clicked = Signal()
    page_size_changed = Signal(int)

    def __init__(self) -> None:
        """Инициализирует виджет пагинации."""
        super().__init__()

        self.current_page: int = 1
        self.total_pages: int = 1
        self.total_records: int = 0

        self.main_layout: QHBoxLayout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(8)
        self.setLayout(self.main_layout)

        self.first_button: QPushButton = QPushButton("Первая")
        self.main_layout.addWidget(self.first_button)

        self.previous_button: QPushButton = QPushButton("Предыдущая")
        self.main_layout.addWidget(self.previous_button)

        self.next_button: QPushButton = QPushButton("Следующая")
        self.main_layout.addWidget(self.next_button)

        self.last_button: QPushButton = QPushButton("Последняя")
        self.main_layout.addWidget(self.last_button)

        self.main_layout.addSpacing(12)

        self.page_size_label: QLabel = QLabel("На странице:")
        self.main_layout.addWidget(self.page_size_label)

        self.page_size_combo: QComboBox = QComboBox()
        self.page_size_combo.addItems(["5", "10", "20", "50"])
        self.page_size_combo.setCurrentText("10")
        self.main_layout.addWidget(self.page_size_combo)

        self.main_layout.addStretch()

        self.page_info_label: QLabel = QLabel("Страница 1 из 1")
        self.main_layout.addWidget(self.page_info_label)

        self.records_info_label: QLabel = QLabel("Записей: 0")
        self.main_layout.addWidget(self.records_info_label)

        self.first_button.clicked.connect(self.first_page_clicked.emit)
        self.previous_button.clicked.connect(self.previous_page_clicked.emit)
        self.next_button.clicked.connect(self.next_page_clicked.emit)
        self.last_button.clicked.connect(self.last_page_clicked.emit)
        self.page_size_combo.currentTextChanged.connect(self._emit_page_size_changed)

        self.update_info(1, 1, 0)

    def _emit_page_size_changed(self, value: str) -> None:
        """
        Отправляет сигнал об изменении размера страницы.

        :param value: новое количество записей на странице
        """
        self.page_size_changed.emit(int(value))

    def update_info(self, current_page: int, total_pages: int, total_records: int) -> None:
        """
        Обновляет состояние виджета пагинации.

        :param current_page: текущая страница
        :param total_pages: общее количество страниц
        :param total_records: общее количество записей
        """
        self.current_page = current_page
        self.total_pages = max(1, total_pages)
        self.total_records = total_records

        self.page_info_label.setText(f"Страница {self.current_page} из {self.total_pages}")
        self.records_info_label.setText(f"Записей: {self.total_records}")

        self.first_button.setEnabled(self.current_page > 1)
        self.previous_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)
        self.last_button.setEnabled(self.current_page < self.total_pages)

    def get_page_size(self) -> int:
        """
        Возвращает текущее количество записей на странице.

        :return: размер страницы
        """
        return int(self.page_size_combo.currentText())

    def set_enabled(self, enabled: bool) -> None:
        """
        Включает или выключает виджет пагинации.

        :param enabled: состояние доступности
        """
        self.first_button.setEnabled(enabled and self.current_page > 1)
        self.previous_button.setEnabled(enabled and self.current_page > 1)
        self.next_button.setEnabled(enabled and self.current_page < self.total_pages)
        self.last_button.setEnabled(enabled and self.current_page < self.total_pages)
        self.page_size_combo.setEnabled(enabled)