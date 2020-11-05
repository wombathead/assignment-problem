from collections import Counter
from fractions import Fraction

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

def PS(prefs):

    players = [i for i in range(len(prefs))]
    objects = [a for a in prefs[0]]
    n = len(players)
    m = len(objects)

    if n != m:
        print("Error: input must be a square matrix")
        return

    # track how much remains of object a
    remaining = {a: 1 for a in objects}

    # track what object agent i is currently consuming
    consuming = {i: prefs[i][0] for i in players}

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
                while remaining[prefs[i][idx]] == 0:
                    idx += 1

                    if idx > n-1:
                        return consumed

                consuming[i] = prefs[i][idx]

def main():
    #prefs = [
    #    [0,1,2,3,4,5],
    #    [0,1,2,3,4,5],
    #    [2,0,1,3,4,5],
    #    [2,4,5,3,0,1],
    #    [4,5,2,3,0,1],
    #    [4,5,2,3,0,1]]

    prefs = [
        [0,1,2],
        [0,2,1],
        [0,1,2]]

    assignment = PS(prefs)
    print_assignment(assignment)

if __name__=="__main__":
    main()
