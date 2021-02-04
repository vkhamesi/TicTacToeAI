import numpy as np


class TicTacToe:
    def __init__(self, player1='-1', player2='1'):
        """
        :param player1:
        :param player2:
        """
        self.__player1__ = player1
        self.__player2__ = player2
        self.__grid__ = np.array([[None, None, None],
                                  [None, None, None],
                                  [None, None, None]])
        self.__isEnded__ = False
        self.__turn__ = [self.__player1__, self.__player2__]*10
        self.__winner__ = None
        self.__gridEvolution__ = []

    def play(self, player):
        """
        :param player:
        :return:
        """
        print("{}, c'est à ton tour !".format(player))
        coordinate = input("Coordonnées séparées par un espace")
        print("\n")
        coordinate = coordinate.split()
        if self.__grid__[int(coordinate[0]), int(coordinate[1])] is not None:
            print("Cette case est déjà jouée, choisis en une autre !")
            self.play(player)
        else:
            self.__grid__[int(coordinate[0]), int(coordinate[1])] = player
        print(self.__grid__)

    def playCoordinates(self, player, coordinate):
        """
        :param player:
        :param coordinate:
        :return:
        """
        self.__grid__[coordinate[0], coordinate[1]] = str(player)
        print(self.__grid__)
        self.__gridEvolution__.append(self.__grid__.tolist())

    def endGame(self, player):
        """
        :param player:
        :return:
        """
        print("\n")
        print("{} a gagné !".format(player))
        print("La partie est terminée.")
        self.__winner__ = player
        self.__isEnded__ = True

    def checkEnd(self):
        """
        :return:
        """
        for i in range(3):
            if (self.__grid__[i, :]).tolist() == [self.__player1__]*3:
                self.endGame(self.__player1__)
                break
            elif (self.__grid__[:, i]).tolist() == [self.__player1__]*3:
                self.endGame(self.__player1__)
                break
            elif (self.__grid__[i, :]).tolist() == [self.__player2__]*3:
                self.endGame(self.__player2__)
                break
            elif (self.__grid__[:, i]).tolist() == [self.__player2__]*3:
                self.endGame(self.__player2__)
                break
        if [self.__grid__[0][0], self.__grid__[1][1], self.__grid__[2][2]] == [self.__player1__]*3:
            self.endGame(self.__player1__)
        elif [self.__grid__[0][2], self.__grid__[1][1], self.__grid__[2][0]] == [self.__player1__]*3:
            self.endGame(self.__player1__)
        elif [self.__grid__[0][0], self.__grid__[1][1], self.__grid__[2][2]] == [self.__player2__]*3:
            self.endGame(self.__player2__)
        elif [self.__grid__[0][2], self.__grid__[1][1], self.__grid__[2][0]] == [self.__player2__]*3:
            self.endGame(self.__player2__)
        elif None not in self.__grid__:
            self.__isEnded__ = True
            print("Aucun vainqueur...")
        else:
            pass

    def playGame(self):
        """
        :return:
        """
        print(self.__grid__)
        k = 0
        while self.__isEnded__ is not True:
            self.play(self.__turn__[k])
            self.checkEnd()
            print("\n")
            k += 1

    def simGame(self, moves):
        """
        :param moves:
        :return:
        """
        print(self.__grid__)
        k = 0
        while self.__isEnded__ is not True:
            self.playCoordinates(moves[k][0], moves[k][1])
            self.checkEnd()
            print("\n")
            k += 1
