from osum import read_raw
import matplotlib.pyplot as plt
import os
import numpy as np
from skimage.filters import threshold_otsu
from scipy.ndimage import sobel, gaussian_filter
from skimage.morphology import dilation, disk
from skimage.feature import match_template
from skimage.transform import rescale
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import random

# Oznake slika koje su se nalazile u folderu koji smo dobili kao skup podataka, True - ima implant/ False - nema implant
Y = [False, True, False, True, True, False, True, False, True, False, True, False, True, False, True, False, True, True,
     False, True, True, True, True, False, False, False, True, False, True, True, True, True, False, False, True, False]

data_folder = 'Data'  # Naziv foldera u kome su sirove slike
X = []  # skup svih slika iz foldera

# Ucitavanje slika iz foldera je ispod u ovoj for petlji
for filename in os.listdir(data_folder):
    filepath = os.path.join(data_folder, filename)
    if os.path.isfile(filepath):
        loaded = read_raw(filepath)

        im = loaded[0]

        im = rescale(im, scale=0.3)  # reskaliranje slike na 30% njenih originalnih dimenzija

        X.append(im)

# Podela na train skup 80% i na test skup 20%
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

#######################################################################################################################
#                                            Genetski algoritam
#######################################################################################################################


# Funkcija koja na svom izlazu da skup najboljih paramtetara kao i njihovu preciznost
def genetski_algoritam(pop_size, ranges, mutation_rate, mutation_widths, elitis_rate, convergence=10, non_converg=50):
    # pop_size je broj jedinki po generaciji
    # ranges su regioni svakog parametra u kojima se trazi optimalna vrednost
    # mutation rate je verovatnoca da ce se desiti mutacija
    # mutation_widths su zapravo maksimalne moguce promene svakog parametra
    # elitis_rate je procetnat najboljih jedinki iz prosle generacije koje ostaju do u sledecoj generaciji
    # convergence je potreban broj generacija sa istom uspesnosti da se algoritam yaustavi i proglasi pobednika
    # non_converg je potreban broj generacija posle kog algoritam proglsava pobendika i ako nije doslo do konvergencije

    last_best = 0
    counter = 0
    population = initialise_population(pop_size, ranges)
    big_counter = 0

    while True:

        print("------------------------------------------------------------------------------------------------------")
        print("                                                 {}.                  ".format(big_counter+1))
        print("------------------------------------------------------------------------------------------------------")
        if big_counter == non_converg:  # provera da li nije proslo prevse generacija bez konvergencije
            return last_best, population[0]
        else:
            big_counter += 1

        ranked, best_cost = rank_population(population)

        if last_best - 0.01 <= best_cost <= last_best + 0.02:  # provera konvergencije
            last_best = best_cost
            counter += 1
        else:
            last_best = best_cost
            counter = 0

        if counter == convergence:  # prekid u slucaju konvergencije
            preciznost = best_cost
            optimalni_parametri = ranked[0]
            return preciznost, optimalni_parametri

        # funkcije dole su opisane svaka na mestu gde je definisana
        pairs = roulette_selection(ranked)
        deca = ukurstanje(pairs)
        mutirani = mutation(deca, mutation_rate, mutation_widths)
        elita = elitis(population, mutirani, elitis_rate, pop_size)
        population = elita


def elitis(chromosomes_old, chromosomes_new, elitis_rate, population_size):
    # chromosomes_old, rangirane jedinke iz stare generacije
    # chromosomes_new, nove sparene jedinke
    # elitis_rate, procenat jedinki iz stare generacije
    # population_size, broj jedinki po generaciji

    old_ind_size = int(np.round(population_size * elitis_rate))
    # Vraca novu generaciju jedinki gde je ostao predefinisani procenat najboljih iz stare generacije
    return chromosomes_old[:old_ind_size] + chromosomes_new[:(population_size - old_ind_size)]


