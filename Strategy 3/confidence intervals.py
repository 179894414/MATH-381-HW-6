import math
import random as rand
import numpy as np

# add a new parameter: increase
# increase means how much increasing in the threshold with every 5 cards being guessed right
def play(players, id, card, deck, cardsUsed, count, canGiveUp, mode,increase):
    if (mode == 1): # to see if we use the first or second type of strategies
        cardsUsed.append(card)
    if (len(deck) == 1): # marginal(base) case: all 60 cards are guessed right in one round
        return (0, 0)
    else:
        if (id==0): #player 1 using the third type of strategies
            nincrease = math.floor(count/5.0)
            threshold = players[id][1]+nincrease*increase
        else:
            threshold = players[id][1]
        if (mode == 1 & id == 0): #if player 1 uses the second type of strategies
            small = 0
            for l in range(len(cardsUsed)):
                if (cardsUsed[l] < card):
                    small += 1
            p_smaller = (card - 1 - small) / (60.0 - len(cardsUsed))
        else:
            p_smaller = (card - 1) / 60.0 #the probability that the next card is smaller than the current card
        p_larger = 1 - p_smaller
        if ((p_smaller >= threshold) and (p_smaller > p_larger)): # if probability for smaller than >= threhold and p_smaller > p_larger
            new_card = deck.pop(0)
            if (mode == 1):
                cardsUsed.append(card)
            if (new_card < card): # player guesses smaller than, and the new card is smaller than the current card
                count += 1
                card = deck.pop(0)
                return play(players, id, card, deck, cardsUsed, count, True, mode,increase)
            else: # player guesses smaller than, but the new card is larger, so he loses, and return his id and count
                return (id, count)
        elif (p_larger >= threshold): # if probability for larger than >= threhold and p_larger > p_small
            new_card = deck.pop(0)
            if (mode == 1):
                cardsUsed.append(card)
            if (new_card > card): # player guesses larger than, and the new card is larger
                count += 1
                card = deck.pop(0)
                return play(players, id, card, deck, cardsUsed, count, True, mode,increase)
            else: # player guesses larger, but the new card is smaller, so he loses, and return his id and count
                return (id, count)
        else: # both p_smaller and p_larger < threshold; players would like to give up this turn if he can
            if (canGiveUp): # he can give up
                if (id == 0): # if the current player is player 1, switch to player 2
                    new_id = 1
                else: # if the current player is player 2, switch to player 2
                    new_id = 0
                return play(players, new_id, card, deck, cardsUsed, count, False, mode,increase)
            else: # he cannot give up, so he compares p_smaller and p_larger and choose the larger probability
                if (p_smaller >= (p_larger)): # p_smaller is larger, he guesses the next card is smaller
                    new_card = deck.pop(0)
                    if (mode == 1):
                        cardsUsed.append(card)
                    if (new_card < card): # he guesses smaller, and the next card is smaller
                        count += 1
                        card = deck.pop(0)
                        return play(players, id, card, deck, cardsUsed, count, True, mode,increase)
                    else: # he guesses smaller, but the next card is larger, he loses and this round ends
                        return (id, count)
                else: # p_larger is larger, he guesses the next card is larger
                    new_card = deck.pop(0)
                    if (mode == 1):
                        cardsUsed.append(card)
                    if (new_card > card): # he guesses larger, and the next card is larger
                        count += 1
                        card = deck.pop(0)
                        return play(players, id, card, deck, cardsUsed, count, True, mode,increase)
                    else: # he guesses larger, but the next card is larger, he loses and this round ends
                        return (id, count)

#Create a list for deck
backup_deck = []
for i in range (60): #store 60 cards fisrt, shuffle will be done in for loop
    backup_deck.append(i)

#how much increasing in threshold for every 5 cards
increase = 0.05

#Store the number of wining for both players
win_count1 = 0
win_count2 = 0

#Store 10 estimates of wining probability for both players
win_p1 = []
win_p2 = []

#store the maximum and minimumm probability (confidence interval) for both players from 4 different levels of increasing
wining_p1 = np.zeros([4,2])
wining_p2 = np.zeros([4,2])

#go through 4 different levels of increasing: 0.05,0.1,0.15,0.2
for row in range(4):
        # probability threshold for players
        p1 = 0.3
        p2 = 0.3
        increase = increase + 0.05*row
        #Create a 2x2 matrix players: first column represents players; second column represents probability shresholds
        # 0 means player 1, 1 means player 2
        players = [[0,p1],[1,p2]]
        win_p1 = []
        win_p2 = []
        for estimate in range(10):
            win_count1 = 0
            win_count2 = 0
            for i in range(20000): # play 20000 games in each estimate
                scores = [0,0] #initialize score when a new game starts
                for j in range(10): # play 10 rounds in each game
                    deck = backup_deck.copy()
                    rand.shuffle(deck)  # shuffle the deck
                    card = deck.pop(0) # turn over the first card
                    cardsUsed = []
                    if (j <= 4): #each player starts 5 rounds in one game
                        result = play(players, 0, card, deck, cardsUsed, 0, False, 0,increase)
                    else:
                        result = play(players, 1, card, deck, cardsUsed, 0, False, 0,increase)
                    lose_player = result[0]
                    score = result[1]
                    scores[lose_player] += score
            #count number of wining for player 1
                if (scores[0] < scores[1]):
                    win_count1 += 1
                elif (scores[0] > scores[1]):
                    win_count2 += 1
            win_p1.append(win_count1/20000)
            win_p2.append(win_count2/20000)
        wining_p1[row][0] = max(win_p1) #write in maximum p
        wining_p1[row][1] = min(win_p1) #write in minimum p
        wining_p2[row][0] = max(win_p2)
        wining_p2[row][1] = min(win_p2)

print(wining_p1)
print(wining_p2)
