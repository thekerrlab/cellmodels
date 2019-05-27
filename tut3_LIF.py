# -*- coding: utf-8 -*-
"""
Created on Mon May 27 13:16:44 2019

@author: Michael
"""

from netpyne import specs, sim

# modifies tut3 to use LIF model and not HH for S population only

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters


## Population parameters
# Creates two populations sensory and motor with 20 cells each of type pyramidal using HH
netParams.popParams['S'] = {'cellType': 'PYR', 'numCells': 20, 'cellModel': 'IntFire1'}  # sensory
netParams.popParams['M'] = {'cellType': 'PYR', 'numCells': 20, 'cellModel': 'HH'}  # motor


# Cell parameters
## conds - condition cell properties
## applies the following cell properties only to neurons where condition is met
## in this case applies to all neurons where cellType = PYR
## specify cells to have a section soma and a Hodgkin-Huxley mechanism
cellRule = {'conds': {'cellType': 'PYR', 'cellModel': 'HH'},  'secs': {}}                            # cell rule dict

cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}                                                 # soma params dict
cellRule['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0}                            # soma geometry
cellRule['secs']['soma']['mechs']['LIF1'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70} # soma hh mechanism

## for the dend section we included the topol dict defining how it connects to its parent soma section
cellRule['secs']['dend'] = {'geom': {}, 'topol': {}, 'mechs': {}}                       # dend params dict
cellRule['secs']['dend']['geom'] = {'diam': 5.0, 'L': 150.0, 'Ra': 150.0, 'cm': 1}      # dend geometry
cellRule['secs']['dend']['topol'] = {'parentSec': 'soma', 'parentX': 1.0, 'childX': 0}  # dend topology
cellRule['secs']['dend']['mechs']['pas'] = {'g': 0.0000357, 'e': -70}                   # dend mechanisms

netParams.cellParams['PYRrule_HH'] = cellRule  # add dict to list of cell properties

## Cell parameters for LIF neurons
cellRule = {'conds': {'cellType': 'PYR', 'cellModel': 'LIF'},  'secs': {}}              # cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'pointps': {}}                                  # soma params dict
cellRule['secs']['soma']['geom'] = {'diam': 10.0, 'L': 10.0, 'cm': 31.831}              # soma geometry
cellRule['secs']['soma']['pointps']['LIF1'] = {'mod':'IntFire1', 'tau':10, 'refrac':5}  # soma hh mechanisms
netParams.cellParams['PYRrule_LIF1'] = cellRule                                         # add dict to list of cell parameters


# Synaptic mechanism parameters
## Define the parameters of a simply excitatory synaptic mechanism exc
## implemented using Exp2Syn with rise time tau, decay time tau2 and equilibrium potential e
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 0.5, 'e': 0}  # excitatory synaptic mechanism


# Stimulation parameters
## adds background stimulation using NEURON's NetStim
## source of stimulation labelled bkg
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 10, 'noise': 0.5}
## specify cells targeted by this stimulation - conds requirement
## Netstims connected with a weight and delay parameters to target the exc synaptic mechanism
netParams.stimTargetParams['bkg->PYR'] = {'source': 'bkg', 'conds': {'cellType': 'PYR'}, 'weight': 0.01, 'delay': 5, 'synMech': 'exc'}

## Cell connectivity rules
netParams.connParams['S->M'] = {    # S -> M label
        'preConds': {'pop': 'S'},   # conditions of presyn cells
        'postConds': {'pop': 'M'},  # conditions of postsyn cells
        'probability': 0.5,         # probability of connection
        'weight': 0.01,             # synaptic weight
        'delay': 5,                 # transmission delay (ms)
        'sec': 'dend',              # section to connect to
        'loc': 1.0,                 # location of synapse
        'synMech': 'exc'}           # synaptic mechanism

## above parameters relate to network model
## below parameters relate to simulation - independent of network

# Simulation parameters
simConfig = specs.SimConfig()           # object of class SimConfig to store simulation configuration

simConfig.duration = 1*1e3              # Duration of the simulation, in ms
simConfig.dt = 0.025                    # Internal integration timestep to use
simConfig.verbose = False               # Show detailed messages
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}  # Dict with traces to record
simConfig.recordStep = 0.1              # Step size in ms to save data (e.g. V traces, LFP, etc)
simConfig.filename = 'model_output'     # Set file output name
simConfig.savePickle = False            # Save params, network and sim output to pickle file

simConfig.analysis['plotRaster'] = True              # Plot a raster
simConfig.analysis['plotTraces'] = {'include': [1]}  # Plot recorded traces for this list of cells
simConfig.analysis['plot2Dnet'] = True               # plot 2D visualization of cell positions and connections

# Create and run the simulation
sim.createSimulateAnalyze(netParams, simConfig)

# new dendrtic component reduces the firing rate (?)