%% FANUC S-420i — Lagrangian dynamics
% M(q) from translational and rotational Jacobians;
% C(q,qdot) from Christoffel symbols; G(q) from potential energy.
% The report uses scalar link inertias and symbolic physical parameters.

clear; clc;
[q, a, d, alpha, theta] = fanuc_s420i_dh();

syms qd1 qd2 qd3 qd4 qd5 qd6 real
qdot = [qd1 qd2 qd3 qd4 qd5 qd6];
syms m1 m2 m3 m4 m5 m6 real
syms I1 I2 I3 I4 I5 I6 real
syms g0 real
m = [m1 m2 m3 m4 m5 m6];
I = [I1 I2 I3 I4 I5 I6];

Gdh = cell(1,6);
T0i = cell(1,6);
for k = 1:6
    Gdh{k} = dh_transform(theta(k), d(k), a(k), alpha(k));
    if k == 1
        T0i{k} = Gdh{k};
    else
        T0i{k} = simplify(T0i{k-1} * Gdh{k});
    end
end

O0 = sym([0;0;0]);
z0 = sym([0;0;1]);
z = cell(1,6);
O = cell(1,6);
for k = 1:6
    z{k} = simplify(T0i{k}(1:3,3));
    O{k} = simplify(T0i{k}(1:3,4));
end

Jv = cell(1,6);
Jw = cell(1,6);
for link = 1:6
    Jv_link = sym(zeros(3,6));
    Jw_link = sym(zeros(3,6));
    for joint = 1:link
        if joint == 1
            axis_j = z0;
            origin_j = O0;
        else
            axis_j = z{joint-1};
            origin_j = O{joint-1};
        end
        Jv_link(:,joint) = cross(axis_j, O{link} - origin_j);
        Jw_link(:,joint) = axis_j;
    end
    Jv{link} = simplify(Jv_link);
    Jw{link} = simplify(Jw_link);
end

M_trans = sym(zeros(6,6));
M_rot = sym(zeros(6,6));
for link = 1:6
    M_trans = M_trans + m(link)*(Jv{link}.'*Jv{link});
    M_rot = M_rot + I(link)*(Jw{link}.'*Jw{link});
end
M = simplify(expand(M_trans + M_rot));

C = sym(zeros(6,6));
for k = 1:6
    row_expression = sym(0);
    for i = 1:6
        for j = 1:6
            c_ijk = sym(1/2)*(diff(M(k,j),q(i)) + ...
                diff(M(k,i),q(j)) - diff(M(i,j),q(k)));
            row_expression = row_expression + c_ijk*qdot(i)*qdot(j);
        end
    end
    C(k,:) = jacobian(row_expression, qdot);
end
C = simplify(expand(C));

% Potential energy expressions transcribed from the report.
P1 = m1*g0;
P2 = m2*g0*(1 + 0.95*sin(q(2)));
P3 = m3*g0*(0.9*sin(q(3)) + 0.95*sin(q(2)) + 1);
P4 = m4*g0*(1.3*sin(q(3)) + 0.95*sin(q(2)) + 1);
P5 = m5*g0*(0.2*sin(q(5)) + 1.3*sin(q(3)) + 0.95*sin(q(2)) + 1);
P6 = m6*g0*(0.3*sin(q(5)) + 1.3*sin(q(3)) + 0.95*sin(q(2)) + 1);
P = simplify(P1 + P2 + P3 + P4 + P5 + P6);
Gvec = simplify(jacobian(P,q).');

save('fanuc_s420i_lagrange_symbolic.mat', 'M','C','Gvec','P','Jv','Jw');
disp('Mass matrix M(q):'); pretty(M);
disp('Coriolis/centrifugal matrix C(q,qdot):'); pretty(C);
disp('Gravity vector G(q):'); pretty(Gvec);
