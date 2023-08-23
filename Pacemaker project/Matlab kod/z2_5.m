% z2.5

%% P regulator - stabilan

P1 = 20;

%% P regulator - nestabilan

P1 = -11;

%% PI rekulator - stabilan, neoscilatoran

P2 = 200;
I = 5;

%% PI rekulator - stabilan, oscilatoran

P2 = 2;
I = ((10+P2)^2)/4 + 100; % može i manje od 100 ali se ne vidi lepo na scope
