from tag_game import Tag_game

if __name__ == "__main__":
    game = Tag_game()
    print("Start position: ")
    print(game)

    while not game.is_solved():
        try:
            row = int(input("Enter row (1-4): "))
            col = int(input('Enter col (1-4): '))
            if game.move(row, col):
                print('Move completed: ')
                print(game)
            else:
                print('Not correct move, try again: ')
        except ValueError:
            print('Enter only numbers!')
        except KeyboardInterrupt:
            print('\nGame stopped!')
            break

    if game.is_solved():
        print("Congratulations, you complete the game!")