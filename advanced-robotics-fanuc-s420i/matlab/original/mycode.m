% syms teta alpha  a  d

clc
clear all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%denavit parameter
a=[0; .95; 0.24; 0; 0;0];
d=[1; 0; 0; 1.3; 0;0.2];
i = [1;2;3;4;5;6];
teta=["teta1";"teta2-90";"teta3";"teta4";"teta5";"teta6"]
alpha=["-90";"0";"90";"-90";"90";"0"]
patients = table(i,a,alpha,d,teta)
% N=input('Enter degree of freedom : ');
N=6;
alpha=[-pi/2;0;pi/2;-pi/2;pi/2;0];
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
%%%%%%%%%%%second method
Jv_method2=simplify(expand(jacobian(O_ee,[teta1,teta2,teta3,teta4,teta5,teta6])))
% J_v2=expand([diff(O_ee(1),teta1)  diff(O_ee(1),teta2) diff(O_ee(1),teta3) diff(O_ee(1),teta4) diff(O_ee(1),teta5) diff(O_ee(1),teta6);
%              diff(O_ee(2),teta1)  diff(O_ee(2),teta2) diff(O_ee(2),teta3) diff(O_ee(2),teta4) diff(O_ee(2),teta5) diff(O_ee(2),teta6);
%              diff(O_ee(3),teta1)  diff(O_ee(3),teta2) diff(O_ee(3),teta3) diff(O_ee(3),teta4) diff(O_ee(3),teta5) diff(O_ee(3),teta6)])


R=T(1:3,1:3);
syms teta1dot teta2dot teta3dot teta4dot teta5dot teta6dot
R_dot=simplify(diff(R,teta1)*teta1dot+diff(R,teta2)*teta2dot+diff(R,teta3)*teta3dot+diff(R,teta4)*teta4dot+diff(R,teta5)*teta5dot+diff(R,teta6)*teta6dot)

s=R_dot*R'
w=[s(3,2);s(1,3);s(2,1)]
R_t=[R(1,1) R(2,1) R(3,1);
    R(1,2) R(2,2) R(3,2);
    R(1,3) R(2,3) R(3,3)]
s=R_dot*R_t
w=simplify([s(3,2);s(1,3);s(2,1)])
Jw_method2=jacobian(w,[teta1dot,teta2dot,teta3dot,teta4dot,teta5dot,teta6dot])
J_method2=[Jv_method2;Jw_method2]

if(simplify(expand(J_method1-J_method2))==zeros(6,6))
    disp('two methodes are the same')
end
%%%%%%%%%%%%%%%%%%%%%%%dynamic lag
J1=[cross(z_0,(O_1-O_0));
    z_0                  ];
J1=[J1 zeros(6,5)];
Jv1=simplify(expand(J1(1:3,:)));
Jw1=simplify(expand(J1(4:6,:)));

J2=[cross(z_0,(O_2-O_0))    cross(z_1,(O_2-O_1))  ;
    z_0                     z_1                 ];
J2=[J2 zeros(6,4)];
Jv2=simplify(expand(J2(1:3,:)));
Jw2=simplify(expand(J2(4:6,:)));

J3=[cross(z_0,(O_3-O_0))    cross(z_1,(O_3-O_1))   cross(z_2,(O_3-O_2)) ;
    z_0                     z_1                    z_2  ];
J3=[J3 zeros(6,3)];
Jv3=simplify(expand(J3(1:3,:)));
Jw3=simplify(expand(J3(4:6,:)));

J4=[cross(z_0,(O_4-O_0))    cross(z_1,(O_4-O_1))   cross(z_2,(O_4-O_2))   cross(z_3,(O_4-O_3)) ;
    z_0                     z_1                    z_2                    z_3 ];
J4=[J4 zeros(6,2)];
Jv4=simplify(expand(J4(1:3,:)));
Jw4=simplify(expand(J4(4:6,:)));

J5=[cross(z_0,(O_5-O_0))    cross(z_1,(O_5-O_1))   cross(z_2,(O_5-O_2))   cross(z_3,(O_5-O_3))   cross(z_4,(O_5-O_4))  ;
    z_0                     z_1                    z_2                    z_3                    z_4 ];
J5=[J5 zeros(6,1)];
Jv5=simplify(expand(J5(1:3,:)));
Jw5=simplify(expand(J5(4:6,:)));

J6=simplify([cross(z_0,(O_ee-O_0)) cross(z_1,(O_ee-O_1)) cross(z_2,(O_ee-O_2)) cross(z_3,(O_ee-O_3)) cross(z_4,(O_ee-O_4))  cross(z_5,(O_ee-O_5));
    z_0                   z_1                   z_2                   z_3                   z_4                    z_5])
Jv6=simplify(expand(J6(1:3,:)))
Jw6=simplify(expand(J6(4:6,:)))

%%%%%
syms m1 m2 m3 m4 m5 m6 i1 i2 i3 i4 i5 i6 g

D1=simplify(expand(m1*Jv1.'*Jv1+m2*Jv2.'*Jv2+m3*Jv3.'*Jv3+m4*Jv4.'*Jv4+m5*Jv5.'*Jv5+m6*Jv6.'*Jv6));
D2=simplify(expand(i1*Jw1.'*Jw1+i2*Jw2.'*Jw2+i3*Jw3.'*Jw3+i4*Jw4.'*Jw4+i5*Jw5.'*Jw5+i6*Jw6.'*Jw6));
D=D1+D2;

t=[teta1 teta2 teta3 teta4 teta5 teta6];
tdot=[teta1dot teta2dot teta3dot teta4dot teta5dot teta6dot];

for k=1:6
    for j=1:6
        for i=1:6
            c(i,j,k)=0.5*(diff(D(k,j),t(i))+diff(D(k,i),t(j))-diff(D(i,j),t(k)));
            cc(i,j,k)=c(i,j,k)*tdot(j)*tdot(i);
        end
    end
    %     C=[C;jacobian(cc(:,:,k),[teta1dot,teta2dot,teta3dot,teta4dot,teta5dot,teta6dot])];
end
C=[];
for k=1:6
    CC=0;
    for i=1:6
        for j=1:6
            CC= CC+ cc(i,j,k);
        end
    end
    C=simplify(expand([C;jacobian(CC,[teta1dot,teta2dot,teta3dot,teta4dot,teta5dot,teta6dot])]));
end

p1=m1*g;
p2=m2*g*(1+0.95*sin(teta2));
p3=m3*g*(0.9*sin(teta3)+0.95*sin(teta2)+1);
p4=m4*g*(1.3*sin(teta3)+.95*sin(teta2)+1);
p5=m5*g*(0.2*sin(teta5)+1.3*sin(teta3)+0.95*sin(teta2)+1);
p6=m6*g*(0.3*sin(teta5)+1.3*sin(teta3)+0.95*sin(teta2)+1);
p=p1+p2+p3+p4+p5+p6;
g=simplify(expand(jacobian(p,[teta1,teta2,teta3,teta4,teta5,teta6]).'));