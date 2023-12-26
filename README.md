THIS PROJECT CAN LIKELY BE REPLACED WITH BLENDER OR HOUDINI, WITH ENOUGH SIMULATION STEPS AND AFTER VERIFYING ACCURACY.

# Project Rebound

Project Rebound utilizes Hanno Rein 's N-body [simulation library](https://github.com/hannorein/rebound) for the purpose of simulation setup for systems within Project Nine ("Simulatione"). 
The immediate goal is to find stable configurations and predicted future trajections for the Doma and X13 systems. Consult P9 for more detailed definition on this project.
This repo is pure simulation and outputs data points. A seperate parser/analyzer/visualizer will be written (likely in Pure/C#/Python) for analyzing those data.

Notice due to the nature of a public fork, this repo is public. In that case, we should avoid referencing Project Nine contents and try to keep this repo a pure-simulation environment.

This code follows original repository setup and utilizes folders inside "examples" For experiment setups. To compile and run any experiment, go to corresponding experiment folder, perform a `make` and run. The C codes will only work on Linux.  
From a software-development perspective, the best way to utilize this is to: 1) Data-driven everything first, 2) Develop and package the software as a proper CLI tool. However, for the purpose of this project, we will just edit in-place and use as-is for immedaite needs. The "tooling" aspect can be done in a seperate fork. See [OriginalREADME](./OriginalREADME.md) for original README file.

Units conventions: Notice REBOUND is designed to work with $G=1$. It's good and makes simulation independent of actual magnitude of things and we should get used to this convention, where both mass and distance are relative.

Below are the Project Nine specific setups:

1. Doma: [./examples/doma](./examples/doma)
