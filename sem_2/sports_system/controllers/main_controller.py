from PySide6.QtWidgets import QFileDialog, QMessageBox

from models.repository import SportsmanRepository
from models.sportsmen import Sportsman
from services.tree_builder import TreeBuilder
from services.xml_dom_writer import XmlDomWriter
from services.xml_sax_reader import XmlSaxReader
from views.add_dialog import AddDialog
from views.delete_dialog import DeleteDialog
from views.main_window import MainWindow
from views.search_dialog import SearchDialog


class MainController:
    """Контроллер главного окна."""

    def __init__(self, repository: SportsmanRepository) -> None:
        """
        Инициализирует контроллер главного окна.

        :param repository: репозиторий для работы с данными спортсменов
        """
        self.repository: SportsmanRepository = repository
        self.page_size: int = 10
        self.current_page: int = 1
        self.current_sportsmen: list[Sportsman] = []

        self.main_window: MainWindow = MainWindow()
        self._connect_signals()
        self.load_page()

    def _connect_signals(self) -> None:
        """Связывает элементы интерфейса с методами контроллера."""
        self.main_window.refresh_button.clicked.connect(self.refresh_data)
        self.main_window.add_button.clicked.connect(self.open_add_dialog)
        self.main_window.search_button.clicked.connect(self.open_search_dialog)
        self.main_window.delete_button.clicked.connect(self.open_delete_dialog)
        self.main_window.reset_search_button.clicked.connect(self.reset_search)

        self.main_window.refresh_action.triggered.connect(self.refresh_data)
        self.main_window.add_action.triggered.connect(self.open_add_dialog)
        self.main_window.search_action.triggered.connect(self.open_search_dialog)
        self.main_window.delete_action.triggered.connect(self.open_delete_dialog)
        self.main_window.reset_search_action.triggered.connect(self.reset_search)
        self.main_window.table_view_action.triggered.connect(self.switch_to_table_view)
        self.main_window.tree_view_action.triggered.connect(self.switch_to_tree_view)
        self.main_window.save_xml_action.triggered.connect(self.save_to_xml)
        self.main_window.load_xml_action.triggered.connect(self.load_from_xml)
        self.main_window.exit_action.triggered.connect(self.main_window.close)

        self.main_window.pagination_widget.first_page_clicked.connect(self.go_to_first_page)
        self.main_window.pagination_widget.previous_page_clicked.connect(self.go_to_previous_page)
        self.main_window.pagination_widget.next_page_clicked.connect(self.go_to_next_page)
        self.main_window.pagination_widget.last_page_clicked.connect(self.go_to_last_page)
        self.main_window.pagination_widget.page_size_changed.connect(self.change_page_size)

    def _update_views(self, sportsmen: list[Sportsman]) -> None:
        """
        Обновляет таблицу и дерево текущими данными.

        :param sportsmen: список спортсменов для отображения
        """
        self.current_sportsmen = sportsmen
        self.main_window.update_table(sportsmen)

        tree_model = TreeBuilder.build_sportsmen_tree(sportsmen)
        self.main_window.update_tree(tree_model)

    def load_page(self) -> None:
        """Загружает текущую страницу записей."""
        total_count: int = self.repository.get_total_count()
        total_pages: int = max(1, (total_count + self.page_size - 1) // self.page_size)

        if self.current_page > total_pages:
            self.current_page = total_pages

        sportsmen: list[Sportsman] = self.repository.get_sportsmen_page(
            self.current_page,
            self.page_size
        )

        self._update_views(sportsmen)
        self.main_window.pagination_widget.update_info(self.current_page, total_pages, total_count)
        self.main_window.statusBar().showMessage("Данные загружены")

    def refresh_data(self) -> None:
        """Обновляет данные в таблице и дереве."""
        self.current_page = 1
        self.load_page()

    def go_to_first_page(self) -> None:
        """Переходит на первую страницу."""
        self.current_page = 1
        self.load_page()

    def go_to_previous_page(self) -> None:
        """Переходит на предыдущую страницу."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_page()

    def go_to_next_page(self) -> None:
        """Переходит на следующую страницу."""
        total_count: int = self.repository.get_total_count()
        total_pages: int = max(1, (total_count + self.page_size - 1) // self.page_size)

        if self.current_page < total_pages:
            self.current_page += 1
            self.load_page()

    def go_to_last_page(self) -> None:
        """Переходит на последнюю страницу."""
        total_count: int = self.repository.get_total_count()
        total_pages: int = max(1, (total_count + self.page_size - 1) // self.page_size)
        self.current_page = total_pages
        self.load_page()

    def change_page_size(self, page_size: int) -> None:
        """
        Изменяет количество записей на странице.

        :param page_size: новый размер страницы
        """
        self.page_size = page_size
        self.current_page = 1
        self.load_page()

    def open_add_dialog(self) -> None:
        """Открывает диалог добавления нового спортсмена."""
        dialog: AddDialog = AddDialog()
        result: int = dialog.exec()

        if result:
            sportsman: Sportsman | None = dialog.get_sportsman_data()

            if sportsman is None:
                return

            self.repository.add_sportsman(sportsman)

            QMessageBox.information(
                self.main_window,
                "Успешно",
                "Новый спортсмен успешно добавлен."
            )

            total_count: int = self.repository.get_total_count()
            total_pages: int = max(1, (total_count + self.page_size - 1) // self.page_size)
            self.current_page = total_pages
            self.load_page()

    def open_search_dialog(self) -> None:
        """Открывает полноценный диалог поиска спортсменов."""
        sports: list[str] = self.repository.get_unique_sports()
        ranks: list[str] = self.repository.get_unique_ranks()

        dialog: SearchDialog = SearchDialog(self.repository, sports, ranks)
        dialog.exec()

    def open_delete_dialog(self) -> None:
        """Открывает диалог удаления спортсменов."""
        sports: list[str] = self.repository.get_unique_sports()
        ranks: list[str] = self.repository.get_unique_ranks()

        dialog: DeleteDialog = DeleteDialog(sports, ranks)
        result: int = dialog.exec()

        if result:
            delete_data: dict = dialog.get_delete_data()
            deleted_count: int = 0

            if delete_data["delete_type"] == "name_or_sport":
                deleted_count = self.repository.delete_by_name_or_sport(
                    delete_data["full_name"],
                    delete_data["sport_type"],
                )
            elif delete_data["delete_type"] == "titles_range":
                deleted_count = self.repository.delete_by_titles_range(
                    delete_data["min_titles"],
                    delete_data["max_titles"],
                )
            elif delete_data["delete_type"] == "name_or_rank":
                deleted_count = self.repository.delete_by_name_or_rank(
                    delete_data["full_name"],
                    delete_data["rank"],
                )

            QMessageBox.information(
                self.main_window,
                "Удаление завершено",
                f"Удалено записей: {deleted_count}"
            )

            self.current_page = 1
            self.load_page()

    def save_to_xml(self) -> None:
        """Сохраняет все записи из базы данных в XML-файл."""
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Сохранить XML",
            "",
            "XML Files (*.xml)"
        )

        if not file_path:
            return

        sportsmen: list[Sportsman] = self.repository.get_all_sportsmen()
        XmlDomWriter.save_to_xml(file_path, sportsmen)

        QMessageBox.information(
            self.main_window,
            "Успешно",
            "Данные успешно сохранены в XML."
        )
        self.main_window.statusBar().showMessage("XML-файл сохранен")

    def load_from_xml(self) -> None:
        """Загружает записи из XML-файла и обновляет базу данных."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Загрузить XML",
            "",
            "XML Files (*.xml)"
        )

        if not file_path:
            return

        sportsmen: list[Sportsman] = XmlSaxReader.load_from_xml(file_path)
        self.repository.replace_all_sportsmen(sportsmen)

        QMessageBox.information(
            self.main_window,
            "Успешно",
            "Данные успешно загружены из XML."
        )

        self.current_page = 1
        self.load_page()
        self.main_window.statusBar().showMessage("XML-файл загружен")

    def reset_search(self) -> None:
        """Обновляет главное окно обычными данными."""
        self.current_page = 1
        self.load_page()
        self.main_window.statusBar().showMessage("Главное окно обновлено")

    def switch_to_table_view(self) -> None:
        """Переключает отображение на таблицу."""
        self.main_window.show_table_view()

    def switch_to_tree_view(self) -> None:
        """Переключает отображение на дерево."""
        self.main_window.show_tree_view()

    def show(self) -> None:
        """Показывает главное окно."""
        self.main_window.show()