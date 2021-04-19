"# IntroToAlgorithmPs" 

1. **function** get_fastest_tour(TRAVEL_TIME):
1. $~~~~$ L = lighthouse_names(TRAVEL_TIME) // Get a list of lighthouses from lighthouse distance map
1. $~~~~$ bestTour = **array** size L // Used to store the running best overall tour that starts at start_light
1. $~~~~$ bestTime = -1 // Used to store the time for the best_tour sequence
1. $~~~~$ travelHistory is a global empty map  // Set up a global map to remember recursive results
1. $~~~~$ 
1. $~~~~$ // If the number of lighthouses is less than 1 then there isn't a tour since there is no travel done 
1. $~~~~$ **if** L.length <= 1 **then**  
1. $~~~~$$~~~~$ **return** L, 0 
1. $~~~~$ 
1. $~~~~$ // Check times when you start at every lighthouse that exists
1. $~~~~$ **for** starting_lighthouse in L **do** 
1. $~~~~$$~~~~$ L_minus = L **with removed** starting_lighthouse
1. $~~~~$$~~~~$ tour, time = fastest_tour(starting_lighthouse, L_minus)
1. $~~~~$$~~~~$ **if** bestTime < 0 **or** time < bestTime **then** // See which full tour was the fastest one
1. $~~~~$$~~~~$$~~~~$ bestTour = tour
1. $~~~~$$~~~~$$~~~~$ bestTime = time
1. $~~~~$ **return** bestTour, bestTime
1.
1. **function** fastest_tour(x, L): 
1. $~~~~$ bestTour = **array** size L // Used to store the running best overall tour that starts at start_light
1. $~~~~$ bestTime = -1 // Used to store the time for the best_tour sequence
1. $~~~~$ 
1. $~~~~$ // BASE CASE: Having only one target and one L means that we only have one best tour
1. $~~~~$ **if** L.length == 1 **then**
1. $~~~~$$~~~~$ best_time = travel_time(x, L[0])
1. $~~~~$$~~~~$ best_tour = [x, L[0]]
1. $~~~~$$~~~~$ return best_tour, best_time
1. $~~~~$ 
1. $~~~~$ // RECURSIVE : We have multiple paths we can still take
1. $~~~~$ **else** 
1. $~~~~$$~~~~$ best_arrival = Null // Stores which lighthouse destination is better
1. $~~~~$$~~~~$ **for** arrival_light in L **do** // Iterate to each destination and get their fastest tour 
1. $~~~~$$~~~~$$~~~~$ L_minus = L **with removed** arrival_light
1. $~~~~$$~~~~$$~~~~$   
1. $~~~~$$~~~~$$~~~~$ // If we have not seen this destination and sublist pair, generate it then store the result
1. $~~~~$$~~~~$$~~~~$ **if** arrival_light with L_minus **not in** travelHistory **then**
1. $~~~~$$~~~~$$~~~~$$~~~~$ tour, time = fastest_tour(arrival_light, L_minus)
1. $~~~~$$~~~~$$~~~~$$~~~~$ **Add** arrival_light with L_minus result **in** travelHistory
1. $~~~~$$~~~~$$~~~~$
1. $~~~~$$~~~~$$~~~~$ // We have already a result for this destination and sublist pair so we use it.
1. $~~~~$$~~~~$$~~~~$ **else**
1. $~~~~$$~~~~$$~~~~$$~~~~$ tour, time = arrival_light with L_minus result **from** travelHistory
1. $~~~~$$~~~~$$~~~~$
1. $~~~~$$~~~~$$~~~~$ // Check if the resulting tour is better than ones previously found
1. $~~~~$$~~~~$$~~~~$ **if** best_time < 0 **or** 
1. $~~~~$$~~~~$$~~~~$   (time + travel_time(start_light, arrival_light)) <
1. $~~~~$$~~~~$$~~~~$       (best_time + travel_time(start_light, best_arrival)) **then**
1. $~~~~$$~~~~$$~~~~$$~~~~$ best_time = time
1. $~~~~$$~~~~$$~~~~$$~~~~$ best_tour = tour
1. $~~~~$$~~~~$$~~~~$$~~~~$ best_arrival = arrival_light
1. $~~~~$$~~~~$
1. $~~~~$$~~~~$ // Update the best time and tour to give back a result containing the starting lighthouse
1. $~~~~$$~~~~$ **Insert** start_light **in front** of best_tour
1. $~~~~$$~~~~$ best_time += travel_time(x, best_arrival)
1. $~~~~$$~~~~$ **return** best_tour, best_time
1.
1. **function** travel_time(lighthouse1, lighthouse2): 
1. $~~~~$ **Retrieve** TRAVEL_TIME
1. $~~~~$ **return** **Get** distance between lighthouse1 and lighthouse2 **from** TRAVEL_TIME


