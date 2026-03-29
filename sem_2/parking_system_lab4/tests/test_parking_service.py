import tempfile
import unittest
from pathlib import Path

from app.models.car import Car
from app.models.parking import Parking
from app.services.parking_service import (
    CarNotFoundError,
    ParkingService,
    PaymentError,
    SpotOccupiedError,
)


class TestParkingService(unittest.TestCase):
    def setUp(self) -> None:
        self.parking = Parking.create_default()
        self.service = ParkingService(self.parking)
        self.car = Car("A111AA", "Toyota", 2020, "Иванов И.И.")

    def test_place_car_success(self) -> None:
        result = self.service.place_car(self.car, "A01")
        self.assertTrue(result)
        self.assertTrue(self.parking.spots["A01"].is_occupied)
        self.assertEqual(self.parking.cars["A111AA"].spot_id, "A01")

    def test_place_car_to_occupied_spot(self) -> None:
        self.service.place_car(self.car, "A01")
        with self.assertRaises(SpotOccupiedError):
            self.service.place_car(Car("B222BB", "BMW", 2022, "Петров П.П."), "A01")

    def test_payment_success(self) -> None:
        self.service.place_car(self.car, "A01")
        receipt = self.service.pay_for_parking("A111AA", "standard")
        self.assertTrue(self.car.paid)
        self.assertEqual(receipt["cost"], 2.0)
        self.assertEqual(self.parking.total_income, 2.0)

    def test_add_service(self) -> None:
        self.service.place_car(self.car, "A01")
        price = self.service.add_service_to_car("A111AA", "wash")
        self.assertEqual(price, 230.0)
        self.assertEqual(self.parking.total_income, 230.0)

    def test_remove_car_without_payment(self) -> None:
        self.service.place_car(self.car, "A01")
        with self.assertRaises(PaymentError):
            self.service.remove_car("A111AA")

    def test_remove_car_success(self) -> None:
        self.service.place_car(self.car, "A01")
        self.service.pay_for_parking("A111AA", "standard")
        result = self.service.remove_car("A111AA")
        self.assertEqual(result["spot_id"], "A01")
        self.assertFalse(self.parking.spots["A01"].is_occupied)

    def test_car_not_found(self) -> None:
        with self.assertRaises(CarNotFoundError):
            self.service.pay_for_parking("UNKNOWN", "standard")

    def test_parking_serialization(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "parking.json"
            self.parking.save_to_file(path)
            loaded = Parking.load_from_file(path)
            self.assertEqual(len(loaded.spots), len(self.parking.spots))
            self.assertEqual(sorted(loaded.tariffs.keys()), sorted(self.parking.tariffs.keys()))


if __name__ == "__main__":
    unittest.main()


from pathlib import Path
import json
from app.models.parking import Parking


def test_load_from_file_normalizes_legacy_license_plates(tmp_path: Path) -> None:
    data = {
        "name": "Test parking",
        "spots": {
            "A01": {"spot_id": "A01", "is_occupied": True, "car_plate": "aA1221Aa", "tariff_id": "standard"},
            "A02": {"spot_id": "A02", "is_occupied": False, "car_plate": None, "tariff_id": "standard"},
        },
        "cars": {
            "aA1221Aa": {
                "license_plate": "aA1221Aa",
                "model": "BMW",
                "year": 2020,
                "owner": "Ivan",
                "entry_time": None,
                "spot_id": "A01",
                "paid": True,
                "paid_time": 1,
                "services": [],
            }
        },
        "tariffs": {
            "standard": {
                "tariff_id": "standard",
                "name": "Стандартный",
                "price": 2.0,
                "min_time": 1,
                "max_time": 1,
            }
        },
        "services": {},
        "total_income": 0.0,
        "security_status": "active",
    }

    file_path = tmp_path / "parking.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    parking = Parking.load_from_file(file_path)

    assert "AA1221AA" in parking.cars
    assert parking.spots["A01"].car_plate == "AA1221AA"
    assert parking.cars["AA1221AA"].spot_id == "A01"
