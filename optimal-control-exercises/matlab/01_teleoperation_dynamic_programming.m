%% Teleoperation system - finite-horizon dynamic programming
% Extracted from "تمرینهای کنترل بهینه" (57-page DOCX).
% Source sections: Teleoperation model and dynamic-programming analysis.
% The A/B block assembly is written explicitly from the A11...B22 equations
% repeated later in the same source document.

clc;
clear;
close all;

%% Master/slave plant parameters (source values)
Jm = 1.5; bm = 11;
Js = 2; bs = 15;
ke = 100; be = 1;
kf = 0.1;
td = 0.1;
Km = [-192.71 -21.32];
Ks = [-227.25 -29.894];
Rs = [-13.157 -0.13];
G2 = 1.315;
Rm = [kf*ke kf*be];

Am = [0 1;0 -bm/Jm];
Bm = [0;1/Jm];
Cm = [1;0];
As = [0 1;0 -bs/Js];
Bs = [0;1/Js];
Cs = [1;0];

%% Simulation and cost matrices
Ts = 0.001;
Tf = 0.1;
t = 0:Ts:Tf;
N = numel(t);
H = [1 0 0 0;0 2 0 0;0 0 3 0;0 0 0 4];
Q = [1 0 0 0;0 2 0 0;0 0 3 0;0 0 0 4];
R = [1 0;0 2];

%% Delayed coupled state-space matrices
M = inv(eye(2) - td * td * Bm * (Rm + G2 * Ks) * Bs * Rs);
S = inv(eye(2) - td * td * Bs * Rs * Bm * (Rm + G2 * Ks));

A11 = M * (Am + Bm * Km - td * Bm * (Rm + G2 * Ks) * Bs * Rs);
A12 = M * (Bm * (Rm + G2 * Ks) - td * Bm * (Rm + G2 * Ks) * (As + Bs * Ks));
A21 = S * (Bs * Rs - td * Bs * Rs * (Am + Bm * Km));
A22 = S * (As + Bs * Ks - td * Bs * Rs * Bm * (Rm + G2 * Ks));
B11 = -M * td * Bm * (Rm + G2 * Ks) * Bs;
B12 = M * Bm;
B21 = S * Bs;
B22 = -S * td * Bs * Rs * Bm;

% Explicit assembly of the overall matrices (shown elsewhere in the source).
A = [A11 A12; A21 A22];
B = [B11 B12; B21 B22];

%% Backward dynamic-programming recursion
F = zeros(2, 4, N);
P = zeros(4, 4, N);
P(:,:,1) = H;

for k = 2:N-1
    F(:,:,N-k) = -(R + B'*P(:,:,k-1)*B)^(-1)*B'*P(:,:,k-1)*A;
    P(:,:,k) = (A + B*F(:,:,N-k))'*P(:,:,k-1)*(A + B*F(:,:,N-k)) ...
        + F(:,:,N-k)'*R*F(:,:,N-k) + Q;
end

%% Optional feedback-gain plotting (commented in the source)
% F1 = F(:,1,:); F1 = F1(:);
% F2 = F(:,2,:); F2 = F2(:);
% F3 = F(:,3,:); F3 = F3(:);
% F4 = F(:,4,:); F4 = F4(:);
% figure(1);
% plot(1:N,F1,1:N,F2,1:N,F3,1:N,F4,'LineWidth',2);
% grid on
% xlabel('Iteration');
% ylabel('F');
% legend('F1','F2','F3','F4');

%% Forward state and input simulation
x = zeros(4,N);
x(:,1) = [1;1;1;1];
u = zeros(2,N);

for i = 1:N-1
    u(:,i) = F(:,:,i)*x(:,i);
    x(:,i+1) = A*x(:,i) + B*u(:,i);
end

figure(2);
subplot(211);
plot(1:N,x,'LineWidth',2);
grid on
xlabel('Iteration');
ylabel('X');
legend('X1','X2','X3','X4');

subplot(212);
plot(1:N,u,'LineWidth',2);
grid on
xlabel('Iteration');
ylabel('U');
legend('U');

%% Optimal cost (source expression)
Jopt = 0.5*x(:,1)'*P(:,:,N-1)*x(:,1)
