# gcode-speed-hotend-compensation

This little script aims to do one thing for now:
Increase the temp of the hotend the faster a layer is printed.

This should compensate for the material being less hot the faster it is extruded.

## ToDo
- Add a deadtime / look-behind to compensate for the latency between m104 command and point in time where the temp is reached
- lookahead to ignore(or calculate a temp in between) layers that are printed faster than the hotend can react
