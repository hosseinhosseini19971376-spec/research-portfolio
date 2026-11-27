# Reproducibility Notes

## Required software

- MATLAB
- Simulink
- Stateflow support for MATLAB Function blocks

The exact MATLAB release used to create the original files has not been confirmed.

## Nominal model

1. Open MATLAB.
2. Set the current folder to the project directory.
3. Open models/withoutDOS.slx.
4. Run the model with its stored configuration.
5. Inspect the scopes and logged outputs.

The nominal model does not contain the tuvar From Workspace block found in the DoS-enabled variants.

## DoS-enabled models

Both models/withDOS.slx and models/RESILIENT.slx contain a From Workspace block configured to read a variable named tuvar.

The original tuvar data or script was not included in the supplied archive. Restore the original attack-signal variable from the experiment workspace or source script before running these models. Its time/value format and attack schedule must match the original experiment. Do not substitute an arbitrary signal when claiming reproduction of the original simulation.

## Stored model configuration

| Model | Stop time | Solver |
|---|---:|---|
| withoutDOS.slx | 30 s | Variable-step automatic |
| withDOS.slx | 5 s | Variable-step automatic |
| RESILIENT.slx | 10 s | Variable-step automatic |

## Results and validation

The supplied package contains no newly generated simulation plots or numerical results. The models have been inspected at the SLX package/XML level but have not been rerun in MATLAB as part of this portfolio preparation.

Before reporting results:
- restore the original tuvar attack input;
- execute each model in a compatible MATLAB/Simulink environment;
- confirm the model configuration and output definitions;
- generate plots from actual simulation outputs;
- document the attack schedule and its frequency/duration constraints;
- compare the results with the relevant figures and claims in the reference paper.

Do not claim numerical convergence rates, attack tolerance, or exact reproduction until those checks have been completed.
