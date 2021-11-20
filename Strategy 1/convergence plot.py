import random as rand
import numpy as np

#Wrtie a recurssive function for playing each round.
# 8 parameters:
# players is 2*2 matrix containting players' id and their probability threshold:
# the first column represents players; the second column represents probability threshold;
# id is an integer, means the id of the player who is currently playing this turn: 0 means player 1, 1 means player 2;
# card is an integer, means the current card being turned over and will be used to compare with the next card;
# deck is a list, means the current deck without cards have been used before;
# count is an integer, means the number of cards being guessed right in this round;
# cardsUsed is a list, means the list contains cards used before;
# canGiveUp is a boolean character, represents if a play can choose skip this turn or not,
# which means if they have at least one guess in this turn or not: true means they can choose to give up; false means they cannot give up
# mode is an integer, represents if two players can remember the cards being turned over before:
# 0 means they cannot remember, thus the first type of strategies; 1 means they can remember, second type of strategies.
def play(players, id, card, deck, cardsUsed, count, canGiveUp, mode):
    if (mode == 1): # to see if we use the first or second type of strategies
        cardsUsed.append(card)
    if (len(deck) == 1): # marginal(base) case: all 60 cards are guessed right in one round
        return (0, 0)
    else:
        threshold = players[id][1]
        p_smaller = (card - 1) / 60.0 #the probability that the next card is smaller than the current card
        p_larger = 1 - p_smaller
        if ((p_smaller >= threshold) and (p_smaller > p_larger)): # if probability for smaller than >= threhold and p_smaller > p_larger
            new_card = deck.pop(0)
            if (mode == 1):
                cardsUsed.append(card)
            if (new_card < card): # player guesses smaller than, and the new card is smaller than the current card
                count += 1
                card = deck.pop(0)
                return play(players, id, card, deck, cardsUsed, count, True, mode)
            else: # player guesses smaller than, but the new card is larger, so he loses, and return his id and count
                return (id, count)
        elif (p_larger >= threshold): # if probability for larger than >= threhold and p_larger > p_small
            new_card = deck.pop(0)
            if (mode == 1):
                cardsUsed.append(card)
            if (new_card > card): # player guesses larger than, and the new card is larger
                count += 1
                card = deck.pop(0)
                return play(players, id, card, deck, cardsUsed, count, True, mode)
            else: # player guesses larger, but the new card is smaller, so he loses, and return his id and count
                return (id, count)
        else: # both p_smaller and p_larger < threshold; players would like to give up this turn if he can
            if (canGiveUp): # he can give up
                if (id == 0): # if the current player is player 1, switch to player 2
                    new_id = 1
                else: # if the current player is player 2, switch to player 2
                    new_id = 0
                return play(players, new_id, card, deck, cardsUsed, count, False, mode)
            else: # he cannot give up, so he compares p_smaller and p_larger and choose the larger probability
                if (p_smaller >= (p_larger)): # p_smaller is larger, he guesses the next card is smaller
                    new_card = deck.pop(0)
                    if (mode == 1):
                        cardsUsed.append(card)
                    if (new_card < card): # he guesses smaller, and the next card is smaller
                        count += 1
                        card = deck.pop(0)
                        return play(players, id, card, deck, cardsUsed, count, True, mode)
                    else: # he guesses smaller, but the next card is larger, he loses and this round ends
                        return (id, count)
                else: # p_larger is larger, he guesses the next card is larger
                    new_card = deck.pop(0)
                    if (mode == 1):
                        cardsUsed.append(card)
                    if (new_card > card): # he guesses larger, and the next card is larger
                        count += 1
                        card = deck.pop(0)
                        return play(players, id, card, deck, cardsUsed, count, True, mode)
                    else: # he guesses larger, but the next card is larger, he loses and this round ends
                        return (id, count)


#Create a list for deck
backup_deck = []
for i in range (60): #store 60 cards fisrt, shuffle will be done in for loop
    backup_deck.append(i)

#store the counting of wining for player 1 in each estimate
win_count = 0

#store the average probability of wining for player 1 calculated every 100 games in each estimate
win_p = []

#store 8 win_p for 8 pairs of thresholds
p_8 = []

#go through 8 pairs of thresholds
for row in range(8):
    # probability threshold for players
    p1 = 0.3
    p2 = 0.3 + 0.1*row
    #Create a 2x2 matrix players: first column represents players; second column represents probability shresholds
    # 0 means player 1, 1 means player 2
    players = [[0,p1],[1,p2]]
    p_8.append([])
    win_count = 0
    win_p = []
    for i in range(100000): # play 100000 games
        scores = [0,0] #initialize score when a new game starts
        for j in range(10): # play 10 rounds in each game
            deck = backup_deck.copy()
            rand.shuffle(deck)  # shuffle the deck
            card = deck.pop(0) # turn over the first card
            cardsUsed = []
            if (j <= 4): # each player starts 5 rounds in one game
                result = play(players, 0, card, deck, cardsUsed, 0, False, 0)
            else:
                result = play(players, 1, card, deck, cardsUsed, 0, False, 0)
            lose_player = result[0]
            score = result[1]
            scores[lose_player] += score
            # count number of wining for player 1
        if (scores[0] < scores[1]):
            win_count += 1
            #count wining probability every 100 game
        if ((i!=0) and ((i+1)%100)==0):
            win_p.append(win_count/(i+1))
    p_8[row] = win_p


import matplotlib.pyplot as plt

# x-axis 
x = []
for i in range(1000):
    x.append(i)

# plot 8 curves for 8 paris of thresholds
for row in range(8):
    plt.plot(x,p_8[row],label=str(0.3)+"," + str(0.3+row*0.1))

plt.xlabel("number of 100 games")
plt.ylabel("average probability to win calculated every 100 games")
plt.title("plot of average probability to win for player 1")

plt.legend()
plt.show()
