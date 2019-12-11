This folder contains benchmark circuits with performance simulations and placement results. 
All the circuits netlist files are under ./Netlists. 
The benchmark currently contains 5 OTA examples:
    Core_FF
    Core_test_flow
    Telescopic_Three_stage
    Telescopic_Three_stage_1

For each layout implementation, as an example under ./Core_FF/Core_FF_0/:
    performance.txt: post layout simulation results
    place.connection: the net and device pin connection information
    place.pin: pin information for each device
    place.result: device placement coordinates
    weight.txt: the net weighting for global placement optimization

For each design, the json files needed for feature extraction is under ./JsonFile.
Design.channel is the device image channel according to subcircuit topology.
Design.json is the device type mappings.

