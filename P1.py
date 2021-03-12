# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

###################################################
#  INSTRUCTOR INPUT BLOCK
#  THIS CELL WILL BE REPLACED BY GRADER INPUTS
#  DO NOT CHANGE THE NAMES OR SIGNATURES OF THESE VARIABLES
#  SAMPLE DATA AND OUTPUTS ARE GIVEN AT THE END OF THIS ASSIGNMENT
###################################################

POINTS = [(6, 6), (4, 7), (17, 3), (6, 18), (2, 13), (12, 5), (5, 10), (18, 16), (2, 20), (13, 1)]
# POINTS = [(6, 4), (6, 32), (6, 25), (6, 27), (6, 14)]
# POINTS = [(6, 4), (32, 4), (25, 4), (27, 4), (14, 4)]
# POINTS = [(-12, 5), (-11, 5), (24, 5), (26, 5)]
# POINTS = [(-5, 5), (10, 14), (-12, -2), (8, -6)]
M = 3


# Each point is a tuple (x,y)
# POINTS is a list of all points (i.e. a list of tuples)
# The data we're expecting as a result is also list of tuples with three elements:
#    point #1, point #2, and the distance between them:  ( (x1,y1),(x2,y2),distance) )
# These are then stacked into a list with up to M entries in it:  M_closest = [(tuple1), (tuple2), ... (tupleM)]


import math

def call_counter(f):
    def wrapped(*args, **kwargs): # deal with any/all arguments
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped

''' 
    Closest Distance, returns the m closest pairs between the points
    Parameter: points - A list of tuples which represent a point.
               m - the number of closest points we are looking for
    Return: m_closest - A list of tuples which each contain (Point1, Point2, distance) ordered on ascending order 
            by distance. If m is equal or smaller than 0, or if points have less than 1 point it returns an empty list
            Otherwise it will returns m tuples. If there there isn't enough to return m tuples it will return 
            the maximum amount it can.
'''
@call_counter
def closestDistance(points, m):
    m_closest = list()
    # If m <= exit because no pairs are being queried
    if m > 0:
        # Pre-sort Points by X to define lines
        sorted_points = merge_sort(points)

        # Call recursive code to get M closest points
        m_closest = closest_pairs(sorted_points, m)

    return m_closest


