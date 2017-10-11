#-------------------------------------------------------------------------------
# Name  	    	: PreProcess.pyt
# ArcGIS Version	: ArcGIS 10.1 +
# Script Version	: 20130706
# Name of Company 	: Environmental System Research Institute
# Author        	: ESRI raster solution team
# Purpose 	    	: Collection of tools required for Mosaic Datasets.
# Required Argument 	: Not applicable
# Optional Argument 	: Not applicable
# Usage         	: Load tools_md.pyt within ArcMap
# Copyright	    : (c) ESRI 2013
# License	    : <your license>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import arcpy
from arcpy import env
import sys, os
import subprocess
from xml.dom import minidom
#import tempfile
from datetime import date

##solutionLib = os.path.dirname(__file__)
##configBase = os.path.dirname(os.path.dirname(__file__)) + "/Parameter/Config"
##pythonPath = os.path.dirname(os.path.dirname(os.__file__)) + "/python.exe"
# tempPath = tempfile.gettempdir()



solutionLib_path = os.path.dirname(os.path.realpath(__file__))
solutionLib_path = os.path.join(os.path.dirname(solutionLib_path), "Scripts")
pythonPath = os.path.dirname(os.path.dirname(os.__file__)) + "/python.exe"
configBase = os.path.dirname(os.path.dirname(__file__)) + "/Parameter/Config/"

sys.path.append(solutionLib_path)
import MDCS


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Process Ortho"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [createSourceMD,createDerivedMD]

