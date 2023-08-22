import numpy as np
import matplotlib.pyplot as plt


def runge_kuta(model, p_model, calculate_u, starting_conditions, t, parameters, broj_iteracija):

    solution = []

    dt = t[1] - t[0]  # Korak u vremenu

    for i in range(len(starting_conditions)):
        solution.append(np.zeros((1, len(t))))
        solution[i][0][0] = starting_conditions[i]

    u = np.zeros((1, len(t)))
    for iteracija in range(broj_iteracija):
        for i in range(1, len(t)):

            prethodno_stanje = []  # Poslednji članovi rešenja

            for s in solution:
                prethodno_stanje.append(s[0][i-1])

            k1 = model(prethodno_stanje[:int(len(prethodno_stanje)/2)], parameters, (u[0][i] + u[0][i-1])/2)
            apdejt_stanja = []
            for j in range(int(len(prethodno_stanje)/2)):
                apdejt_stanja.append(prethodno_stanje[j] + 0.5*k1[j] * dt)

            k2 = model(apdejt_stanja[:int(len(prethodno_stanje)/2)], parameters, (u[0][i] + u[0][i-1])/2)
            apdejt_stanja = []
            for j in range(int(len(prethodno_stanje)/2)):
                apdejt_stanja.append(prethodno_stanje[j] + 0.5 * k2[j] * dt)

            k3 = model(apdejt_stanja[:int(len(prethodno_stanje)/2)], parameters, (u[0][i] + u[0][i-1])/2)
            apdejt_stanja = []
            for j in range(int(len(prethodno_stanje)/2)):
                apdejt_stanja.append(prethodno_stanje[j] + 0.5 * k3[j] * dt)

            k4 = model(apdejt_stanja[:int(len(prethodno_stanje)/2)], parameters, (u[0][i] + u[0][i-1])/2)

            for j, s in enumerate(solution[:int(len(solution)/2)]):
                s[0][i] = s[0][i-1] + dt/6 * (k1[j] + 2*k2[j] + 2*k3[j] + k4[j])

        for i in range(1, len(t)):

            stanje = []
            for s in solution:
                stanje.append(s[0][-i])

            k1 = p_model(stanje, parameters, (u[0][- i] + u[0][-i+1])/2)
            apdejt_stanja = stanje[:int(len(stanje)/2)]
            for j in range(int(len(stanje)/2), len(stanje)):
                apdejt_stanja.append(stanje[j] + 0.5 * k1[j-int(len(stanje)/2)] * dt)

            k2 = p_model(apdejt_stanja, parameters, (u[0][- i] + u[0][-i+1])/2)
            apdejt_stanja = stanje[:int(len(stanje)/2)]
            for j in range(int(len(stanje) / 2), len(stanje)):
                apdejt_stanja.append(stanje[j] + 0.5 * k2[j-int(len(stanje)/2)] * dt)

            k3 = p_model(apdejt_stanja, parameters, (u[0][- i] + u[0][-i+1])/2)
            apdejt_stanja = stanje[:int(len(stanje) / 2)]
            for j in range(int(len(stanje) / 2), len(stanje)):
                apdejt_stanja.append(stanje[j] + 0.5 * k3[j - int(len(stanje) / 2)] * dt)

            k4 = p_model(apdejt_stanja, parameters, (u[0][- i] + u[0][-i+1])/2)
            k1 = np.array(k1)
            k2 = np.array(k2)
            k3 = np.array(k3)
            k4 = np.array(k4)

            aditiv = 1/6 * (k1 + 2*k2 + 2*k3 + k4)

            for j, s in enumerate(solution[int(len(solution)/2):]):
                s[0][-i-1] = s[0][-i] - aditiv[j]

        if not calculate_u:
            pass
        else:
            for i in range(len(t)):

                stanje_za_u = []
                for j, s in enumerate(solution):
                    stanje_za_u.append(s[0][i])

                u[0][i] = calculate_u(stanje_za_u, parameters)

    return solution[:int(len(solution)/2)], u[0]


def u_vakcina(stanje, parameters):

    beta, gamma, A1, A2, A3, C3, N = parameters[0], \
                                     parameters[1], \
                                     parameters[2], \
                                     parameters[3], \
                                     parameters[4], \
                                     parameters[5], \
                                     parameters[6]

    S, I, R, p1, p2, p3 = stanje[0], stanje[1], stanje[2], stanje[3], stanje[4], stanje[5]

    u_novo = (p1 * S - p3 * S) / (2 * C3 * N)
    if u_novo < 0:
        u_novo = 0
    elif u_novo > 0.1:
        u_novo = 0.1

    return u_novo


