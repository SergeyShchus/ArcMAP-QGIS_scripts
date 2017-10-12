#-------------------------------------------------------------------------------
# Name              : Elevation Tools.pyt
# ArcGIS Version    : ArcGIS 10.1 sp1
# Script Version    : 20130225
# Name of Company     : Environmental System Research Institute
# Author            : ESRI raster solution team
# Date              : 16-09-2012
# Purpose             : This script is to build Gptool to work in ArcGIS enviroment
# Created            : 14-08-2012
# LastUpdated          : 17-09-2012
# Required Argument     : Not applicable
# Optional Argument     : Not applicable
# Usage         :  To run within ArcMap/Model Builder.
# Copyright        : (c) ESRI 2012
# License        : <your license>
#-------------------------------------------------------------------------------

import arcpy
from arcpy import env
import sys, os
import subprocess

solutionLib_path = os.path.dirname(os.path.realpath(__file__))
pythonPath = os.path.dirname(os.path.dirname(os.__file__)) + "/python.exe"

#sys.path.append(solutionLib_path)
import MDCS
import solutionsLib
from xml.dom import minidom
#config editor
UIElements = {
'source' : {
   'displayName' : 'source inputs',
   'list' : {
        'workspace' : ['Local Database'],
        'artfile' : ['xml','art']
   },
   'UIOrder' : [
        'input_cfg',
        'output_cfg',
        'outputName',
        'cmd',
        'workspace',
        'md_name',
        'srs',
        'datapath',
        'artfile',
        'artfilter',
        'datasetid',
        'le90',
        'ce90',
        'startdt',
        'enddt',
        'source_url',
        'vert_datum',
        'metadata',
        'dem_type'
        ],
   'datatype' : {
        'workspace' : 'Workspace',
        'md_name' : 'String',
        'input_cfg' : 'DEFile',
        'output_cfg' : 'DEFile',
        'outputName' : 'String',
        'cmd' : 'String',
        'srs' : 'GPCoordinateSystem',
        'artfile' : 'GPType',
        'artfilter' : 'String',
        'datasetid' : 'String',
        'le90' : 'Double',
        'ce90' : 'Double',
        'startdt' : 'Date',
        'enddt' : 'Date',
        'source_url' : 'String',
        'vert_datum' : 'String',
        'metadata' : 'String',
        'dem_type' : 'Long',
        'datapath' : 'Folder'
    },
    'displaylabel' : {
        'workspace' : 'Path to the geodatabase',
        'md_name' : 'Mosaic dataset name',
        'input_cfg' : 'Input Configuration File',
        'output_cfg' : 'Output config',
        'outputName' : 'Output Configuration File Name',
        'cmd' : 'Command(s)',
        'srs' : 'Spatial Reference',
        'artfile' : 'Raster Type',
        'artfilter' : 'Filter',
        'datasetid' : 'Dataset ID',
        'le90' : 'LE 90',
        'ce90' : 'CE 90',
        'startdt' : 'Start Date',
        'enddt' : 'End Date',
        'source_url' : 'Source URL',
        'vert_datum' : 'Vertical Datum',
        'metadata' : 'Metadata Link',
        'dem_type' : 'DEM Type',
        'datapath' : 'Data path'


    },
    'category' : {
        'Calculate Values' :
        {
            'datasetid' : '',
            'le90' : '',
            'ce90' : '',
            'startdt' : '',
            'enddt' : '',
            'source_url' : '',
            'vert_datum' : '',
            'metadata' : '',
            'dem_type' : ''
        },
        'Add Raster Parameters' :
         {
            'datapath' : '',
            'artfile' : '',
            'artfilter' : ''
         }

    },
    'paramType' : {
        'input_cfg' : 'Required',
        'output_cfg' : 'Derived'
    },
    'direction' : {
        'output_cfg' : 'Output'
    },

    'controlStatus' : {
        'derived' : {
            'input_cfg' : '',
            'output_cfg' : '',
            'cmd' : '',
            'workspace' : '',
            'md_name' : '',
            'srs' : '',
            'artfile' : '',
            'artfilter' : '',
            'outputName': '',
            'datapath' : ''
            },
        'referenced' : {
            'input_cfg' : '',
            'output_cfg' : '',
            'cmd' : '',
            'workspace' : '',
            'md_name' : '',
            'srs' : '',
#            'artfile' : '',
            'outputName':'',
            'artfilter' : '',
            'datapath' : ''
            }

    },
    'xpath' :
    {
        'cmd' :
        {
            'node' : 'Command',
            'key' : 'Application/Command'
        },
        'datapath' :
        {
            'node' : 'data_path',
            'key' : 'Application/Workspace/MosaicDataset/AddRasters/AddRaster/Sources/data_path'
        },

        'workspace' :
        {
            'node' : 'WorkspacePath',
            'key' : 'Application/Workspace/WorkspacePath'
        },
        'md_name' :
        {
            'node' : 'Name',
            'key' : 'Application/Workspace/MosaicDataset/Name'
        },
        'srs' :
        {
            'node' : 'SRS',
            'key' : 'Application/Workspace/MosaicDataset/SRS'
        },
        'artfile' :
        {
            'node' : 'raster_type',
            'key' : 'Application/Workspace/MosaicDataset/AddRasters/AddRaster/raster_type'
        },
        'artfilter' :
        {
            'node' : 'Filter',
            'key' : 'Application/Workspace/MosaicDataset/AddRasters/AddRaster/Filter'
        },
        'datasetid' :
        {
            'node' : 'dataset_id',
            'key' : 'Application/Workspace/MosaicDataset/AddRasters/AddRaster/dataset_id'
        },
        'le90' :
        {
            'node' : 'FieldName',
            'key' : 'Application/Workspace/MosaicDataset/Processes/CalculateValues/CalculateValue/FieldName',
            'sub_key' : 'Expression'
        },
        'ce90' :
        {
            'node' : 'FieldName',
            'key' : 'Application/Workspace/MosaicDataset/Processes/CalculateValues/CalculateValue/FieldName',
            'sub_key' : 'Expression'
        },
        'startdt' :
        {
            'node' : 'FieldName',
            'value' : 'Date_Start',
            'key' : 'Application/Workspace/MosaicDataset/Processes/CalculateValues/CalculateValue/FieldName',
            'sub_key' : 'Expression'
        },
        'enddt' :
        {
            'node' : 'FieldName',
            'value' : 'Date_End',
            'key' : 'Application/Workspace/MosaicDataset/Processes/CalculateValues/CalculateValue/FieldName',
            'sub_key' : 'Expression'
        },
        'source_url' :
        {
            'node' : 'FieldName',
            'value' : 'Source_URL',
            'key' : 'Application/Workspace/MosaicDataset/Processes/CalculateValues/CalculateValue/FieldName',
            'sub_key' : 'Expression'
        },
        'vert_datum' :
        {
            'node' : 'FieldName',
            'value' : 'VerticalDatum',
            'key' : 'Application/Workspace/MosaicDataset/Processes/CalculateValues/CalculateValue/FieldName',
            'sub_key' : 'Expression'
        },
        'metadata' :
        {
            'node' : 'FieldName',
            'value' : 'Metadata',
            'key' : 'Application/Workspace/MosaicDataset/Processes/CalculateValues/CalculateValue/FieldName',
            'sub_key' : 'Expression'
        },
        'dem_type' :
        {
            'node' : 'FieldName',
            'value' : 'DEM_Type',
            'key' : 'Application/Workspace/MosaicDataset/Processes/CalculateValues/CalculateValue/FieldName',
            'sub_key' : 'Expression'
        }

    }   #xpath
}
}


