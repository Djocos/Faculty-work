import pandas as pd
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def create_gantt_chart(schedule, jobs, machines, za_bojenje):
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
              "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    plt.figure(figsize=(10, 6))
    plt.title("Gantt Chart")

    y_labels = ["Machine {}".format(i+1) for i in range(len(schedule))]
    y_pos = [i for i in range(len(schedule))]
    plt.yticks(y_pos, y_labels)

    legends = []
    jobs_passed = []
    for i, sch in enumerate(schedule):

        job_color_index = 0
        machine_counter = 0
        job_index = 0
        for p, process in enumerate(sch):
            job_color_index = za_bojenje[i][p]

            plt.barh(i, process[1]-process[0], left=process[0], height=0.3,
                     color=colors[job_color_index-1], edgecolor='black')

            if job_color_index not in jobs_passed:
                legends.append(Patch(facecolor=colors[job_color_index-1], label='Job {}'.format(job_color_index)))
                jobs_passed.append(job_color_index)

    plt.legend(handles=sorted(legends, key=lambda x: x.get_label()))
    plt.show()


def elitis(chromosomes_old, old_costs, chromosomes_new, new_costs, elitis_rate):
    parents, old_costs_ranked = rank_chromosomes(chromosomes_old, old_costs)
    kids, new_costs_ranked = rank_chromosomes(chromosomes_new, new_costs)

    index = int(round(len(chromosomes_old)*elitis_rate))
    new_generation = parents[:index] + kids[:(len(chromosomes_old)-index)]
    return new_generation


def mutation(kids, probability_of_mutation, data, machines):

    muted_chromosoms = []

    for kid in kids:
        prob = random.random()
        if probability_of_mutation >= prob:
            operations = kid[0].copy()
            kid_machines = kid[1].copy()
            choice = round(random.random())
            if choice == 0:  # Mutacija operacija, a masine se podesavaju tako da bude moguci niz
                mutation_index = random.randint(0, len(operations)-2)
                switch1 = operations[mutation_index]
                switch2 = operations[mutation_index+1]
                operations[mutation_index] = switch2
                operations[mutation_index+1] = switch1  # zamenjena mesta

                count_of_switched1 = 0
                count_of_switched2 = 0

                for i in range(mutation_index+2):
                    if operations[i] == switch1:
                        count_of_switched1 += 1
                    elif operations[i] == switch2:
                        count_of_switched2 += 1

                for info in data:
                    if info["Job"] == operations[mutation_index]:
                        if info["Operation"] == count_of_switched2:
                            lastings = info["Lasting"]
                            while True:
                                machine = random.choice(machines)
                                index = int(machine[1:]) - 1
                                if lastings[index] > 0:
                                    kid_machines[mutation_index] = machine
                                    break
                    if info["Job"] == operations[mutation_index + 1]:
                        if info["Operation"] == count_of_switched1:
                            lastings = info["Lasting"]
                            while True:
                                machine = random.choice(machines)
                                index = int(machine[1:]) - 1
                                if lastings[index] > 0:
                                    kid_machines[mutation_index + 1] = machine
                                    break

                muted_chromosoms.append([operations, kid_machines])

            else:  # Mutacija samo masine
                mutation_index = random.randint(0, len(kid_machines) - 1)
                count_of_operation = 0
                for i in range(mutation_index + 1):
                    if operations[i] == operations[mutation_index]:
                        count_of_operation += 1

                for info in data:
                    if info["Job"] == operations[mutation_index]:
                        if info["Operation"] == count_of_operation:
                            lastings = info["Lasting"]
                            while True:
                                machine = random.choice(machines)
                                index = int(machine[1:]) - 1
                                if lastings[index] > 0:
                                    kid_machines[mutation_index] = machine
                                    break
                muted_chromosoms.append([operations, kid_machines])
        else:
            muted_chromosoms.append(kid)
    return muted_chromosoms


