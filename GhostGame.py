import random


def play_ghost(trie):
    current_node = trie.root
    current_string = ""
    difficulty = int(input("Pick a difficulty level from 1-5 "))

    player_first = input("Do you want to go first (y/n)? ")
    while player_first not in ['y', 'n']:
        player_first = input("Error, please input y or n ")
    user_turn = (player_first == 'y')
    game_over = False

    while not game_over:
        if user_turn:
            if current_string == "":
                print("Current string is empty.")
            else:
                print("Current string is " + current_string)
            next_char = input("Type in a letter or HELP  \n").upper()
            while next_char == "HELP":
                winning_moves = []
                losing_moves = []
                for child_node in current_node.children.values():
                    if child_node.is_win:
                        winning_moves.append(child_node.letter)
                    else:
                        losing_moves.append(child_node.letter)
                if len(winning_moves) > 0:
                    print("Winning letters for you: ")
                    print(winning_moves)
                else:
                    print("Your only options are losing moves\nSorry...\n")
                    print("These letters will get you to a word and avoid a challenge at least: ")
                    print(losing_moves)
                next_char = input("Type in a letter  ").upper()
            current_string += next_char
            print("Current string is " + current_string)
            if next_char not in current_node.children:
                game_over = True
                print("Challenge.\nYou can't make a word in the current dictionary starting with " + current_string)
                print("I WIN")
            else:
                current_node = current_node.children[next_char]
                if current_node.is_word:
                    game_over = True
                    print(current_string + " is a word.")
                    print("I win this time.")
            user_turn = False
        else:
            # This section handles the computer's move
            # for each difficulty level beyond 1, the computer picks another random choice
            # and checks to see if one of those choices is a winning move
            # as difficulty increases
            # computer gets more chances to pick a winning move

            # random.choices picks k random valid moves
            possible_moves = random.choices(list(current_node.children.values()), k=difficulty)

            next_move = possible_moves[0]

            for move in possible_moves:
                if move.is_win:
                    next_move = move
                    break

            print("My next move is " + next_move.letter)
            current_string += next_move.letter
            current_node = next_move

            if current_node.is_word:
                game_over = True
                print(current_string + " is a word.")
                print("It appears that I have lost this one...")
                print("GOOD JOB YOU WIN!!!!!!")

            user_turn = True