const_string_datatype_  = 'datatype'
const_string_displayname_ = 'displaylabel'
const_string_UI_direction_ = 'direction'
const_string_UI_paramType_ = 'paramType'
const_string_UI_xpath_ = 'xpath'
const_string_UI_category_ = 'category'
const_string_UI_status_ = 'controlStatus'
const_string_UI_order_ = 'UIOrder'
#ends

class Toolbox(object):

    def __init__(self):
        ##Define the toolbox (the name of the toolbox is the name of the.pyt file).##
        self.label = "ElevationTools"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool, DerivedMD, ToolConfig]

class Tool(object):
    doc = None
    def __init__(self):
        ##Define the tool (tool name is the name of the class).##
        self.label = "Source Mosaic Dataset"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        ##Define parameter definitions##
        config = arcpy.Parameter(
        displayName = "Configuration File",
        name = "Configuration File",
        datatype = "DEFile",
        parameterType = "Required",
        direction = "Input")

        com = arcpy.Parameter(
        displayName = "Command",
        name = "command",
        datatype = "GPString",
        parameterType = "Optional",
        direction = "Input")

        gdbPath = arcpy.Parameter(
        displayName = "Path to the geodatabase",
        name = "Path to the geodatabase",
        datatype = "DEWorkspace",
        parameterType = "Optional",
        direction = "Input")
        gdbPath.filter.list = ["Local Database"]

        mdname = arcpy.Parameter(
        displayName = "Mosaic Dataset Name",
        name = "Mosaic Dataset Name",
        datatype = "GPString",
        parameterType = "Optional",
        direction = "Input")

        dataPath = arcpy.Parameter(
        displayName = "Input Data Path",
        name = "Input Data Path",
        datatype = "DEFolder",
        parameterType = "Optional",
        direction = "Input",
        multiValue=True)


        mdPath = arcpy.Parameter(
        displayName = "Mosaic Dataset Path",
        name = "Mosaic Dataset Path",
        datatype = "GPMosaicLayer",
        parameterType = "Derived",
        direction = "Output")

        params = [config, com,gdbPath,mdname,dataPath,mdPath]

        return params

    def isLicensed(self):
        ##Set whether tool is licensed to execute.##
        return True

    def getXMLNode(self, doc, nodeName) :
        if (doc == None):
            return ''
        node = doc.getElementsByTagName(nodeName)
        if (node == None or
            node.length == 0 or
            node[0].firstChild.nodeType != minidom.Node.TEXT_NODE):
            return ''

        return node[0]


    def setXMLNodeValue1(self, doc, xPath, key, value, sub_key, sub_value):

        nodes = doc.getElementsByTagName(key)
        for node in nodes:
            parents = []
            c = node
            while(c.parentNode != None):
                parents.insert(0, c.nodeName)
                c = c.parentNode
            p = '/'.join(parents)
            if (p == xPath):
                if (sub_key != ''):
                    try:
                        if (node.firstChild.nodeValue == value):       #taking a short-cut to edit/this could change in future to support any child-node lookup
                            if (node.nextSibling.nextSibling.nodeName == sub_key):
                                node.nextSibling.nextSibling.firstChild.data = sub_value
                            break
                    except:
                        break
                    continue

                node.firstChild.data  = value
                break

    def updateParameters(self, parameters):
        ##Modify the values and properties of parameters before internal validation is performed.  This method is called whenever a parameter has been changed.##
        import Base
        import ProcessInfo

        config_s = ''
        try:
            apply_change = False
            config_s = parameters[0].valueAsText
            self.doc = minidom.parse(config_s)
            base = Base.Base()
            hshProcessInfo = ProcessInfo.ProcessInfo(base)
            bSuccess = hshProcessInfo.init(config_s)

            if (parameters[0].altered) == True:
                try:
                    apply_change = True

                except:
                    Warning = True

            if (apply_change == True):
                for p in parameters:
                    ctrl_name = p.name
                    if (not p.altered):
                        try:
                            if (ctrl_name == 'Mosaic Dataset Name'):
                                p.value = hshProcessInfo.mdName
                            elif(ctrl_name == 'Path to the geodatabase'):
                                p.value = hshProcessInfo.geoPath
                            elif(ctrl_name == 'command'):
                                p.value = hshProcessInfo.commands
                        except:
                            Error = True

        except:
            Error = True


        if (config_s == 'None' or config_s == ''):
            return

        if (os.path.exists(str(config_s)) == False):
            arcpy.AddMessage('Error: Input config file doesn\'t exist!')
            return


        parameters[5].value = str(parameters[2].valueAsText) + "/" + str(parameters[3].valueAsText)
        if parameters[2].hasError():
            parameters[2].clearMessage()
        return

    def updateMessages(self, parameters):
        ##Modify the messages created by internal validation for each tool parameter.  This method is called after internal validation.##
        return

    def execute(self, parameters, messages):
        ##The source code of the tool.##