''' A merge sort that sorts points in ascending order using the coordiantes '''
@call_counter
def merge_sort(points):
    # Base case 1: There is one or no elements in the given list
    if len(points) <= 1:
        return points

    # Recursive case 1: Divide list into two lists cut by the middle

    left_sub_points = merge_sort(points[0:len(points)//2])
    right_sub_points = merge_sort(points[len(points)//2:])

    # Merge the returning sub lists
    sorted_points = merge(left_sub_points, right_sub_points)
    return sorted_points


''' Merge sort helper to merge the given arrays '''
@call_counter
def merge(left_sub_points, right_sub_points):

    merged_points = list()

    # Choose the smallest point from the leading elements and add it to the merge list
    while (len(left_sub_points) > 0) and (len(right_sub_points) > 0):
        if left_sub_points[0] < right_sub_points[0]:
            merged_points.append(left_sub_points.pop(0))
        elif left_sub_points[0] > right_sub_points[0]:
            merged_points.append(right_sub_points.pop(0))
        else:
            if left_sub_points[1] < right_sub_points[1]:
                merged_points.append(left_sub_points.pop(0))
            else:
                merged_points.append(right_sub_points.pop(0))

    # If there are points left on left add them to the sorted list
    while len(left_sub_points) > 0:
        merged_points.append(left_sub_points.pop(0))

    # If there are points right on left add them to the sorted list
    while len(right_sub_points) > 0:
        merged_points.append(right_sub_points.pop(0))

    return merged_points


''' Implements a divide and conquer tactic to find the closest points '''
@call_counter
def closest_pairs(points, m):
    # Get number of points in list to choose a recursive or a base case.
    point_count = len(points)

    # Base Case 1: If there is none or 1 point there are no close points
    if point_count <= 1:
        # Return empty list
        return list()

    # Base Case 2: If there are two points return the only pair possible
    elif point_count == 2:
        # Return the only distance pair
        m_closest = closes_points(points, m)
        return m_closest

    # Recursive Case 1: If there are enough combination of points to get m pairs
    elif (math.factorial(point_count)/(2*math.factorial(point_count-2))) > m:

        # Assuming points is sorted, divide the list in 2 sub lists
        left_points = points[0:point_count//2]
        right_points = points[point_count//2:point_count]

        # Keep dividing the sub lists to start finding the m closest pairs
        closest_left = closest_pairs(left_points, m)
        closest_right = closest_pairs(right_points, m)

        # Get the number of pairs achieved from the sublists
        closest_left_count = len(closest_left)
        closest_right_count = len(closest_right)

        # Get the minimum range needed to decide if there are middle points that we need to check
        if (closest_left_count > 0) and (closest_right_count > 0):
            if closest_left[closest_left_count-1][2] > closest_right[closest_right_count-1][2]:
                middle_points_threshold = closest_left[closest_left_count-1][2]
            else:
                middle_points_threshold = closest_right[closest_right_count-1][2]
        else:
            if closest_left_count > 0:
                middle_points_threshold = closest_left[closest_left_count-1][2]
            else:
                middle_points_threshold = closest_right[closest_right_count-1][2]

        # Create a list with points that are horizontally close enough to make distances shorter than the current max
        middle_left = list()
        middle_right = list()

        for point in left_points:
            if (point[0] > points[point_count//2][0] - middle_points_threshold) & (point[0] < points[point_count//2][0] + middle_points_threshold):
                middle_left.append(point)
        for point in right_points:
            if (point[0] > points[point_count//2][0] - middle_points_threshold) & (point[0] < points[point_count//2][0] + middle_points_threshold):
                middle_right.append(point)

        # Get the m distances possible from middle points
        middle_closest = middle_closest_pairs(middle_left, middle_right, m)

        # Get the m closest points from between the corner pairs
        corner_closest = list()

        for count in range(0, m):
            if (len(closest_left) > 0) and (len(closest_right) > 0):
                if closest_left[0][2] < closest_right[0][2]:
                    corner_closest.append(closest_left.pop(0))
                else:
                    corner_closest.append(closest_right.pop(0))
            elif len(closest_left) > 0:
                corner_closest.append(closest_left.pop(0))
            elif len(closest_right) > 0:
                corner_closest.append(closest_right.pop(0))
            else:
                break

        # Get the m closest points from all the found distances
        m_closest = list()

        for count in range(0, m):
            if (len(corner_closest) > 0) and (len(middle_closest) > 0):
                if corner_closest[0][2] < middle_closest[0][2]:
                    m_closest.append(corner_closest.pop(0))
                else:
                    m_closest.append(middle_closest.pop(0))
            elif len(corner_closest) > 0:
                m_closest.append(corner_closest.pop(0))
            elif len(middle_closest) > 0:
                m_closest.append(middle_closest.pop(0))
            else:
                break

        # Return the m closest points
        return m_closest

    # Base Case 3: If there aren't enough points to get m pairs
    else:
        # Calculate and return closest points possible
        m_closest = closes_points(points, m)
        return m_closest


''' Finds the closest points between the points of a list '''
@call_counter
def closes_points(points, m):

    # Prepare variables for search
    m_points = list()
    m_count = 0
    point_count = len(points)

    # Iterate for each possible combination of points
    for point_num in range(0, point_count):
        for distance_to in range(1 + point_num, point_count):

            # Calculate distance
            distance = math.sqrt(pow(points[point_num][0] - points[distance_to][0], 2) + pow(points[point_num][1] - points[distance_to][1], 2))

            # If there is no distance registered, add the first one as the smallest distance
            if m_count == 0:
                m_count = 1
                m_points.append((points[point_num], points[distance_to], distance))
            else:
                # Check registered distances and make sure it contains the minimum m distances
                for m_point_index in range(0, len(m_points)):

                    # If the new distance is smaller than one that is already in the closest list, insert it there
                    if distance < m_points[m_point_index][2]:
                        m_points.insert(m_point_index, (points[point_num], points[distance_to], distance))

                        # If we have exceeded the maximum number of closest (m) remove the largest distance registered
                        if m_count >= m:
                            m_points.pop()
                        break

                    # If there aren't yet m closest points add the newest distance as the largest
                    elif (m_count <= m) and (m_count == m_point_index+1):
                        m_points.append((points[point_num], points[distance_to], distance))
                        break

                # Count that we reached m closest points
                if m_count < m:
                    m_count = m_count + 1
    return m_points


''' Finds the closest points between two list of points '''
@call_counter
def middle_closest_pairs(left_points, right_points, m):

    # Prepare variables for search
    m_points = list()
    m_count = 0
    left_point_count = len(left_points)
    right_points_count = len(right_points)

    # Iterate for each possible combination of points between two lists
    for left_point_num in range(0, left_point_count):
        for right_point_num in range(0, right_points_count):

            # Calculate distance
            distance = math.sqrt(pow(left_points[left_point_num][0] - right_points[right_point_num][0], 2) + pow(left_points[left_point_num][1] - right_points[right_point_num][1], 2))

            # If there is no distance registered, add the first one as the smallest distance
            if m_count == 0:
                m_count = 1
                m_points.append((left_points[left_point_num], right_points[right_point_num], distance))
            else:
                # Check registered distances and make sure it contains the minimum m distances
                for m_point_index in range(0, m_count):

                    # If the new distance is smaller than one that is already in the closest list, insert it there
                    if distance < m_points[m_point_index][2]:
                        m_points.insert(m_point_index, (left_points[left_point_num], right_points[right_point_num], distance))

                        # If we have exceeded the maximum number of closest (m) remove the largest distance registered
                        if m_count >= m:
                            m_points.pop()
                        break

                    # If there aren't yet m closest points add the newest distance as the largest
                    if (m_count <= m) & (m_count == m_point_index+1):
                        m_points.append((left_points[left_point_num], right_points[right_point_num], distance))
                        break

                # Count that we reached m closest points
                if m_count < m:
                    m_count = m_count + 1
    return m_points

# This block should run your function and produce output that matches the input and output given in the Instructor
# Input Block and the sample data at the end of this assignment

M_closest = closestDistance(POINTS, M)


print("closest {}-{} pairs of points are: ".format(M, len(M_closest)))
for pair in M_closest:
    print("Points {} and {}, distance = {}".format(pair[0], pair[1], pair[2]))

import random
import math

# Data creation
x1_number_of_points = list()
y1_number_of_calls = list()
y1_assymtotic_time = list()
x2_changes_in_m = list()
y2_number_of_calls = list()
y2_assymtotic_time = list()

dummy = list()
dummy.append((random.random()*1000, random.random()*1000))

# May take a few seconds
m = 1
for quantity in range(1,1000):
    dummy.append((random.random()*1000, random.random()*1000))
    if (quantity % 50) == 0:
        x1_number_of_points.append(quantity)
        closests = closestDistance(dummy, m)
        y1_number_of_calls.append(closestDistance.calls + merge_sort.calls + merge.calls + closest_pairs.calls + closes_points.calls + middle_closest_pairs.calls)
        y1_assymtotic_time.append((quantity*math.log10(quantity)) + (m*math.log10(quantity)) + (m*math.pow(quantity, 2)*math.log10(quantity)))

for quantity in range(0,50):
    dummy.append((random.random()*1000, random.random()*1000))

for m_increment in range(0, 1000, 50):
    x2_changes_in_m.append(m+m_increment)
    closests = closestDistance(dummy, m+m_increment)
    y2_number_of_calls.append(closestDistance.calls + merge_sort.calls + merge.calls + closest_pairs.calls + closes_points.calls + middle_closest_pairs.calls)
    y2_assymtotic_time.append((50*math.log(50)) + ((m+m_increment)*math.log(50)) + ((m+m_increment)*math.pow(50, 2)*math.log(50)))