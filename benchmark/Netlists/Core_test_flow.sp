// Generated for: spectre
// Generated on: Dec  9 17:25:45 2018
// Design library name: Two_stage_miller
// Design cell name: Core
// Design view name: schematic
// simulator lang=spectre

// Cell name: Core
// View name: schematic

subckt Core_test_flow INM INP OUTM OUTP VBIAS_P VDD VREF VSS
MP1c (net020 VBIAS_P VDD VDD) pfet l=120.0n w=16.0u m=1 nf=8
M20 (net028 VBIAS_P VDD VDD) pfet l=120.0n w=16.0u m=1 nf=8
M7 (vbias_n VBIAS_P VDD VDD) pfet l=120.0n w=16.0u m=1 nf=8
M5 (VBIAS_P VBIAS_P VDD VDD) pfet l=120.0n w=16.0u m=1 nf=8
MP1a (intm VBIAS_P VDD VDD) pfet l=120.0n w=40u m=1 nf=20 
MP1b (intp VBIAS_P VDD VDD) pfet l=120.0n w=40u m=1 nf=20
C1 (OUTM net037) mom_cap
C0 (OUTP net047) mom_cap
M10 (net7 vbias_n VSS VSS) nfet_lvt l=120.0n w=32.0u m=1 nf=16 
M9 (OUTM vbias_n VSS VSS) nfet_lvt l=120.0n w=12.0u m=1 nf=6 
M6 (OUTP vbias_n VSS VSS) nfet_lvt l=120.0n w=12.0u m=1 nf=6
M13 (vcmfb vcmfb VSS VSS) nfet_lvt l=120.0n w=4u m=1 nf=2 
M12 (net025 net025 VSS VSS) nfet_lvt l=120.0n w=4u m=1 nf=2 
M11 (net7 vcmfb VSS VSS) nfet_lvt l=120.0n w=8u m=1 nf=4 
M4 (vbias_n vbias_n VSS VSS) nfet_lvt l=120.0n w=8u m=1 nf=4 
M19 (net025 VREF net028 VDD) pfet_lvt l=120.0n w=16.0u m=1 nf=8 
M17 (net025 VREF net020 VDD) pfet_lvt l=120.0n w=16.0u m=1 nf=8 
M15 (vcmfb OUTP net020 VDD) pfet_lvt l=120.0n w=16.0u m=1 nf=8 
M25 (net037 VSS intp VDD) pfet_lvt l=120.0n w=24.0u m=1 nf=12 
M23 (net047 VSS intm VDD) pfet_lvt l=120.0n w=24.0u m=1 nf=12
M3 (OUTP intm VDD VDD) pfet_lvt l=120.0n w=24.0u m=1 nf=12 
M1 (OUTM intp VDD VDD) pfet_lvt l=120.0n w=24.0u m=1 nf=12
M18 (vcmfb OUTM net028 VDD) pfet_lvt l=120.0n w=16.0u m=1 nf=8 
M0 (intp INM net7 VSS) nfet_ud l=500n w=60u multi=1 nf=12 
M2 (intm INP net7 VSS) nfet_ud l=500n w=60u multi=1 nf=12 
ends Core_test_flow

