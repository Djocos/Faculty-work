%% Tacka 3.

% Predložiti strukturu regulatora (P, PI, PD, PID) tako da sistem u zatvorenoj povratnoj
% sprezi bude stabilan i da greška u ustaljenom stanju bude nula. 
% Za koje vrednosti parametara regulatora ?e sistem biti stabilan? 
% Proveriti dobijene rezultate u simulaciji.

B = 5.28;
M = 0.264;
k = 2.64;
referenca = 70;
s = tf('s');

G_p = 8/(s + 8);
G_h = 1/(M*s^2 + B*s + k);

% Predložen regulator je PI, I dejstvo je neophodno 
% da bi greška u ustaljenom stanju bila 0 zbog neophodnog astatizma

% Routhovom metodom je zaklju?eno da je sistem stabilan za:

% Skripta racun_ki.m

% Nakon nekoliko simulacija, zaklju?ili smo da parametri koji ne daju
% preskok, relativno brzo ulaze u ustaljeno stanje, a daju stabilan odziv 
% su parametri predstavljeni ispod 


kp = 12;
ki = 5;

G_c = (kp*s + ki)/s;

%% Tacka 4.

T_u = 0.5;
K_u = 153.3296;
K_p = 1/k;

kp2 = 0.45 * K_u;
ki2 = 0.833 * T_u;



%% Tacka 6.
T = 0.001;