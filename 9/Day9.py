from collections import deque, defaultdict


def marble_game(players: int, last_worth: int):
    scores = defaultdict(int)

    board = deque([0])

    for marble_worth in range(1, last_worth+1):

        if marble_worth % 23 == 0:
            board.rotate(7)
            scores[marble_worth % players] += marble_worth + board.pop()
            board.rotate(-1)
        else:
            board.rotate(-1)
            board.append(marble_worth)

    return scores[max(scores, key=scores.get)]


if __name__ == '__main__':
    PLAYERS = 403
    LAST_MARBLE_WORTH = 71920

    print(marble_game(players=PLAYERS, last_worth=LAST_MARBLE_WORTH))
    print(marble_game(players=PLAYERS, last_worth=LAST_MARBLE_WORTH*100))
