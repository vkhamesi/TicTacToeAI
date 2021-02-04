import random
from main import TicTacToe
from tensorflow.keras import *
from tensorflow.keras.layers import *
import numpy as np


def simulateMoves():
    possiblemoves = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    mademoves = []
    for j in range(len(possiblemoves)):
        random.shuffle(possiblemoves)
        move = possiblemoves.pop()
        k = j % 2
        if k == 0:
            mademoves.append((-1, move))
        else:
            mademoves.append((1, move))
    return mademoves


# Nombre de parties d'apprentissage
n = 100
# Historique des gagnants
winners = []
# Historique des parties
dataset = []
for _ in range(n):
    game = TicTacToe('-1', '1')
    game.simGame(simulateMoves())
    dataset.append(game.__gridEvolution__)
    winners.append(game.__winner__)

stat = {'-1': 0, '1': 0, None: 0}
for winner in winners:
    if winner == '-1':
        stat['-1'] += 1
    elif winner == '1':
        stat['1'] += 1
    elif winner is None:
        stat[None] += 1

# Il faut remplacer chaque élément de dataset par des -1,0,1
for i in range(len(dataset)):
    for j in range(len(dataset[i])):
        for k in range(len(dataset[i][j])):
            for l in range(len(dataset[i][j][k])):
                if dataset[i][j][k][l] == '-1':
                    dataset[i][j][k][l] = -1
                elif dataset[i][j][k][l] == '1':
                    dataset[i][j][k][l] = 1
                elif dataset[i][j][k][l] is None:
                    dataset[i][j][k][l] = 0

# Idem avec winners
for i in range(len(winners)):
    if winners[i] == '-1':
        winners[i] = -1
    elif winners[i] == '1':
        winners[i] = 1
    elif winners[i] is None:
        winners[i] = 0

history = []
for i in range(len(dataset)):
    gameEvol = []
    for j in range(len(dataset[i])):
        elt = (winners[i], dataset[i][j])
        gameEvol.append(elt)
    history.append(gameEvol)

for i in range(len(history)):
    while len(history[i]) != 9:
        history[i].append(history[i][-1])

model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(9, )))
model.add(Dense(128, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(3, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

# Réseau de neurones entrainé
input = []
output = []
for dataset in history:
    for data in dataset:
        input.append(data[1])
        output.append(data[0])
X = np.array(input).reshape((-1, 9))
y = utils.to_categorical(output, num_classes=3)
model.fit(X, y, batch_size=32, epochs=100)

# Pour prédire la qualité d'un move, on écrit
print(model.predict(np.array([[1, 0, 1],
                              [-1, 1, 0],
                              [-1, 0, 1]]).reshape(-1, 9))[0])
# L'idée est de tester tous les move possibles et de choisir celui qui a la plus grand proba de faire gagner
# [1, 0, 0] : favorable au match nul
# [0, 1, 0] : favorable au joueur 1
# [0, 0, 1] : favorable au joueur -1

"""
Situation initiale
np.array([[0, 0, 0],
         [0, -1, 0],
         [0, 0, 0]])

np.array([[0, 1, 0],
         [0, -1, 0],
         [0, 0, 0]])

np.array([[0, 1, 0],
         [0, -1, 0],
         [-1, 0, 0]])
"""


def testPossibleMoves(grid):
    possiblemoves = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] is None or grid[i][j] == 0:
                possiblemoves.append([i, j])
    return possiblemoves


def bestMove(grid, player):
    possiblemoves = testPossibleMoves(grid)
    maxi = 0
    bestmove = possiblemoves[0]
    for move in possiblemoves:
        chance = model.predict(np.array(grid).reshape(-1, 9))[0][player]
        if chance > maxi:
            maxi = chance
            bestmove = move
    print("{} % de chance de gagner en jouant en {}".format(maxi, bestmove))
    return bestmove
