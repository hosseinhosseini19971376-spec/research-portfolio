% syms teta alpha  a  d

clc
clear all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%denavit parameter
a=[0; .95; 0.24; 0; 0;0];
alpha=[-pi/2;0;pi/2;-pi/2;pi/2;0];
d=[1; 0; 0; 1.3; 0;0.2];
i = [1;2;3;4;5;6];
teta=["teta1";"teta2-90";"teta3";"teta4";"teta5";"teta6"]
patients = table(i,a,alpha,d,teta)
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
%%%%%%%%%%%%%%%%%%%%%%%%%%%work space
% for T1=0:50:360
%     for T2=0:50:142
%         for T3=0:50:135
%             for T4=0:100:600
%                 for T5=0:50:260
%                     t1=T1*(pi/180);
%                     t2=T2*(pi/180);
%                     t3=T3*(pi/180);
%                     t4=T4*(pi/180);
%                     t5=T5*(pi/180);
%                     position=subs(subs(subs(subs(subs(Tee,teta1,T1),teta2,T2),teta3,T3),teta4,T4),teta5,T5);
%                     xee=position(1);
%                     yee=position(2);
%                     zee=position(3);
%                     plot3(xee(:),yee(:),zee(:),'*')
%                     hold on
%                 end
%             end
%         end
%     end
% end


%%%%%%%%%%jocobian%%%%%%%%%%%%%
%%%%first method
%%%%j=[z_0*(O_ee-O_0) z_1*(O_ee-O_1) z_2*(O_ee-O_2) z_3*(O_ee-O_3) z_4*(O_ee-O_4)  z_5*(O_ee-O_5)
%%%   ;z_0            z_1            z_2            z_3            z_4             z_5

z_0=[0;0;1];
O_0=[0;0;0];

z_1=T1(1:3,3);
O_1=T1(1:3,4);

T2_0=T1*T2;
z_2=T2_0(1:3,3);
O_2=T2_0(1:3,4);

T3_0=T2_0*T3;
z_3=T3_0(1:3,3);
O_3=T3_0(1:3,4);

T4_0=T3_0*T4;
z_4=T4_0(1:3,3);
O_4=T4_0(1:3,4);

T5_0=T4_0*T5;
z_5=T5_0(1:3,3);
O_5=T5_0(1:3,4);

J_method1=simplify([cross(z_0,(O_ee-O_0)) cross(z_1,(O_ee-O_1)) cross(z_2,(O_ee-O_2)) cross(z_3,(O_ee-O_3)) cross(z_4,(O_ee-O_4))  cross(z_5,(O_ee-O_5));
    z_0                   z_1                   z_2                   z_3                   z_4                    z_5])
Jv_method1=simplify(expand(J_method1(1:3,:)))
Jw_method1=simplify(expand(J_method1(4:6,:)))

J=J_method1;
D=det(J)==0;
solve(D,[teta1 teta2 teta3 teta4 teta5 teta6])