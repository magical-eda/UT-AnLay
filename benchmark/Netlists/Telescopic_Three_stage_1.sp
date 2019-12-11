// Generated for: spectre
// Generated on: Aug 28 14:33:38 2019
// Design library name: Telescopic_Three_stage_1
// Design cell name: Telescopic_Three_stage_manual_XT
// Design view name: schematic
// simulator lang=spectre

// Cell name: Telescopic_Three_stage_1
// View name: schematic

subckt Telescopic_Three_stage_1 INM INP OUTM OUTP VBN1 VDD VREF VSS
M112 (net1 VCMFB1 VSS VSS) nfet l=300n w=3u m=1 nf=1 
M60 (net057 net056 net058 VSS) nfet l=300n w=18.0u m=1 nf=6 
M113 (VCMFB3 VREF net058 VSS) nfet l=300n w=18.0u m=1 nf=6 
M24 (VBN1 VBN1 VBN VSS) nfet l=2u w=30u m=1 nf=4 
M107 (VOM2 VCMFB2 VSS VSS) nfet l=300n w=12.0u m=1 nf=4 
M106 (OUTM VOP2 VSS VSS) nfet l=300n w=36.0u m=1 nf=12 
M108 (OUTP VOM2 VSS VSS) nfet l=300n w=36.0u m=1 nf=12
M104 (VOP2 VCMFB2 VSS VSS) nfet l=300n w=12.0u m=1 nf=4 
M3 (VOM1 VBN1 VSHM1 VSS) nfet l=400n w=20u m=1 nf=10 
M110 (VOP1 VBN1 VSHP1 VSS) nfet l=400n w=20u m=1 nf=10 
M63 (net057 net057 VDD VDD) pfet l=300n w=12.0u m=1 nf=4 
M115 (VOM2 VOP1 net062 VDD) pfet l=800n w=60u m=1 nf=6 
M109 (OUTP VBP VDD VDD) pfet l=1u w=25.6u m=1 nf=4
M98 (OUTM VCMFB3 VDD VDD) pfet l=1u w=51.2u m=1 nf=8 
M119 (VCMFB3 net057 VDD VDD) pfet l=300n w=12.0u m=1 nf=4 
M26 (VBP1 VBP1 VDD VDD) pfet l=2u w=30u m=1 nf=4 
M90 (VBP VBP VDD VDD) pfet l=1u w=25.6u m=1 nf=4 
M111 (OUTP VCMFB3 VDD VDD) pfet l=1u w=51.2u m=1 nf=8 
M14 (OUTM VBP VDD VDD) pfet l=1u w=25.6u m=1 nf=4 
M116 (net062 VBP VDD VDD) pfet l=1u w=51.2u m=1 nf=8 
M114 (VOP2 VOM1 net062 VDD) pfet l=800n w=60u m=1 nf=6 
M117 (net08 VBP VDD VDD) pfet l=1u w=25.6u m=1 nf=4 
M118 (net07 VBP VDD VDD) pfet l=1u w=25.6u m=1 nf=4
M103 (VOP1 VBP1 net08 VDD) pfet l=600n w=24.0u m=1 nf=10 
M6 (VOM1 VBP1 net07 VDD) pfet l=600n w=24.0u m=1 nf=10 
C1 (VOM2 net038) mom_cap
C3 (VOM1 net032) mom_cap
C4 (VOP1 net031) mom_cap
C6 (VOP2 net037) mom_cap
R11 (VOM2 VCMFB2 VSS) poly_res
R19 (net038 net032 VSS ) poly_res
R21 (OUTM net031 VSS ) poly_res
R13 (VCMFB1 VOP1 VSS ) poly_res
R10 (net056 OUTM VSS ) poly_res
R14 (VOM1 VCMFB1 VSS ) poly_res
R15 (OUTP net032 VSS ) poly_res
R0 (OUTP net056 VSS ) poly_res
R20 (net037 net031 VSS ) poly_res
R12 (VCMFB2 VOP2 VSS ) poly_res
M12 (VSHM1 INP net1 VSS) nfet_ud l=800n w=100.0000u multi=1 nf=10 
M5 (VSHP1 INM net1 VSS) nfet_ud l=800n w=100.0000u multi=1 nf=10 
M16 (net058 VBN VSS VSS) nfet_lvt l=800n w=32.0u multi=1 nf=8
M10 (VBP1 VBN VSS VSS) nfet_lvt l=800n w=16.0u multi=1 nf=4 
M9 (VBN VBN VSS VSS) nfet_lvt l=800n w=16.0u multi=1 nf=4
M15 (VBP VBN VSS VSS) nfet_lvt l=800n w=16.0u multi=1 nf=4 
ends Telescopic_Three_stage_1

