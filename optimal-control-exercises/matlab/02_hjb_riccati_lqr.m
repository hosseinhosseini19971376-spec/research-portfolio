%% HJB / Riccati LQR implementation extracted from the source DOCX
% Source paragraph range: 206-302.
% The original recursion and indexing are preserved; see EXTRACTION_NOTES.md.

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
P = zeros(4 , 4 , N);
P(:,:,N) = H ;
for k = N-1:-1:2
P(:,:,k-1) = P(: , : , k) + Ts*(Q -P(: , : , k)*B*R^(-1)*B'*P(: , : , k)+P(: , : , k)*A+A'*P(: , : , k)) ;
end
%%%%
P11 = P(1 ,1 ,:);
P12 = P(1,2,:);
P22 = P(2,2,:);
P11 = P11(:);
P12 = P12(:);
P22 = P22(:);
P33 = P(3,3,:);
P33 = P33(:);
P44 = P(4,4,:);
P44 = P44(:);
P13 = P(1,3,:);
P13 = P13(:);
P23 = P(2,3,:);
P23 = P23(:);
P34 = P(3,4,:);
P34 = P34(:);
P14 = P(1,4,:);
P14 = P14(:);
P24 = P(2,4,:);
P24 = P24(:);
%%
x = zeros(4 , N) ; x(: , 1) = [1;-1;3;-3];
u = zeros(2 , N) ;
for i = 1:N-1
u(:,i) = -R^(-1)*B'*P(:,:,i)*x(: ,i);
x(: , i+1) = x(: , i) + Ts*(A*x(: , i) + B*u(:,i));
end
figure(2) ;
subplot(211);
plot(t ,x , 'LineWidth' , 2);
grid on
xlabel('Iteration');
ylabel('X');
legend('X1' , 'X2')
subplot(212);
plot(t ,u , 'LineWidth' , 2);
grid on
xlabel('Iteration');
ylabel('U');
legend('U')
%%% cost
