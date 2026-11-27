%%
clc;
clear all;
close all;

%% Graphic
g = ncgr_graphic();

%% Scara robot DH-Parameters
global N_DOFS;
N_DOFS = 5;

theta = [0 0 0 0 0 0];
alpha = [-pi/2 0 pi/2 -pi/2 pi/2 0];
offset = [0 -pi/2 0 0 0 0];
a = [0 0.95 0.24 0 0];
d = [1 0  0 1.3 0 0];
type = ['r' 'r' 'r' 'r' 'r' 'r'];
base = [0; 0; 0];

scara = cgr_create(theta, d, a, alpha, offset, type, base);
scara = cgr_self_update(scara, [0 0 0 0 0 0]);
g = ncgr_plot(g, scara);

pause(1);
scara = cgr_self_update(scara, [0 0 0 -0.2 0 0]);
g = ncgr_plot(g, scara);

pause(1);
scara = cgr_self_update(scara, [0 0 0 0 0 0]);
g = ncgr_plot(g, scara);

%% Demo inverese kinematics
[q, k, err]= cgr_ikine1(scara, [-.2 -.2 -.2], 0.01, 100);
scara = cgr_self_update(scara, q);
g = ncgr_plot(g, scara);
pause(0.1);