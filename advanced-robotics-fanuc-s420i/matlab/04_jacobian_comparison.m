%% FANUC S-420i — geometric and differential Jacobian comparison
clear; clc;
[q, a, d, alpha, theta] = fanuc_s420i_dh();

G = cell(1,6);
T0i = cell(1,6);
for k = 1:6
    G{k} = dh_transform(theta(k), d(k), a(k), alpha(k));
    if k == 1
        T0i{k} = G{k};
    else
        T0i{k} = simplify(T0i{k-1} * G{k});
    end
end

T = simplify(T0i{6});
O_ee = simplify(T(1:3,4));
R = simplify(T(1:3,1:3));

z{1} = sym([0;0;1]);
O{1} = sym([0;0;0]);
for k = 1:5
    z{k+1} = simplify(T0i{k}(1:3,3));
    O{k+1} = simplify(T0i{k}(1:3,4));
end

% Method 1: geometric Jacobian, following the report's cross-product form.
Jv_method1 = sym(zeros(3,6));
Jw_method1 = sym(zeros(3,6));
for k = 1:6
    Jv_method1(:,k) = cross(z{k}, O_ee - O{k});
    Jw_method1(:,k) = z{k};
end
J_method1 = simplify([Jv_method1; Jw_method1]);

% Method 2: differentiate position and orientation.
Jv_method2 = simplify(jacobian(O_ee, q));
syms qd1 qd2 qd3 qd4 qd5 qd6 real
qdot = [qd1 qd2 qd3 qd4 qd5 qd6];

R_dot = sym(zeros(3,3));
for k = 1:6
    R_dot = R_dot + diff(R,q(k))*qdot(k);
end
S = simplify(R_dot * R.');
omega = simplify([S(3,2); S(1,3); S(2,1)]);
Jw_method2 = simplify(jacobian(omega, qdot));
J_method2 = simplify([Jv_method2; Jw_method2]);

difference = simplify(J_method1 - J_method2);
methods_match = isequal(difference, sym(zeros(6,6)));

disp('Geometric Jacobian:'); pretty(J_method1);
disp('Differential Jacobian:'); pretty(J_method2);
fprintf('The two symbolic methods match: %d\n', methods_match);

% Optional Peter Corke numerical cross-check:
% run('02_peter_corke_robot_model.m');
% q_num = zeros(1,6);
% J0_peter_corke = jacob0(Robot, q_num);
% Je_peter_corke = jacobe(Robot, q_num);
