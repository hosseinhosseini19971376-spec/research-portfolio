clc
clear all
a=[0;0;0.95;0.24;0;0;0];
d=[1; 0; 0;1.3; 0;0.2;0];
N=6;
alpha=[0;-pi/2;0;pi/2;-pi/2;pi/2;0];
syms teta1 teta2 teta3 teta4 teta5 teta6
teta=[teta1 teta2-pi/2 teta3 teta4 teta5 teta6 0];
for i=1:N+1
    
    G{i}=[cos(teta(i))   -sin(teta(i)) 0 a(i);
        sin(teta(i))*floor(cos(alpha(i))) cos(teta(i))*floor(cos(alpha(i))) -floor(sin(alpha(i))) -floor(sin(alpha(i)))*d(i);
        sin(teta(i))*floor(sin(alpha(i)))           cos(teta(i))*floor(sin(alpha(i)))               floor(cos(alpha(i)))            floor(cos(alpha(i)))*d(i);
        0            0                                  0                               1];
end
T1=expand(G{1});
T2=expand(G{2});
T3=expand(G{3});
T4=expand(G{4});
T5=expand(G{5});
T6=expand(G{6});
Tee=expand(G{7});
Tzz=simplify(T1*T2*T3*T4*T5*T6*Tee);

w{1}=zeros(3,1);
w_dot{1}=zeros(3,1);
f{7}=zeros(3,1);
n{7}=zeros(3,1);
syms teta1dot teta2dot teta3dot teta4dot teta5dot teta6dot teta1dd teta2dd teta3dd teta4dd teta5dd teta6dd
syms L1 L2 L3 L4 L5 L6 m1 m2 m3 m4 m5 m6 g
v_dot{1}=[0;g;0];
m=[m1 m2 m3 m4 m5 m6];
L=[L1 L2 L3 L4 L5 L6];
teta_dot=[teta1dot teta2dot teta3dot teta4dot teta5dot teta6dot];
teta_dd=[teta1dd teta2dd teta3dd teta4dd teta5dd teta6dd];
for i=1:6
    
w{i+1}=G{i}(1:3,1:3).'*w{i}+teta_dot(i)*[0;0;1];
w_dot{i+1}=G{i}(1:3,1:3).'*w_dot{i}+cross(G{i}(1:3,1:3).'*w{i},teta_dot(i)*[0;0;1])+teta_dd(i)*[0;0;1];
v_dot{i+1}=G{i}(1:3,1:3).'*(v_dot{i}+cross(w_dot{i},G{i}(1:3,4))+cross(w{i},cross(w{i},G{i}(1:3,4))));
vc_dot{i+1}=v_dot{i+1}+cross(w_dot{i+1},[L(i);0;0])+cross(w{i+1},cross(w{i+1},[L(i);0;0]));
F{i}=m(i)*vc_dot{i+1};
end

for i=6:-1:1
    f{i}=F{i}+G{i}(1:3,1:3)*f{i+1};
    n{i}=G{i}(1:3,1:3)*n{i+1}+cross([L(i);0;0],F{i})+cross(G{i}(1:3,4),G{i}(1:3,1:3)*f{i+1});
    tav{i}=n{i}.'*[0;0;1];
end
TAV=[tav{1};tav{2};tav{3};tav{4};tav{5};tav{6}];
M=jacobian(TAV,[teta1dd, teta2dd ,teta3dd ,teta4dd ,teta5dd ,teta6dd]);
C=jacobian(TAV,[teta1dot,teta2dot,teta3dot,teta4dot,teta5dot,teta6dot]);
g=subs(subs(TAV,teta_dot.',zeros(6,1)),teta_dd.',zeros(6,1))