#config, com,gdbPath,mdname,dataPath,mdPath
        #args = [pythonPath, os.path.join(solutionLib_path,'MDCS.py'), '#gprun']
        args = ['#gprun']

        if not parameters[0].valueAsText == None:
            config = '-i:'+ parameters[0].valueAsText
            args.append(config)
        if not parameters[1].valueAsText == None:
            com = '-c:'+ parameters[1].valueAsText
            args.append(com)
        if not parameters[2].valueAsText == None and \
            not parameters[3].valueAsText == None:

            gdbPath = parameters[2].valueAsText
            mdName = parameters[3].valueAsText
            full_path_ = '-m:' + os.path.join(gdbPath, mdName)
            args.append(full_path_)

        if not parameters[4].valueAsText == None:
            datapath = '-s:'+ parameters[4].valueAsText
            args.append(datapath)
        messages.addMessage(args)

        argc = len(args)
        ret = MDCS.main(argc, args)

##        p = subprocess.Popen(args, creationflags=subprocess.SW_HIDE, shell=True, stdout=subprocess.PIPE)
##        message = ''
##        while True:
##            message = p.stdout.readline()
##            if not message:
##                break
##            arcpy.AddMessage(message.rstrip())      #remove newline before adding.

        return

class DerivedMD(object):
    def __init__(self):
        ##Define the tool (tool name is the name of the class).##
        self.label = "Derived Mosaic Dataset"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        ##Define parameter definitions##
        config = arcpy.Parameter(
        displayName = "Configuration File",
        name = "Configuration File",
        datatype = "DEFile",
        parameterType = "Required",
        direction = "Input")

        com = arcpy.Parameter(
        displayName = "command",
        name = "command",
        datatype = "GPString",
        parameterType = "Optional",
        direction = "Input")

        gdbPath = arcpy.Parameter(
        displayName = "Path to the geodatabase",
        name = "Path to the geodatabase",
        datatype = "DEWorkspace",
        parameterType = "Optional",
        direction = "Input")
        gdbPath.filter.list = ["Local Database"]

        mdname = arcpy.Parameter(
        displayName = "Mosaic Dataset Name",
        name = "Mosaic Dataset Name",
        datatype = "GPString",
        parameterType = "Optional",
        direction = "Input")

        dataPath = arcpy.Parameter(
        displayName = "Input Data Path",
        name = "Input Data Path",
        datatype = "GPMosaicLayer",
        parameterType = "Optional",
        direction = "Input",
        multiValue=True)

        mdPath = arcpy.Parameter(
        displayName = "Mosaic Dataset Path",
        name = "Mosaic Dataset Path",
        datatype = "GPMosaicLayer",
        parameterType = "Derived",
        direction = "Output")

        params = [config, com,gdbPath,mdname,dataPath,mdPath]

        return params

    def isLicensed(self):
        ##Set whether tool is licensed to execute.##
        return True

    def getXMLNode(self, doc, nodeName) :
        if (doc == None):
            return ''
        node = doc.getElementsByTagName(nodeName)
        if (node == None or
            node.length == 0 or
            node[0].firstChild.nodeType != minidom.Node.TEXT_NODE):
            return ''

        return node[0]


    def setXMLNodeValue1(self, doc, xPath, key, value, sub_key, sub_value):

        nodes = doc.getElementsByTagName(key)
        for node in nodes:
            parents = []
            c = node
            while(c.parentNode != None):
                parents.insert(0, c.nodeName)
                c = c.parentNode
            p = '/'.join(parents)
            if (p == xPath):
                if (sub_key != ''):
                    try:
                        if (node.firstChild.nodeValue == value):       #taking a short-cut to edit/this could change in future to support any child-node lookup
                            if (node.nextSibling.nextSibling.nodeName == sub_key):
                                node.nextSibling.nextSibling.firstChild.data = sub_value
                            break
                    except:
                        break
                    continue

                node.firstChild.data  = value
                break


    def updateParameters(self, parameters):
        ##Modify the values and properties of parameters before internal validation is performed.  This method is called whenever a parameter has been changed.##
        import Base
        import ProcessInfo

        config_d = ''
        try:
            apply_change = False
            config_d = parameters[0].valueAsText
            self.doc = minidom.parse(config_d)
            base = Base.Base()
            hshProcessInfo = ProcessInfo.ProcessInfo(base)
            bSuccess = hshProcessInfo.init(config_d)

            if (parameters[0].altered) == True:
                try:
                    apply_change = True

                except:
                    Warning = True

            if (apply_change == True):
                for p in parameters:
                    ctrl_name = p.name
                    if (not p.altered):
                        try:
                            if (ctrl_name == 'Mosaic Dataset Name'):
                                p.value = hshProcessInfo.mdName
                            elif(ctrl_name == 'Path to the geodatabase'):
                                p.value = hshProcessInfo.geoPath
                            elif(ctrl_name == 'command'):
                                p.value = hshProcessInfo.commands
                        except:
                            Error = True
        except:
            Error = True

        if (config_d == 'None' or config_d == ''):
            return

        if (os.path.exists(str(config_d)) == False):
            arcpy.AddMessage('Error: Input config file doesn\'t exist!')
            return

        parameters[5].value = str(parameters[2].valueAsText) + "/" + str(parameters[3].valueAsText)
        if parameters[2].hasError():
            parameters[2].clearMessage()
        return

    def updateMessages(self, parameters):
        ##Modify the messages created by internal validation for each tool parameter.  This method is called after internal validation.##
        return

    def execute(self, parameters, messages):
        ##The source code of the tool.##

        #args = [pythonPath, os.path.join(solutionLib_path,'MDCS.py'), '#gprun']
        args = ['#gprun']

        if not parameters[0].valueAsText == None:
            config = '-i:'+ parameters[0].valueAsText
            args.append(config)
        if not parameters[1].valueAsText == None:
            com = '-c:'+ parameters[1].valueAsText
            args.append(com)
        if not parameters[2].valueAsText == None and \
            not parameters[3].valueAsText == None:

            gdbPath = parameters[2].valueAsText
            mdName = parameters[3].valueAsText
            full_path_ = '-m:' + os.path.join(gdbPath, mdName)
            args.append(full_path_)

        if not parameters[4].valueAsText == None:
            datapath = '-s:'+ parameters[4].valueAsText
            args.append(datapath)

        messages.addMessage(args)
        argc = len(args)
        ret = MDCS.main(argc, args)

