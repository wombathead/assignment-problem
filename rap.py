from collections import Counter
from fractions import Fraction
from itertools import permutations 

def object_available(remaining):
    return any(remaining.values())

def print_assignment(assignment):
    if assignment is None:
        print("Error: invalid assingment")
        return

    for i in assignment.keys():
        for a in assignment[i].keys():
            print(assignment[i][a], end='\t')
        print()

def PS(preferences):

    players = [i for i in range(len(preferences))]
    objects = [a for a in preferences[0]]
    n = len(players)
    m = len(objects)

    if n != m:
        print("Error: input must be a square matrix")
        return

    # track how much remains of object a
    remaining = {a: 1 for a in objects}

    # track what object agent i is currently consuming
    consuming = {i: preferences[i][0] for i in players}

    # track the proportion of object a player i receives
    consumed = {i: {a: 0 for a in objects} for i in players}

    while True:
        # get the most consumed object
        c = Counter(consuming.values()).most_common()

        # the object being the most consumed
        most_consumed = c[0][0]

        # the number of agents consuming this object
        agents_consuming = c[0][1]

        # each player consumes delta more of the object they are consuming in
        # this time step
        delta = Fraction(remaining[most_consumed], agents_consuming)

        # give delta more share to each agent of their currently consumed
        # object
        for i in players:
            consumed[i][consuming[i]] += delta
            remaining[consuming[i]] -= delta

        # player i consumes their next most preferred object that is available
        for i in players:
            if remaining[consuming[i]] == 0:
                idx = 0
                while remaining[preferences[i][idx]] == 0:
                    idx += 1

                    if idx > n-1:
                        return consumed

                consuming[i] = preferences[i][idx]

def sd(p, q, preferences):
    """ return TRUE if allocation Pi stochastically dominates allocation Qi
    according to PREFERENCES for player i """

    for t in range(len(preferences)):
        t += 1
        best_items = preferences[:t]

        p_sum = sum([p[i] for i in best_items])
        q_sum = sum([q[i] for i in best_items])

        if q_sum > p_sum:
            return False

    return True

def prefers(p, q, preferences):
    """ return TRUE if player i gets her best best object with greater
    probability in P than Q, OR if she gets her best with equal probability and
    her next best with greater probability in P than Q, OR ... """

    for t in range(len(preferences)):
        t += 1
        best_items = preferences[:t]

        p_sum = sum([p[i] for i in best_items])
        q_sum = sum([q[i] for i in best_items])

        if p_sum > q_sum:
            return True
        elif q_sum > p_sum:
            return False

def main():

    preferences = [
        [0,1,2],
        [0,2,1],
        [1,0,2]]

    p = PS(preferences)
    q = PS(preferences[:2] + [list([0,1,2])])

    print_assignment(p)
    print()
    print_assignment(q)
    print()

    print(sd(p[2], q[2], preferences[2]))
    print(prefers(p[2], q[2], preferences[2]))

    #for perm in permutations(preferences[2]):
    #    profile = preferences[:2] + [list(perm)]
    #    print(profile)
    #    print_assignment(PS(profile))
    #    print()

if __name__=="__main__":
    main()
