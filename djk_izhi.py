# Test for izhi2007b.mod file. Compare traces with: http://www.physics.usyd.edu.au/teach_res/mp/ns/doc/nsIzhikevich3.htm

from netpyne import specs, sim

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

## Population parameters
netParams.popParams['E'] = {'cellType': 'E', 'numCells': 1, 'cellModel': 'Izhi'}

## Cell properties for Izhi_E neurons
cellRule = {'label': 'PYRrule_Izhi', 'conds': {'cellType': ['E'], 'cellModel': 'Izhi'},  'secs': {}} # cell rule dict
### Soma section
cellRule['secs']['soma'] = {'geom': {}, 'pointps':{}}  # soma properties
cellRule['secs']['soma']['geom'] = {'diam': 10, 'L': 10, 'cm': 31.831}
# The link at the top uses C = 100 pF, but Cliff uses C = 1 pF to get the same plots. Why...?
cellRule['secs']['soma']['pointps']['Izhi'] = {'mod':'Izhi2007b', 
        'C':100, 'k':0.7, 'vr':-60, 'vt':-40, 'vpeak':35, 'a':0.03, 'b':-2, 'c':-50, 'd':100, 'celltype':1}
netParams.cellParams['PYRrule_Izhi'] = cellRule  # add dict to list of cell properties

## Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'IClamp', 'del': 100, 'dur': 900, 'amp': 0.07}   # IClamp expressed in nA. This is 70 pA.
netParams.stimTargetParams['bkg->all'] = {'source': 'bkg', 'conds': {'cellType': ['E','I'], 'cellModel': 'Izhi'}, 'sec': 'soma', 'loc': 0.5}

# Simulation parameters
simConfig = specs.SimConfig()        # object of class SimConfig to store simulation configuration

## Simulation options
simConfig.duration = 1*1e3          # Duration of the simulation, in ms
simConfig.dt = 0.025                 # Internal integration timestep to use
simConfig.seeds = {'conn': 1, 'stim': 1, 'loc': 1}  # Seeds for randomizers (connectivity, input stimulation and cell locations)
simConfig.createNEURONObj = True  # create HOC objects when instantiating network
simConfig.createPyStruct = True  # create Python structure (simulator-independent) when instantiating network
simConfig.timing = True  # show timing  and save to file

### Recording
simConfig.recordCells = []  # list of cells to record from 
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'},
                          'u':{'sec':'soma', 'pointp':'Izhi', 'var':'u'}}  # Dict with traces to record # changed from cellmodels
simConfig.recordStim = True  # record spikes of cell stims
simConfig.recordStep = 0.025 # Step size in ms to save data (eg. V traces, LFP, etc)

### Saving
simConfig.filename = 'Izhi_params'  # Set file output name
simConfig.saveFileStep = 1000 # step size in ms to save data to disk
simConfig.savePickle = False # Whether or not to write spikes etc. to a .mat file
simConfig.saveJson = False # Whether or not to write spikes etc. to a .mat file
simConfig.saveMat = False # Whether or not to write spikes etc. to a .mat file
simConfig.saveTxt = False # save spikes and conn to txt file
simConfig.saveDpk = False # save to a .dpk pickled file

### Analysis and plotting
simConfig.analysis['plotTraces'] = {'include': [0,80], 'saveFig': 'Izhi_cellTrace_test.png'}     # plot recorded traces for this list of cells  # changed from cellmodels.py

# Create network and run simulation
sim.createSimulateAnalyze(netParams, simConfig)