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
%%%%%%%%%%%%%%%%%%%end effector
O_ee=T(1:3,4);
%%%%%%%%%%%%%%%%%%%Inverse kinematics
syms X_ee Y_ee Z_ee t4 t5 t6 o_z_ee
t1=atan2(Y_ee,X_ee);
D=(X_ee^2+Y_ee^2+(Z_ee-1)^2-1.19^2-1.3^2)/(2*1.19*1.3);
t3=atan2(D,sqrt(1-D^2));
t2=atan2(sqrt(X_ee^2+Y_ee^2),Z_ee-1)-atan2(1.19+1.3*cos(t3),1.3*sin(t3));
e1=(19*cos(t1)*sin(t2))/20 + (sin(t5)*(cos(t1)*cos(t2)*cos(t4)*sin(t3) - sin(t1)*sin(t4) + cos(t1)*cos(t3)*cos(t4)*sin(t2)))/5 + (13*cos(t1)*sin(t2)*sin(t3))/10 - (cos(t2 + t3)*cos(t1)*cos(t5))/5 - (13*cos(t1)*cos(t2)*cos(t3))/10 + (6*cos(t1)*cos(t2)*sin(t3))/25 + (6*cos(t1)*cos(t3)*sin(t2))/25 == X_ee;
e2=(19*sin(t1)*sin(t2))/20 + (sin(t5)*(cos(t1)*sin(t4) + cos(t2)*cos(t4)*sin(t1)*sin(t3) + cos(t3)*cos(t4)*sin(t1)*sin(t2)))/5 + (6*cos(t2)*sin(t1)*sin(t3))/25 + (6*cos(t3)*sin(t1)*sin(t2))/25 + (13*sin(t1)*sin(t2)*sin(t3))/10 - (cos(t2 + t3)*cos(t5)*sin(t1))/5 - (13*cos(t2)*cos(t3)*sin(t1))/10 == Y_ee;
e3=sin(t6)*(sin(t2 + t3)*sin(t5) - cos(t2 + t3)*cos(t4)*cos(t5)) - cos(t2 + t3)*cos(t6)*sin(t4) == o_z_ee;
S=solve([e1 e2 e3],[t4 t5 t6]);
t4=S.t4;
t5=S.t5;
t6=S.t6;