# SLM_phase_control
A small GUI application for controlling the phase of the SLM.
The project was first created for the Hamamatsu SLM (Attolab), but has been updated to work with the santec SLM-300 (D-Lab).

To run the program, execute "controlPhaseSLM.py", it wil load all the other files as it needs to.

Some settings (the wavelength used in the lab and the SLM type used) still need to be made on the code level before the program is run.
These can be found and changed in the file "settings.py".



### Updates

Currently being updated to generate Hologram phase patterns with the Gerchberg-Saxton-algorithm.
The GS-algorithm is already implemented "gerchberg_saxton.py", but not yet included in the main program.