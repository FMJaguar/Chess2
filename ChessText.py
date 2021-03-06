#/usr/bin/env python

from ChessBoard import ChessBoard
import sys
import getpass
import math
import string
from itertools import izip_longest


class ChessClient:
    def grouped(self, iterable, n):
        "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
        return izip_longest(*[iter(iterable)] * n)

    def mainLoop(self):
        print "White Player, choose an army:"
        print "1. Classic   2. Nemesis   3. Reaper"
        print "4. Empowered 5. Two Kings 6. Animals"
        while True:
            print 'Type the number, not the name.'
            userInput = getpass.getpass('> ')
            if userInput in string.digits:
                if int(userInput) < 7:
                    if int(userInput) > 0:
                        break
                print 'Please enter only one of the above.'
            else:
                print 'Please enter only one character'
        wArmy = userInput

        print "Black Player, choose an army:"
        print "1. Classic   2. Nemesis   3. Reaper"
        print "4. Empowered 5. Two Kings 6. Animals"
        while True:
            print 'Type the number, not the name.'
            userInput = getpass.getpass('> ')
            if userInput in string.digits:
                if int(userInput) < 7:
                    if int(userInput) > 0:
                        break
                print 'Please enter only one of the above.'
            else:
                print 'Please enter only one of the above.'
        bArmy = userInput

        pieces = {}
        chess = ChessBoard(int(wArmy), int(bArmy))
        board = chess.getBoard()
        turn = chess.getTurn()

        while True:
            chess.printBoard()
            if not chess.isGameOver():
                if chess._turn == chess.BLACK:
                    curArmy = chess._black_army
                else:
                    curArmy = chess._white_army
                if chess._secondTurn:
                    print "%s's Warrior King turn. Type your move, or type \"decline\" to skip." % str(chess.value_to_color_dict[turn])
                else:
                    print "%s's turn. Type your move." % str(chess.value_to_color_dict[turn])
                move = raw_input("> ")
                if move == "exit":
                    sys.exit(0)
                elif any(var in move for var in ("SAN", "san")):
                    san = chess.getAllTextMoves(chess.SAN)
                    if san:
                        for x, y in self.grouped(san, 2):
                            print "%s %s" % (x, y)
                elif any(var in move for var in ("LAN", "lan")):
                    lan = chess.getAllTextMoves(chess.LAN)
                    if lan:
                        for x, y in self.grouped(lan, 2):
                            print "%s %s" % (x, y)
                elif any(var in move for var in ("AN", "an")):
                    an = chess.getAllTextMoves(chess.AN)
                    if an:
                        for x, y in self.grouped(an, 2):
                            print "%s %s" % (x, y)
                elif any(var in move for var in ("FEN", "fen")):
                    print chess.getFEN()
                elif len(move) < 2:
                    print "Type a real move."
                elif any(var in move for var in ("whirlwind", "ww", "Whirlwind", "WW")):
                    if curArmy == chess.TWOKINGS:
                        print "Which Warrior King performs the whirlwind?"
                        while True:
                            location = raw_input("> ")
                            if location == "exit":
                                sys.exit(0)
                            elif len(location) != 2:
                                print "Please only enter the square."
                            else:
                                location = chess.locationToTuple(location)
                                res = chess.moveTwoKingsWhirlwind(location)
                                if not res:
                                    print "Can't whirlwind there."
                                board = chess.getBoard()
                                turn = chess.getTurn()
                                break
                    else:
                        print "You're not playing Two Kings!"
                elif move == "decline":
                    if curArmy == chess.TWOKINGS:
                        if chess._secondTurn:
                            print "Second turn skipped."
                            chess._secondTurn = False
                            if chess._turn == chess.BLACK:
                                chess._turn = chess.WHITE
                            else:
                                chess._turn = chess.BLACK
                            board = chess.getBoard()
                            turn = chess.getTurn()
                    else:
                        print "You're not playing Two Kings!"
                else:
                    res = chess.checkTextMove(move)
                    if res == -1 or (res is False):
                        result = chess.addTextMove(move)
                        if result:
                            print chess.getLastTextMove(chess.SAN)
                            board = chess.getBoard()
                            turn = chess.getTurn()
                            chess.updateRoyalLocations()
                        else:
                            print "%s" % chess.move_reason_list[chess.getReason()]
                    else:
                        if turn == 0:
                            unturn = 1
                        else:
                            unturn = 0
                        print "%s, would you like to initiate a duel? It will cost %d." % (str(chess.value_to_color_dict[unturn]), res)
                        while True:
                            answer = raw_input("> ")
                            if any(var in answer for var in ('y', 'Y', 'Yes', 'yes')):
                                chess.payDuelCost(res)
                                print "White stones: %d" % chess.getStones(chess.WHITE)
                                print "Black stones: %d" % chess.getStones(chess.BLACK)
                                print "%s, how much would you like to bid?" % str(chess.value_to_color_dict[unturn])
                                while True:
                                    defending_bid = getpass.getpass("> ")
                                    if defending_bid == "exit":
                                        sys.exit(0)
                                    elif defending_bid in string.digits:
                                        if int(defending_bid) < 3:
                                            if int(defending_bid) > -1:
                                                break
                                            print 'Please only bid a number of stones between 0 and 2.'
                                        print 'Please only bid a number of stones between 0 and 2.'
                                    else:
                                        print 'Please only bid a number of stones between 0 and 2.'
                                print "%s, how much would you like to bid?" % str(chess.value_to_color_dict[turn])
                                while True:
                                    attacking_bid = getpass.getpass("> ")
                                    if attacking_bid == "exit":
                                        sys.exit(0)
                                    elif attacking_bid in string.digits:
                                        if int(attacking_bid) < 3:
                                            if int(attacking_bid) > -1:
                                                break
                                            print 'Please only bid a number of stones between 0 and 2.'
                                        print 'Please only bid a number of stones between 0 and 2.'
                                    else:
                                        print 'Please only bid a number of stones between 0 and 2.'
                                duel_results = chess.initiateDuel(int(attacking_bid), int(defending_bid))
                                # duel_results will now be either None, 1, or 2
                                print "%s bid: %d" % (chess.value_to_color_dict[chess._turn], int(attacking_bid))
                                print "%s bid: %d" % (chess.value_to_color_dict[chess._unturn], int(defending_bid))
                                if duel_results is None:
                                    print "Someone tried to bid too much!"
                                    break
                                elif duel_results == 0:
                                    print "%s called the bluff! Do you want to gain a stone or force %s to lose a stone?" % (
                                        chess.value_to_color_dict[chess._turn], chess.value_to_color_dict[chess._unturn])
                                    while True:
                                        bluff_choice = raw_input("> ")
                                        if bluff_choice == "exit":
                                            sys.exit(0)
                                        elif any(var in bluff_choice for var in ("g", "gain", "G", "Gain")):
                                            chess.addStones(chess._turn, 1)
                                            break
                                        elif any(var in bluff_choice for var in ("l", "lose", "L", "Lose")):
                                            chess.addStones(chess._unturn, -1)
                                            break
                                        else:
                                            print 'Please only bid a number of stones between 0 and 2.'
                                elif duel_results == 1:
                                    print "Attacker wins!"
                                    att_result = chess.addTextMove(move)
                                    if att_result:
                                        print chess.getLastTextMove(chess.SAN)
                                        board = chess.getBoard()
                                        turn = chess.getTurn()
                                        chess.updateRoyalLocations()
                                    else:
                                        print "%s" % chess.move_reason_list[chess.getReason()]
                                else:
                                    print "Defender wins!"
                                    att_result = chess.addTextMove(move, True)
                                    if att_result:
                                        print chess.getLastTextMove(chess.SAN)
                                        board = chess.getBoard()
                                        turn = chess.getTurn()
                                        chess.updateRoyalLocations()
                                    else:
                                        print "%s" % chess.move_reason_list[chess.getReason()]
                                board = chess.getBoard()
                                turn = chess.getTurn()
                                break
                            else:
                                board = chess.getBoard()
                                turn = chess.getTurn()
                                break
            else:
                break
        chess.printBoard()
        print "Game over! %s" % chess.game_result_list[chess.getGameResult()]


def main():
    g = ChessClient()
    g.mainLoop()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