##        p = subprocess.Popen(args, creationflags=subprocess.SW_HIDE, shell=True, stdout=subprocess.PIPE)
##        message = ''
##        while True:
##            message = p.stdout.readline()
##            if not message:
##                break
##            arcpy.AddMessage(message.rstrip())      #remove newline before adding.

        return


    def isLicensed(self):
        ##Set whether tool is licensed to execute.##
        return True

    def getXMLNode(self, doc, nodeName) :
        if (doc == None):
            return ''
        node = doc.getElementsByTagName(nodeName)
        if (node == None or
            node.length == 0 or
            node[0].firstChild.nodeType != minidom.Node.TEXT_NODE):
            return ''

        return node[0]


    def setXMLNodeValue1(self, doc, xPath, key, value, sub_key, sub_value):

        nodes = doc.getElementsByTagName(key)
        for node in nodes:
            parents = []
            c = node
            while(c.parentNode != None):
                parents.insert(0, c.nodeName)
                c = c.parentNode
            p = '/'.join(parents)
            if (p == xPath):
                if (sub_key != ''):
                    try:
                        if (node.firstChild.nodeValue == value):       #taking a short-cut to edit/this could change in future to support any child-node lookup
                            if (node.nextSibling.nextSibling.nodeName == sub_key):
                                node.nextSibling.nextSibling.firstChild.data = sub_value
                            break
                    except:
                        break
                    continue

                node.firstChild.data  = value
                break

    def updateParameters(self, parameters):
        ##Modify the values and properties of parameters before internal validation is performed.  This method is called whenever a parameter has been changed.##

        import Base
        import ProcessInfo

        config_r = ''
        try:
            apply_change = False
            config_r = parameters[0].valueAsText
            self.doc = minidom.parse(config_r)
            base = Base.Base()
            hshProcessInfo = ProcessInfo.ProcessInfo(base)
            bSuccess = hshProcessInfo.init(config_r)

            if (parameters[0].altered) == True:
                try:
                    apply_change = True

                except:
                    Warning = True

            if (apply_change == True):
                for p in parameters:
                    ctrl_name = p.name
                    if (not p.altered):
                        try:
                            if (ctrl_name == 'Mosaic Dataset Name'):
                                p.value = hshProcessInfo.mdName
                            elif(ctrl_name == 'Path to the geodatabase'):
                                p.value = hshProcessInfo.geoPath
                            elif(ctrl_name == 'command'):
                                p.value = hshProcessInfo.commands
                        except:
                            Error = True
        except:
            Error = True

        if (config_r == 'None' or config_r == ''):
            return

        if (os.path.exists(str(config_r)) == False):
            arcpy.AddMessage('Error: Input config file doesn\'t exist!')
            return


        parameters[5].value = str(parameters[2].valueAsText) + "/" + str(parameters[3].valueAsText)
        if parameters[2].hasError():
            parameters[2].clearMessage()
        return

    def updateMessages(self, parameters):
        ##Modify the messages created by internal validation for each tool parameter.  This method is called after internal validation.##
        return

    def execute(self, parameters, messages):
        ##The source code of the tool.##

        #args = [pythonPath, os.path.join(solutionLib_path,'MDCS.py'), '#gprun']
        args = ['#gprun']

        if not parameters[0].valueAsText == None:
            config = '-i:'+ parameters[0].valueAsText
            args.append(config)
        if not parameters[1].valueAsText == None:
            com = '-c:'+ parameters[1].valueAsText
            args.append(com)
        if not parameters[2].valueAsText == None and \
            not parameters[3].valueAsText == None:

            gdbPath = parameters[2].valueAsText
            mdName = parameters[3].valueAsText
            full_path_ = '-m:' + os.path.join(gdbPath, mdName)
            args.append(full_path_)

        if not parameters[4].valueAsText == None:
            datapath = '-s:'+ parameters[4].valueAsText
            args.append(datapath)

        messages.addMessage(args)
        argc = len(args)
        ret = MDCS.main(argc, args)

