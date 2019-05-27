# -*- coding: utf-8 -*-
"""
Created on Mon May 27 12:38:24 2019

@author: Michael
"""

from netpyne import specs, sim

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

## Population parameters
# Creates two populations sensory and motor with 20 cells each of type pyramidal using HH
netParams.popParams['S'] = {'cellType': 'PYR', 'numCells': 20, 'cellModel': 'HH'}  # sensory
netParams.popParams['M'] = {'cellType': 'PYR', 'numCells': 20, 'cellModel': 'HH'}  # motor

# Cell parameters
## conds - condition cell properties
## applies the following cell properties only to neurons where condition is met
## in this case applies to all neurons where cellType = PYR
## specify cells to have a section soma and a Hodgkin-Huxley mechanism
cellRule = {'conds': {'cellType': 'PYR'},  'secs': {}}  # cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}                                                                                                    # soma params dict
cellRule['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0}                                                               # soma geometry
cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}      # soma hh mechanism
netParams.cellParams['PYRrule'] = cellRule  # add dict to list of cell properties

# Synaptic mechanism parameters
## Define the parameters of a simply excitatory synaptic mechanism exc
## implemented using Exp2Syn with rise time tau, decay time tau2 and equilibrium potential e
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 0.5, 'e': 0} # excitatory synaptic mechanism

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
