import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from models.car import Car
from models.parking import Parking
from.services.parking_service import PaskingService

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ParkingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.parking = Parking.load_from_file()
        self.servece = PaskingService(self.parking)

        self.title("Модель автостоянки")
        self.geometry("1000*700")
        self.resizable(True, True)

        self.create_widgets()