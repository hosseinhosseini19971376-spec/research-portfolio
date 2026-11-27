%% Hamiltonian LQR - unconstrained input
% Extracted from source paragraph range: 373-520.
% Original state-space, Riccati recursion, simulation, and cost calculation retained.

clc;
clear;
close all;
%%
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
Ts = 0.001;
Tf = 10;
t = 0:Ts:Tf ;
N = numel(t);
H = [1 0 0 0;0 2 0 0;0 0 3 0;0 0 0 4];
Q = [1 0 0 0;0 2 0 0;0 0 3 0;0 0 0 4];
R = [1 0;0 2];
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
A = [A11 A12;A21 A22];
B = [B11 B12;B21 B22];
K = zeros(4 , 4 , N);
K(:,:,N) = H ;
for i = N-1:-1:2
K(:,:,i-1) = K(: , : , i) + Ts*(Q -K(: , : , i)*B*R^(-1)*B'*K(: , : , i)+K(: , : , i)*A+A'*K(: , : , i)) ;
end
%%%%
K11 = K(1 ,1 ,:);
K12 = K(1,2,:);
K22 = K(2,2,:);
K11 = K11(:);
K12 = K12(:);
K22 = K22(:);
K33 = K(3,3,:);
K33 = K33(:);
K44 = K(4,4,:);
K44 = K44(:);
K13 = K(1,3,:);
K13 = K13(:);
K23 = K(2,3,:);
K23 = K23(:);
K34 = K(3,4,:);
K34 = K34(:);
K14 = K(1,4,:);
K14 = K14(:);
K24 = K(2,4,:);
K24 = K24(:);
plot(t ,K11, 'LineWidth' , 2);
grid on
hold on
plot(t ,K12, 'LineWidth' , 2);
grid on
hold on
plot(t ,K13, 'LineWidth' , 2);
grid on
hold on
plot(t ,K14, 'LineWidth' , 2);
grid on
hold on
plot(t ,K22, 'LineWidth' , 2);
grid on
hold on
plot(t ,K23, 'LineWidth' , 2);
grid on
hold on
plot(t ,K24, 'LineWidth' , 2);
grid on
hold on
plot(t ,K33, 'LineWidth' , 2);
grid on
hold on
plot(t ,K34, 'LineWidth' , 2);
grid on
hold on
plot(t ,K44, 'LineWidth' , 2);
grid on
legend('K11','K12','K13','K14','K22','K23','K24','K33','K34','K44')
xlabel('Iteration');
ylabel('K');
hold on
%%
x = zeros(4 , N) ; x(: , 1) = [1;-1;3;-3];
u = zeros(2 , N) ;
for i = 1:N-1
u(:,i) = -R^(-1)*B'*K(:,:,i)*x(: ,i);
x(: , i+1) = x(: , i) + Ts*(A*x(: , i) + B*u(:,i));
end
figure(2) ;
subplot(211);
plot(t ,x , 'LineWidth' , 2);
grid on
xlabel('Iteration');
ylabel('X');
legend('X1' , 'X2','X3' , 'X4')
subplot(212);
plot(t ,u , 'LineWidth' , 2);
grid on
xlabel('Iteration');
ylabel('U');
legend('u1','u2')
%%% cost
Jopt = x(1,end)^2+2* x(2,end)^2+3*x(3,end)^2+4*x(4,end)^2+ sum(x(1,:).^2 + 2*x(2,:).^2 +3*x(3,:).^2 +4*x(4,:).^2+u(1,:).^2+2*u(2,:).^2 )*Ts
