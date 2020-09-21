import random
from math import inf

buffer = ["Ä", " ", " ", " ", " ", " ", " ", " ", " ", " "]


def display():
    print("\n" * 100)
    print(f"      |      "  "  |\n"
          f" {buffer[7]}    |   {buffer[8]}  "f"  |  {buffer[9]}\n"
          "      |      "  "  |\n"
          "--------------------")
    print(f"      |      "  "  |\n"
          f" {buffer[4]}    |   {buffer[5]}  "f"  |  {buffer[6]}\n"
          "      |      "  "  |\n"
          "--------------------")
    print(f"      |      "  "  |\n"
          f" {buffer[1]}    |   {buffer[2]}  "f"  |  {buffer[3]}\n"
          "      |      "  "  |\n")


def user_choice(player):
    choice = 'WRONG'
    acceptable_range = range(1, 10)
    within_range = False
    while not within_range:
        choice = input(f"Please Player {player} enter a number between 1 and 9: ")
        if not choice.isdigit():
            print("Sorry, that is not a digit!")
            continue
        elif int(choice) not in acceptable_range:
            print("Sorry, you are out of acceptable range (1-9)")
            continue
        if not free_space_check(choice):
            print("Sorry, this position is already taken!")
            continue
        within_range = True
    return int(choice)


def set_marker(marker, position):
    buffer[position] = marker


def win_check(mark, player_, computer=False):
    win_pos = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    for x in win_pos:
        check = True
        for y in x:
            if buffer[y] != mark:
                check = False
                break
        if check:
            if not computer:
                display()
                print(f"Player {player_} won the Game!")
            return True
    if " " not in buffer:
        if not computer:
            display()
            print("DRAW!")
        return True
    return False


def choose_first():
    player_1 = random.randint(1, 2)
    print(f"Player {player_1} starts the game!")
    while True:
        player_1_marker = input(f"Please Player {player_1} select X or O!")
        if player_1_marker != "X" and player_1_marker != "O":
            print("Sorry, that was not X nor O!")
            continue
        else:
            break
    player_2_marker = "X" if player_1_marker == "O" else "O"
    player_2 = 2 if player_1 == 1 else 1
    return {"player_1_marker": player_1_marker, "player_1": player_1,
            "player_2_marker": player_2_marker, "player_2": player_2}


def free_space_check(position):
    return True if buffer[int(position)] == " " else False


def avail_spots():
    return [x for x in range(len(buffer)) if buffer[x] == " "]


def replay():
    while True:
        x = input("Do you want to play again? (Yes/No)").lower()
        if x != "yes" and x != "no":
            continue
        else:
            break
    if x == "yes":
        for x in range(1, 10):
            buffer[x] = " "
        return True
    return False


def minimax(buffer, depth, is_maximizing, player_mark):
    enemy_marker = "X" if player_mark != "X" else "O"

    if win_or_prevention(enemy_marker) < 10 or win_or_prevention("O") < 10 or depth == 0:
        if win_or_prevention(enemy_marker) < 10:
            return -10 + depth
        elif win_or_prevention(player_mark) < 10:
            return 10 - depth
        else:
            return 0

    free_spots = avail_spots()
    if is_maximizing:
        max_score = -inf
        for spot in free_spots:
            buffer[spot] = player_mark
            score = minimax(buffer, depth + 1, False, player_mark)
            buffer[spot] = " "
            if score > max_score:
                max_score = score
        return max_score
    else:
        min_score = inf
        for spot in free_spots:
            buffer[spot] = enemy_marker
            score = minimax(buffer, depth + 1, True, player_mark)
            buffer[spot] = " "
            if score < min_score:
                min_score = score
        return min_score


def ai_move(ai_marker):
    free_spots = avail_spots()
    depth = len(free_spots)
    best_score = -inf
    best_move = -1
    for spots in free_spots:
        buffer[spots] = ai_marker
        score = minimax(buffer, depth, True, ai_marker)
        buffer[spots] = " "
        if score > best_score:
            best_score = score
            best_move = spots
    set_marker(ai_marker, best_move)


def win_or_prevention(marker):
    index_computer = 1
    while index_computer < 10:
        if buffer[index_computer] == " ":
            buffer[index_computer] = marker
            if win_check(marker, "Computer", True):
                buffer[index_computer] = " "
                return index_computer
            else:
                buffer[index_computer] = " "
        index_computer += 1
    return index_computer


def set_marker_computer(marker):
    enemy_marker = "X" if marker != "X" else "O"
    win = win_or_prevention(marker)
    prevention = win_or_prevention(enemy_marker)
    if win < 10:
        set_marker(marker, win)
        return
    elif prevention < 10:
        set_marker(marker, prevention)
        return

    random_number = random.choice(avail_spots())
    set_marker(marker, random_number)


def vs_computer():
    while True:
        x = input("Do you want to play vs computer? (Yes/No)").lower()
        if x != "yes" and x != "no":
            continue
        else:
            break
    if x == "no":
        return
    if x == "yes":
        while True:
            x = input("Do you want to play vs unbeatable AI? (Yes/No)").lower()
            if x != "yes" and x != "no":
                continue
            else:
                break
        if x == "yes":
            return "ai_game"
        return "easy_comp"


if __name__ == "__main__":
    print("Welcome to Tic Tac Toe!")
    while True:
        mode = vs_computer()
        display()
        player_dict = choose_first()
        while True:
            set_marker(player_dict["player_1_marker"], user_choice(player_dict["player_1"]))
            display()
            if win_check(player_dict["player_1_marker"], player_dict["player_1"]):
                break
            if mode != "ai_game" and mode != "easy_comp":
                set_marker(player_dict["player_2_marker"], user_choice(player_dict["player_2"]))
            elif mode == "ai_game":
                ai_move(player_dict["player_2_marker"])
            else:
                set_marker_computer(player_dict["player_2_marker"])
            display()
            if win_check(player_dict["player_2_marker"], player_dict["player_2"]):
                break
        if not replay():
            break