##        p = subprocess.Popen(args, creationflags=subprocess.SW_HIDE, shell=True, stdout=subprocess.PIPE)
##        message = ''
##        while True:
##            message = p.stdout.readline()
##            if not message:
##                break
##            arcpy.AddMessage(message.rstrip())      #remove newline before adding.

        return


class ToolConfig(object):

    doc = None

    def __init__(self):
        ##Define the tool (tool name is the name of the class).##
        self.label = "Configuration Editor"
        self.description = ""
        self.canRunInBackground = False

    def getXMLNodeValue(self, doc, nodeName) :
        if (doc == None):
            return ''
        node = doc.getElementsByTagName(nodeName)
        if (node == None or
            node.length == 0 or
            node[0].firstChild.nodeType != minidom.Node.TEXT_NODE):
            return ''

        return node[0].firstChild.data


    def getParameterInfo(self):

        params = []

        active_tool_ = 'source'
        for key in UIElements:
            for key in UIElements[active_tool_][const_string_UI_order_]:

                dataType = 'String'

                if (UIElements[active_tool_][const_string_datatype_].has_key(key)):
                    dataType = UIElements[active_tool_][const_string_datatype_][key]
                    if (dataType.lower() == 'boolean'):
                        isTrue = False

                displayLabel  = key.replace('_', ' ').title()
                if (UIElements[active_tool_].has_key(const_string_displayname_)):
                    if (UIElements[active_tool_][const_string_displayname_].has_key(key)):
                            displayLabel = UIElements[active_tool_][const_string_displayname_][key]


                #chs
                UI_direction = 'Input'
                if (UIElements[active_tool_].has_key(const_string_UI_direction_)):
                    if (UIElements[active_tool_][const_string_UI_direction_].has_key(key)):
                            UI_direction = UIElements[active_tool_][const_string_UI_direction_][key]


                UI_paramType = 'Optional'
                if (UIElements[active_tool_].has_key(const_string_UI_paramType_)):
                    if (UIElements[active_tool_][const_string_UI_paramType_].has_key(key)):
                            UI_paramType = UIElements[active_tool_][const_string_UI_paramType_][key]


                multivalue_ = 'False'
                if (key == 'datapath'):
                    multivalue_ = True
                    dataType = ['Folder', 'File']