def crossover(pairs, unique_jobs_list, point_percentage=0.6):
    """Ova funkcija vrsi ukrstanje u jednoj tacki, posebno za redosled operacija, a posebno za masine. Prilikom
    ukrštanja kod operacija, odredi se tačka gde će se ukrstiti (inicijalno 60%). Prvo dete je u prvih 60% isto kao
    roditelj 1 a u ostalih 40% se kombinuju neizvršene operacije na osnovu redosleda od roditelja 2. Ista logika
    se primenjuje i za dete 2. Kod ukrštanja mašina se takođe na dete 1 prepisuje prvih 60% od roditelja 1, a za
    ostalih 40% se gleda koja je operacija u pitanju, pa se od roditelja 2 prepisuje mašina za tu operaciju."""

    specifications = []  # Koliko puta treba da se pojavi konkretan posao

    for unique in sorted(unique_jobs_list):
        specifications.append(np.sum(unique == np.array(pairs[0][0][0])))

    deca = []

    for pair in pairs:

        r1 = pair[0]
        r2 = pair[1]

        index_of_crossing = math.ceil(point_percentage*len(r1[0]))

        d1_o = r1[0][:index_of_crossing]
        d1_m = r1[1][:index_of_crossing]

        d2_o = r2[0][:index_of_crossing]
        d2_m = r2[1][:index_of_crossing]

        for operation in r2[0]:
            if np.sum(np.array(d1_o) == operation) < specifications[operation - 1]:
                d1_o.append(operation)

                operation_no = d1_o.count(operation)
                counter = 0
                index = 0
                for i in range(len(r2[0])):
                    if r2[0][i] == operation:
                        counter += 1
                    if counter == operation_no:
                        index = i
                        break
                d1_m.append(r2[1][index])

        for operation in r1[0]:
            if np.sum(np.array(d2_o) == operation) < specifications[operation - 1]:
                d2_o.append(operation)

                operation_no = d2_o.count(operation)
                counter = 0
                index = 0
                for i in range(len(r1[0])):
                    if r1[0][i] == operation:
                        counter += 1
                    if counter == operation_no:
                        index = i
                        break
                d2_m.append(r1[1][index])

        deca.append([d1_o, d1_m])
        deca.append([d2_o, d2_m])

    return deca


def roulette_selection(parents):  # TODO mozda ubaciti i funkciju za neku drugu selekciju pa uporediti performanse
    pairs = []
    for i in range(0, len(parents), 2):

        weights = []
        for j in range(len(parents)):
            weights.append((len(parents) - j) * random.random())
        if weights[0] >= weights[1]:
            max_ind1 = 0
            max_ind2 = 1
        else:
            max_ind1 = 1
            max_ind2 = 0

        for j in range(2, len(parents)):
            if weights[j] > weights[max_ind1]:
                max_ind2 = max_ind1
                max_ind1 = j
            elif weights[j] > weights[max_ind2]:
                max_ind2 = 1
        pairs.append([parents[max_ind1], parents[max_ind2]])

    return pairs


def rank_chromosomes(chromosomes, costs):

    ranked = sorted(list(zip(chromosomes, costs)), key=lambda c: c[1])

    return list(zip(*ranked))  # prvi argument su rangirani hromozomi a drugi rangirana trajanja


def provera_ispravnosti(schedule):

    """Samo selfcheck da li je dobro napravljen schedule, tj da nema negde da se preklapaju termini"""
    results = []
    for machine in schedule:
        concatenated = sum(machine, [])
        result = all(concatenated[i] <= concatenated[i + 1] for i in range(len(concatenated) - 1))
        results.append(result)

    return all(results)


def get_costs(chromosoms, data, machines, no_jobs):
    """Vreaća listu čij je svaki element jedna lista koja u sebi sadrži vremenski raspored operacija po mašinama,
    što čini prvi element, dok je drugi element ukupna dužina trajanja procesa"""

    lista_za_bojenje = []
    output = []

    for ch in chromosoms:
        schedule, za_bojenje_grafika = calculate_cost(ch, data, machines, no_jobs)
        concatenated_schedule = sum(sum(schedule, []), [])
        cost = max(concatenated_schedule)
        output.append([schedule, cost])
        lista_za_bojenje.append(za_bojenje_grafika)

    return output, lista_za_bojenje


