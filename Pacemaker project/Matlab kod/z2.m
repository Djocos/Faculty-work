%% 2.1

fs = 500; % ws = 2 * 500 * pi a to je vece od 1500 * 2
t = 0:1/fs:10;
omega1 = 30;
omega2 = 1500;

signal = cos(omega1 * t) + sin(omega2 * t);

X = fft(signal);

f_osa = 0:fs/numel(X):fs-fs/numel(X);
f_osa = f_osa(1:int64(numel(f_osa)/2));
omega_osa = f_osa*2*pi;
X = X(1:int64(numel(X)/2));

figure

stem(omega_osa, abs(X))
xlabel('Kružna frekvencija [rad/s]')
title('Spektar signala: cos(30\pit) + sin(1500\pit)')

%% 2.3
% Rad ovog filtra je simuliran u simulinku, a izracunat na papiru. Za K
% dobijana je vrednost 35, ali se nakon nekoliko eksperimenata pokazalo da
% je za 45 odziv mnogo bolji

s = tf('s');
K = 45;
G = K * 1/(s+35);

figure
bode(G)

%% 2.3
w_max = 1500;
disp("Maksimalna frekvencija je 1500 rad/s, dakle maksimalna perioda odabiranja je:")

disp(((2*pi)/w_max)/2)
T_ok = 0.001;
T_not = 0.004;

t_ok = 0:T_ok:10;
t_not = 0:T_not:10;

omega1 = 30;
omega2 = 1500;

% Perioda odabiranja koja zadovoljava kriterijum
signal1 = cos(omega1 * t_ok) + sin(omega2 * t_ok);

X1 = fft(signal1);

w_osa = 0:(2*pi/T_ok)/numel(X1):2*pi/T_ok-(2*pi/T_ok)/numel(X1);

figure
subplot(211)
stem(w_osa, abs(X1))
xlabel('Kružna frekvencija [rad/s]')
title('Spektar signala: cos(30\pit) + sin(1500\pit), T = 0.001')
% Perioda odabiranja koja ne zadovoljava kriterijum
signal2 = cos(omega1 * t_not) + sin(omega2 * t_not);

X2 = fft(signal2);

w_osa = 0:(2*pi/T_not)/numel(X2):2*pi/T_not-(2*pi/T_not)/numel(X2);
subplot(212)
stem(w_osa, abs(X2))
xlabel('Kružna frekvencija [rad/s]')
title('Spektar signala: cos(30\pit) + sin(1500\pit), T = 0.004')

% Moze se primetiti da ako perioda odabiranja nije bar 2 puta manja od
% periode signala,dci ce do aliasing-a

