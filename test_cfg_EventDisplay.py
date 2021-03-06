import FWCore.ParameterSet.Config as cms

import sys
import optparse
import commands

process = cms.Process("unpack")
process.load('HGCal.RawToDigi.hgcaltbdigis_cfi')
process.load('HGCal.RawToDigi.hgcaltbdigisplotter_cfi')
process.load('HGCal.Reco.hgcaltbrechitproducer_cfi')
process.load('HGCal.Reco.hgcaltbrechitplotter_cfi')

RunNumber = sys.argv[2]
#energy = sys.argv[3]

process.source = cms.Source("HGCalTBTextSource",
                            run=cms.untracked.int32(1),####provide file name below
                            fileNames=cms.untracked.vstring("file:/hgcaldata/data/HGCRun_Output_000%s.txt" %RunNumber) ### here a vector is provided, but in the .cc only the first one is used TO BE FIXED
#                            fileNames=cms.untracked.vstring("file:/afs/cern.ch/work/r/rslu/public/HGC_TB_data_Aug2016/PED_Output_000111.txt")
)

process.dumpRaw = cms.EDAnalyzer("DumpFEDRawDataProduct",
                              dumpPayload=cms.untracked.bool(True))

process.dumpDigi = cms.EDAnalyzer("HGCalDigiDump")

process.output = cms.OutputModule("PoolOutputModule",
                                  compressionAlgorithm = cms.untracked.string('LZMA'),
                                  compressionLevel = cms.untracked.int32(4),
                                  dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('USER'),
        filterName = cms.untracked.string('')
        ),
                                 eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
                                 fastCloning = cms.untracked.bool(False),
                                 fileName = cms.untracked.string('test_output.root'), #options.output),
                                 )
### electron beam
#process.TFileService = cms.Service("TFileService", fileName = cms.string("../../../analysis/hist/region2/100GeV/HGC_Output_EventDisplay_%s.root" %RunNumber)) ### Analyzed output file with histograms
### pion beam
process.TFileService = cms.Service("TFileService", fileName = cms.string("../../../analysis/hist/pion/withLead/region2/HGC_Output_EventDisplay_%s.root" %RunNumber))

########Activate this to produce event displays#########################################
process.p =cms.Path(process.hgcaltbdigis*process.hgcaltbrechits*process.hgcaltbrechitsplotter_highgain_new)

################Not needed for DQM purposes, produces digi histograms for each channel, and the pedestal txt file needed for Digi->Reco
#process.p =cms.Path(process.hgcaltbdigis*process.hgcaltbdigisplotter)

################Produces Reco histograms for each channel as well as a scatter plot of the Reco per channel####################
#process.p =cms.Path(process.hgcaltbdigis*process.hgcaltbrechits*process.hgcaltbrechitsplotter_highgain_correlation_cm)

#################Produces Clusters of Recos(7cells, 19cells and all cells(full hexagons only))################
#process.p =cms.Path(process.hgcaltbdigis*process.hgcaltbrechits*process.LayerSumAnalyzer)

process.end = cms.EndPath(process.output)