def arrange_workshop(lasting, index, current_job, last_points, checkpoints, jobs_za_bojenje):
    """Raspoređuje zadatke optimalno tako da ima najmanje praznog hoda"""

    if len(last_points) == 1:
        last_points = last_points[0]
    if len(checkpoints[index]) == 0:  # Ako masina nema jos zadataka
        if last_points[current_job] == 0:
            checkpoints[index].append([0, lasting])
            last_points[current_job] = lasting
            jobs_za_bojenje[index].append(current_job+1)
        else:
            checkpoints[index].append([last_points[current_job], last_points[current_job] + lasting])
            last_points[current_job] += lasting
            jobs_za_bojenje[index].append(current_job + 1)

    elif len(checkpoints[index]) < 2:
        if last_points[current_job] == 0:
            if checkpoints[index][0][0] >= lasting:
                checkpoints[index].insert(0, [0, lasting])
                last_points[current_job] = lasting
                jobs_za_bojenje[index].insert(0, current_job + 1)
            else:
                checkpoints[index].append([checkpoints[index][0][1], checkpoints[index][0][1] + lasting])
                last_points[current_job] = checkpoints[index][0][1] + lasting
                jobs_za_bojenje[index].append(current_job + 1)
        else:
            if last_points[current_job] + lasting <= checkpoints[index][0][0]:
                checkpoints[index].insert(0, [last_points[current_job], last_points[current_job] + lasting])
                last_points[current_job] += lasting
                jobs_za_bojenje[index].insert(0, current_job + 1)
            elif last_points[current_job] <= checkpoints[index][0][1]:
                checkpoints[index].append([checkpoints[index][0][1], checkpoints[index][0][1] + lasting])
                last_points[current_job] = checkpoints[index][0][1] + lasting
                jobs_za_bojenje[index].append(current_job + 1)
            else:
                checkpoints[index].append([last_points[current_job], last_points[current_job] + lasting])
                last_points[current_job] = last_points[current_job] + lasting
                jobs_za_bojenje[index].append(current_job + 1)
    else:
        try:
            for j in range(1, len(checkpoints[index]) + 1):
                if (checkpoints[index][j][0] - checkpoints[index][j - 1][1] >= lasting and
                        last_points[current_job] + lasting <= checkpoints[index][j][0]):
                    if checkpoints[index][j - 1][1] >= last_points[current_job]:
                        checkpoints[index].insert(j, [checkpoints[index][j - 1][1],
                                                      checkpoints[index][j - 1][1] + lasting])
                        last_points[current_job] = checkpoints[index][j - 1][1] + lasting
                        jobs_za_bojenje[index].insert(j, current_job + 1)
                        break
                    else:
                        checkpoints[index].insert(j, [last_points[current_job],
                                                      last_points[current_job] + lasting])
                        last_points[current_job] = last_points[current_job] + lasting
                        jobs_za_bojenje[index].insert(j, current_job + 1)
                        break
        except IndexError:
            if checkpoints[index][len(checkpoints[index])-1][1] >= last_points[current_job]:
                checkpoints[index].append([checkpoints[index][len(checkpoints[index])-1][1],
                                           checkpoints[index][len(checkpoints[index])-1][1] + lasting])
                last_points[current_job] = checkpoints[index][len(checkpoints[index])-1][1]
                jobs_za_bojenje[index].append(current_job + 1)
            else:
                checkpoints[index].append([last_points[current_job],
                                           last_points[current_job] + lasting])
                last_points[current_job] += lasting
                jobs_za_bojenje[index].append(current_job + 1)
    return last_points, checkpoints, jobs_za_bojenje


def calculate_cost(chromosom, data, machines, no_jobs):

    last_points = np.zeros((1, no_jobs))
    checkpoints = []
    za_bojenje = []

    for i in range(len(machines)):
        checkpoints.append([])
        za_bojenje.append([])

    index = 0  # Ovo samo da mi se python ne zali
    lasting = 0  # I ovo isto
    operation_counter = np.ones((1, no_jobs))
    for i in range(len(chromosom[0])):
        job = chromosom[0][i]
        machine = chromosom[1][i]

        # Uzimanje podatka o trajanju operacije na konkretnoj masini
        for info in data:
            if int(info["Job"]) == int(job):
                if int(info["Operation"]) == operation_counter[0][job - 1]:
                    lastings = info["Lasting"]
                    index = int(machine[1:]) - 1
                    lasting = lastings[index]
                    operation_counter[0][job - 1] += 1
                    break
        last_points, checkpoints, za_bojenje = arrange_workshop(lasting, index, job-1, last_points,
                                                                        checkpoints, za_bojenje)

    return checkpoints, za_bojenje


