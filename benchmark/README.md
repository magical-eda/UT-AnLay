# Benchmark Overview #
This folder contains benchmark circuits with performance simulations and placement results. 
Run the script under UT-Anlay to extract the benchmark
```
    source extract.sh 
```
## Designs ##
More information on the circuits netlist files are under ./Netlists. 
The benchmark currently contains 4 OTA examples:
- Telescopic_Three_stage
- Telescopic_Three_stage_1
- Core_FF
- Core_test_flow

## Performance Simulation ##
More information on the circuits test bench are under ./Simulation. 
With each circuit layout implementation, the netlist first need to be extracted for parasitics and then simulated with the test bench.
We currently rely on Calibre PEX for layout parasitic extraction:
https://go.mentor.com/4ii9y
We currently rely on Cadence Spectre for performance simulation, the ocean script files are under ./Simulation, which could be initiated with in the command line with:
```
    ocean --replay ./Simulation/#Name_Of_Test#.ocn    
```
Note that it is possible that other initializer files are needed to fully run the ocean simulation script.


## Placement and peformance ##
For each layout implementation, as an example under ./Core_FF/Core_FF_0/ contains the respective performance results.
### Performance ###
- performance.txt: post layout simulation results
### Placement Solution ###
- place.connection: the net and device pin connection information
- place.pin: pin information for each device
- place.result: device placement coordinates
#### place.connection ####
Each line in the file is the connected pin of the net in the following format:
```
NetName DeviceName0 PinType0 DeviceName1 PinType1 ...
```
The Pin indincate the pintype of the device:
- CMOS: D/G/S/B respectively for drain, gate, source and bulk
- Resistor and capacitor: PLUS/MINUS/B respectively for plus, minus and bulk. Note that there is no electrical difference between PLUS and MINUS.
#### place.pin ####
This file includes all the pin shapes of each implemented device layout.
The pin shapes are currently in the form of rectangles and the coordinate are based on device layout before placement. The final pin shape should also include the offset based on where each device is placed.
For this current version, each device would consist of multiple pins (bulk shape not included). The format for this file is as follows:
```
DeviceName
PinType0 NumberOfShapes0
    MetalLayer0 RectangleTuple0
...
```
#### place.result ####
The resulting coordinate for each device placement.
```
DeviceName OriginX OriginY Width Height
```
### Misc. ###
- weight.txt: the net weighting for global placement optimization

The layout generation based on MAGICAL (https://github.com/magical-eda/MAGICAL). The analytical placement engine optimizes weighted wire-length and area, while also enforcing symmetry constraints. Different netweighting would lead to different placement solutions and post layout performance results.

## Feature extraction ##
More information on the json files needed for feature extraction is under ./JsonFile.
