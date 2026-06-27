# game.py

from gameparts.parts import Board
# Добавился ещё один импорт - исключение CellOccupiedError.
from gameparts.exceptions import CellOccupiedError, FieldIndexError
def save_result(result):
    with open('results', 'a') as f:
        f.write(result)
        f.close()

def check_winner(board, size):
    # Проверка строк
    for row in board:
        if row[0] != ' ' and all(cell == row[0] for cell in row):
            return row[0]

    # Проверка столбцов
    for col in range(size):
        if board[0][col] != ' ' and all(board[row][col] == board[0][col] for row in range(size)):
            return board[0][col]

    # Проверка главной диагонали
    if board[0][0] != ' ' and all(board[i][i] == board[0][0] for i in range(size)):
        return board[0][0]

    # Проверка побочной диагонали
    if board[0][size-1] != ' ' and all(board[i][size-1-i] == board[0][size-1] for i in range(size)):
        return board[0][size-1]

    return None

def main():
    game = Board()
    current_player = 'X'
    running = True
    game.display()

    while running:

        print(f'Ход делают {current_player}')

        # Запускается бесконечный цикл.
        while True:
            try:
                row = int(input('Введите номер строки: '))
                if row < 0 or row >= game.field_size:
                    raise FieldIndexError
                column = int(input('Введите номер столбца: '))
                if column < 0 or column >= game.field_size:
                    raise FieldIndexError
                if game.board[row][column] != ' ':
                    # Вот тут выбрасывается новое исключение.
                    raise CellOccupiedError
            except FieldIndexError:
                print(
                    'Значение должно быть неотрицательным и меньше '
                    f'{game.field_size}.'
                )
                print('Введите значения для строки и столбца заново.')
                continue
            except CellOccupiedError:
                print('Ячейка занята')
                print('Введите другие координаты.')
                continue
            except ValueError:
                print('Буквы вводить нельзя. Только числа.')
                print('Введите значения для строки и столбца заново.')
                continue
            except Exception as e:
                print(f'Возникла ошибка: {e}')
            else:
                break

        game.make_move(row, column, current_player)
        game.display()
        winner = check_winner(game.board, game.field_size)
        if winner is not None:
            result = f"Победил {winner}"
            print(result)
            save_result(result)
            running = False
            break

        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == '__main__':
    main()
