%%
n1 = (NoLoad{305:501,1} - 20) > 0;
n1 = n1.*(NoLoad{305:501,1} - 20);
n2 = (NoLoad{506:650,1} - 20) > 0;
n2 = n2.*(NoLoad{506:650,1} - 20);
n3 = (NoLoad{692:845,1} - 20) > 0;
n3 = n3.*(NoLoad{692:845,1} - 20);
n = NoLoad{2444:2671,1};
figure(1)
plot(n2, 'Linewidth', 3)
hold on
plot(n, 'Linewidth', 3)
title("No Load Elbow Movement")
xlabel("Number of data points")
ylabel("EMG Amplitude")
legend("With Exoskeleton", "No Exoskeleton")

%%
figure(2)
l1 = (Load{2874:3162,1} - 20) > 0;
l1 = l1.*(Load{2874:3162,1} - 20);
l = Load{85:639,1};
plot(l1, 'Linewidth', 3)
hold on
plot(l, 'Linewidth', 3)
title("2 kg Load Elbow Movement")
xlabel("Number of data points")
ylabel("EMG Amplitude")
legend("With Exoskeleton", "No Exoskeleton")