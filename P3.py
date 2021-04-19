####################################################
# INSTRUCTOR INPUT BLOCK
# THIS BLOCK WILL BE REPLACED BY INSTRUCTOR INPUTS
# DO NOT CHANGE THE NAMES OF THESE VARIABLES/METHODS
####################################################
# TRAVEL_TIME = {
#     ('Lightship Chesapeake', 'Concord Point'): 0.8,
#     ('Lightship Chesapeake', 'Point Lookout'): 2.3,
#     ('Lightship Chesapeake', 'Sandy Point'): 0.7166666666666667,
#     ('Lightship Chesapeake', 'Drum Point'): 1.62,
#     ('Concord Point', 'Point Lookout'): 3.1166666666666667,
#     ('Concord Point', 'Sandy Point'): 1.45,
#     ('Concord Point', 'Drum Point'): 2.23,
#     ('Point Lookout', 'Sandy Point'): 2.1166666666666667,
#     ('Point Lookout', 'Drum Point'): 0.7666666666666667,
#     ('Sandy Point', 'Drum Point'): 1.4333333333333333
# }
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
LIGHTS = list(set([item for k in TRAVEL_TIME.keys() for item in k]))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
####################################################
# Utility functions that you can use if you wish

'''Returns a list of L that does not have x in it'''
def list_minus(L, x):
    return list(set(L) - {x})


'''Looks up x and y in TRAVEL_TIME in a way that order does not matter, returns a time'''
def travel_time(key1, key2):

    global TRAVEL_TIME
    if (key1, key2) in TRAVEL_TIME:
        tm = TRAVEL_TIME[(key1, key2)]
    else:
        tm = TRAVEL_TIME[(key2, key1)]
    return tm


'''
    Generates a random list of n lighthouses
    returns a dictionary in the same format as TRAVEL_TIME and a list of lighthouses (new_L)
'''
def random_lighthouses(n):
    from string import ascii_uppercase
    from random import uniform
    from itertools import combinations  # students aren't allowed to use itertools for this assignment
    from math import sqrt

    new_TRAVEL_TIME = {}
    new_L = []
    letters = list(ascii_uppercase)

    for i in range(1, n + 1):
        x = uniform(1, 100)
        y = uniform(1, 100)
        if i - 1 < len(ascii_uppercase):
            pt_name = letters[i - 1]
        else:
            pt_name = letters[(i - 1) % len(ascii_uppercase)] + str(i-1)

        pt = (pt_name, (x, y))
        new_L.append(pt)

    pairs = list(combinations(new_L, 2))
    for i in pairs:
        pt1 = i[0][1]
        pt2 = i[1][1]
        dist = sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
        name = (i[0][0], i[1][0])
        new_TRAVEL_TIME[name] = dist
    return new_TRAVEL_TIME


'''Gets a list of the names of the lighthouses in dictionary L'''
def lighthouse_names(TL):
    return list(set([item for k in TL.keys() for item in k]))


'''Counts the number of times a method gets called'''
def call_counter(f):
    def wrapped(*args, **kwargs):  # deal with any/all arguments
        wrapped.calls += 1
        return f(*args, **kwargs)

    wrapped.calls = 0
    return wrapped


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

####################################################
# MY RECURSIVE FUNCTION

'''
 Accepts start_point (starting lighthouse name), list L (all lighthouses)
 Returns best_tour (sequential list of lighthouses) and best_time (float value of best time in hours)
 You must keep the signatures the same (accepts start_light, L and returns best_tour, best_time;
     start_light is a string, best_tour and L are lists of strings, and best_time is a float)
'''

