from __future__ import annotations
from flask import Flask, flash, redirect, render_template, request, url_for
from app.facade import ParkingFacade
from app.services.parking_service import CarNotFoundError, PaymentError, SpotOccupiedError

app = Flask(__name__)
app.config["SECRET_KEY"] = "parking-system-lab4-secret"


def get_facade() -> ParkingFacade:
    return ParkingFacade()


@app.get("/")
def index():
    facade = get_facade()
    return render_template(
        "index.html",
        stats=facade.stats(),
        cars=facade.cars_for_view(),
        tariffs=facade.tariffs_for_view(),
        services=facade.services_for_view(),
        security_info=None,
    )


@app.post("/park")
def park_car():
    facade = get_facade()
    try:
        facade.place_car(
            license_plate=request.form["license_plate"],
            model=request.form["model"],
            year=int(request.form["year"]),
            owner=request.form["owner"],
            spot_id=request.form["spot_id"],
        )
        flash("Автомобиль успешно размещён.", "success")
    except (ValueError, SpotOccupiedError) as error:
        flash(str(error), "error")
    return redirect(url_for("index"))


@app.post("/pay")
def pay_car():
    facade = get_facade()
    try:
        result = facade.pay_for_parking(
            license_plate=request.form["license_plate"],
            tariff_id=request.form["tariff_id"],
        )
        flash(f"Оплата выполнена: {result['cost']} $.", "success")
    except (ValueError, CarNotFoundError) as error:
        flash(str(error), "error")
    return redirect(url_for("index"))


@app.post("/service")
def add_service():
    facade = get_facade()
    try:
        price = facade.add_service(
            license_plate=request.form["license_plate"],
            service_id=request.form["service_id"],
        )
        flash(f"Услуга добавлена. Стоимость: {price} $.", "success")
    except (ValueError, CarNotFoundError) as error:
        flash(str(error), "error")
    return redirect(url_for("index"))


@app.post("/remove")
def remove_car():
    facade = get_facade()
    try:
        result = facade.remove_car(request.form["license_plate"])
        flash(f"Автомобиль {result['license_plate']} выдан клиенту.", "success")
    except (CarNotFoundError, PaymentError) as error:
        flash(str(error), "error")
    return redirect(url_for("index"))


@app.post("/security")
def security():
    facade = get_facade()
    security_info = None
    try:
        security_info = facade.security_info(request.form["license_plate"])
    except CarNotFoundError as error:
        flash(str(error), "error")

    return render_template(
        "index.html",
        stats=facade.stats(),
        cars=facade.cars_for_view(),
        tariffs=facade.tariffs_for_view(),
        services=facade.services_for_view(),
        security_info=security_info,
    )


@app.post("/reset-income")
def reset_income():
    facade = get_facade()
    facade.reset_income()
    flash("Общий доход обнулён.", "success")
    return redirect(url_for("index"))
