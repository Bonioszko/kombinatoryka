import random
import copy
import itertools
import pandas as pd


def distance_graph_generate(distance_min, distance_max, n):
    # generowanie macierzy dystansu pomiedzy poszczególnymi punktami
    distances = []
    for i in range(n):
        distances.append([0]*n)
    for i in range(n-1):
        for j in range(i+1, n):
            distances[j][i] = distances[i][j] = random.randint(
                distance_min, distance_max)
    return distances

# wzor na obliczanie czasu przejazdu to s/v


def distance_from_base_generate(distance_min, distance_max, n):
    distances = []
    for i in range(n):
        distances.append(random.randint(distance_min, distance_max))
    return distances


def times_from_base_generate(distances, speed):
    times = copy.deepcopy(distances)
    n = len(distances)
    for i in range(n):
        times[i] = distances[i] / speed*60
    return times


def time_graph_generate(speed, distances):
    # generacja macierzy czasu potrzebnego na przejechanmie czas w godzinach,
    times = copy.deepcopy(distances)
    for i in range(len(distances)-1):
        for j in range(i+1, len(distances)):
            times[i][j] = times[j][i] = distances[i][j]/speed * 60

    return times


# czas będziemy podawać w minutach od rozpączecia dnia, pierwszy czas to poczatek dostęności, drugi to koniec, czyli np zakres(300,660) odpowiada dostępności w godzinach 5:00 do 11:00
# zeby algorymt mial szanse sie wykonac, to zakladamy, ze ktos jest w domu przez 500 min
def time_stamps_generate(n, min_time, max_time):
    time_stamps = []
    for i in range(n):
        time_stamps.append([0, 0])
    for i in range(n):
        a = random.randint(min_time, max_time)
        time_stamps[i][0] = a
        time_stamps[i][1] = a+500
    return time_stamps
# do generacji permutacji uzyjemy wbudowanej biblioteki pythopa
# tutaj brute force, który wygeneruje wszystkie możliwe rozwiązania i sprawdzi przy którym pokonamy najmniejszy dystanms (parametry to wszystkie grpahy które wygenerowalismy + start i koniec pracy )


# ten nie dziala
def brute_force_min_dist(base_times, base_distances, time_stamps, distances, times, start, end):
    n = len(time_stamps)
    best_road = [0]*n
    min_dist = 100000000
    work_time = end-start
    # generuje tutaj wszystkie mozliwe permutacje listy o dlugosci n
    iterations = list(itertools.permutations(list(range(n))))
    print(base_times, end="\n")
    print(base_distances, end="\n")

    for i in iterations:
        d = end
        dist = 0
        time = start
        time_stamps[i[0]][0]
        if time_stamps[i[0]][0] < start+base_times[i[0]] and time_stamps[i[0]][1] > start + base_times[i[0]]:

            dist += base_distances[i[0]]
            time += base_times[i[0]]
            for j in range(n-1):
                # dopisac mozliwość czekania przez ciezarowke
                if time_stamps[i[j+1]][0] > times[i[j]][i[j+1]]+time or time_stamps[i[j+1]][1] < times[i[j]][i[j+1]]+time:
                    continue
                dist += distances[i[j]][i[j+1]]
                time += times[i[j]][i[j+1]]
            dist += distances[i[-1]][i[0]]
            time += times[i[-1]][i[0]]
            dist += base_distances[i[-1]]
            time += base_times[i[-1]]
            if time > end:
                continue
            elif dist < min_dist:
                min_dist = dist
                best_road = i

    return min_dist, best_road


def brute_force_min_time(base_times, base_distances, time_stamps, distances, times, start, end):
    n = len(time_stamps)
    best_road = [0]*n
    min_dist = 100000000
    work_time = end-start
    min_time = 1000000
    # generuje tutaj wszystkie mozliwe permutacje listy o dlugosci n
    iterations = list(itertools.permutations(list(range(n))))
    print(base_times, end="\n")
    print(base_distances, end="\n")

    for i in iterations:
        d = end
        dist = 0
        time = start
        div_start = time_stamps[i[0]][0] - time - base_times[i[0]]
        if div_start > 0:
            time += div_start
        if time_stamps[i[0]][1] > start + base_times[i[0]]:

            dist += base_distances[i[0]]
            time += base_times[i[0]]
            for j in range(n-1):
                div = time_stamps[i[j+1]][0] - time - times[i[j]][i[j+1]]
                if div > 0:
                    time += div
                if time_stamps[i[j+1]][1] < times[i[j]][i[j+1]]+time:
                    continue
                dist += distances[i[j]][i[j+1]]
                time += times[i[j]][i[j+1]]
            dist += distances[i[-1]][i[0]]
            time += times[i[-1]][i[0]]
            dist += base_distances[i[-1]]
            time += base_times[i[-1]]
            if time > end:
                continue

            elif time-start < min_time:
                min_time = time-start
                best_road = i

    return min_time, best_road


