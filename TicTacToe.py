def main():
    inpt=input("Welcome to Tic Tac Toe!\n"
               "Press any key to continue")
    sign = ['', '']
    turn = ['PlayerOne', 'PlayerTwo']
    sign[0] = input(turn[0] + ' would you like to be X or O?')
    sign[0] = sign[0].upper()
    if sign[0] == 'X':
        sign[1] = 'O'
    else:
        sign[1] = 'X'
    print(turn[1] + ' you will be '+ sign[1] + '.')
    while True:
        #Game initializations
        board = [' ']*10
        player = 0
        flag = 0
        game_on = 0
        board_print(board)
        #game undergoing
        while game_on != 1:
            while flag == 0:
                    pick = int(input(turn[player] + " please pick a square 1-9:"))
                    if 1 <= pick <= 9 and board[pick] == ' ':
                        board[pick] = sign[player]
                        flag = 1
                        print('\n' * 25)

                    else:
                        print('\n' * 25)
                        print("Invalid/Taken square, please choose a different one.\n")
                    board_print(board)
            flag = 0
            game_on = check_win(board, sign[player])
            if game_on == 1:
                print("Congratulations "+turn[player]+" has won!")

            #set next turn
            if player == 0:
                player += 1
            else:
                player -= 1

        answer = input("Would you like to player another game?\n"
                       "Press n to quit.")
        if answer[0].lower() == 'n':
            print("Thank you for playing!!!")
            exit()
        else:
            print ('\n' * 25)
            print("Resetting game...")



def check_win(board, mark):
    '''
        checks for a winning condition, returns 1 if won
    '''
    return row_check(board, mark) or col_check(board, mark) or diag_check(board, mark)


def row_check(board, mark):
    i = 1
    result = 0
    while i <= 7:
        result = (board[i] == mark and board[i+1] == mark and board[i+2] == mark)
        if result == 1:
            return result
        i += 3
    return result


def col_check(board, mark):
    i = 9
    result = 0
    while i >= 7:
        result = (board[i] == mark and board[i - 3] == mark and board[i - 6] == mark)
        if result == 1:
            return result
        i -= 1
    return result


def diag_check(board, mark):
    return (board[1] == mark and board[5] == mark and board[9] == mark) or (board[3] == mark and board[5] == mark and board[7] == mark)


def board_print(board):
    print(board[7] + '|' + board[8] + '|' + board[9])
    print(board[4] + '|' + board[5] + '|' + board[6])
    print(board[1] + '|' + board[2] + '|' + board[3])




if __name__ == "__main__":
    main()