def mutation(chromosomes, mutation_rate, mutation_widths):
    # chromosomes, jedinke iz ukrstene jedinke koje mogu da podlegnu mutaciji
    # mutation_rate, verovatnoca mutacije, borj (0-1)
    # mutation_widths, maksimalna promena vrednosti svaog parametra, lista 7 vrednosti

    mutated_chromosomes = []
    for chromosome in chromosomes:
        y = []
        for i in range(0, len(chromosome)):
            if random.random() < mutation_rate:  # da li se desava mutacija
                r = random.random()

                y.append(chromosome[i] + mutation_widths[i] * 2 * (r - 0.5))  # promena vrednosti za parametre
            else:
                y.append(chromosome[i])  # ako nema mutacije vrati se ista jedinka

        mutated_chromosomes.append(y)
    # Vraca generaciju dece jedinki koje su mozda mutirani
    return mutated_chromosomes


def ukurstanje(pairs):

    # pairs je lista parova jedinki

    deca = []

    for a, b in pairs:

        r = random.random()  # tacka preseka izmedju dva roditelja (koje dete ce cije gene vise da nasledi)
        y1 = []
        y2 = []
        for i in range(len(a)):
            y1.append(r * a[i] + (1 - r) * b[i])
            y2.append((1 - r) * a[i] + r * b[i])
        deca.append(y1)
        deca.append(y2)

    # Za svaki par se dobije po dvoje dece cime se osigurava konstantna velicina populacije
    return deca


def roulette_selection(parents):

    # Funkcija koja formira parove jedinki na osnovu ruletske selekcije. Prima rangirane jedinke, svakoj jedinki je
    # dodeljen njen redni broj (najboljoj jedinki se dodeljuje najveci broj), koji se mnozi sa random brojem (0-1).
    # Nakon toga se nadju dve jednike sa dva najbolja broja i idu u ukrstanje. Ovo se ponavlja dok se ne formira
    # broj jedinki/2 parova
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

        for k in range(2, len(parents)):
            if weights[k] > weights[max_ind1]:
                max_ind2 = max_ind1
                max_ind1 = k
            elif weights[k] > weights[max_ind2]:
                max_ind2 = 1
        pairs.append([parents[max_ind1], parents[max_ind2]])

    return pairs


def rank_population(population):

    # Funkcija koja vraca sortirane jedinke na osnovu njihovog fitnessa i pored toga govori koji je najbolji fitness

    costs = []
    for i, individual in enumerate(population):
        print("[{}/{}]".format(i+1, len(population)))  # Posto je dugotrajno, pokazuje napredak u trenutnoj generaciji
        cost = cost_function(individual)
        costs.append(cost)

    population_with_costs = list(zip(population, costs))

    # Sort the population based on fitness in descending order
    population_with_costs.sort(key=lambda x: x[1], reverse=True)
    best_cost = max(costs)

    # Extract the ranked population
    ranked_population = [individual for individual, _ in population_with_costs]
    print("Najbolja jedinka iz ove iteracije je: {}\n"
          "Njen score je: {}".format(ranked_population[0], best_cost))
    return ranked_population, best_cost


def initialise_population(pop_size, ranges):

    # Funkcija koja formira pocetnu populaciju, prima velicinu generacije i opsege u kojima se se mogu naci vrednosti
    # svakog parametra

    population = []

    for chromosome in range(pop_size):
        individual = []
        for opseg in ranges:
            parameter_value = random.uniform(opseg[0], opseg[1])
            individual.append(parameter_value)
        population.append(individual)

    print("Populacija inicijalizovana")

    return population

# Opssezi za koje je pusten genetski algoritam
# opsezi = [[2, 6], [1, 2], [200, 400], [2, 5], [2, 5], [2, 15], [0.01, 0.1]]


