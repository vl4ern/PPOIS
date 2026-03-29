from database.db_manager import DatabaseManager
from models.sportsmen import Sportsman


class SportsmanRepository:
    """Класс для работы с таблицей sportsmen."""

    def __init__(self, db_manager: DatabaseManager) -> None:
 
        self.db_manager: DatabaseManager = db_manager

    def add_sportsman(self, sportsman: Sportsman) -> None:
        query: str = """
        INSERT INTO sportsmen (
            full_name,
            squad_status,
            position,
            titles_count,
            sport_type,
            rank
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(
            query,
            (
                sportsman.full_name,
                sportsman.squad_status,
                sportsman.position,
                sportsman.titles_count,
                sportsman.sport_type,
                sportsman.rank,
            )
        )
        self.db_manager.connection.commit()

    def delete_all_sportsmen(self) -> None:

        query: str = "DELETE FROM sportsmen"

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query)
        self.db_manager.connection.commit()

    def replace_all_sportsmen(self, sportsmen: list[Sportsman]) -> None:
    
        self.delete_all_sportsmen()

        for sportsman in sportsmen:
            self.add_sportsman(sportsman)

    def get_all_sportsmen(self) -> list[Sportsman]:
   
        query: str = """
        SELECT
            id,
            full_name,
            squad_status,
            position,
            titles_count,
            sport_type,
            rank
        FROM sportsmen
        ORDER BY id
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        sportsmen: list[Sportsman] = []

        for row in rows:
            sportsman: Sportsman = Sportsman(
                id=row[0],
                full_name=row[1],
                squad_status=row[2],
                position=row[3],
                titles_count=row[4],
                sport_type=row[5],
                rank=row[6],
            )
            sportsmen.append(sportsman)

        return sportsmen

    def get_sportsmen_page(self, page: int, page_size: int) -> list[Sportsman]:
  
        offset: int = (page - 1) * page_size

        query: str = """
        SELECT
            id,
            full_name,
            squad_status,
            position,
            titles_count,
            sport_type,
            rank
        FROM sportsmen
        ORDER BY id
        LIMIT ? OFFSET ?
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()

        sportsmen: list[Sportsman] = []

        for row in rows:
            sportsman: Sportsman = Sportsman(
                id=row[0],
                full_name=row[1],
                squad_status=row[2],
                position=row[3],
                titles_count=row[4],
                sport_type=row[5],
                rank=row[6],
            )
            sportsmen.append(sportsman)

        return sportsmen

    def get_total_count(self) -> int:

        query: str = "SELECT COUNT(*) FROM sportsmen"

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query)
        row = cursor.fetchone()

        return int(row[0])

    def search_by_name_or_sport(self, full_name: str, sport_type: str) -> list[Sportsman]:
  
        query: str = """
        SELECT
            id,
            full_name,
            squad_status,
            position,
            titles_count,
            sport_type,
            rank
        FROM sportsmen
        WHERE full_name = ? OR sport_type = ?
        ORDER BY id
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query, (full_name, sport_type))
        rows = cursor.fetchall()

        sportsmen: list[Sportsman] = []

        for row in rows:
            sportsman: Sportsman = Sportsman(
                id=row[0],
                full_name=row[1],
                squad_status=row[2],
                position=row[3],
                titles_count=row[4],
                sport_type=row[5],
                rank=row[6],
            )
            sportsmen.append(sportsman)

        return sportsmen

    def search_by_titles_range(self, min_titles: int, max_titles: int) -> list[Sportsman]:
        
        query: str = """
        SELECT
            id,
            full_name,
            squad_status,
            position,
            titles_count,
            sport_type,
            rank
        FROM sportsmen
        WHERE titles_count BETWEEN ? AND ?
        ORDER BY id
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query, (min_titles, max_titles))
        rows = cursor.fetchall()

        sportsmen: list[Sportsman] = []

        for row in rows:
            sportsman: Sportsman = Sportsman(
                id=row[0],
                full_name=row[1],
                squad_status=row[2],
                position=row[3],
                titles_count=row[4],
                sport_type=row[5],
                rank=row[6],
            )
            sportsmen.append(sportsman)

        return sportsmen

    def search_by_name_or_rank(self, full_name: str, rank: str) -> list[Sportsman]:
   
        query: str = """
        SELECT
            id,
            full_name,
            squad_status,
            position,
            titles_count,
            sport_type,
            rank
        FROM sportsmen
        WHERE full_name = ? OR rank = ?
        ORDER BY id
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query, (full_name, rank))
        rows = cursor.fetchall()

        sportsmen: list[Sportsman] = []

        for row in rows:
            sportsman: Sportsman = Sportsman(
                id=row[0],
                full_name=row[1],
                squad_status=row[2],
                position=row[3],
                titles_count=row[4],
                sport_type=row[5],
                rank=row[6],
            )
            sportsmen.append(sportsman)

        return sportsmen

    def delete_by_name_or_sport(self, full_name: str, sport_type: str) -> int:
    
        query: str = """
        DELETE FROM sportsmen
        WHERE full_name = ? OR sport_type = ?
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query, (full_name, sport_type))
        deleted_count: int = cursor.rowcount
        self.db_manager.connection.commit()

        return deleted_count

    def delete_by_titles_range(self, min_titles: int, max_titles: int) -> int:
   
        query: str = """
        DELETE FROM sportsmen
        WHERE titles_count BETWEEN ? AND ?
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query, (min_titles, max_titles))
        deleted_count: int = cursor.rowcount
        self.db_manager.connection.commit()

        return deleted_count

    def delete_by_name_or_rank(self, full_name: str, rank: str) -> int:
  
        query: str = """
        DELETE FROM sportsmen
        WHERE full_name = ? OR rank = ?
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query, (full_name, rank))
        deleted_count: int = cursor.rowcount
        self.db_manager.connection.commit()

        return deleted_count

    def get_unique_sports(self) -> list[str]:
  
        query: str = """
        SELECT DISTINCT sport_type
        FROM sportsmen
        ORDER BY sport_type
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        sports: list[str] = []

        for row in rows:
            sports.append(row[0])

        return sports

    def get_unique_ranks(self) -> list[str]:
   
        query: str = """
        SELECT DISTINCT rank
        FROM sportsmen
        ORDER BY rank
        """

        cursor = self.db_manager.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        ranks: list[str] = []

        for row in rows:
            ranks.append(row[0])

        return ranks