from data import dataset

design_performance = {
    'OTA1' : 'Offset_Voltage',
    'OTA2' : 'Offset_Voltage', 
    'OTA3' : 'Offset_Voltage',
    'OTA4' : 'CMRR'
}

designs = ['OTA1', 'OTA2', 'OTA3', 'OTA4']

ds_args = dict()
ds_args['balance'] = False
ds_args['alpha'] = 0.8
ds_args['nofeat'] = False
for design in designs:
    print("Checking embedding data for design:", design)
    ds_args['design'] = design
    ds_args['performance'] = design_performance[design]
    ds = dataset.dataset(ds_args)