class createSourceMD(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Source Mosaic"
        self.description = ""
        self.canRunInBackground = True

        self.tool = 'createSourceMD'
#        self.UI = UI()


    def getParameterInfo(self):

        """Define parameter definitions"""
        refGroup = 'Reference Mosaic Datasets'

        workspace = arcpy.Parameter(
        displayName="Output Geodatabase",
        name="workspace",
        datatype="DEType",
        parameterType="Required",
        direction="Input")
        #workspace.filter.list = ["Local Database","File System"]

        md_name = arcpy.Parameter(
        displayName="Mosaic Dataset Name",
        name="md_name",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        spref = arcpy.Parameter(
        displayName="Spatial Reference",
        name="spref",
        datatype="GPCoordinateSystem",
        parameterType="Required",
        direction="Input")
        spref.value = 3857

        datapath = arcpy.Parameter(
        displayName="Input Data",
        name="datapath",
        #datatype="DEGeodatasetType",
        datatype="DEFolder",
        parameterType="Required",
        direction="Input")

        inYear = arcpy.Parameter(
        displayName="Year (YYYY)",
        name="inYear",
        datatype="GPLong",
        parameterType="Required",
        direction="Input")

        inMonth = arcpy.Parameter(
        displayName="Month",
        name="inMonth",
        datatype="GPLong",
        parameterType="Required",
        direction="Input")
        inMonth.filter.list = [1,2,3,4,5,6,7,8,9,10,11,12]
        inMonth.value = 1

        leaf = arcpy.Parameter(
        displayName="Leaf",
        name="leaf",
        datatype="GPString",
        parameterType="Required",
        direction="Input")
        leaf.enabled = True
        leaf.filter.list = ["On","Off","Unknown"]
        leaf.value = "On"

        bfootprint = arcpy.Parameter(
        displayName="Footprint ",
        name="bfootprint",
        datatype="GPString",
        parameterType="Required",
        direction="Input")
        bfootprint.enabled = True
        bfootprint.filter.list = ["Remove black edges around imagery","Do not trim tiles as they are edge matched"]
        bfootprint.value = "Remove black edges around imagery"

        sourceurl = arcpy.Parameter(
        displayName="Source URL",
        name="sourceurl",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")

        metadataurl = arcpy.Parameter(
        displayName="MetaData URL",
        name="metadataurl",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")

        parameters = [workspace,md_name,spref,datapath,bfootprint,inYear,leaf,sourceurl,metadataurl]
        return parameters

    def isLicensed(parameters):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):

        if (parameters[0].altered == True):
            gdbValue = parameters[0].valueAsText
            mdsValue = ''
            if (parameters[1].altered == True):
                mdsValue = parameters[1].valueAsText

            mdsDesc = arcpy.Describe(parameters[0].value)

            if hasattr(mdsDesc, "dataType"):

                if (mdsDesc.dataType == 'MosaicDataset'):
                    parameters[2].value = str(mdsDesc.spatialReference.factorycode)
                    parameters[2].enabled = False

                    if (mdsValue != ''):
                        parameters[0].value = os.path.dirname(gdbValue)
                        if (parameters[1].valueAsText != os.path.basename(gdbValue)):
                            parameters[1].value = os.path.basename(gdbValue)
                    else:
                        parameters[0].value = os.path.dirname(gdbValue)
                        parameters[1].value = os.path.basename(gdbValue)
                else:
                    parameters[2].enabled = True

        return parameters

    def updateMessages(self, parameters):
        """ test"""

##        if (parameters[0].altered == True):
##            gdbValue = parameters[0].valueAsText
##            gdbDesc = arcpy.Describe(gdbValue)
##            if hasattr(gdbDesc,"dataType"):
##                if (gdbDesc.dataType != 'Workspace'):
##                    parameters[0].SetErrorMessage("Invalid data type. Select a Mosaic Dataset or Geodatabase.")
##                    return
##                else:
##                    parameters[0].clearMessage
##
##            if (parameters[1].altered == True):
##                mdvalue = parameters[1].valueAsText
##                mdchkValue = arcpy.Exists(os.path.join(gdbValue,mdvalue))
##                if (mdchkValue == False):
##                    if (parameters[2].altered == False):
##                        #parameters[1].SetWarningMessage("New Mosaic Dataset specified, please select the input data.")
##                        pass
##                    else:
##                        parameters[1].clearMessage
##                else:
##                    parameters[1].clearMessage

        return parameters

    def execute(self, parameters, messages):
        """The source code of the tool."""


        for pr in parameters:
            if (pr.hasError() or pr.hasWarning()):
                return

        workspace = parameters[0].valueAsText
        md_name = parameters[1].valueAsText
        datapath = parameters[3].valueAsText
        ssrs = parameters[2].ValueAsText
        sYear = parameters[5].value
        bfootprint = parameters[4].valueAsText
#        inMonth = parameters[6].value
        useLeaf = parameters[6].valueAsText
        sourceURL = parameters[7].valueAsText
        mURL = parameters[8].valueAsText


        sourceMD = '-m:' + os.path.join(workspace,md_name)
        if bfootprint.lower() == 'remove black edges around imagery' :
            configName = 'PreProcess/S_CCMs_Generic.xml'
        elif bfootprint.lower() == 'do not trim tiles as they are edge matched' :
            configName = 'PreProcess/S_TiledOrthos_Generic.xml'
        sourcePara = '-i:'+ os.path.join(configBase, configName )
        arcpy.AddMessage(solutionLib_path)
#        args = [pythonPath, os.path.join(solutionLib_path,'MDCS.py'), '#gprun']

        args= []
        args = ['#gprun']

        args.append(sourcePara)
        args.append(sourceMD)

        data = '-s:'+ datapath
        args.append(data)


        ssrsReplace = '-P:' + str(ssrs) + '$' +'sSRS'
        args.append(ssrsReplace)
##        if parameters[3].altered == True:
##            inYearReplace = '-P:'+str(inYear)+'$'+'sYear'
##            args.append(inYearReplace)
##        if parameters[4].altered == True:
##            sMonthReplace = '-P:'+str(inMonth)+'$'+'sMonth'
##            args.append(sMonthReplace)
##        refdate = date(1899,12,30)
###        indate = date(int(inYear),int(inMonth),1)
##
##        indays = (sDate - refdate).days
##        indaysReplace = '-P:'+ str(indays)+'$'+'sDate'
##        args.append(indaysReplace)
        sYearReplace = '-p:' + str(sYear) + '$'+'sYear'
        args.append(sYearReplace)
        sLeafReplace = '-p:'+ str(useLeaf) +'$'+'sLeaf'
        args.append(sLeafReplace)
        sourceURLReplace  = '-p:'+ str(sourceURL) +'$'+'sSource'
        args.append(sourceURLReplace)
        mURLReplace = '-p:'+str(mURL) + '$'+'smURL'
        args.append(mURLReplace)

        messages.addMessage(args)

        argc = len(args)
        ret = MDCS.main(argc, args)

        #p = subprocess.Popen(args, creationflags=subprocess.SW_HIDE, shell=True, stdout=subprocess.PIPE)
#        p = subprocess.Popen(args, creationflags=subprocess.SW_HIDE, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
##        message = ''
##        while True:
##            message = p.stdout.readline()
##            if not message:
##                break
##            arcpy.AddMessage(message.rstrip())


        return

class createDerivedMD(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Derived Mosaic"
        self.description = ""
        self.canRunInBackground = True

        self.tool = 'createSourceMD'
#        self.UI = UI()


    def getParameterInfo(self):

        """Define parameter definitions"""

        workspace = arcpy.Parameter(
        displayName="Output Geodatabase",
        name="workspace",
        datatype="DEType",
        parameterType="Required",
        direction="Input")
        #workspace.filter.list = ["Local Database","File System"]

        md_name = arcpy.Parameter(
        displayName="Mosaic Dataset Name",
        name="md_name",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        datapath = arcpy.Parameter(
        displayName="Input Data",
        name="datapath",
        #datatype="DEGeodatasetType",
        datatype="GPMosaicLayer",
        parameterType="Required",
        direction="Input")
        datapath.multiValue = True

        dspref = arcpy.Parameter(
        displayName="Spatial Reference",
        name="dspref",
        datatype="GPCoordinateSystem",
        parameterType="Required",
        direction="Input")
        dspref.value = 3857

        parameters = [workspace,md_name,dspref,datapath]
        return parameters

    def isLicensed(parameters):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):

        if (parameters[0].altered == True):
            gdbValue = parameters[0].valueAsText
            mdsValue = ''
            if (parameters[1].altered == True):
                mdsValue = parameters[1].valueAsText

            mdsDesc = arcpy.Describe(parameters[0].value)

            if hasattr(mdsDesc, "dataType"):

                if (mdsDesc.dataType == 'MosaicDataset'):

                    parameters[2].value = str(mdsDesc.spatialReference.factorycode)
                    parameters[2].enabled = False

                    if (mdsValue != ''):
                        parameters[0].value = os.path.dirname(gdbValue)
                        if (parameters[1].valueAsText != os.path.basename(gdbValue)):
                            parameters[1].value = os.path.basename(gdbValue)
                    else:
                        parameters[0].value = os.path.dirname(gdbValue)
                        parameters[1].value = os.path.basename(gdbValue)
                else:
                    parameters[2].enabled = True

        return parameters

    def updateMessages(self, parameters):
        """ test"""

##        if (parameters[0].altered == True):
##            gdbValue = parameters[0].valueAsText
##            gdbDesc = arcpy.Describe(gdbValue)
##            if hasattr(gdbDesc,"dataType"):
##                if (gdbDesc.dataType != 'Workspace'):
##                    parameters[0].SetErrorMessage("Invalid data type. Select a Mosaic Dataset or Geodatabase.")
##                    return
##                else:
##                    parameters[0].clearMessage
##
##            if (parameters[1].altered == True):
##                mdvalue = parameters[1].valueAsText
##                mdchkValue = arcpy.Exists(os.path.join(gdbValue,mdvalue))
##                if (mdchkValue == False):
##                    if (parameters[3].altered == False):
##                        #parameters[1].SetWarningMessage("New Mosaic Dataset specified, please select the input data.")
##                        pass
##                    else:
##                        parameters[1].clearMessage
##                else:
##                    parameters[1].clearMessage

        return parameters

    def execute(self, parameters, messages):
        """The source code of the tool."""

        dargs = []
        dargs = ['#gprun']

        for pr in parameters:
            if (pr.hasError() or pr.hasWarning()):
                return

        dworkspace = parameters[0].valueAsText
        dmd_name = parameters[1].valueAsText
        dsrs = parameters[2].valueAsText
        ddatapath = parameters[3].valueAsText

        derivedMD = '-m:' + os.path.join(dworkspace,dmd_name)

        configName = 'PreProcess/D_Preprocessed_Generic.xml'
        derivedPara = '-i:'+ os.path.join(configBase, configName )

        dargs.append(derivedPara)
        dargs.append(derivedMD)
        dsrsReplace = '-P:' + str(dsrs) + '$' +'sSRS'
        dargs.append(dsrsReplace)
        ddata = '-s:'+ ddatapath
        dargs.append(ddata)
        messages.addMessage(dargs)


        #p = subprocess.Popen(dargs, creationflags=subprocess.SW_HIDE, shell=True, stdout=subprocess.PIPE)
        argslen = len(dargs)
        ret = MDCS.main(argslen,dargs)

##        message = ''
##        while True:
##            message = p.stdout.readline()
##            if not message:
##                break
##            arcpy.AddMessage(message.rstrip())


        return