##                elif(key == 'artfile'):
##                    dataType = 'File'#GPRasterBuilder' #['String', 'File']

                inputXML = arcpy.Parameter(
                displayName=displayLabel,
                name= active_tool_ + ':' + key,
                datatype=dataType,
                parameterType=UI_paramType,
                direction=UI_direction,
                multiValue=multivalue_)


                for k in UIElements[active_tool_][const_string_UI_category_]:
                    if (UIElements[active_tool_][const_string_UI_category_][k].has_key(key)):
                        inputXML.category = k
                        break;

##                if (UIElements[active_tool_]['list'].has_key(key)):
##                        inputXML.filter.list = UIElements[active_tool_]['list'][key]


                params.append(inputXML)

        return params


    def isLicensed(self):
        ##Set whether tool is licensed to execute.##
        return True

    def updateParameters(self, parameters):
        ##Modify the values and properties of parameters before internal validation is performed.  This method is called whenever a parameter has been changed.##

  #      sys.path.append(os.path.join(solutionLib_path, 'Base'))
 #       sys.path.append(os.path.join(solutionLib_path, 'ProcessInfo'))

        import Base
        import ProcessInfo

        config_ = ''
        active_tool_ = 'source'
        if not parameters[2].altered:
            parameters[1].value = str(parameters[0].value)
        else:
            parameters[1].value =os.path.join(os.path.dirname(str(parameters[0].value)),(str(parameters[2].value)+".xml"))
        try:
            apply_change = False
            for p in parameters:
                ctrl_name = p.name
                if (ctrl_name == 'source:input_cfg'):
                    config_ = str(p.value)
