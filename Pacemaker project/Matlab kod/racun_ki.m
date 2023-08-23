% Racun za ki

B = 5.28;
M = 0.264;
k = 2.64;
% Jednacina ispod je dobijena iz c1
koreni = roots([64*M (64*M*k - 64*B^2 - 8*B*k - 512*B*M) -1*(64*B*B + 8*B*k*k + 512*B*M*k)]);
disp('Opseg u kome se kp moze nalaziti je:')
disp(koreni)
% Posto su korani prvog prvog clana (kvadratna jednacina) 153.3296 i
% -1.5296 drugi clan po apsolutnoj vrednosti mora biti manji od prvog za svako kp iz ovog opsega, a
% posto je drugi clan uvek negativan, kp se mora uvek uzeti iz navedenog
% opsega
kp = 153;

prvi_clan = 64*B*B + 8*B*k*k + 512*B*M*k - 64*M*kp*k + 64*B*B*kp + 8*B*k*kp + 512*B*M*kp - 64*M*kp*kp;

drugi_clan = 8*B*B + 128*B*M + 512*M*M;

ki = prvi_clan/drugi_clan;
disp('Maksimalno ki za dato kp:')
disp(ki)
disp('kp za koje se dobija maksimalno moguce ki u sistemu:')
kp_za_max_ki = sum(koreni)/2;
disp(kp_za_max_ki)

kp_osa = -1.5296:0.01:153.3296;
ki_osa = (64*B*B + 8*B*k*k + 512*B*M*k - 64*M*kp_osa*k + 64*B*B*kp_osa + 8*B*k*kp_osa + 512*B*M*kp_osa - 64*M*kp_osa.^2)/(8*B*B + 128*B*M + 512*M*M);

figure, plot(kp_osa, ki_osa, 'linewidth', 2)
title('Prikaz maskimalnog moguceg ki za izabrano kp')
xlabel('Izabrano kp')
ylabel('Maksimalno ki')