%% FANUC S-420i — Peter Corke Robotics Toolbox model
% Follows the Link([theta d a alpha]) definitions and limits in the report.
% The source comments call links 2 and 3 prismatic, but the shown
% constructors do not explicitly request prismatic joints. See notes.

clear; clc;

L(1) = Link([0, 1.0, 0, -pi/2]);
L(1).qlim = [0, 2*pi];

L(2) = Link([0, 0, 0.95, 0]);
L(2).qlim = [0, 142*(pi/180)];
L(2).offset = -pi/2;

L(3) = Link([0, 0, 0.24, pi/2]);
L(3).qlim = [0, 135*(pi/180)];

L(4) = Link([0, 1.3, 0, -pi/2]);
L(4).qlim = [0, 600*(pi/180)];
L(4).offset = 0;

L(5) = Link([0, 0, 0, pi/2]);
L(5).qlim = [0, 260*(pi/180)];
L(5).offset = 0;

L(6) = Link([0, 0.2, 0, 0]);
L(6).qlim = [0, 720*(pi/180)];
L(6).offset = 0;

Robot = SerialLink(L, 'name', 'FANUC S-420i');
q_home = -pi/4 * ones(1,6);
T_home = Robot.fkine(q_home);

disp('Robot model:');
Robot
disp('Forward kinematics at q_home:');
disp(T_home);

% Uncomment when a graphics backend is available:
% Robot.plot(q_home);
