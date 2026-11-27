clc;
clear all
% Joint space variables
Th_1 = -pi/4;
Th_2 = -pi/4;
Th_3 = -pi/4;
Th_4 = -pi/4;
Th_5 = -pi/4;
Th_6 = -pi/4;


% Setting DH parameters for joints
L(1) = Link([0, 1, 0, -pi/2]);      % DH parameters
L(1).qlim = [0 2*pi];             % joint limits

L(2) = Link([0, 0, 0.95, 0]);  % DH parameters                 % for prismatic joint
L(2).qlim = [0 142*(pi/180)];              % joint limits
L(2).offset = -pi/2;

L(3) = Link([0, 0, .24, pi/2]);      % DH parameters                % for prismatic joint
L(3).qlim = [0 135*(pi/180)];              % joint limits


L(4) = Link([0, 1.3, 0, -pi/2]);  % DH parameters
L(4).qlim = [0 600*(pi/180)];             % joint limits
L(4).offset = 0;                % joint offset

L(5) = Link([0, 0, 0, pi/2]);   % DH parameters
L(5).qlim = [0 260*(pi/180)];             % joint limits
L(5).offset = 0;                % joint offset

L(6) = Link([0, 0.2, 0, 0]);   % DH parameters
L(6).qlim = [0 720*(pi/180)];             % joint limits
L(6).offset = 0;



% creating robot object from the links array
Robot = SerialLink(L)
Robot.name = 'RRRRRR'


% plotting the robot in specific position
figure(1)
Robot.plot([Th_1 Th_2 Th_3  Th_4 Th_5 Th_6]);
hold on;


N = 60;
L1 = linspace(0,2*pi,N);
L2 = linspace(0, 142*(pi/180),N);
L3 = linspace(0 ,135*(pi/180),N);
L4 = linspace(0, 600*(pi/180),N);
L5 = linspace(0, 260*(pi/180),N);
L6 = linspace(0, 720*(pi/180),N);


for x=1:1:N-1
    Robot.plot([L1(x) L2(x) L3(x) L4(x) L5(x) L6(x)]);
    T = Robot.fkine([L1(x) L2(x) L3(x) L4(x) L5(x) L6(x)]);
    plot3(T.t(1),T.t(2),T.t(3),'.');
    hold on
end

syms teta1 teta2 teta3 teta4 teta5 teta6 teta1_dot teta2_dot teta3_dot teta4_dot teta5_dot teta6_dot
syms teta1_2dot teta2_2dot teta3_2dot teta4_2dot teta5_2dot teta6_2dot
T = Robot.fkine([teta1 teta2 teta3 teta4 teta5 teta6]);
% qi=Robot.ikine6s(T)

q=[teta1 teta2 teta3 teta4 teta5 teta6];
qd=[teta1_dot teta2_dot teta3_dot teta4_dot teta5_dot teta6_dot ];
qdd=[teta1_2dot teta2_2dot teta3_2dot teta4_2dot teta5_2dot teta6_2dot ];
 J1 = jacob0(Robot, q);
 J2 = jacobe(Robot, q);
% %  D=det(J1)

%%%%%%%%%%%%%%singular
i=1;
for T1=0:50:360
    for T2=0:50:142
        for T3=0:50:135
            for T4=0:100:600
                for T5=0:50:260
                    for T6=0:125:720
                        t1=T1*(pi/180);
                        t2=T2*(pi/180);
                        t3=T3*(pi/180);
                        t4=T4*(pi/180);
                        t5=T5*(pi/180);
                        t6=T6*(pi/180);
                        input=[t1 t2 t3 t4 t5 t6];
                        J_num=jacob0(Robot, input);
                        D=det(J_num);
                        if(D==0)
                            singular{i}=input;
                            i=i+1;
                        end
                    end
                end
            end
        end
    end
end

%
% %   q=[0 0 0 0 0 0];
% %   tau = rne(q,q_d,q_dd);
%
%
%