def cost_function(chromosome):

    # Funkcija koja racuna uspesnost date jedinke (skupa parametara)

    # chromosome[0] - red korena koji primenjujem na piksele (inicijalizovati na 4)
    # chromosome[1] - multiplayer za prag tamnosti, inicijalizovati na 1.2
    # chromosome[2] - velicina kvadrata u kome se trazi tamni deo, inicijalizovati na 300
    # chromosome[3] - sigma for unsharp inicijalizovati na 3
    # chromosome[4] - strength for unsharp inicijalizovati na 3
    # chromosome[5] - velicina diska za dilataciju, inicijalizovati na 5
    # chromosome[6] - procenat true piksela na u kruznoj masci, inicijalizovati na 0.015

    true_values = y_train  # tacne vrednosti sa kojima se uporedjuje rezultat

    prediction = []

    for img in x_train:

        im = img

        tamna_maska = create_dark_mask(im ** (1 / chromosome[0]), chromosome[1], round(chromosome[2]))

        otsu_mask = find_region_with_steep_edge(im**(1/chromosome[0]), chromosome[3], chromosome[4],
                                                round(chromosome[5]))

        kombinacija = otsu_mask & tamna_maska

        rez = postojanje(kombinacija, create_circle_mask(im), chromosome[6])

        prediction.append(rez)

    # Preciznost je bitnija od tacnosti za ono sto se trazi, ali se tacnost ne sme ignorisati

    matrica_konfuzije = confusion_matrix(true_values, prediction)

    tp = matrica_konfuzije[1, 1]
    tn = matrica_konfuzije[0, 0]
    fp = matrica_konfuzije[0, 1]
    fn = matrica_konfuzije[1, 0]

    tacnost = (tp + tn)/len(prediction)

    if tacnost >= 0.6:
        print("Tacnost zadovoljenja: {}".format(tacnost))
        preciznost = tp / (tp + fp)
        print("Prciznost je onda: {}".format(preciznost))
    else:
        print("Tacnost nezadovoljena: {}. To se mnozi sa 0.5.".format(tacnost))
        return tacnost * 0.5

    return preciznost


#######################################################################################################################
#                                                   Obrada slike
#######################################################################################################################

def postojanje(image, mask, threshold=0.015):

    # Funkcija koja proverava procenat true piksela na osnovu kog odredjuje da li na slici ima ili nema implanta

    broj_svih = np.sum(mask)

    if np.sum(image[mask]) >= broj_svih * threshold:
        return True

    return False


