import random
import sys
from numpy import *
c = 0
r = 0
m = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
highscore = 0


def g():
    global y
    y = int(input("number:"))
    while y <= 1:
        print("Invaild input, you can only input between 2 and 10")
        y = int(input("number:"))


def exit():
    sys.exit()


def display(m, score, highscore):  # display the interface and score
    """
    :param m: the game matrix
    :param score: to calculate the total score
    """

    print('{0:4} {1:4} {2:4} {3:4}'.format(m[0][0], m[0][1], m[0][2], m[0][3]))
    print('{0:4} {1:4} {2:4} {3:4}'.format(m[1][0], m[1][1], m[1][2], m[1][3]))
    print('{0:4} {1:4} {2:4} {3:4}'.format(m[2][0], m[2][1], m[2][2], m[2][3]))
    print('{0:4} {1:4} {2:4} {3:4}'.format(m[3][0], m[3][1], m[3][2], m[3][3]))
    print("Total score: ", score)
    print("high score:", highscore)


def init(m):  # initial the matrix
    """
    :param m: the initial game matrix
    """
    g()
    for r in range(4):  # random generate 0, 2 and 4 to start the game but 4 will be more rare
        m[r] = [random.choice([0, 0, 0, 0, y, y, y, y**2])for x in m[r]]


def align(matrix, direction):  # align non-zero numbers
    """
    :param matrix: the matrix row or col
    :param direction: the direction that the system can accept
    """
    for r in range(matrix.count(0)):  # found frequency of zero
        matrix.remove(0)  # remove all zeros
    zeros = [0 for x in range(4 - len(matrix))]  # add zeros to non-zero side
    if direction == 'left':
        matrix.extend(zeros)
    if direction == 'right':
        matrix[:0] = zeros


def merge(matrix, direction):  # when the user move, if the number are the same,
    """
    :param matrix: the game matrix will be merge
    :param direction:
    :return: true
    """
    score = 0            # merge them and return the added score, false otherwise
    if direction == 'left':
        for r in [0, 1, 2]:
            if matrix[r] == matrix[r + 1] != 0:  # these two number can be merge
                matrix[r] *= y  # number will multiply itself
                matrix[r + 1] = 0  # i + 1 return zero
                score += matrix[r]  # score plus the new number
                return {'move': True, 'score': score}
    if direction == 'right':
        for r in [3, 2, 1]:
            if matrix[r - 1] == matrix[r] != 0:
                matrix[r] *= y
                matrix[r - 1] = 0
                score += matrix[r]
                return {'move': True, 'score': score}
    return{'move': False, 'score': score}


def handle(matrix, direction):  # handle one row/column, get the value of the row/column and return the score
    """
    :param matrix:  the matrix that will be manipulated
    :param direction: different direction that system accepted
    :return: total score
    """
    global result
    totalscore = 0
    align(matrix, direction)
    result = merge(matrix, direction)
    totalscore += result['score']
    return totalscore


def operation(matrix):  # After user move, recompute the matrix value and return the score
    """
    :param matrix: the game matrix
    :return: the state of the game and score
    """
    global r, c, m
    totalscore = 0  # left and up both use 'left', down and right both use 'right'
    gameOver = False
    direction = 'left'
    o = input('operator:')
    if o in ['a', 'A']:  # left
        direction = 'left'
        for r in range(4):
            totalscore += handle(matrix[r], direction)
    elif o in ['d', 'D']:  # right
        direction = 'right'
        for r in range(4):
            totalscore += handle(matrix[r], direction)
    elif o in ['w', 'W']:  # up
        matrix = numpy.transpose(matrix)  # transpose the matrix and then left will equal to up
        matrix = [matrix[0].tolist(), matrix[1].tolist(), matrix[2].tolist(), matrix[3].tolist()]
        direction = 'left'
        for r in range(4):
            totalscore += handle(matrix[r], direction)
        matrix = numpy.transpose(matrix)  # transpose the matrix and then left will equal to up
        matrix = [matrix[0].tolist(), matrix[1].tolist(), matrix[2].tolist(), matrix[3].tolist()]
        m = matrix
    elif o in ['s', 'S']:  # down
        matrix = numpy.transpose(matrix)  # transpose the matrix and then right will equal to down
        matrix = [matrix[0].tolist(), matrix[1].tolist(), matrix[2].tolist(), matrix[3].tolist()]
        direction = 'right'
        for r in range(4):
            totalscore += handle(matrix[r], direction)
        matrix = numpy.transpose(matrix)  # transpose the matrix and then left will equal to up
        matrix = [matrix[0].tolist(), matrix[1].tolist(), matrix[2].tolist(), matrix[3].tolist()]
        m = matrix
    elif o in ['Exit']:
        exit()
    elif o in ['Restart']:
        print('The game has been restarted')
        game()
    else:
        print(' Invalid input, please enter character in [A, S, W, D, Exit, Restart] or the lower case')
        return{'gameOver': gameOver, 'score': totalscore}

    b = 0  # blank space
    for p in matrix:
        b += p.count(0)
        # print(f'b is equal to: {b}')
    if b == 0 and (matrix[r][c - 1] != matrix[r][c] or matrix[r - 1][c] != matrix[r][c]):
        # neither blank spaces nor two same numbers, game over
        gameOver = True
        return{'gameOver': gameOver, 'score': totalscore}

    newnum = random.choice([y, y, y, y**2])  # still 4 will be rare
    k = random.randrange(1, b + 1)
    u = 0
    for r in range(4):
        for c in range(4):
            if matrix[r][c] == 0:
                u += 1
                if u == k:
                    m[r][c] = newnum
                    break
    # print('Type of total score is: ')
    # print(type(totalscore))
    # print(totalscore)
    return{'gameOver': gameOver, 'score': totalscore}


def comparehighscore(totalscore, highscore):
    if totalscore > highscore:
        return totalscore
    else:
        return highscore


def game():
    global highscore
    init(m)
    score = 0
    print('Input character A(left) S(down) W(up) D(right) Exit Restart')
    while True:

        highscore = comparehighscore(score, highscore)
        display(m, score, highscore)
        result = operation(m)
        # print('result equals: ')
        # print(result)
        score += result['score']
        # print(f'Your maximum value is: {y**11}')
        if result['gameOver']:
            print('Game Over, try next time!')
            print('Your total score:', score)
            game()
        elif m[r][c] >= y**11:
            print('Game over, you win!')
            print('Your total score:', score)


game()