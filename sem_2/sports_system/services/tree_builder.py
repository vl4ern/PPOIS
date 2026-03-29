from PySide6.QtGui import QStandardItem, QStandardItemModel

from models.sportsmen import Sportsman


class TreeBuilder:
    """Строит древовидную модель по списку спортсменов."""

    @staticmethod
    def build_sportsmen_tree(sportsmen: list[Sportsman]) -> QStandardItemModel:
        model: QStandardItemModel = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Спортсмены FC Bayern Munich"])

        for sportsman in sportsmen:
            root_item: QStandardItem = QStandardItem(sportsman.full_name)

            squad_item: QStandardItem = QStandardItem(f"Состав: {sportsman.squad_status}")
            position_item: QStandardItem = QStandardItem(f"Позиция: {sportsman.position}")
            titles_item: QStandardItem = QStandardItem(f"Количество титулов: {sportsman.titles_count}")
            sport_item: QStandardItem = QStandardItem(f"Вид спорта: {sportsman.sport_type}")
            rank_item: QStandardItem = QStandardItem(f"Разряд: {sportsman.rank}")

            root_item.appendRow(squad_item)
            root_item.appendRow(position_item)
            root_item.appendRow(titles_item)
            root_item.appendRow(sport_item)
            root_item.appendRow(rank_item)

            model.appendRow(root_item)

        return model