def create_circle_mask(image):
    # Funkcija koja kreira kruznu masku na sred slike u kojoj se trazi implant
    height, width = image.shape[:2]
    circle_radius = min(height, width) // 2.5
    circle_center = (width // 2, height // 2)

    y, x = np.ogrid[:height, :width]
    mask = ((x - circle_center[0]) ** 2 + (y - circle_center[1]) ** 2 <= circle_radius ** 2)

    return mask


def unsharp_mask(image, sigma=3, strength=3):

    # Funkcija koja vraca sliku sa pojacanim ivicama pomocu metode unsharp masking
    # (ispostavilo se da nije dobro raditi ovo)

    image = image.astype(np.float32)

    blurred = gaussian_filter(image, sigma)
    high_pass = image - blurred
    enhanced = image + strength * high_pass
    enhanced = np.clip(enhanced, 0, 255)
    enhanced = enhanced.astype(np.uint8)

    return enhanced


def dilate(image, disk_size=5):

    # Prosirivanje detektovane ivice pomocu morfoloske dilatacije

    dilated_image = dilation(image, footprint=disk(disk_size))

    return dilated_image


def contrast(im):

    # Ekvalizacija histograma

    contrasted = ((im-np.min(im))/(np.max(im)-np.min(im)) * 255).astype(np.uint8)

    return contrasted


def find_region_with_steep_edge(image, sigma=3, strength=3, disk_size=5):

    # Funkcija koja vraca binarnu masku ivica uz pomoc sobelovog postupka uz otsuovu metodu trazenja praga

    gray = unsharp_mask(contrast(image.copy()), sigma, strength)/255
    gradient_magnitude = np.hypot(sobel(gray, axis=0), sobel(gray, axis=1))
    threshold = threshold_otsu(gradient_magnitude)

    binary_mask = gradient_magnitude < threshold

    dark_objects_mask = np.logical_not(binary_mask)

    morphology_mask = dilate(dark_objects_mask, disk_size)

    return morphology_mask


def create_dark_mask(im, multiplajer=1.2, square_size=300):

    # Funkcija koja vraca binarnu masku na mestima gde su najtamnije regij, a otseca ivice jer na ivicama se cesto
    # nalazi crni okvir (stitnik od zracenja)

    image = contrast(im)
    height, width = image.shape[:2]
    # trazenje najtamnijeg piksela samo u kvadratu koji iseca centralni kvadrat
    top = (height - square_size) // 2
    bottom = top + square_size
    left = (width - square_size) // 2
    right = left + square_size
    square_region = image[top:bottom, left:right]

    darkest_pixel = np.min(square_region)
    threshold = darkest_pixel * multiplajer

    mask = np.where(image < threshold, 1, 0)

    return mask


def draw_red_square(image_array, binary_mask_array):

    # Funkcija koja trazi trazi mesto implanta i oznacava ga crvenim kvadratom na slici

    true_pixels_indices = np.where(binary_mask_array == 1)
    # Pravljenje granica kvadtata vv
    min_x = np.min(true_pixels_indices[1])
    max_x = np.max(true_pixels_indices[1])
    min_y = np.min(true_pixels_indices[0])
    max_y = np.max(true_pixels_indices[0])

    image_rgb = np.stack((image_array, image_array, image_array), axis=-1)

    # Crtanje crvenog kvadrata
    image_rgb[min_y:max_y, min_x:max_x, 0] = 255
    plt.imshow(image_rgb, cmap='gray')
    plt.axis('off')
    plt.show()


def prikazi_slike(chromosome, slike):

    # Funkcija koja prikazuje medjukorakre ya svaku od prosledjenih slika, prima parametre za sve hunkcije i listu slika
    # chromosome[0] - red korena koji primenjujem na piksele (inicijalizovati na 4)
    # chromosome[1] - multiplayer za prag tamnosti, inicijalizovati na 1.2
    # chromosome[2] - velicina kvadrata u kome se trazi tamni deo, inicijalizovati na 300
    # chromosome[3] - sigma for unsharp inicijalizovati na 3
    # chromosome[4] - strength for unsharp inicijalizovati na 3
    # chromosome[5] - velicina diska za dilataciju, inicijalizovati na 5
    # chromosome[6] - procenat true piksela na u kruznoj masci, inicijalizovati na 0.015

    prediction = []

    for img in slike:

        im = img

        fig, axs = plt.subplots(1, 4, figsize=(15, 5))

        # Prikaz originalne slike (uradjen je 4. koren da vi se bolje videla struktura)

        axs[0].imshow(im ** (1 / 4), cmap='gray')
        axs[0].set_title('Rendgenska slika **(1/4)')

        # Prikaz binarne maske koja se dobija nakon pregovanja

        tamna_maska = create_dark_mask(im ** (1 / chromosome[0]), chromosome[1], round(chromosome[2]))

        axs[1].imshow(tamna_maska, cmap='gray')
        axs[1].set_title('Pragovano')

        # Prikaz binarne maske koja se dobija nakon detekcije ivice

        otsu_mask = find_region_with_steep_edge(im ** (1 / chromosome[0]), chromosome[3], chromosome[4],
                                                round(chromosome[5]))
        axs[2].imshow(otsu_mask, cmap='gray')
        axs[2].set_title('Otsu')

        # Kombinovanje prethodne dve binarne maske i kružne maskeu kojoj se traži implant

        kombinacija = otsu_mask & tamna_maska

        rez = postojanje(kombinacija, create_circle_mask(im), chromosome[6])
        axs[3].imshow(kombinacija & create_circle_mask(im), cmap='gray')
        axs[3].set_title('Resenje na osnovu koga se odlucuje')

        prediction.append(rez)
        print("Ova slika je predviđena kao: {}".format(rez))
        plt.show()

        # Ako je klasfikovano kao da ima implanta, crtanje crvenog kvadrata preko njega
        if rez:
            draw_red_square(im ** (1 / 4), kombinacija & create_circle_mask(im))


def rezultat(chromosome, slike, izlazi):
    # chromosome[0] - red korena koji primenjujem na piksele (inicijalizovati na 4)
    # chromosome[1] - multiplayer za prag tamnosti, inicijalizovati na 1.2
    # chromosome[2] - velicina kvadrata u kome se trazi tamni deo, inicijalizovati na 300
    # chromosome[3] - sigma for unsharp inicijalizovati na 3
    # chromosome[4] - strength for unsharp inicijalizovati na 3
    # chromosome[5] - velicina diska za dilataciju, inicijalizovati na 5
    # chromosome[6] - procenat true piksela na u kruznoj masci, inicijalizovati na 0.015

    true_values = izlazi

    prediction = []

    for img in slike:

        im = img

        tamna_maska = create_dark_mask(im ** (1 / chromosome[0]), chromosome[1], round(chromosome[2]))

        otsu_mask = find_region_with_steep_edge(im ** (1 / chromosome[0]), chromosome[3], chromosome[4],
                                                round(chromosome[5]))

        kombinacija = otsu_mask & tamna_maska

        rez = postojanje(kombinacija, create_circle_mask(im), chromosome[6])

        prediction.append(rez)
        print("Ova slika je predvi]ena kao: {}".format(rez))

    matrica_konfuzije = confusion_matrix(true_values, prediction)

    tp = matrica_konfuzije[1, 1] # True posotive
    tn = matrica_konfuzije[0, 0] # True negative
    fp = matrica_konfuzije[0, 1] # False positive
    fn = matrica_konfuzije[1, 0] # False negative

    tacnost = (tp + tn)/len(prediction)

    preciznost = tp / (tp + fp)

    print("Tacnost algoritma na datom skupu je: {}%\n"
          "Preciznost algoritma na datom skupu je: {}%\n"
          "-------------------------------------------\n"
          "Odnos pravih pozitiva i laznih pozitiva je'\n"
          "Pravi pozitivi : Lazni pozitivi\n"
          "    {:.2f}%     :      {:.2f}%      ".format(tacnost*100, preciznost*100, tp*100/(tp+fn), fp*100/(tn+fp)))
    print(matrica_konfuzije)


def detekcija_implanta(chromosome, data_folder="Data"):

    slike = []
    # Otvaranje foldera i preuzimanje svake slike iz njega, pretvaranje u numpy format, reskaliranje na 30% veličine
    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)
        if os.path.isfile(filepath):
            loaded = read_raw(filepath)

            im = loaded[0]

            im = rescale(im, scale=0.3)
            slike.append(im)

    prediction = []
    # Klasifikacija svake od učitanih slika
    for im in slike:

        fig, axs = plt.subplots(1, 4, figsize=(15, 5))
        axs[0].imshow(im ** (1 / 4), cmap='gray')
        axs[0].set_title('Rendgenska slika **(1/4)')

        tamna_maska = create_dark_mask(im ** (1 / chromosome[0]), chromosome[1], round(chromosome[2]))

        axs[1].imshow(tamna_maska, cmap='gray')
        axs[1].set_title('Pragovano')

        otsu_mask = find_region_with_steep_edge(im ** (1 / chromosome[0]), chromosome[3], chromosome[4],
                                                round(chromosome[5]))
        axs[2].imshow(otsu_mask, cmap='gray')
        axs[2].set_title('Otsu')

        kombinacija = otsu_mask & tamna_maska

        axs[3].imshow(kombinacija & create_circle_mask(im), cmap='gray')
        axs[3].set_title('Resenje na osnovu koga se odlucuje')

        plt.show()

        rez = postojanje(kombinacija, create_circle_mask(im), chromosome[6])
        prediction.append(rez)

    return prediction # Vraca matricu sa izlazima iz klasifikacije redom kojim su slike ucitane (Abecedno)


