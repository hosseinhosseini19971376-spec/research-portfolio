%% FANUC S-420i — symbolic forward kinematics
clear; clc;
[q, a, d, alpha, theta] = fanuc_s420i_dh();

N = 6;
G = cell(1,N);
for k = 1:N
    G{k} = dh_transform(theta(k), d(k), a(k), alpha(k));
end

T01 = simplify(G{1});
T02 = simplify(G{1}*G{2});
T03 = simplify(T02*G{3});
T04 = simplify(T03*G{4});
T05 = simplify(T04*G{5});
T06 = simplify(T05*G{6});

T = simplify(T06);
R_ee = simplify(T(1:3,1:3));
O_ee = simplify(T(1:3,4));

disp('End-effector homogeneous transform T = ');
pretty(T);
disp('End-effector position O_ee = ');
pretty(O_ee);
disp('End-effector orientation R_ee = ');
pretty(R_ee);