def generate_initial_chromosomes(jobs, machines, data, unique_jobs, pop_size):
    chromosoms = []
    for i in range(pop_size):

        jobs = random.sample(jobs, len(jobs))

        operation_counter = np.ones((1, len(unique_jobs)))
        machine_schedule = []

        for job in jobs:

            for info in data:
                if int(info["Job"]) == int(job):
                    if int(info["Operation"]) == operation_counter[0][job-1]:
                        lastings = info["Lasting"]
                        while True:
                            machine = random.choice(machines)
                            index = int(machine[1:])-1
                            if lastings[index] > 0:
                                machine_schedule.append(machine)
                                break
                        operation_counter[0][job-1] += 1
                        break

        chromosoms.append([jobs, machine_schedule])
    return chromosoms


def handle_job_list(job_list):

    df = pd.read_csv(job_list)

    jobs = df['Jobs'].to_list()
    machines = df.columns.to_list()
    machines.remove("Jobs")
    machines.remove("Operation")

    data = []
    for i in range(df.shape[0]):
        dic = {"Job": df["Jobs"][i],
               "Operation": df["Operation"][i],
               "Lasting": df[machines].loc[i].to_list()}
        data.append(dic)
    unique_jobs = df['Jobs'].unique()
    return jobs, machines, data, unique_jobs


def check_schedule(costs):

    # Provera ispravnosti formiranja schedule i deljenje na posebne skupove --------------------------------------------
    test = []
    schedules = []
    fitness_values = []
    for co in range(len(costs)):
        r = provera_ispravnosti(costs[co][0])
        schedules.append(costs[co][0])
        fitness_values.append(costs[co][1])

        test.append(r)

    if all(test):
        print("ISPRAVNO formirani schedule-i!")
    else:
        print("Something went wrong....")

    return schedules, fitness_values


def genetic_algorithm(pop_size, mutation_probability, elitis_rate, konvergencija=20, csv="job_list.csv"):

    generation_counter = 0
    convergence_counter = 0
    last_best_fitness = np.inf
    chromosomes, machines, data, unique_jobs, no_jobs = [], [], [], [], 0
    best_schedule = []

    while convergence_counter != konvergencija:
        if generation_counter == 0:
            # Ucitavanje podataka iz tabele i obrada tako da odgovara koriscenju u kodu
            jobs, machines, data, unique_jobs = handle_job_list(csv)
            no_jobs = len(unique_jobs)

            # Formiranje prve generacije
            chromosomes = generate_initial_chromosomes(jobs, machines, data, unique_jobs, pop_size)
        costs, za_bojenje_grafika = get_costs(chromosomes, data, machines, no_jobs)
        print("PROVERA NOVE GENERACIJE")
        schedules, fitness_values = check_schedule(costs)

        # Rangiranje hromozoma po duzini trajanja citavog procesa
        parents, fitness_values = rank_chromosomes(chromosomes, fitness_values)

        # Kreiranje parova rulet selekcijom i formiranje novih jedinki ukrstanjem
        parovi = roulette_selection(parents)
        deca = crossover(parovi, unique_jobs)

        # Mutacija odredjenih novonastalih jedinki na odredjeni nacin
        mutirana_deca = mutation(deca, mutation_probability, data, machines)
        costs_mut, za_bojenje_grafika = get_costs(mutirana_deca, data, machines, no_jobs)
        print("PROVERA GENERACIJE NAKON MUTACIJE")
        schedules_mut, fitness_values_mut = check_schedule(costs_mut)

        # Elitizam
        hope_generation = elitis(parents, fitness_values, mutirana_deca, fitness_values_mut, elitis_rate)

        # Provera
        hope_costs, za_bojenje_grafika = get_costs(hope_generation, data, machines, no_jobs)
        print("PROVERA GENERACIJE NAKON ELITIZMA")
        schedules_hope, fitness_values_hope = check_schedule(hope_costs)
        hope_generation_ranked, fitness_values_hope_ranked = rank_chromosomes(hope_generation, fitness_values_hope)

        chromosomes = hope_generation_ranked


        generation_counter += 1
        print("#######################################################################################################")
        print("Gneracija: {}".format(generation_counter))
        print("Najbolji hromozom iz generacije:")
        print(chromosomes[0])
        print("Njegov fitness je: {}".format(fitness_values_hope_ranked[0]))
        print("A schedule:")
        print(schedules_hope[0])
        print("#######################################################################################################")

        if fitness_values_hope_ranked[0] == last_best_fitness:
            convergence_counter += 1
        last_best_fitness = fitness_values_hope_ranked[0]
        best_schedule = schedules_hope[0]
    hope_costs, za_bojenje_grafika = get_costs(chromosomes, data, machines, no_jobs)

    create_gantt_chart(best_schedule, chromosomes[0][0], chromosomes[0][1], za_bojenje_grafika[0])


