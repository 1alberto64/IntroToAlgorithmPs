####################################################
# INSTRUCTOR INPUT BLOCK
# THIS BLOCK WILL BE REPLACED BY INSTRUCTOR INPUTS
# DO NOT CHANGE THE NAMES OF THESE VARIABLES/METHODS
####################################################

TRAVEL_TIME = {
    ('Fort Washington', 'Choptank River'): 2.05,
    ('Fort Washington', 'Hooper Strait'): 1.9333333333333333,
    ('Fort Washington', 'Point Lookout'): 1.8333333333333335,
    ('Fort Washington', 'Sandy Point'): 1.1,
    ('Fort Washington', 'Cove Point'): 1.4666666666666668,
    ('Fort Washington', 'Drum Point'): 1.3833333333333333,
    ('Choptank River', 'Hooper Strait'): 0.65,
    ('Choptank River', 'Point Lookout'): 3.066666666666667,
    ('Choptank River', 'Sandy Point'): 1.1,
    ('Choptank River', 'Drum Point'): 2.3833333333333333,
    ('Choptank River', 'Cove Point'): 2.3833333333333333,
    ('Hooper Strait', 'Point Lookout'): 2.966666666666667,
    ('Hooper Strait', 'Sandy Point'): 1.0,
    ('Hooper Strait', 'Drum Point'): 2.283333333333333,
    ('Hooper Strait', 'Cove Point'): 2.283333333333333,
    ('Point Lookout', 'Sandy Point'): 2.1166666666666667,
    ('Point Lookout', 'Drum Point'): 0.6833333333333333,
    ('Point Lookout', 'Cove Point'): 0.8833333333333333,
    ('Sandy Point', 'Drum Point'): 1.4333333333333333,
    ('Sandy Point', 'Cove Point'): 1.45,
    ('Drum Point', 'Cove Point'): 0.25,
}

L = list(set([item for k in TRAVEL_TIME.keys() for item in k]))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Utility functions that you can use if you wish


def list_minus(L, x):
    # Returns a list of L that does not have x in it
    return list(set(L) - {x})


def travel_time(key1, key2):
    # Looks up x and y in TRAVEL_TIME in a way that order does not matter, returns a time
    global TRAVEL_TIME
    if (key1, key2) in TRAVEL_TIME:
        tm = TRAVEL_TIME[(key1, key2)]
    else:
        tm = TRAVEL_TIME[(key2, key1)]
    return tm


def random_lighthouses(n):
    # Generates a random list of n lighthouses
    # returns a dictionary in the same format as TRAVEL_TIME and a list of lighthouses (new_L)

    from string import ascii_uppercase
    from random import uniform
    from itertools import combinations  # students aren't allowed to use itertools for this assignment
    from math import sqrt

    new_TRAVEL_TIME = {}
    new_L = []
    letters = list(ascii_uppercase)

    for i in range(1, n):
        x = uniform(1, 100)
        y = uniform(1, 100)
        pt_name = letters[i - 1]
        pt = (pt_name, (x, y))
        new_L.append(pt)

    pairs = list(combinations(new_L, 2))
    for i in pairs:
        pt1 = i[0][1]
        pt2 = i[1][1]
        dist = sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
        name = (i[0][0], i[1][0])
        new_TRAVEL_TIME[name] = dist
    return new_TRAVEL_TIME, new_L


def lighthouse_names(TL):
    # Gets a list of the names of the lighthouses in dictionary L
    return list(set([item for k in TL.keys() for item in k]))


def call_counter(f):
    def wrapped(*args, **kwargs):  # deal with any/all arguments
        wrapped.calls += 1
        return f(*args, **kwargs)

    wrapped.calls = 0
    return wrapped


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

####################################################
# MY RECURSIVE FUNCTION


from math import inf

'''
 Accepts start_point (starting lighthouse name), list L (all lighthouses)
 Returns best_tour (sequential list of lighthouses) and best_time (float value of best time in hours)
 You must keep the signatures the same (accepts start_light, L and returns best_tour, best_time;
     start_light is a string, best_tour and L are lists of strings, and best_time is a float)
'''


