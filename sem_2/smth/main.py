name = input("Введите имя игрока: ")
goals = int(input("Введите голы за сезон: "))
matches = int(input("Введите матчи: "))

if matches == 0:
    print("Матчей не может быть ноль!")
else:
    average = goals / matches

print(f"Игрок: {name}")
print(f"Голы: {goals}")
print(f"Матчи: {matches}")
print(f"Среднее кол-во голов за матч: {average}")