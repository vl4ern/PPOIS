def get_rubles():
    while True:
        try:
            rubles = int(input("Введите количество рублей: "))
            if rubles > 0:
                return rubles
            else:
                print("Надо ввести положительное число!")
        except ValueError:
            print("Надо ввести целое число.")

def convert_to_usd(rubles, rate):
    balance_usd = rubles * rate
    return balance_usd

def show_balance(usd_amount):
    print(f"Ваш баланс в долларах: ${usd_amount:.2f}.")

def main():
    current_rate = 3.3
    my_money = get_rubles()
    balance_usd = convert_to_usd(my_money, current_rate)
    show_balance(balance_usd)

if __name__ == "__main__":
    main()