def u_lecenje(stanje, parameters):

    beta, gamma, A1, A2, A3, C2, N = parameters[0], \
                                     parameters[1], \
                                     parameters[2], \
                                     parameters[3], \
                                     parameters[4], \
                                     parameters[5], \
                                     parameters[6]

    S, I, R, p1, p2, p3 = stanje[0], stanje[1], stanje[2], stanje[3], stanje[4], stanje[5]

    u_novo = (p2 * I - p3 * I) / (2 * C2 * N)
    if u_novo < 0:
        u_novo = 0
    elif u_novo > 0.1:
        u_novo = 0.1

    return u_novo


def u_karantin(stanje, parameters):

    beta, gamma, A1, A2, A3, C1, N = parameters[0], \
                                     parameters[1], \
                                     parameters[2], \
                                     parameters[3], \
                                     parameters[4], \
                                     parameters[5], \
                                     parameters[6]

    S, I, R, p1, p2, p3 = stanje[0], stanje[1], stanje[2], stanje[3], stanje[4], stanje[5]

    u_novo = (p2 * beta * S * I - p1 * beta * S * I) / (2 * C1 * N)
    if u_novo < 0:
        u_novo = 0
    elif u_novo > 0.5:
        u_novo = 0.5

    return u_novo


def sirv_model(y, parameters, u):

    beta, gamma, A1, A2, A3, C3, N = parameters[0], \
                                     parameters[1], \
                                     parameters[2], \
                                     parameters[3], \
                                     parameters[4], \
                                     parameters[5], \
                                     parameters[6]

    S, I, R = y

    dSdt = -beta * S * I/N - u * S
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I + u * S

    return [dSdt, dIdt, dRdt]


def sirv_p_model(y, parameters, u):
    S, I, R, p1, p2, p3 = y
    beta, gamma, A1, A2, A3, C3, N = parameters[0], \
                                     parameters[1], \
                                     parameters[2], \
                                     parameters[3], \
                                     parameters[4], \
                                     parameters[5], \
                                     parameters[6]

    dp1dt = -(A1 - p1*beta*I - p1*beta*u + p2*I + p3*u)/N
    dp2dt = -(A2 - p1 * beta * S/N + p2 * beta * S/N - p2 * gamma + p3 * gamma)
    dp3dt = -A3
    return [dp1dt, dp2dt, dp3dt]


def sirl_model(y, parameters, u):

    beta, gamma, A1, A2, A3, C2, N = parameters[0], \
                                     parameters[1], \
                                     parameters[2], \
                                     parameters[3], \
                                     parameters[4], \
                                     parameters[5], \
                                     parameters[6]

    S, I, R = y

    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - u * I
    dRdt = u * I

    return [dSdt, dIdt, dRdt]


def sirl_p_model(y, parameters, u):
    S, I, R, p1, p2, p3 = y
    beta, gamma, A1, A2, A3, C2, N = parameters[0], \
                                     parameters[1], \
                                     parameters[2], \
                                     parameters[3], \
                                     parameters[4], \
                                     parameters[5], \
                                     parameters[6]

    dp1dt = -(A1 - p1*I*beta + p2*beta*I)/N
    dp2dt = -(A2 - p1 * beta * S/N + p2 * beta * S/N - p2 * u + p3 * u)
    dp3dt = -A3
    return [dp1dt, dp2dt, dp3dt]


def sirq_model(y, parameters, u):
    # Sa N delim jer je na takav način zgodno porediti više modela, pa čak i sa različitih brojeva populacije
    # Bez deljenja sa N se dobiju jako cudna resenja (Google kaže)
    beta, gamma, A1, A2, A3, C1, N = parameters[0], \
                                     parameters[1], \
                                     parameters[2], \
                                     parameters[3], \
                                     parameters[4], \
                                     parameters[5], \
                                     parameters[6]
    S, I, R = y
    dSdt = -(1-u)*beta*S*I/N
    dIdt = (1-u)*beta*S*I/N - gamma*I
    dRdt = gamma * I

    return [dSdt, dIdt, dRdt]


def sirq_p_model(y, parameters, u):
    S, I, R, p1, p2, p3 = y
    beta, gamma, A1, A2, A3, C1, N = parameters[0], \
                                     parameters[1], \
                                     parameters[2], \
                                     parameters[3], \
                                     parameters[4], \
                                     parameters[5], \
                                     parameters[6]
    dp1dt = -(A1 + I*(p2*(1-u)*beta - p1*(1-u)*beta))/N
    dp2dt = -(A2 - p1 * (1-u) * beta * S/N + p2 * (1 - u) * beta * S/N - p2 * gamma + p3 * gamma)
    dp3dt = -A3
    return [dp1dt, dp2dt, dp3dt]