#                    config_ = p.value
                    self.doc = minidom.parse(config_)
                    base = Base.Base()
                    hshProcessInfo = ProcessInfo.ProcessInfo(base)
                    bSuccess = hshProcessInfo.init(config_)

                    if (p.altered):
                        try:
                            apply_change = True

                            break;
                        except:
                            Warning = True

            if (apply_change == True):
                for p in parameters:
                    ctrl_name = p.name
                    sep = ctrl_name.split(':')
                    active_UI_element = sep[1]

                    if (not p.altered):
                        try:
                            mdType = self.getXMLNodeValue(self.doc, u'MosaicDatasetType')
                            if (ctrl_name == 'source:md_name'):
                                p.value = hshProcessInfo.mdName
                            elif(ctrl_name == 'source:workspace'):
                                p.value = hshProcessInfo.geoPath
                            elif(ctrl_name == 'source:cmd'):
                                p.value = hshProcessInfo.commands
                            elif(ctrl_name == 'source:srs'):
                                p.value = self.getXMLNodeValue(self.doc, u'SRS')
                            elif(ctrl_name == 'source:datasetid'):
                                if mdType == 'source':
                                    p.value = self.getXMLNodeValue(self.doc, u'dataset_id')
                            elif(ctrl_name == 'source:artfile'):
                                art_ = self.getXMLNodeValue(self.doc, u'raster_type')
##                                if (os.path.exists(art_) == True):
                                p.value = art_
                            elif(ctrl_name == 'source:artfilter'):
                                p.value = self.getXMLNodeValue(self.doc, u'Filter')
                            elif(ctrl_name == 'source:datapath'):
#                                if mdType != 'Referenced':
                                 p.value = self.getXMLNodeValue(self.doc, u'data_path')
                            else:
                                for k in hshProcessInfo.processInfo['calculatevalues']:
                                    if (UIElements[active_tool_][const_string_UI_xpath_].has_key(active_UI_element)):
                                        fieldname = active_UI_element.upper()
                                        if (UIElements[active_tool_][const_string_UI_xpath_][active_UI_element].has_key('value')):
                                            fieldname = UIElements[active_tool_][const_string_UI_xpath_][active_UI_element]['value']

                                        if (k['fieldname'] == fieldname):
                                           p.value = k['expression']

                        except:
                            Error = True

        except:
            Error = True


        if (config_ == 'None' or config_ == ''):
            return

##        try:
##            c = open('d:/debug.txt', "w")
##            c.write(config_)
##            c.close()
##        except:
##            Error = True

        if (os.path.exists(str(config_)) == False):
            arcpy.AddMessage('Error: Input config file doesn\'t exist!')
            return

        ActiveUITool = self.getXMLNodeValue(self.doc, u'MosaicDatasetType').lower()

        for p in parameters:
            ctrl_name = p.name
            sep = ctrl_name.split(':')
            active_UI_element = sep[1]
            p.enabled = False

            for k in UIElements[active_tool_][const_string_UI_status_]:
                if (UIElements[active_tool_][const_string_UI_status_].has_key(ActiveUITool) == False):
                    p.enabled = True
                    break

                if (UIElements[active_tool_][const_string_UI_status_][ActiveUITool].has_key(active_UI_element)):
                    p.enabled = True
                    break;

        return

    def updateMessages(self, parameters):
        ##Modify the messages created by internal validation for eachx tool parameter.  This method is called after internal validation.##
        try:

            if parameters[0].value != None:
##                if parameters[2].value != None:
##                    parameters[1].value = "dddd"#os.path.dir(str(parameters[0].value)) + "/" + str(parameters[2].value)
                self.doc = minidom.parse((parameters[0].value))

                mdType = self.getXMLNodeValue(self.doc, u'MosaicDatasetType')
                if mdType == 'Referenced':
                    for um in parameters:
                        if um.name == 'source:datapath':
                            if str(um.value).find(';') >= 0:
                                um.setErrorMessage("Referenced Mosaic Dataset takes only one Source as input")
        except:
            Error = True

        try:
            if parameters[1].hasError() == True:
                parameters[1].setWarningMessage("OutFile will be over written")
        except:
            Error = True

