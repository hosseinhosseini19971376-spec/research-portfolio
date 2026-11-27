%% FANUC S-420i — joint-grid singularity scan
% The report's code in the workspace section computes Jacobian determinants
% and stores singular configurations; it does not generate the plotted
% workspace point cloud. The complete point-cloud code is absent.

clear; clc;
run('02_peter_corke_robot_model.m');

singular = {};
idx = 1;
det_tolerance = 1e-8;

for T1 = 0:50:360
    for T2 = 0:50:142
        for T3 = 0:50:135
            for T4 = 0:100:600
                for T5 = 0:50:260
                    for T6 = 0:125:720
                        q_deg = [T1 T2 T3 T4 T5 T6];
                        q_rad = q_deg * (pi/180);

                        J_num = jacob0(Robot, q_rad);
                        detJ = det(J_num);

                        if abs(detJ) < det_tolerance
                            singular{idx,1} = q_rad; %#ok<SAGROW>
                            idx = idx + 1;
                        end
                    end
                end
            end
        end
    end
end

fprintf('Singular configurations found: %d\n', numel(singular));
save('fanuc_s420i_singular_configurations.mat', 'singular');