def fastest_tour(start_light, L):
    best_tour = []  # used to store the running best overall tour that starts at start_light
    best_time = inf  # used to store the time for the best_tour sequence

    # BASE CASE
    if len(L) == 1:
        # Add code to calculate the base case here
        best_time = travel_time(start_light, L[0])
        best_tour = [start_light, L[0]]
        return best_tour, best_time

    # RECURSIVE CASE
    else:
        best_arrival = L[0]
        for arrival_light in L:
            # This should recursively compute all possible tours through L which begin at start_point

            L_minus = list_minus(L, arrival_light)

            if (arrival_light, tuple(L_minus)) not in travelHistory:
                tour, time = fastest_tour(arrival_light, L_minus)
                travelHistory[(arrival_light, tuple(L_minus))] = time, tour
            else:
                tour = list(travelHistory[(arrival_light, tuple(L_minus))][1])
                time = travelHistory[(arrival_light, tuple(L_minus))][0]

            if (time + travel_time(start_light, arrival_light)) < (best_time + travel_time(start_light, best_arrival)):
                best_time = time
                best_tour = tour[:]
                best_arrival = arrival_light

        best_tour.insert(0, start_light)
        best_time += travel_time(start_light, best_arrival)

        return best_tour, best_time

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

####################################################
# MY MAIN

# Suggested structure to kick off your calculations
# You will need to adjust this code to match your implementation


def get_fastest_tour(L):
    bestTour = []
    bestTime = inf

    global travelHistory

    travelHistory = {}

    if len(L) <= 1:
        return L, 0

    for start_light in L:
        L_minus = list_minus(L, start_light)
        tour, time = fastest_tour(start_light, L_minus)
        if time < bestTime:
            bestTour = tour
            bestTime = time

    return bestTour, bestTime


best_tour, best_time = get_fastest_tour(L)

print("The best tour is: ", ', '.join(best_tour))
print("The best time is: ", best_time)

