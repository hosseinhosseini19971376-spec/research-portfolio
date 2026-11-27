function check_model_prerequisites()
%CHECK_MODEL_PREREQUISITES Check files and workspace inputs before simulation.
% This helper does not run or modify any Simulink model.

projectRoot = fileparts(fileparts(mfilename('fullpath')));
modelDir = fullfile(projectRoot, 'models');

models = {
    'withoutDOS.slx', false
    'withDOS.slx', true
    'RESILIENT.slx', true
};

fprintf('\nResilient consensus project preflight\n');
fprintf('Project root: %s\n\n', projectRoot);

missingFiles = {};
for k = 1:size(models, 1)
    modelFile = fullfile(modelDir, models{k, 1});
    if isfile(modelFile)
        fprintf('[OK] Model file found: %s\n', models{k, 1});
    else
        fprintf('[MISSING] %s\n', modelFile);
        missingFiles{end+1} = models{k, 1}; %#ok<AGROW>
    end
end

if license('test', 'Simulink')
    fprintf('[OK] Simulink license is available.\n');
else
    warning('Simulink license is not available in this MATLAB session.');
end

needsTuvar = any(cell2mat(models(:, 2)));
if needsTuvar
    hasTuvar = evalin('base', 'exist(''tuvar'', ''var'') == 1');
    if hasTuvar
        fprintf('[OK] Variable tuvar exists in the MATLAB base workspace.\n');
    else
        warning(['The DoS-enabled models expect a base-workspace variable named tuvar. ' ...
            'The original attack signal was not included in the supplied archive. ' ...
            'Restore the original experiment data before running withDOS.slx or RESILIENT.slx.']);
    end
end

if ~isempty(missingFiles)
    warning('One or more SLX files are not present in the models/ directory.');
else
    fprintf('\nAll three model files are present.\n');
end

fprintf(['\nThis is a preflight check only. It does not validate the attack schedule, ' ...
    'execute simulations, or establish convergence claims.\n\n']);
end
