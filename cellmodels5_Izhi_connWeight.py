## cellmodels5_Izhi_connWeight.py

# Plots the firing rate of Izhi neurons vs sweep of connection weight

from netpyne import specs, sim


# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

## Population parameters
netParams.popParams['E'] = {'cellType': 'E', 'numCells': 80, 'cellModel': 'Izhi'}
netParams.popParams['I'] = {'cellType': 'I', 'numCells': 20, 'cellModel': 'Izhi'}

## Cell properties for Izhi_E and Izhi_I neurons
cellRule = {'label': 'PYRrule_Izhi', 'conds': {'cellType': ['E','I'], 'cellModel': 'Izhi'},  'secs': {}} # cell rule dict
### Soma section
cellRule['secs']['soma'] = {'geom': {}, 'pointps':{}}  # soma properties
cellRule['secs']['soma']['geom'] = {'diam': 10, 'L': 10, 'cm': 31.831}
cellRule['secs']['soma']['pointps']['Izhi'] = {'mod':'Izhi2007b', 
        'C':1, 'k':0.7, 'vr':-60, 'vt':-40, 'vpeak':35, 'a':0.03, 'b':-2, 'c':-50, 'd':100, 'celltype':1}
netParams.cellParams['PYRrule_Izhi'] = cellRule  # add dict to list of cell properties

### Dendritic section
# cellRule['secs']['dend'] = {'geom': {}, 'topol': {}, 'mechs': {}}                                       # dend params dict
# cellRule['secs']['dend']['geom'] = {'diam': 5.0, 'L': 150.0, 'Ra': 150.0, 'cm': 1, 'pt3d': []}          # dend geometry
# cellRule['secs']['dend']['topol'] = {'parentSec': 'soma', 'parentX': 1.0, 'childX': 0}                  # dend topology
# cellRule['secs']['dend']['mechs']['pas'] = {'g': 0.0000357, 'e': -70}                                   # dend mechanisms
# netParams.cellParams['PYRrule_Izhi'] = cellRule                                                         # add dict to list of cell parameters

## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {'mod': 'ExpSyn', 'tau': 0.1, 'e': 0}                  # AMPA synaptic mechanism
netParams.synMechParams['inh'] = {'mod': 'Exp2Syn', 'tau1': 0.6, 'tau2': 8.5, 'e': -70} # GABA synaptic mechanism

## Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 2.8, 'noise': 0.3}
### stimTargetParams different for Izhi neurons
netParams.stimTargetParams['bkg->all'] = {'source': 'bkg', 'conds': {'cellType': ['E','I'], 'cellModel': 'Izhi'}, 
                                            'weight': 1.0, 'delay': 'uniform(1,5)', 'synMech': 'exc'}


allFiringRates = []
connWeights = [x*0.1 for x in range(11)]
for connWeight in connWeights:

    ## Cell connectivity rules
    netParams.connParams['E->all'] = {         # label
            'preConds': {'pop': 'E'},          # conditions of presyn cells
            'postConds': {'pop': ['E','I']},   # conditions of postsyn cells
            'probability': 0.2,                # probability of connection
            'weight': connWeight,                     # synaptic weight
            'delay': '0.2+normal(13.0,1.4)',   # transmission delay (ms) min=0.2, mean=13.0, var = 1.4
            'threshold': 10,                   # threshold
            'convergence': 'uniform(0,5)',     # convergence (num presyn targeting postsyn) is uniformly distributed between 1 and 10
            'sec': 'dend',                     # section to connect to
            'loc': 1.0,                        # location of synapse
            'synMech': 'exc'}                  # synaptic mechanism, target synapse
    
    netParams.connParams['I->E'] = {           # label
            'preConds': {'pop': 'I'},          # conditions of presyn cells
            'postConds': {'pop': 'E'},         # conditions of postsyn cells
            'probability': 0.2,                # probability of connection
            'weight': connWeight,                     # synaptic weight
            'delay': '0.2+normal(13.0,1.4)',   # transmission delay (ms) min=0.2, mean=13.0, var = 1.4
            'threshold': 10,                   # threshold
            'convergence': 'uniform(0,5)',     # convergence (num presyn targeting postsyn) is uniformly distributed between 1 and 10
            'sec': 'dend',                     # section to connect to
            'loc': 1.0,                        # location of synapse
            'synMech': 'inh'}                  # synaptic mechanism, target synapse
    
    
    # Simulation parameters
    simConfig = specs.SimConfig()        # object of class SimConfig to store simulation configuration
    
    ## Simulation options
    simConfig.duration = 2*1e3          # Duration of the simulation, in ms
    simConfig.dt = 0.025                 # Internal integration timestep to use
    simConfig.seeds = {'conn': 1, 'stim': 1, 'loc': 1}  # Seeds for randomizers (connectivity, input stimulation and cell locations)
    simConfig.createNEURONObj = True  # create HOC objects when instantiating network
    simConfig.createPyStruct = True  # create Python structure (simulator-independent) when instantiating network
    simConfig.timing = True  # show timing  and save to file
    
    ### Recording
    simConfig.recordCells = []  # list of cells to record from 
    simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}  # Dict with traces to record # changed from cellmodels
    simConfig.recordStim = True  # record spikes of cell stims
    simConfig.recordStep = 0.025 # Step size in ms to save data (eg. V traces, LFP, etc)
    
    ### Saving
    simConfig.filename = 'HH_params'  # Set file output name
    simConfig.saveFileStep = 1000 # step size in ms to save data to disk
    simConfig.savePickle = False # Whether or not to write spikes etc. to a .mat file
    simConfig.saveJson = False # Whether or not to write spikes etc. to a .mat file
    simConfig.saveMat = False # Whether or not to write spikes etc. to a .mat file
    simConfig.saveTxt = False # save spikes and conn to txt file
    simConfig.saveDpk = False # save to a .dpk pickled file
    
    ### Analysis and plotting
    # simConfig.analysis['plotRaster'] = {'orderInverse': False, 'saveFig': 'HH_raster_%s.png'} % connWeight #True # Whether or not to plot a raster
    # simConfig.analysis['plotTraces'] = {'include': [0,80], 'saveFig': 'HH_cellTrace_%s.png'}  % connWeight   # plot recorded traces for this list of cells  # changed from cellmodels.py
    # simConfig.analysis['plotRatePSD'] = {'include': ['allCells', 'E', 'I'], 
    # 'smooth': 10, 'saveFig': 'HH_PSD_%s.png'} % connWeight # plot recorded traces for this list of cells
    # simConfig.analysis['plot2Dnet'] = True               # plot 2D visualization of cell positions and connections

    # Create network and run simulation
    sim.createSimulateAnalyze(netParams, simConfig)
    
    sim.firingRate
    allFiringRates.append(sim.firingRate)

import pylab as pl
pl.plot(connWeights, allFiringRates)
pl.xlabel('Connection weight')
pl.ylabel('Firing rate (Hz)')
pl.title('Parameter sweep of connection weight for Izhi neurons')