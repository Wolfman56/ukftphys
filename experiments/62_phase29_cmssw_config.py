"""
Phase 29 — CMSSW Configuration: Event Dump for run=202016, lumi=209, event=229639465

This CMSSW python config extracts the following from the target event in the
/DoubleMuParked/Run2012C-22Jan2013-v1/AOD dataset:
  - All muon properties (pT, eta, phi, isolation, dxy, dz, chi2, kink)
  - Secondary vertex candidates
  - Trigger paths (HLT_DoubleMu*)
  - Primary vertex
  - Missing transverse energy

USAGE:
  # With GRID certificate access to CMS DAS:
  dasgoclient --query='file run=202016 lumi=209 dataset=/DoubleMuParked/Run2012C-22Jan2013-v1/AOD'
  # Set FILE_PATH below with the returned file path
  cmsRun phase29_cmssw_event_dump.py

  # With CMS Open Data (no credentials):
  # Add root://eospublic.cern.ch/ prefix to the file path
  
IMPORTANT: Run with CMSSW_5_3_X or CMSSW_6_2_X (2012 data era)
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  cmsrel CMSSW_5_3_32_patch3
  cd CMSSW_5_3_32_patch3/src && cmsenv
"""
import FWCore.ParameterSet.Config as cms

# ---- EDIT THIS: replace with the file found by phase29_das_locate.py ----
FILE_PATH = "root://eospublic.cern.ch//eos/opendata/cms/Run2012C/DoubleMuParked/AOD/22Jan2013-v1/000/202/016/AAAAAAAAAAAAAAA.root"
# -------------------------------------------------------------------------

TARGET_RUN  = 202016
TARGET_LUMI = 209
TARGET_EVT  = 229639465

process = cms.Process("EVENTDUMP")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

process.source = cms.Source("PoolSource",
    fileNames=cms.untracked.vstring(FILE_PATH),
    eventsToProcess=cms.untracked.VEventRange(
        cms.untracked.EventRange(TARGET_RUN, TARGET_LUMI, TARGET_EVT,
                                 TARGET_RUN, TARGET_LUMI, TARGET_EVT)
    )
)

# Load Global Tag for Run2012C data
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = "FT53_V21A_AN6::All"

# Load muon reconstruction
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

# Custom analyzer to print muon properties
process.muonDump = cms.EDAnalyzer("MuonAnalyzer",
    muonTag   = cms.InputTag("muons"),
    vertexTag = cms.InputTag("offlinePrimaryVertices"),
    metTag    = cms.InputTag("pfMet"),
)

# Simple event content dump (alternative: use EDM event content dumper)
process.edmDump = cms.EDAnalyzer("EventContentAnalyzer")

process.p = cms.Path(process.muonDump + process.edmDump)

process.output = cms.OutputModule("PoolOutputModule",
    fileName=cms.untracked.string("phase29_event_dump.root"),
    outputCommands=cms.untracked.vstring(
        "keep *_muons_*_*",
        "keep *_offlinePrimaryVertices_*_*",
        "keep *_offlineBeamSpot_*_*",
        "keep *_pfMet_*_*",
        "keep *_TriggerResults_*_HLT",
        "keep *_hltTriggerSummaryAOD_*_HLT",
        "keep *_inclusiveSecondaryVertices_*_*",
        "keep *_combinedSecondaryVertex*_*_*",
    ),
    SelectEvents=cms.untracked.PSet(
        SelectEvents=cms.vstring("p")
    )
)
process.e = cms.EndPath(process.output)