@call_counter
def fastest_tour_faster(start_light, L):
    best_tour = []  # used to store the running best overall tour that starts at start_light
    best_time = -1  # used to store the time for the best_tour sequence

    # BASE CASE: Having only one target and one L means that we only have one best tour
    if len(L) == 1:
        best_time = travel_time(start_light, L[0])
        best_tour = [start_light, L[0]]
        return best_time, best_tour

    # RECURSIVE : We have multiple paths we can still take
    else:
        best_arrival = None  # Stores which lighthouse destination is better

        for arrival_light in L:  # Iterate to each destination and get their fastest tour

            L_minus = list_minus(L, arrival_light)  # Remove destination from remaining lighthouses
            # If we have not seen this destination and sublist pair, generate it then store the result
            if (arrival_light, tuple(L_minus)) not in travelHistory:
                time, tour = fastest_tour_faster(arrival_light, L_minus)
                travelHistory[(arrival_light, tuple(L_minus))] = time, tour
            # We have already a result for this destination and sublist pair so we use it.
            else:
                tour = list(travelHistory[(arrival_light, tuple(L_minus))][1])
                time = travelHistory[(arrival_light, tuple(L_minus))][0]
            # Check if the resulting tour is better than ones previously found
            if best_time < 0 or (time + travel_time(start_light, arrival_light)) < (best_time + travel_time(start_light, best_arrival)):
                best_time = time
                best_tour = tour[:]
                best_arrival = arrival_light

        # Update the best time and tour to give back a result containing the starting lighthouse
        best_tour.insert(0, start_light)
        best_time += travel_time(start_light, best_arrival)

        return best_time, best_tour

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

####################################################
# MY MAIN

'''
 Accepts list L (all lighthouses)
 Returns best_tour (sequential list of lighthouses) and best_time (float value of best time in hours)
 You must keep the signatures the same (accepts start_light, L and returns best_tour, best_time;
     start_light is a string, best_tour and L are lists of strings, and best_time is a float)
'''
@call_counter
def get_fastest_tour_faster(L):

    global TRAVEL_TIME

    bestTour = []  # used to store the running best overall tour that starts at start_light
    bestTime = -1  # used to store the time for the best_tour sequence

    # Set up a global log to remember recursive results
    global travelHistory

    # Reset history
    travelHistory = {}

    # If the number of lighthouses is less than 1 then there isn't a tour since there is no travel done
    if len(L) <= 1:
        return L, 0
    # Check times when you start at every lighthouse that exists
    for start_light in L:
        L_minus = list_minus(L, start_light)
        time, tour = fastest_tour_faster(start_light, L_minus)
        # See which full tour was the fastest one
        if bestTime < 0 or time < bestTime:
            bestTour = tour
            bestTime = time

    return bestTime, bestTour


best_time, best_tour = get_fastest_tour_faster(LIGHTS)

print("The best tour is: ", ', '.join(best_tour))
print("The best time is: ", best_time)


####################################################
# MY NEAREtST NEIGHBOR AND MONTE CARLO FUNCTIONS
'''
 Accepts list L (all lighthouses)
 Returns best_tour (sequential list of lighthouses) and best_time (float value of best time in hours)
 You must keep the signatures the same (accepts start_light, L and returns best_tour, best_time;
     start_light is a string, best_tour and L are lists of strings, and best_time is a float)
'''
@call_counter
def nearest_neighbor(L):
    if len(L) <= 1:  # If the number of lighthouses is less than 1 exit tour.
        return 0, L
    fastest_time = -1
    fastest_tour = []
    for starting in L:  # Start a tour from each light house
        time, tour = get_greedy_path(starting, list_minus(L, starting))
        if fastest_time == -1 or fastest_time > time:  # Select the fastest tour as the final answer.
            fastest_time = time
            fastest_tour = tour

    return fastest_time, fastest_tour

