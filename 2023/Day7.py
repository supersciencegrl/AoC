example = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''
example = example.split('\n')

with open('Day7.txt', 'rt') as fin:
    input_text = fin.readlines()

card_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
hand_ranks = [[5], [1, 4], [2, 3], [1, 1, 3], [1, 2, 2], [1, 1, 1, 2], [1, 1, 1, 1, 1]]
hand_ranks.reverse()

def find_hand_type(hand: str):
    duplicates = {}
    for card in hand:
        if card not in duplicates.keys():
            duplicates[card] = 5 - len(hand.replace(card, '')) # Count card duplicates

    hand_type = sorted(list(duplicates.values()))

    return hand_type

def rank_hands(input_text):
    #input_dict = {k:v for k,v in [item.split() for item in input_text]}
    rank_list = [item.split() for item in input_text]
    rank_dict = dict(enumerate(rank_list))

    ranks = []
    # Label hands with their hand type (as an index of hand type strength - high is strong)
    for i, [hand, bid] in rank_dict.items():
        hand_type = find_hand_type(hand)
        rank_dict[i].append(hand_ranks.index(hand_type))

    
    rank_sorted = sorted(rank_dict.values(), key = lambda x: (-x[2], card_ranks.index(x[0][0]), card_ranks.index(x[0][1]), card_ranks.index(x[0][2]), card_ranks.index(x[0][3]), card_ranks.index(x[0][4])))
    rank_sorted.reverse()

    winnings = [int(value[1])*(i+1) for (i,value) in enumerate(rank_sorted)]
    total_winnings = sum(winnings)
    
    return total_winnings

part1_result = rank_hands(input_text)
print(f'Part 1 result: {part1_result}')
if part1_result == 251136060:
    print('PASS')