1. **function** nearest_neighbor(L): // Takes list of lighthouses L
1. $~~~~$ bestTour = **array** size L // Used to store the running best overall tour that starts at start_light
1. $~~~~$ bestTime = -1 // Used to store the time for the best_tour sequence
1. $~~~~$ // If the number of lighthouses is less than 1 then there isn't a tour since there is no travel done 
1. $~~~~$ **if** L.length <= 1 **then**  
1. $~~~~$$~~~~$ **return** 0, L 
1. $~~~~$ 
1. $~~~~$ // Check times when you start at every lighthouse that exists
1. $~~~~$ **for** starting_lighthouse in L **do** 
1. $~~~~$$~~~~$ L_minus = L **with removed** starting_lighthouse
1. $~~~~$$~~~~$ time, tour = get_greedy_path(starting_lighthouse, L_minus)
1. $~~~~$$~~~~$ **if** bestTime < 0 **or** time < bestTime **then** // See which full tour was the fastest one
1. $~~~~$$~~~~$$~~~~$ bestTour = tour
1. $~~~~$$~~~~$$~~~~$ bestTime = time
1. $~~~~$ **return** bestTime, bestTour

1. **function** get_greedy_path(start_light, L):  
1. $~~~~$ **if** L.length <= 0 **then**  // Base Case 1: There are no other lighthouses to travel to.
1. $~~~~$$~~~~$ **return** 0, L
1. $~~~~$ **if** L.length == 1 **then**  // Base Case 2: There is only one lighthouse to travel to.
1. $~~~~$$~~~~$ **return** distance from current to L[0], [current, L[0]] 
1. $~~~~$ shortest // Closest lighthouse to start
1. $~~~~$ **for** next_lighthouse in L **do** // Recursive Case: Find closest lighthouse
1. $~~~~$$~~~~$ **if** shortest is empty **do**
1. $~~~~$$~~~~$$~~~~$ shortest = next_lighthouse
1. $~~~~$$~~~~$ **else if** distance from current to shortest > distance from current to next_lighthouse **do**
1. $~~~~$$~~~~$$~~~~$ shortest = next_lighthouse
1. $~~~~$ // Recursively find the next lighthouse after shortest
1. $~~~~$ time, tour = get_greedy_path(shortest, list_minus(L, shortest)) 
1. $~~~~$
1. $~~~~$ // Add current lighthouse to tour
1. $~~~~$ tour.insert(0, current) 
1. $~~~~$ time = time + travel_time(current, shortest) 
1. $~~~~$ **return** time, tour

1. **function** monte_carlo(m, n):
1. $~~~~$ TRAVEL_TIME = {} // Preparing travel time variable
1. $~~~~$ counter = 0, result = list()
1. $~~~~$ **while** counter < m **do**
1. $~~~~$$~~~~$ TRAVEL_TIME = random_lighthouses(n) // Create a random set of lighthouses size n
1. $~~~~$$~~~~$ LIGHTS = lighthouse_names(TRAVEL_TIME) // Get lighthouse names
1. $~~~~$$~~~~$ bruteforce_time, tour = get_fastest_tour_faster(LIGHTS)
1. $~~~~$$~~~~$ nearneigh_time, tour = nearest_neighbor(LIGHTS)
1. $~~~~$$~~~~$ diffpct = abs(nearneigh_time - bruteforce_time) / bruteforce_time // Calculate difference
1. $~~~~$$~~~~$ result.append(diffpct) // Save result
1. $~~~~$$~~~~$ counter = counter + 1
1. $~~~~$ **return** result

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