'''
 Accepts start_point (starting lighthouse name), list L (all lighthouses)
 Returns best_tour (sequential list of lighthouses) and best_time (float value of best time in hours)
 You must keep the signatures the same (accepts start_light, L and returns best_tour, best_time;
     start_light is a string, best_tour and L are lists of strings, and best_time is a float)
'''
@call_counter
def get_greedy_path(start_point, L):
    if len(L) <= 0:  # If there are no lighthouses left to visit, exit
        return 0, L
    if len(L) == 1:  # If there is only one lighthouse left return its tour
        return travel_time(start_point, L[0]), [start_point, L[0]]
    shortest = None  # Store the closest light house
    for next in L:  # Check every light house to see which is closest to the current one
        if shortest is None:
            shortest = next  # Assume the first lighthouse seen to be the closest
        elif travel_time(start_point, shortest) > travel_time(start_point, next):
            shortest = next  # If the next lighthouse is closer than the shortest make next the shortest.

    time, tour = get_greedy_path(shortest, list_minus(L, shortest))  # Search for the next closest lighthouse.

    tour.insert(0, start_point)  # Add the current lighthouse to tour
    time = time + travel_time(start_point, shortest)

    return time, tour


best_time, best_tour = nearest_neighbor(LIGHTS)

print("The best tour is: ", ', '.join(best_tour))
print("The best time is: ", best_time)

''' 
Accepts an integer M, for the number of iterations of the test to execute, and n, an integer value
for the number of lighthouses in each test run.  Returns an M-length list of the percent difference between
the optimal and approximate solution for each random iteration
'''
def monte_carlo(m, n):
    global TRAVEL_TIME
    counter = 0
    result = []
    # Do calculations M times
    while counter < m:
        TRAVEL_TIME = random_lighthouses(n)  # Create a random set of lighthouses
        LIGHTS = lighthouse_names(TRAVEL_TIME) # Get lighthouse names

        bruteforce_time, tour = get_fastest_tour_faster(LIGHTS)

        nearneigh_time, tour = nearest_neighbor(LIGHTS)

        diffpct = abs(nearneigh_time - bruteforce_time) / bruteforce_time
        result.append(diffpct)
        counter = counter + 1
    return result

# def sort_converter(travelLog):
#     log = travelLog.items()
#     log = merge_sort(log)
#     for item in log:
#         travelLog[item[0]] = item[1]
#     return travelLog
#
# ''' A merge sort that sorts points in ascending order using the coordiantes '''
# @call_counter
# def merge_sort(log):
#     # Base case 1: There is one or no elements in the given list
#     if len(log) <= 1:
#         return log
#
#     # Recursive case 1: Divide list into two lists cut by the middle
#
#     left_sub_logs = merge_sort(log[0:len(log)//2])
#     right_sub_logs = merge_sort(log[len(log)//2:])
#
#     # Merge the returning sub lists
#     sorted_points = merge(left_sub_logs, right_sub_logs)
#     return sorted_points
#
#
# ''' Merge sort helper to merge the given arrays '''
# @call_counter
# def merge(left_sub_logs, right_sub_logs):
#
#     merged_log = list()
#
#     # Choose the smallest point from the leading elements and add it to the merge list
#     while (len(left_sub_logs) > 0) and (len(right_sub_logs) > 0):
#         if left_sub_logs[0][1] < right_sub_logs[0][1]:
#             merged_log.append(right_sub_logs.pop(0))
#         else:
#             merged_log.append(right_sub_logs.pop(0))
#
#
#     # If there are points left on left add them to the sorted list
#     while len(left_sub_logs) > 0:
#         merged_log.append(right_sub_logs.pop(0))
#
#     # If there are points right on left add them to the sorted list
#     while len(left_sub_logs) > 0:
#         merged_log.append(right_sub_logs.pop(0))
#
#     return merged_log
#
# def multi_fragment(L):
#     global TRAVEL_TIME
#     travelLog = TRAVEL_TIME.copy()
#     travelLog = sort_converter(travelLog)
#     time = 0
#     tours = []
#     for path in travelLog:
#         for tour in tours:
#             if (path[0][0] == tour[0] or path[0][0] == tour[len(tour)-1]) and (path[0][1] == tour[0] or path[0][1] == tour[len(tour)-1]) and (len(travelLog) != 1 or len(tour) < len(L)):
#                 continue
#             elif path[0][0] in tour and (path[0][0] != tour[0] and path[0][0] != tour[len(tour)-1]) or path[0][1] in tour and (path[0][1] != tour[0] and path[0][1] != tour[len(tour)-1]):
#                 continue
#             elif (path[0][0] == tour[0] or path[0][0] == tour[len(tour)-1]) and (path[0][1] == tour[0] or path[0][1] == tour[len(tour)-1]) and (len(travelLog) == 1 and len(tour) == len(L)):
#                 return time, tour
#             elif path[0][0] == tour[0]:
#                 tour.insert(0, path[0][1])
#                 time = time + tour[1]
#                 break
#             elif path[0][1] == tour[0]:
#                 tour.insert(0, path[0][0])
#                 time = time + tour[1]
#                 break
#             elif path[0][0] == tour[len(tour)-1]:
#                 tour.append(path[0][1])
#                 time = time + tour[1]
#                 break
#             elif path[0][1] == tour[len(tour)-1]:
#                 tour.append(path[0][0])
#                 time = time + tour[1]
#                 break
#         tours.append(path[0])

