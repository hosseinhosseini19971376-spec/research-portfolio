clc
clear all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%denavit parameter
a=[0; .95; 0.24; 0; 0;0];
alpha=[-pi/2;0;pi/2;-pi/2;pi/2;0];
d=[1; 0; 0; 1.3; 0;0.2];
i = [1;2;3;4;5;6];
teta=["teta1";"teta2-90";"teta3";"teta4";"teta5";"teta6"];
patients = table(i,a,alpha,d,teta);
% N=input('Enter degree of freedom : ');
N=6;
syms teta1 teta2 teta3 teta4 teta5 teta6
teta=[teta1 teta2-pi/2 teta3 teta4 teta5 teta6];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%forward kenamatic
for i=1:N
    %  a(i)=input(['Enter a' num2str(i)  ': ']);
    %  alpha(i)=input(['Enter alpha' num2str(i)  ': ']);
    %  d(i)=input(['Enter d' num2str(i)  ': ']);
    %  teta{i}=input(['Enter teta' num2str(i)  ': '],'s');
    %  T=str2sym(teta{i})
    G{i}=[cos(teta(i))   -sin(teta(i))*floor(cos(alpha(i))) sin(teta(i))*floor(sin(alpha(i))) a(i)*cos(teta(i));
        sin(teta(i)) cos(teta(i))*floor(cos(alpha(i))) -cos(teta(i))*floor(sin(alpha(i))) a(i)*sin(teta(i));
        0            floor(sin(alpha(i)))               floor(cos(alpha(i)))            d(i);
        0            0                                  0                               1];
end
%%%%%%%%%%%%%%%%%%%%transformation matrix
T1=expand(G{1});
T2=expand(G{2});
T3=expand(G{3});
T4=expand(G{4});
T5=expand(G{5});
T6=expand(G{6});
T=simplify(T1*T2*T3*T4*T5*T6);
%%%%%%%%%%%%%%%%%%%%Rotationa Matrix
R=T(1:3,1:3);
%%%%%%%%%%%%%%%%%%% X-Y-Z fixed angles
pitch=atan2(-R(3,1),sqrt(R(1,1)^2+R(2,1)^2));
roll=atan2(R(2,1)/cos(pitch),R(1,1)/cos(pitch));
yaw=atan2(R(3,2)/cos(pitch),R(3,3)/cos(pitch));
%%%%%%%%%%%%%%%%%%% Z-Y-Z Euler angles
beta_e=atan2(sqrt(R(3,1)^2+R(3,2)^2),R(3,3));
alpha_e=atan2(R(2,3)/sin(beta_e),R(1,3)/sin(beta_e));
gama_e=atan2(R(3,2)/sin(beta_e),R(3,1)/sin(beta_e));
%%%%%%%%%%%%%%%%%%% Equivalent angle-axis
theta_aa=acos((trace(R)-1)/2);
k_aa=(0.5/sin(theta_aa))*[R(3,2)-R(2,3);R(1,3)-R(3,1);R(2,1)-R(1,2)];
%%%%%%%%%%%%%%%%%%% unit quaternion
e4=0.5*sqrt(1+trace(R));
e1=(R(3,2)-R(2,3))/(4*e4);
e2=(R(1,3)-R(3,1))/(4*e4);
e3=(R(2,1)-R(1,2))/(4*e4);