'''
# INSTRUCTOR-PROVIDED TEST DATA
# Ensure that your code matches both the input signature and the expected output
# For grading, different test data will be pasted into the input cell and your code cells will be executed
# Be sure that your input and output signatures match the provided sample data

# Test #1
TRAVEL_TIME = {
    ('D', 'E'): 9.8874546134365,
    ('D', 'B'): 8.650955785569098,
    ('D', 'C'): 4.527990409960845,
    ('D', 'A'): 9.817667809230786,
    ('E', 'B'): 10.931854306263975,
    ('E', 'C'): 7.255251488484818,
    ('E', 'A'): 12.917982527478712,
    ('B', 'C'): 4.113565483054365,
    ('B', 'A'): 9.560863383439097,
    ('C', 'A'): 7.854345573910511,
}
# Expected output
# The best tour is:  A, B, C, D, E
# The best time is:  28.089873889890804

# Test #2
TRAVEL_TIME = {
    ('B', 'C'): 6.429795406216918,
    ('B', 'A'): 11.629846115160516,
    ('B', 'D'): 7.679251919404714,
    ('B', 'E'): 9.347706263090837,
    ('C', 'A'): 12.280646160363432,
    ('C', 'D'): 7.746192483295421,
    ('C', 'E'): 9.90681627370574,
    ('A', 'D'): 12.227183481562683,
    ('A', 'E'): 16.655823285647106,
    ('D', 'E'): 8.25715774835559,
}
# Expected output
# The best tour is:  A, B, C, D, E
# The best time is:  34.06299175302845

# Test #3
TRAVEL_TIME = {
    ('F', 'E'): 7.453320453415392,
    ('F', 'D'): 6.170569410345761,
    ('F', 'I'): 10.448429302986911,
    ('F', 'G'): 6.187750187309644,
    ('F', 'C'): 12.090422838563583,
    ('F', 'H'): 11.539119418380032,
    ('F', 'A'): 13.23865323724485,
    ('F', 'J'): 14.209616157057711,
    ('F', 'B'): 12.029520235766265,
    ('E', 'D'): 4.594971038617467,
    ('E', 'I'): 9.488857351897519,
    ('E', 'G'): 4.661282508675182,
    ('E', 'C'): 10.705763401441896,
    ('E', 'H'): 10.12354365573923,
    ('E', 'A'): 12.05863087182219,
    ('E', 'J'): 12.857918364285274,
    ('E', 'B'): 10.915808926216425,
    ('D', 'I'): 8.773798408565863,
    ('D', 'G'): 3.549820998388679,
    ('D', 'C'): 9.084763991756446,
    ('D', 'H'): 8.47244200438249,
    ('D', 'A'): 10.768085646027655,
    ('D', 'J'): 11.205467989446557,
    ('D', 'B'): 9.811703475051996,
    ('I', 'G'): 4.856711290250502,
    ('I', 'C'): 10.303247633652786,
    ('I', 'H'): 9.72873923304563,
    ('I', 'A'): 11.752971702744057,
    ('I', 'J'): 12.386140947772116,
    ('I', 'B'): 10.715926552978804,
    ('G', 'C'): 8.939922836985131,
    ('G', 'H'): 8.325372714362043,
    ('G', 'A'): 10.658709470483634,
    ('G', 'J'): 11.05300320168352,
    ('G', 'B'): 9.726036954632448,
    ('C', 'H'): 14.85107596522508,
    ('C', 'A'): 16.127909792272288,
    ('C', 'J'): 17.54748278310382,
    ('C', 'B'): 14.699070399680458,
    ('H', 'A'): 15.723529687188293,
    ('H', 'J'): 17.10791004081554,
    ('H', 'B'): 14.306778662449995,
    ('A', 'J'): 16.949188359233272,
    ('A', 'B'): 14.239542023142393,
    ('J', 'B'): 16.6207970728817,
}
# Expected output
# The best tour is:  A, B, C, D, E, F, G, H, I, J
# The best time is:  86.69967098910159

# Test 4 - test against some actual lighthouses used in the challenge, so
# you can see the original motivation for this assignment.  Times are from
# maps.google.com and reflect best possible driving times between two
# lighthouses subject to current traffic conditions.
TRAVEL_TIME = {
    ('Fort Washington', 'Choptank River'): 2.05,
    ('Fort Washington', 'Hooper Strait'): 1.9333333333333333,
    ('Fort Washington', 'Point Lookout'): 1.8333333333333335,
    ('Fort Washington', 'Sandy Point'): 1.1,
    ('Fort Washington', 'Cove Point'): 1.4666666666666668,
    ('Fort Washington', 'Drum Point'): 1.3833333333333333,
    ('Choptank River', 'Hooper Strait'): 0.65,
    ('Choptank River', 'Point Lookout'): 3.066666666666667,
    ('Choptank River', 'Sandy Point'): 1.1,
    ('Choptank River', 'Drum Point'): 2.3833333333333333,
    ('Choptank River', 'Cove Point'): 2.3833333333333333,
    ('Hooper Strait', 'Point Lookout'): 2.966666666666667,
    ('Hooper Strait', 'Sandy Point'): 1.0,
    ('Hooper Strait', 'Drum Point'): 2.283333333333333,
    ('Hooper Strait', 'Cove Point'): 2.283333333333333,
    ('Point Lookout', 'Sandy Point'): 2.1166666666666667,
    ('Point Lookout', 'Drum Point'): 0.6833333333333333,
    ('Point Lookout', 'Cove Point'): 0.8833333333333333,
    ('Sandy Point', 'Drum Point'): 1.4333333333333333,
    ('Sandy Point', 'Cove Point'): 1.45,
    ('Drum Point', 'Cove Point'): 0.25,
}
# Expected output
# The best tour is:  Point Lookout, Drum Point, Cove Point, Fort Washington, Sandy Point, Hooper Strait, Choptank River
# The best time is:  5.15

# If you want to visualize this tour, it's here:
# https://goo.gl/maps/h9NbbQT5kS3S6kZ98
# If you go there, try reversing the order of Drum Point and Cove Point.
# Depending on the time of day, it may be faster to take one over the other.
# That is, it may be faster to skip past Drum Point and head to Cove Point,
# then come back to Drum on way to rt 235.  At certain times, the time from
# Cove to Ft. Washington is actually more than backtracking to the faster
# route 235 and heading to Ft. Washington that way.  This is what makes TSP
# such an interesting problem.
'''