##        for um in parameters:
##            if um.name == 'source:artfile':
##                pvalue = str(um.value)
##                if pvalue == 'Table':
##                    um.setWarningMessage('Not a valid Raster Type File')

        return

    def getXMLNode(self, doc, nodeName) :
        if (doc == None):
            return ''
        node = doc.getElementsByTagName(nodeName)
        if (node == None or
            node.length == 0 or
            node[0].firstChild.nodeType != minidom.Node.TEXT_NODE):
            return ''

        return node[0]


    def setXMLNodeValue1(self, doc, xPath, key, value, sub_key, sub_value):

        nodes = doc.getElementsByTagName(key)
        for node in nodes:
            parents = []
            c = node
            while(c.parentNode != None):
                parents.insert(0, c.nodeName)
                c = c.parentNode
            p = '/'.join(parents)
            if (p == xPath):
                if (sub_key != ''):
                    try:
                        if (node.firstChild.nodeValue == value):       #taking a short-cut to edit/this could change in future to support any child-node lookup
                            if (node.nextSibling.nextSibling.nodeName == sub_key):
                                node.nextSibling.nextSibling.firstChild.data = sub_value
                            break
                    except:
                        break
                    continue

                node.firstChild.data  = value
                break


    def execute(self, parameters, messages):
        ##The source code of the tool.##

#        sys.path.append(os.path.join(solutionLib_path, 'Base'))
#        sys.path.append(os.path.join(solutionLib_path, 'ProcessInfo'))

        import Base
        import ProcessInfo
        config_ = ''
        doc = None
        Error = False
        for p in parameters:
            ctrl_name = p.name
            if (ctrl_name == 'source:input_cfg'):
                try:
                    config_ = str(p.value)
                    doc = minidom.parse(config_)

                except:
                    arcpy.AddMessage('*** - Error')
                    Error  = True
                    break

        if (Error == True):
            return


        output_cfg = ''
        active_tool_ = 'source'


        for p in parameters:
            ctrl_name = p.name
            try:
                setValue = ''
                nodeName = ''
                sep = ctrl_name.split(':')
                active_UI_element = sep[1]

                if (ctrl_name == 'source:md_name'):
                    setValue = str(p.value)
                    nodeName = 'Name'
                elif(ctrl_name == 'source:workspace'):
                    setValue = str(p.value)
                    nodeName = 'WorkspacePath'
                elif(ctrl_name == 'source:srs'):
                    setValue = str(p.value)
                    nodeName = 'SRS'
                elif(ctrl_name == 'source:cmd'):
                    setValue = str(p.value)
                    nodeName = 'Command'
                elif(ctrl_name == 'source:output_cfg'):
                    if (p.value != None):
                        output_cfg = str(p.value)
                else:
                    if (p.value != None):
                        setValue = str(p.value)

                if (setValue != ''):
                    if (UIElements[active_tool_][const_string_UI_xpath_].has_key(active_UI_element)):

                        xpath = UIElements[active_tool_][const_string_UI_xpath_][active_UI_element]['key']
                        nodeName = UIElements[active_tool_][const_string_UI_xpath_][active_UI_element]['node']

                        key = xpath
                        value = setValue
                        sub_key = ''
                        sub_value = ''

                        if (UIElements[active_tool_][const_string_UI_xpath_][active_UI_element].has_key('sub_key')):
                            sub_key = UIElements[active_tool_][const_string_UI_xpath_][active_UI_element]['sub_key']
                            sub_value = setValue
                            value = active_UI_element.upper()
                            if (UIElements[active_tool_][const_string_UI_xpath_][active_UI_element].has_key('value')):
                                value = UIElements[active_tool_][const_string_UI_xpath_][active_UI_element]['value']
                        try:
                            if (nodeName ==  'WorkspacePath'):

                                (p, f) = os.path.split(os.path.join(value, 'md'))
                                f = f.strip()
                                const_gdb_ext_len_ = 4
                                if (p[-const_gdb_ext_len_:].lower() == '.gdb'
                                    and f != ''):
                                    p = p.replace('\\', '/')
                                    w = p.split('/')
                                    workspace_ = ''
                                    for i in range(0, len(w) - 1):
                                        workspace_ = w[i] #+ '/'

                                    gdb_ = w[len(w) -1]

                                    geodatabase_ = w[len(w) - 1][:len(gdb_) - const_gdb_ext_len_]
                                    self.setXMLNodeValue1(doc, key, nodeName, workspace_, sub_key, sub_value)

                                    key = 'Application/Workspace/Geodatabase'
                                    nodeName  = 'Geodatabase'
                                    self.setXMLNodeValue1(doc, key, nodeName, gdb_, sub_key, sub_value)
                                continue

                            self.setXMLNodeValue1(doc, key, nodeName, value, sub_key, sub_value)
                        except:
                            Warning = True

            except:
                Error = True


        if (output_cfg == ''):
            output_cfg = config_

        try:
            c = open(output_cfg, "w")
            c.write(doc.toxml())
            c.close()
        except:
            Error = True

        return