def p_score(a):
    if len(a) == 0:
        return 0
    add = sum(a)
    score1 = add - p_score(a[1:])
    score2 = add - p_score(a[:-1])
    return max(score1, score2)

n = int(input())
a = list(map(int, input().split()))
tot = sum(a)
p1 = p_score(a)
p2 = tot - p1
if p1 > p2:
    print("Player 1 wins")
elif p1 < p2:
    print("Player 2 wins")
else:
    print("Its a draw")
