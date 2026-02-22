import unittest
from datetime import datetime

from models.car import Car
from models.parking import Parking
from services.parking_service import PaskingService, SpotOccuoiedError, CArNotFound, PaymentError

class TestParkingService(unittest.TestCase):
    
    def setUp(self):
        self.parking = Parking.create_default()
        self.service = PaskingService(self.parking)
        
        # Стандартная тестовая машина
        self.test_car = Car("A111AA", "Toyota", 2020, "Иванов И.И.")

    def test_place_car_success(self):
        result = self.service.place_car(self.test_car, "A01")
        self.assertTrue(result)
        self.assertTrue(self.parking.spots["A01"].is_occupied)
        self.assertEqual(self.parking.cars["A111AA"].spot_id, "A01")

    def test_place_car_invalid_spot(self):
        #Проверка исключения (Ожидаем ValueError)
        with self.assertRaises(ValueError):
            self.service.place_car(self.test_car, "Z99")

    def test_place_car_occupied_spot(self):
        #Проверка исключения (Ожидаем SpotOccuoiedError)
        self.service.place_car(self.test_car, "A01")
        second_car = Car("B222BB", "BMW", 2022, "Петров П.П.")
        with self.assertRaises(SpotOccuoiedError):
            self.service.place_car(second_car, "A01")


    def test_pay_for_parking_success(self):
        """Успешная оплата парковки"""
        self.service.place_car(self.test_car, "A01")
        receipt = self.service.pay_for_parking("A111AA", "standart")
        
        self.assertTrue(self.test_car.paid)
        self.assertEqual(receipt['cost'], 2.0)
        self.assertEqual(self.parking.total_income, 2.0)

    def test_pay_for_parking_car_not_found(self):
        """Попытка оплатить за машину, которой нет на парковке"""
        with self.assertRaises(CArNotFound):
            self.service.pay_for_parking("GHOST_CAR", "standart")

    def test_add_service_to_car_success(self):
        self.service.place_car(self.test_car, "A01")
        cost = self.service.add_service_to_car("A111AA", "wash")
        
        self.assertEqual(cost, 230.0)
        self.assertIn("wash", self.test_car.services)
        self.assertEqual(self.parking.total_income, 230.0)

    def test_remove_car_success(self):
        self.service.place_car(self.test_car, "A01")
        self.service.pay_for_parking("A111AA", "standart")
        
        result = self.service.remove_car("A111AA")
        
        # Проверяем, что машина удалена из словаря
        self.assertNotIn("A111AA", self.parking.cars)
        # Проверяем, что место A01 снова свободно
        self.assertFalse(self.parking.spots["A01"].is_occupied)
        # Проверяем возврат данных
        self.assertEqual(result['spot_id'], "A01")

    def test_remove_car_without_payment(self):
        #проверка исключения PaymentError
        self.service.place_car(self.test_car, "A01")
        with self.assertRaises(PaymentError):
            self.service.remove_car("A111AA")

    def test_optimize_traffic_stats(self):
        #Проверка правильности подсчета статистики парковки
        self.service.place_car(self.test_car, "A01")         
        stats = self.service.optimize_traffic()        
        self.assertEqual(stats['total_spots'], 14)
        self.assertEqual(stats['occupied_spots'], 1)
        self.assertEqual(stats['free_spots'], 13)
        self.assertEqual(stats['occupancy_rate'], 7.1)

    def test_reset_income(self):
        #Проверка очистки счетчика дохода
        self.service.place_car(self.test_car, "A01")
        self.service.pay_for_parking("A111AA", "standart") 
        self.service.add_service_to_car("A111AA", "wash")  
        
        self.assertEqual(self.parking.total_income, 232.0)
        
        # Обнуляем
        self.service.reset_income()
        self.assertEqual(self.parking.total_income, 0.0)

if __name__ == '__main__':
    unittest.main()