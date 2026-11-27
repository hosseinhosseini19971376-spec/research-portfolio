%% FANUC S-420i — Peter Corke recursive Newton-Euler call
% The report contains only this call: tau = rne(q,q_d,q_dd);
% It does not provide numeric masses, COM vectors or inertia tensors.
%
% Preconditions:
%   Robot : SerialLink model from 02_peter_corke_robot_model.m
%   q     : 1x6 joint positions [rad]
%   qd    : 1x6 joint velocities
%   qdd   : 1x6 joint accelerations
%
% Populate Robot.links(i).m, .r and .I with real physical parameters first.
% Then, for Peter Corke Robotics Toolbox:
% tau = Robot.rne(q, qd, qdd);
%
% Verbatim source call:
% tau = rne(q,q_d,q_dd);
