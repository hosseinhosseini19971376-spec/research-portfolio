%% FANUC S-420i — recursive Newton-Euler dynamics
% Source formulation retained; physical masses and COM distances remain
% symbolic. The source does not provide full inertia tensors.

clear; clc;
N = 6;
a = [0; 0; 0.95; 0.24; 0; 0; 0];
d = [1; 0; 0; 1.3; 0; 0.2; 0];
alpha = [0; -pi/2; 0; pi/2; -pi/2; pi/2; 0];

syms q1 q2 q3 q4 q5 q6 real
q = [q1 q2 q3 q4 q5 q6];
theta = [q1, q2-pi/2, q3, q4, q5, q6, 0];

Gdh = cell(1,N+1);
for k = 1:N+1
    ct = cos(theta(k));
    st = sin(theta(k));
    ca = round(cos(alpha(k)));
    sa = round(sin(alpha(k)));
    Gdh{k} = [ct, -st, 0, a(k);
              st*ca, ct*ca, -sa, -sa*d(k);
              st*sa, ct*sa, ca, ca*d(k);
              0, 0, 0, 1];
end

Tzz = simplify(Gdh{1}*Gdh{2}*Gdh{3}*Gdh{4}*Gdh{5}*Gdh{6}*Gdh{7}); %#ok<NASGU>

syms qd1 qd2 qd3 qd4 qd5 qd6 real
syms qdd1 qdd2 qdd3 qdd4 qdd5 qdd6 real
syms L1 L2 L3 L4 L5 L6 real
syms m1 m2 m3 m4 m5 m6 real
syms g0 real

qdot = [qd1 qd2 qd3 qd4 qd5 qd6];
qdd = [qdd1 qdd2 qdd3 qdd4 qdd5 qdd6];
m = [m1 m2 m3 m4 m5 m6];
L = [L1 L2 L3 L4 L5 L6];

w = cell(1,N+1);
wdot = cell(1,N+1);
vdot = cell(1,N+1);
vc_dot = cell(1,N+1);
F = cell(1,N);
f = cell(1,N+1);
n = cell(1,N+1);
tau_link = cell(1,N);

w{1} = zeros(3,1);
wdot{1} = zeros(3,1);
vdot{1} = [0; g0; 0];
f{N+1} = zeros(3,1);
n{N+1} = zeros(3,1);

for k = 1:N
    Rk = Gdh{k}(1:3,1:3);
    pk = Gdh{k}(1:3,4);
    z_axis = [0;0;1];

    w{k+1} = Rk.'*w{k} + qdot(k)*z_axis;
    wdot{k+1} = Rk.'*wdot{k} + ...
        cross(Rk.'*w{k}, qdot(k)*z_axis) + qdd(k)*z_axis;
    vdot{k+1} = Rk.'*(vdot{k} + ...
        cross(wdot{k},pk) + cross(w{k},cross(w{k},pk)));

    com_vector = [L(k);0;0];
    vc_dot{k+1} = vdot{k+1} + ...
        cross(wdot{k+1},com_vector) + ...
        cross(w{k+1},cross(w{k+1},com_vector));
    F{k} = m(k)*vc_dot{k+1};
end

for k = N:-1:1
    Rk = Gdh{k}(1:3,1:3);
    pk = Gdh{k}(1:3,4);
    f{k} = F{k} + Rk*f{k+1};
    n{k} = Rk*n{k+1} + ...
        cross([L(k);0;0],F{k}) + cross(pk,Rk*f{k+1});
    tau_link{k} = n{k}.'*[0;0;1];
end

TAU = [tau_link{1}; tau_link{2}; tau_link{3}; ...
       tau_link{4}; tau_link{5}; tau_link{6}];
M = simplify(jacobian(TAU, qdd));
C = simplify(jacobian(TAU, qdot));
Gvec = simplify(subs(subs(TAU, qdot.', zeros(6,1)), qdd.', zeros(6,1)));

save('fanuc_s420i_newton_euler_symbolic.mat', 'TAU','M','C','Gvec');
disp('Generalized torque vector:'); pretty(TAU);
disp('Mass matrix M(q):'); pretty(M);
disp('Velocity-dependent matrix C(q,qdot):'); pretty(C);
disp('Gravity vector G(q):'); pretty(Gvec);
