%% MATLAB Function block code - constrained Euler/Pontryagin state-costate model
% Extracted from source paragraph range: 335-352.

function [x1_dot,x2_dot,x3_dot,x4_dot,p1_dot,p2_dot,p3_dot,p4_dot,p5_dot,p6_dot,w1_dot,w2_dot] = fcn(x1,x2,x3,x4,p1,p2,p3,p4,p5,p6,u1,u2)
x1_dot=x2;
x2_dot=-148.18*x1 -20.34*x2 -498.03*x3 -66.69*x4 +1.32*u1+.67*u2;
x3_dot=x4;
x4_dot=-7.54*x1 +.46*x2 -116.86*x3 -22.88*x4 +0.56*u1+.004*u2;
p1_dot=x1+148.18*p2 +7.54*p4;
p2_dot=x2+ 20.34*p2 -.46*p4 -p1 ;
p3_dot=x3+ 498.03*p2 +116.86*p4 ;
p4_dot=x4+ 66.69*p2 +22.88*p4 -p3;
w2_dot=u2'*u2;
w1_dot=u1'*u1;
p5_dot=0;
p6_dot=0;
