import xml.sax
from xml.sax.handler import ContentHandler

from models.sportsmen import Sportsman


class SportsmenSaxHandler(ContentHandler):
    """SAX-обработчик для чтения спортсменов из XML."""

    def __init__(self) -> None:
        """Инициализирует SAX-обработчик."""
        super().__init__()

        self.sportsmen: list[Sportsman] = []
        self.current_tag: str = ""
        self.current_data: dict[str, str] = {}
        self.current_text: str = ""

    def startElement(self, name: str, attrs) -> None:
        """
        Вызывается при открытии XML-тега.

        :param name: имя тега
        :param attrs: атрибуты тега
        """
        self.current_tag = name
        self.current_text = ""

        if name == "sportsman":
            self.current_data = {
                "full_name": "",
                "squad_status": "",
                "position": "",
                "titles_count": "0",
                "sport_type": "",
                "rank": "",
            }

    def characters(self, content: str) -> None:
        """
        Вызывается при чтении текстового содержимого тега.

        :param content: текстовое содержимое
        """
        self.current_text += content

    def endElement(self, name: str) -> None:
        """
        Вызывается при закрытии XML-тега.

        :param name: имя тега
        """
        text_value: str = self.current_text.strip()

        if name in self.current_data:
            self.current_data[name] = text_value

        if name == "sportsman":
            sportsman: Sportsman = Sportsman(
                id=None,
                full_name=self.current_data["full_name"],
                squad_status=self.current_data["squad_status"],
                position=self.current_data["position"],
                titles_count=int(self.current_data["titles_count"]),
                sport_type=self.current_data["sport_type"],
                rank=self.current_data["rank"],
            )
            self.sportsmen.append(sportsman)

        self.current_tag = ""
        self.current_text = ""


class XmlSaxReader:
    """Отвечает за чтение списка спортсменов из XML через SAX."""

    @staticmethod
    def load_from_xml(file_path: str) -> list[Sportsman]:
        """
        Загружает список спортсменов из XML-файла.

        :param file_path: путь к XML-файлу
        :return: список спортсменов
        """
        handler: SportsmenSaxHandler = SportsmenSaxHandler()
        xml.sax.parse(file_path, handler)
        return handler.sportsmen