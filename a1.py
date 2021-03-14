# a1.py - Jason Leung

import random
import sys
import time

from search import *
from collections import deque

state = []

# Take command line argument input from user if it exists
if (len(sys.argv) == 10):
    for i in range (1, 10):
        state.append(int(sys.argv[i]))
else:
    state = [1, 2, 3, 
             4, 5, 6, 
             7, 8, 0]

puzzle = EightPuzzle(tuple(state))

def make_rand_8puzzle():

    global state
    global puzzle
    actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    scramble = []

    # Randomly chooses 100 actions to make in order to randomize the puzzle
    for _ in range(100):
        scramble.append(random.choice(actions))

    # If the move can be made, then overwrite state with the resulting state given action and create a new EightPuzzle
    for move in scramble:
        if move in puzzle.actions(state):
            state = list(puzzle.result(state, move))
            puzzle = EightPuzzle(tuple(state))

def display(state):

    # Display current state
    for i in range(0, 9, 3):
        if (state[i] == 0):
            print("*", state[i + 1], state[i + 2])
        elif (state[i + 1] == 0):
            print(state[i], "*", state[i + 2])
        elif (state[i + 2] == 0):
            print(state[i], state[i + 1], "*")
        else:
            print(state[i], state[i + 1], state[i + 2])

def search(h, display):

    return astar_search(puzzle, h, display).solution()

def stats(h, display):

    # Print stats of astar_search
    start = time.time()
    solution = search(h, display)
    elapsed = time.time() - start

    print("Length:", len(solution))
    print("Time:", elapsed)

def manhattan(n):

    state = n.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_pos = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    distance = 0

    # Iterate through each position in the state, and initialize initial as the current position in the state
    # Grab the goal position of the state in the current position
    # ex.   3 2 1
    # state[0] = 3
    # initial = [0, 0] (the position it is currently at)
    # final = [0, 2] (the goal state position it should be in)
    for i in range(len(state)):
        if (state[i] != 0):
            initial = index_pos[i]
            final = index_goal[state[i]]

            # Get the x and y distance from initial to goal
            x = abs(initial[1] - final[1])
            y = abs(initial[0] - final[0])

            # Add up all the distances together
            distance = x + y + distance

    # Returns distance
    return distance

def gaschnig(n):

    temp_state = list(n.state)
    index_goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    index_counter = 0
    swaps = 0

    while True:
        # If the blank is in the 8th position, test if it is in the goal state
        if (temp_state.index(0) == 8):
            # If goal state has been reached, break out of loop
            if (puzzle.goal_test(tuple(temp_state))):
                break
            else:
                # Iterate through the positions checking which values are in the correct position
                # Values that are misplaced will swap with blank
                if (temp_state[index_counter] != index_goal[index_counter]):
                    blank_pos = temp_state.index(0)
                    temp_state[blank_pos], temp_state[index_counter] = temp_state[index_counter], temp_state[blank_pos]
                    swaps = swaps + 1
                    index_counter = index_counter + 1
                else:
                    index_counter = index_counter + 1
        else:
            # Say the blank is in state[5], that means it is in the 6th position
            # Therefore it needs to swap with the position of value 6
            blank_pos = temp_state.index(0)
            value = blank_pos + 1
            value_pos = temp_state.index(value)

            temp_state[blank_pos], temp_state[value_pos] = temp_state[value_pos], temp_state[blank_pos]
            swaps = swaps + 1

    # Returns amount of swaps
    return swaps

# ----

# Define variables
counter = 0

while True:

    # If puzzle is not solvable, keep generating a new random puzzle
    make_rand_8puzzle()
    solvable = puzzle.check_solvability(state)

    if (solvable == True):
        break
    elif (counter >= 5):
        print("Unable to reach goal state")
        break
    else:
        counter = counter + 1

# Only run if puzzle is solvable
if (solvable == True):
    node = Node(state)
    mdh = manhattan(node)
    gh = gaschnig(node)

    # Prints initial puzzle state
    print()
    display(state)

    # Prints Misplaced-Tiles Algorithm stats
    print()
    print("Misplaced-Tiles Algorithm:")
    stats(None, True)

    # Prints Manhattan Distance Algorithm stats
    print()
    print("Manhattan Distance Algorithm:")
    stats(manhattan, True)
    print("Heuristic:", mdh)

    # Prints Gaschnig Algorithm stats
    print()
    print("Gaschnig Algorithm:")
    stats(gaschnig, True)
    print("Heuristic:", gh)

    print()