# Zakomentarisan kod je koriscen za pokretanje genetskog algoritma kako bi se nasli optimalni parametri

"""pop_size = 30
ranges = [[2, 6], [0.5, 2], [50, 300], [2, 10], [2, 10], [2, 15], [0.01, 0.1]]
mutation_rate = 0.2
mutation_widths = [2, 0.3, 25, 1.5, 1.5, 2, 0.009]
elitis_rate = 0.1

preciznost, optimalni_parametri = genetski_algoritam(pop_size, ranges, mutation_rate, mutation_widths, elitis_rate)

print("#############################################################################################################")
print("Dobijeni su najbolji parametri: \n"
      "{}".format(optimalni_parametri))
print("Dobijeni parametri rade sa preciznoscu: {}".format(preciznost))"""

# Parametri dobijeni iz GA
best_param = [5.899515074617773, 1.6015800732679997, 232.90019708993964, 7.482168056966877, 8.65930248822951,
              6.211205942723931, 0.0206465461321652]

# Todo kod ispod ovoga se pokreće za dobijanje performansi algoritma
# rezultat(best_param, x_test, y_test)

#  Todo kod ispod ovoga se pokreće kako bi se prikazali rezultati međukoraka kao i slike na osnovu koje se zaključilo
# prikazi_slike(best_param, x_train)

# Todo kod ispod ovoga se pokreće kao finalni produkt, vraca samo true ili false

print(detekcija_implanta(best_param, data_folder="Nova slika"))