def brute_force_min_dist2(base_times, base_distances, time_stamps, distances, times, start, end):
    n = len(time_stamps)
    best_road = [0]*n
    min_dist = 100000000
    work_time = end-start
    min_time = 1000000
    # generuje tutaj wszystkie mozliwe permutacje listy o dlugosci n
    iterations = list(itertools.permutations(list(range(n))))
    print(base_times, end="\n")
    print(base_distances, end="\n")

    for i in iterations:
        d = end
        dist = 0
        time = start
        div_start = time_stamps[i[0]][0] - time - base_times[i[0]]
        if div_start > 0:
            time += div_start
        if time_stamps[i[0]][1] > start + base_times[i[0]]:

            dist += base_distances[i[0]]
            time += base_times[i[0]]
            for j in range(n-1):
                div = time_stamps[i[j+1]][0] - time - times[i[j]][i[j+1]]
                if div > 0:
                    time += div
                if time_stamps[i[j+1]][1] < times[i[j]][i[j+1]]+time:
                    continue
                dist += distances[i[j]][i[j+1]]
                time += times[i[j]][i[j+1]]
            dist += distances[i[-1]][i[0]]
            time += times[i[-1]][i[0]]
            dist += base_distances[i[-1]]
            time += base_times[i[-1]]
            if time > end:
                continue

            elif dist < min_dist:
                min_dist = dist
                best_road = i

    return min_dist, best_road


def return_min_value_column(array, visited):
    index_min = 0
    min = 100000
    for i in range(len(array)):
        if array[i][0] < min and visited[i] == 0:
            index_min = i
            min = array[i][0]
    return index_min
# po wszystkich tych ktorzy sa najwczesniej dostępni, wyniki nawet maja sens


def shortest_time(base_times, base_distances, time_stamps, distances, times, start, end):
    n = len(distances)
    visited = [0]*n
    path = []
    dist = 0
    time = start
    x = 1
    current = 0
    start_time = 100000
    start_index = 10000
    for i in range(n):
        if start_time > time_stamps[i][0]:
            start_time = time_stamps[i][0]
            start_index = i
    div_start = time_stamps[start_index][0]-time-base_times[start_index]
    if div_start > 0:
        time += div_start
    # to nizej do wywalenia, ale dla testu niech teraz bedzie
    if time_stamps[start_index][1] < start + base_times[start_index]:
        print("zle algorytm")
    visited[start_index] = 1
    time += base_times[start_index]
    dist += base_distances[start_index]
    current = start_index
    # za chwile zobacze to na dole
    # while(len(path) < n):
    #     min = 1000000
    #     for i in range(n):
    #         if i == current:
    #             continue
    #         if time_stamps[i][0] < min and visited[i] == 0:
    for i in range(n):
        next = return_min_value_column(time_stamps, visited)
        visited[next] = 1
        dist += distances[current][next]
        time += times[current][next]
        path.append(current)
        current = next

    dist += base_distances[current]
    time += base_times[current]

    return dist, path


n = 8
speed = 100
distances = distance_graph_generate(2, 10, n)
times = time_graph_generate(20, distances)
time_stamps = time_stamps_generate(n, 200, 900)
# time_stamps = []
# for i in range(n):
#     time_stamps.append([100, 1200])
print(time_stamps)
base_distances = distance_from_base_generate(20, 50, n)
base_times = times_from_base_generate(base_distances, speed)

# print(list(itertools.permutations(list(range(n)))))
# print(distances)
# print(times)
# print(time_stamps)
print(distances)
distancesss, best_roadsss = brute_force_min_dist2(
    base_times, base_distances, time_stamps, distances, times, 100, 1440)
distances_sh_time, path_sh_time = shortest_time(
    base_times, base_distances, time_stamps, distances, times, 100, 1440)
print(distancesss)
print(best_roadsss)

print(distances_sh_time)
print(path_sh_time)
# dwa brute forcy zrobione teraz dopisac cos jeszcze jakies heurystyki czy cos