def sir_model(y, t, N, beta, gamma):
    # Sa N delim jer je na takav način zgodno porediti više modela, pa čak i sa različitih brojeva populacije
    # Bez deljenja sa N se dobiju jako cudna resenja (Google kaže)

    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]


def prikaz_SIRU(t, S, I, R, u):

    plt.figure()

    plt.subplot(4, 1, 1)
    plt.plot(t, S, label="S")
    plt.title("Stanovnici podložni zarazi")
    plt.xlabel("Vreme")
    plt.ylabel("Broj stanovnika")
    plt.legend()

    plt.subplot(4, 1, 2)
    plt.plot(t, I, label="I")
    plt.title("Broj zaraženih stanovnika")
    plt.xlabel("Vreme")
    plt.ylabel("Broj stanovnika")
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.plot(t, R, label="R")
    plt.title("Broj oporavljenih (imunih) stanovnika")
    plt.xlabel("Vreme")
    plt.ylabel("Broj stanovnika")
    plt.legend()

    plt.subplot(4, 1, 4)
    plt.plot(t, u, label="U")
    plt.title("Upravljanje")
    plt.xlabel("Vreme")
    plt.ylabel("Upravljanje")
    plt.legend()


def prikaz_SIRU_plavo_crveno(t, S, I, R, Su, Iu, Ru, uu):

    plt.figure()

    plt.subplot(4, 1, 1)
    plt.plot(t, S, label="S")
    plt.plot(t, Su, 'r', label="S - vakcina")
    plt.title("Stanovnici podložni zarazi")
    plt.xlabel("Vreme")
    plt.ylabel("Broj stanovnika")
    plt.legend()

    plt.subplot(4, 1, 2)
    plt.plot(t, I, label="I")
    plt.plot(t, Iu, 'r', label="I - vakcina")
    plt.title("Broj zaraženih stanovnika")
    plt.xlabel("Vreme")
    plt.ylabel("Broj stanovnika")
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.plot(t, R, label="R")
    plt.plot(t, Ru, 'r', label="R - vakcina")
    plt.title("Broj oporavljenih (imunih) stanovnika")
    plt.xlabel("Vreme")
    plt.ylabel("Broj stanovnika")
    plt.legend()

    plt.subplot(4, 1, 4)
    plt.plot(t, uu, label="U", color='red')
    plt.title("Upravljanje")
    plt.xlabel("Vreme")
    plt.ylabel("Upravljanje")
    plt.legend()
    plt.subplots_adjust(hspace=0.5)
    plt.show()


def prikaz_crveno_plavo(t, bez_upravljanja, sa_upravljanjem, title):

    pik_bez_upravljanja = np.argmax(bez_upravljanja)
    pik_sa_upravljanjem = np.argmax(sa_upravljanjem)

    fig, ax = plt.subplots()

    ax.plot(t, bez_upravljanja, 'b', label='Bez upravljanja')
    ax.annotate(int(round(bez_upravljanja[pik_bez_upravljanja])),
                xy=(t[pik_bez_upravljanja], bez_upravljanja[pik_bez_upravljanja]),
                xycoords='data', xytext=(30, -30),
                textcoords='offset points', arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2"),
                color='black')
    ax.axvline(t[pik_bez_upravljanja], color='blue', linestyle='--', alpha=0.3)
    ax.plot(t, sa_upravljanjem, 'r', label='Sa upravljanjem')
    ax.annotate(int(round(sa_upravljanjem[pik_sa_upravljanjem])),
                xy=(t[pik_sa_upravljanjem], sa_upravljanjem[pik_sa_upravljanjem]),
                xycoords='data', xytext=(60, -20),
                textcoords='offset points', arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.4"),
                color='black')
    ax.axvline(t[pik_sa_upravljanjem], color='red', linestyle='--', alpha=0.3)
    plt.xlabel('Vreme')
    plt.ylabel('Broj stanovnika')
    plt.title(title)
    ax.legend()
    plt.show()


