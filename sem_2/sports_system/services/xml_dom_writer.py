from xml.dom.minidom import Document

from models.sportsmen import Sportsman


class XmlDomWriter:
    """Отвечает за сохранение списка спортсменов в XML через DOM."""

    @staticmethod
    def save_to_xml(file_path: str, sportsmen: list[Sportsman]) -> None:
        """
        Сохраняет список спортсменов в XML-файл.

        :param file_path: путь к XML-файлу
        :param sportsmen: список спортсменов
        """
        document: Document = Document()

        root_element = document.createElement("sportsmen")
        document.appendChild(root_element)

        for sportsman in sportsmen:
            sportsman_element = document.createElement("sportsman")
            root_element.appendChild(sportsman_element)

            XmlDomWriter._append_text_element(document, sportsman_element, "full_name", sportsman.full_name)
            XmlDomWriter._append_text_element(document, sportsman_element, "squad_status", sportsman.squad_status)
            XmlDomWriter._append_text_element(document, sportsman_element, "position", sportsman.position)
            XmlDomWriter._append_text_element(document, sportsman_element, "titles_count", str(sportsman.titles_count))
            XmlDomWriter._append_text_element(document, sportsman_element, "sport_type", sportsman.sport_type)
            XmlDomWriter._append_text_element(document, sportsman_element, "rank", sportsman.rank)

        with open(file_path, "w", encoding="utf-8") as xml_file:
            xml_file.write(document.toprettyxml(indent="    "))

    @staticmethod
    def _append_text_element(
        document: Document,
        parent_element,
        tag_name: str,
        text_value: str,
    ) -> None:
        """
        Создает XML-элемент с текстом и добавляет его в родительский элемент.

        :param document: DOM-документ
        :param parent_element: родительский XML-элемент
        :param tag_name: имя тега
        :param text_value: текстовое значение
        """
        child_element = document.createElement(tag_name)
        text_node = document.createTextNode(text_value)
        child_element.appendChild(text_node)
        parent_element.appendChild(child_element)