y = monte_carlo(50, 5)

for val in y:
    print(val)








# Require: Sorted set of all edges of the problem E.
# Ensure: A tour T.
# 1: for each e in E do
# 2: if (e is closing T and size(T) < n) or (e has a city already connected to
# two others) then
# 3: go to the next edge
# 4: end if
# 5: if e is closing T and size(T) = n then
# 6: add e to T
# 7: return T
# 8: end if
# 9: add e to T
# 10: end for
# 11: return T

# m = 10
# n = 5
# x_number_of_runs = range(1, m+1)
# y_monte_carlo = monte_carlo(m, n)
#
# # %matplotlib inline
# import matplotlib.pyplot as plt
#
# # plt.rcParams['figure.figsize'] = [10,5]
# plt.figure()
# plt.title("Algorithm Performance", size="xx-large")
# plt.ylabel("Total Function Calls", size="x-large")
# plt.xlabel("Total of Lighthouses", size="x-large")
# # plt.ylim([0,30]) # y-axis scale
#
# # The "b^-" has meaning - "b" means blue, "^" means triangles (try *, s, o),
# # "-" means draw a line
# plt.plot(x_number_of_runs, y_monte_carlo, "b^-", markersize=10, linewidth=2, label="exec steps")
# plt.tick_params(axis="both", which="major", labelsize=14)
# plt.legend(loc=(0.25,0.75), scatterpoints=1)

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
#
# import random
# import math
#
#
# def fact(n):
#     if n <= 1:
#         return 1
#     else:
#         return n*fact(n-1)
#
# # Data creation
# x_number_of_destinations = range(3, 10)
# y1_number_of_calls = list()
# y2_assymtotic_time = list()
# for number_of_destinations in x_number_of_destinations:
#     TRAVEL_TIME = random_lighthouses(number_of_destinations)
#     best_tour, best_time = get_fastest_tour()
#     y1_number_of_calls.append(get_fastest_tour.calls + fastest_tour.calls)
#     y2_assymtotic_time.append(fact(number_of_destinations*number_of_destinations))
#
#
#
# # %matplotlib inline
# import matplotlib.pyplot as plt
#
# # plt.rcParams['figure.figsize'] = [10,5]
# plt.figure()
# plt.title("Algorithm Performance", size="xx-large")
# plt.ylabel("Total Function Calls", size="x-large")
# plt.xlabel("Total of Lighthouses", size="x-large")
# # plt.ylim([0,30]) # y-axis scale
#
# # The "b^-" has meaning - "b" means blue, "^" means triangles (try *, s, o),
# # "-" means draw a line
# plt.plot(x_number_of_destinations, y1_number_of_calls, "b^-", markersize=10, linewidth=2, label="exec steps")
# plt.plot(x_number_of_destinations, y2_assymtotic_time, "r*-", markersize=10, linewidth=2, label="exec steps")
# plt.tick_params(axis="both", which="major", labelsize=14)
# plt.legend(loc=(0.25,0.75), scatterpoints=1)