from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from models.sportsmen import Sportsman
from views.widgets.pagination_widget import PaginationWidget


class MainWindow(QMainWindow):
    """Главное окно приложения."""

    def __init__(self) -> None:
        """Инициализирует главное окно и его интерфейс."""
        super().__init__()

        self.setWindowTitle("FC Bayern Munich Sports System")
        self.resize(1280, 760)

        self._create_actions()
        self._create_menu()
        self._create_toolbar()
        self._create_status_bar()
        self._create_central_widget()
        self._apply_styles()

    def _create_actions(self) -> None:
        """Создает действия для меню и панели инструментов."""
        self.refresh_action: QAction = QAction("Обновить", self)
        self.add_action: QAction = QAction("Добавить", self)
        self.search_action: QAction = QAction("Поиск", self)
        self.delete_action: QAction = QAction("Удалить", self)
        self.reset_search_action: QAction = QAction("Сбросить поиск", self)
        self.table_view_action: QAction = QAction("Таблица", self)
        self.tree_view_action: QAction = QAction("Дерево", self)
        self.save_xml_action: QAction = QAction("Сохранить XML", self)
        self.load_xml_action: QAction = QAction("Загрузить XML", self)
        self.exit_action: QAction = QAction("Выход", self)

    def _create_menu(self) -> None:
        """Создает строку меню."""
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction(self.refresh_action)
        file_menu.addAction(self.save_xml_action)
        file_menu.addAction(self.load_xml_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        records_menu = menu_bar.addMenu("Записи")
        records_menu.addAction(self.add_action)
        records_menu.addAction(self.search_action)
        records_menu.addAction(self.delete_action)
        records_menu.addAction(self.reset_search_action)

        view_menu = menu_bar.addMenu("Вид")
        view_menu.addAction(self.table_view_action)
        view_menu.addAction(self.tree_view_action)

    def _create_toolbar(self) -> None:
        """Создает панель инструментов."""
        self.toolbar: QToolBar = QToolBar("Главная панель")
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.toolbar.addAction(self.refresh_action)
        self.toolbar.addAction(self.add_action)
        self.toolbar.addAction(self.search_action)
        self.toolbar.addAction(self.delete_action)
        self.toolbar.addAction(self.reset_search_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.save_xml_action)
        self.toolbar.addAction(self.load_xml_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.table_view_action)
        self.toolbar.addAction(self.tree_view_action)

    def _create_status_bar(self) -> None:
        """Создает строку состояния."""
        self.statusBar().showMessage("Готово к работе")

    def _create_central_widget(self) -> None:
        """Создает центральную часть окна."""
        self.central_widget: QWidget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(16, 16, 16, 12)
        self.main_layout.setSpacing(12)
        self.central_widget.setLayout(self.main_layout)

        self.title_label: QLabel = QLabel("Система учета спортсменов FC Bayern Munich")
        self.title_label.setObjectName("titleLabel")
        self.main_layout.addWidget(self.title_label)

        self.subtitle_label: QLabel = QLabel(
            "Bayern Edition • просмотр, поиск, удаление, импорт и экспорт записей"
        )
        self.subtitle_label.setObjectName("subtitleLabel")
        self.main_layout.addWidget(self.subtitle_label)

        self.content_frame: QFrame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        self.content_layout: QVBoxLayout = QVBoxLayout()
        self.content_layout.setContentsMargins(12, 12, 12, 12)
        self.content_layout.setSpacing(10)
        self.content_frame.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_frame)

        self.view_stack: QStackedWidget = QStackedWidget()
        self.content_layout.addWidget(self.view_stack)

        self.table_widget: QTableWidget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
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
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.view_stack.addWidget(self.table_widget)

        self.tree_view: QTreeView = QTreeView()
        self.tree_view.setHeaderHidden(False)
        self.view_stack.addWidget(self.tree_view)

        self.actions_panel: QFrame = QFrame()
        self.actions_panel.setObjectName("bottomPanel")
        self.actions_layout: QHBoxLayout = QHBoxLayout()
        self.actions_layout.setContentsMargins(10, 8, 10, 8)
        self.actions_layout.setSpacing(8)
        self.actions_panel.setLayout(self.actions_layout)
        self.content_layout.addWidget(self.actions_panel)

        self.refresh_button: QPushButton = QPushButton("Обновить")
        self.actions_layout.addWidget(self.refresh_button)

        self.add_button: QPushButton = QPushButton("Добавить")
        self.actions_layout.addWidget(self.add_button)

        self.search_button: QPushButton = QPushButton("Поиск")
        self.actions_layout.addWidget(self.search_button)

        self.delete_button: QPushButton = QPushButton("Удалить")
        self.actions_layout.addWidget(self.delete_button)

        self.reset_search_button: QPushButton = QPushButton("Сбросить поиск")
        self.actions_layout.addWidget(self.reset_search_button)

        self.actions_layout.addStretch()

        self.pagination_panel: QFrame = QFrame()
        self.pagination_panel.setObjectName("bottomPanel")
        self.pagination_layout: QVBoxLayout = QVBoxLayout()
        self.pagination_layout.setContentsMargins(10, 8, 10, 8)
        self.pagination_panel.setLayout(self.pagination_layout)
        self.content_layout.addWidget(self.pagination_panel)

        self.pagination_widget: PaginationWidget = PaginationWidget()
        self.pagination_layout.addWidget(self.pagination_widget)

    def _apply_styles(self) -> None:
        """Применяет темную стилизацию с красными акцентами."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d0d0d;
            }

            QWidget {
                color: #f3f4f6;
                font-size: 13px;
            }

            QMenuBar {
                background-color: #111111;
                border-bottom: 1px solid #2a2a2a;
                padding: 4px;
                color: #f3f4f6;
            }

            QMenuBar::item {
                padding: 6px 10px;
                background: transparent;
            }

            QMenuBar::item:selected {
                background: #b00020;
                border-radius: 6px;
            }

            QMenu {
                background-color: #151515;
                border: 1px solid #2a2a2a;
                color: #f3f4f6;
            }

            QMenu::item {
                padding: 8px 20px;
            }

            QMenu::item:selected {
                background-color: #b00020;
            }

            QToolBar {
                background-color: #111111;
                border: none;
                border-bottom: 1px solid #2a2a2a;
                spacing: 6px;
                padding: 6px;
            }

            QToolButton {
                background-color: #1a1a1a;
                border: 1px solid #2b2b2b;
                border-radius: 8px;
                padding: 6px 10px;
                color: #f3f4f6;
            }

            QToolButton:hover {
                background-color: #b00020;
                border: 1px solid #d90429;
            }

            QToolButton:pressed {
                background-color: #8d0019;
            }

            QLabel#titleLabel {
                font-size: 24px;
                font-weight: 700;
                color: #ffffff;
                padding-top: 4px;
            }

            QLabel#subtitleLabel {
                font-size: 13px;
                color: #9ca3af;
                padding-bottom: 2px;
            }

            QFrame#contentFrame {
                background-color: #121212;
                border: 1px solid #262626;
                border-radius: 14px;
            }

            QFrame#bottomPanel {
                background-color: #161616;
                border: 1px solid #2b2b2b;
                border-radius: 10px;
            }

            QTableWidget, QTreeView {
                background-color: #101010;
                alternate-background-color: #161616;
                border: 1px solid #2a2a2a;
                border-radius: 10px;
                gridline-color: #262626;
                selection-background-color: #b00020;
                selection-color: #ffffff;
                color: #f3f4f6;
            }

            QHeaderView::section {
                background-color: #1a1a1a;
                color: #ffffff;
                padding: 8px;
                border: none;
                border-right: 1px solid #2b2b2b;
                border-bottom: 1px solid #2b2b2b;
                font-weight: 600;
            }

            QPushButton {
                background-color: #1a1a1a;
                border: 1px solid #2b2b2b;
                border-radius: 8px;
                padding: 7px 12px;
                min-width: 95px;
                color: #f3f4f6;
            }

            QPushButton:hover {
                background-color: #b00020;
                border: 1px solid #d90429;
            }

            QPushButton:pressed {
                background-color: #8d0019;
            }

            QPushButton:disabled {
                color: #6b7280;
                background-color: #161616;
                border: 1px solid #222222;
            }

            QComboBox {
                background-color: #1a1a1a;
                border: 1px solid #2b2b2b;
                border-radius: 8px;
                padding: 6px 10px;
                color: #f3f4f6;
                min-width: 70px;
            }

            QComboBox {
                background-color: #1a1a1a;
                border: 1px solid #2b2b2b;
                border-radius: 8px;
                padding: 6px 10px;
                color: #f3f4f6;
                min-width: 70px;
            }

            QComboBox:hover {
                border: 1px solid #d90429;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border-left: 1px solid #2b2b2b;
                background-color: #151515;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }

            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #151515;
                color: #f3f4f6;
                border: 1px solid #2b2b2b;
                outline: 0;
                selection-background-color: #b00020;
                selection-color: #ffffff;
                padding: 4px;
            }

            QComboBox QAbstractItemView::item {
                min-height: 26px;
                padding: 6px 10px;
                background-color: #151515;
                color: #f3f4f6;
            }

            QComboBox QAbstractItemView::item:selected {
                background-color: #b00020;
                color: #ffffff;
            }

            QComboBox QAbstractItemView::item:hover {
                background-color: #8d0019;
                color: #ffffff;
            }

            QComboBox:hover {
                border: 1px solid #d90429;
            }

            QStatusBar {
                background-color: #111111;
                border-top: 1px solid #2a2a2a;
                color: #d1d5db;
            }

            QScrollBar:vertical {
                background: #111111;
                width: 12px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background: #b00020;
                min-height: 30px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover {
                background: #d90429;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }

            QScrollBar:horizontal {
                background: #111111;
                height: 12px;
                margin: 0;
            }

            QScrollBar::handle:horizontal {
                background: #b00020;
                min-width: 30px;
                border-radius: 6px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #d90429;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0;
            }
        """)

    def update_table(self, sportsmen: list[Sportsman]) -> None:
        """
        Обновляет содержимое таблицы.

        :param sportsmen: список спортсменов для отображения
        """
        self.table_widget.setRowCount(len(sportsmen))

        for row_index, sportsman in enumerate(sportsmen):
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(str(sportsman.id)))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(sportsman.full_name))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(sportsman.squad_status))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(sportsman.position))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(str(sportsman.titles_count)))
            self.table_widget.setItem(row_index, 5, QTableWidgetItem(sportsman.sport_type))
            self.table_widget.setItem(row_index, 6, QTableWidgetItem(sportsman.rank))

        self.table_widget.resizeRowsToContents()

    def update_tree(self, model: QStandardItemModel) -> None:
        """
        Обновляет древовидное представление.

        :param model: модель дерева
        """
        self.tree_view.setModel(model)
        self.tree_view.expandAll()
        self.tree_view.resizeColumnToContents(0)

    def show_table_view(self) -> None:
        """Переключает отображение на таблицу."""
        self.view_stack.setCurrentIndex(0)
        self.statusBar().showMessage("Режим просмотра: таблица")

    def show_tree_view(self) -> None:
        """Переключает отображение на дерево."""
        self.view_stack.setCurrentIndex(1)
        self.statusBar().showMessage("Режим просмотра: дерево")