def karantin():

    N = 82965
    I0, R0 = 771, 59
    S0 = N - I0 - R0
    y0 = [S0, I0, R0]

    beta, gamma = 0.3238, 0.0487

    t = np.linspace(0, 121, 121)

    pocetni = [S0, I0, R0, 0, 0, 0]  # Poslednje tri nule su vrednosti za p1, p2 i p3 u krajnjem trenutku
    A1, A2, A3, C1 = -1, 1, 0, 0.5
    parametri = [beta, gamma, A1, A2, A3, C1, N]

    solution = runge_kuta(sirq_model, sirq_p_model, u_karantin, pocetni, t, parametri, 200)
    print(solution)
    prikaz_SIRU(t, solution[0][0][0], solution[0][1][0], solution[0][2][0], solution[1])
    solution_bez_u = runge_kuta(sirq_model, sirq_p_model, False, pocetni, t, parametri, 1)
    print(solution_bez_u)

    prikaz_SIRU(t, solution_bez_u[0][0][0], solution_bez_u[0][1][0], solution_bez_u[0][2][0], solution_bez_u[1])
    plt.show()
    prikaz_SIRU_plavo_crveno(t, solution_bez_u[0][0][0], solution_bez_u[0][1][0], solution_bez_u[0][2][0],
                             solution[0][0][0], solution[0][1][0], solution[0][2][0], solution[1])

    prikaz_crveno_plavo(t, solution_bez_u[0][0][0], solution[0][0][0], "S sa i bez karantina")
    prikaz_crveno_plavo(t, solution_bez_u[0][1][0], solution[0][1][0], "I sa i bez karantina")
    prikaz_crveno_plavo(t, solution_bez_u[0][2][0], solution[0][2][0], "R sa i bez karantina")


def lecenje():

    N = 82965
    I0, R0 = 771, 59
    S0 = N - I0 - R0
    y0 = [S0, I0, R0]

    beta, gamma = 0.3238, 0.0487

    t = np.linspace(0, 121, 121)

    pocetni = [S0, I0, R0, 0, 0, 0]  # Poslednje tri nule su vrednosti za p1, p2 i p3 u krajnjem trenutku
    A1, A2, A3, C1 = 0, 1.5, 0, 0.5
    parametri = [beta, gamma, A1, A2, A3, C1, N]

    solution = runge_kuta(sirl_model, sirl_p_model, u_lecenje, pocetni, t, parametri, 200)
    print(solution)
    prikaz_SIRU(t, solution[0][0][0], solution[0][1][0], solution[0][2][0], solution[1])

    solution_bez_u = runge_kuta(sirq_model, sirq_p_model, False, pocetni, t, parametri, 1)
    print(solution_bez_u)

    prikaz_SIRU(t, solution_bez_u[0][0][0], solution_bez_u[0][1][0], solution_bez_u[0][2][0], solution_bez_u[1])
    plt.show()
    prikaz_SIRU_plavo_crveno(t, solution_bez_u[0][0][0], solution_bez_u[0][1][0], solution_bez_u[0][2][0],
                             solution[0][0][0], solution[0][1][0], solution[0][2][0], solution[1])

    prikaz_crveno_plavo(t, solution_bez_u[0][0][0], solution[0][0][0], "S sa i bez lečenja")
    prikaz_crveno_plavo(t, solution_bez_u[0][1][0], solution[0][1][0], "I sa i bez lečenja")
    prikaz_crveno_plavo(t, solution_bez_u[0][2][0], solution[0][2][0], "R sa i bez lečenja")


def vakcina():

    N = 82965
    I0, R0 = 771, 59
    S0 = N - I0 - R0
    y0 = [S0, I0, R0]

    beta, gamma = 0.3238, 0.0487

    t = np.linspace(0, 121, 121)

    pocetni = [S0, I0, R0, 0, 0, 0]  # Poslednje tri nule su vrednosti za p1, p2 i p3 u krajnjem trenutku
    A1, A2, A3, C3 = 0, 10, 0, 0.5
    parametri = [beta, gamma, A1, A2, A3, C3, N]

    solution = runge_kuta(sirv_model, sirv_p_model, u_vakcina, pocetni, t, parametri, 200)
    print(solution)
    prikaz_SIRU(t, solution[0][0][0], solution[0][1][0], solution[0][2][0], solution[1])

    solution_bez_u = runge_kuta(sirv_model, sirv_p_model, False, pocetni, t, parametri, 1)
    print(solution_bez_u)

    prikaz_SIRU(t, solution_bez_u[0][0][0], solution_bez_u[0][1][0], solution_bez_u[0][2][0], solution_bez_u[1])
    plt.show()
    prikaz_SIRU_plavo_crveno(t, solution_bez_u[0][0][0], solution_bez_u[0][1][0], solution_bez_u[0][2][0],
                             solution[0][0][0], solution[0][1][0], solution[0][2][0], solution[1])

    prikaz_crveno_plavo(t, solution_bez_u[0][0][0], solution[0][0][0], "S sa i bez vakcine")
    prikaz_crveno_plavo(t, solution_bez_u[0][1][0], solution[0][1][0], "I sa i bez vakcine")
    prikaz_crveno_plavo(t, solution_bez_u[0][2][0], solution[0][2][0], "R sa i bez vakcine")


# karantin()
# lecenje()
vakcina()
