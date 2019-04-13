clear all, clc;
load('data.mat');
%% Init
exo = data{:, 1};
exo(isnan(exo)) = [];
no_exo = data{:, 2};
no_exo(isnan(no_exo)) = [];
t1 = data{:, 3};
t1(isnan(t1)) = [];
exo_ang = data{:, 4};
exo_ang(isnan(exo_ang)) = [];
t2 = data{:, 5};
t2(isnan(t2)) = [];
no_exo_ang = data{:, 6};
no_exo_ang(isnan(no_exo_ang)) = [];

%%
plot(exo_ang, (exo(end:-length(exo)/length(exo_ang):1)));
hold on
plot(no_exo_ang, (no_exo(end:-length(no_exo)/length(no_exo_ang):1)));

set ( gca, 'xdir', 'reverse' )
title("Exo vs No-Exo")
legend("Exo", "No-Exo")
xlabel("Elbow Angle \theta")
ylabel("EMG Amplitude")