def isprobavanje():

    job_list_csv = "job_list.csv"
    jobs, machines, data, unique_jobs = handle_job_list(job_list_csv)
    pop_size = 1000
    no_jobs = len(unique_jobs)
    chromosomes = generate_initial_chromosomes(jobs, machines, data, unique_jobs, pop_size)
    print("Izgled jednog hromozoma: ")
    print(chromosomes[0])

    costs, za_bojenje_grafika = get_costs(chromosomes, data, machines, no_jobs)
    print("Izgled jednog schedule-a sa njegovim fitnessom: ")
    print(costs[0])

    # Provera ispravnosti formiranja schedule i deljenje na posebne skupove --------------------------------------------
    schedules, fitness_values = check_schedule(costs)
    cudan = [[[3, 3, 3, 1, 3, 4, 1, 2, 1, 2, 3, 1, 4, 4, 2, 4], ['M3', 'M4', 'M4', 'M1', 'M4', 'M3', 'M3', 'M2', 'M4', 'M1', 'M2', 'M4', 'M2', 'M1', 'M1', 'M4']],
             [[3, 2, 4, 4, 3, 1, 1, 4, 2, 1, 4, 2, 3, 1, 3, 3], ['M4', 'M1', 'M2', 'M3', 'M1', 'M1', 'M3', 'M3', 'M2', 'M1', 'M1', 'M4', 'M4', 'M1', 'M1', 'M2']]]
    costs, za_bojenje_grafika = get_costs(cudan, data, machines, no_jobs)
    create_gantt_chart(costs[0][0], cudan[0][0], cudan[0][1], za_bojenje_grafika[0])
    print("Fitnesi prve generacije:")
    print(fitness_values)

    parents, fitness_values = rank_chromosomes(chromosomes, fitness_values)
    parovi = roulette_selection(parents)

    deca = crossover(parovi, unique_jobs)
    print("\n"
          "Primer jednog deteta: ")
    print(deca[0])
    # Provera ispravnosti formiranja schedule i deljenje na posebne skupove --------------------------------------------

    costs, za_bojenje_grafika = get_costs(deca, data, machines, no_jobs)
    schedules, fitness_values = check_schedule(costs)
    print("Izgled jednog schedule-a sa njegovim fitnessom: ")
    print(costs[0])

    mutirana_deca = mutation(deca, 0.1, data, machines)
    print("Prikaz dece dobijene ukurstanjem i dece nakon mutacije (ako ispod pise True, nije se desila mutacija na"
          "ta dva hromozoma)")
    print(deca[:2])
    print(mutirana_deca[:2])
    print(deca[:2] == mutirana_deca[:2])

    costs, za_bojenje_grafika = get_costs(mutirana_deca, data, machines, no_jobs)
    schedules, fitness_values = check_schedule(costs)


# isprobavanje()
genetic_algorithm(100, 0.1, 0.1)
