function [q, a, d, alpha, theta] = fanuc_s420i_dh()
% FANUC_S420I_DH  DH data transcribed from the Advanced Robotics report.
% Robot: FANUC S-420i, 6 joints.
% Length units are not explicitly stated in the report.

    syms q1 q2 q3 q4 q5 q6 real
    q = [q1 q2 q3 q4 q5 q6];

    a     = [0, 0.95, 0.24, 0, 0, 0];
    d     = [1, 0, 0, 1.3, 0, 0.2];
    alpha = [-pi/2, 0, pi/2, -pi/2, pi/2, 0];
    theta = [q1, q2-pi/2, q3, q4, q5, q6];
end
