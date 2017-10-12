Find further discussion regarding this workflow here:
http://esriurl.com/ManagingElevation

Download sample data in a separate zip file here:
http://esriurl.com/ElevationData

Adapting the workflow to your data

In order to use the tools and batch files demonstrated in the previous sections, steps must be taken to adapt them to your particular data. In this section, you will explore the following tasks:

Setting up your file structure to parallel the sample project
Using the geoprocessing tool with your own data
Creating custom configuration files
Creating and using batch files to automate the workflow with your own data
Note:
Both the geoprocessing tools and batch files call a Python script called MDCS.py. The parameters for this script are specified in the tool dialog box (in the case of the geoprocessing tools) or in xml configuration files (in the case of the batch files). More information about MDCS and the configuration parameters can be found on the MDCS GitHub page.

Set up your file structure

While your project and associated directories can be set up in many ways, these instructions will mirror the sample project structure.

Copy the Managing Elevation workflow directory into C:/Image_Mgmt_Workflows/. Rename the new directory to suit your project.
Ensure that the data, logs, and MD directories are empty.
Copy your data collections into the data directory (organize each collection in a separate folder).
Create the file geodatabase you wish to use and save it to the MD directory.
Using the geoprocessing tools with your data

The geoprocessing tools allow you to use existing XML configuration templates (which provide the input parameters needed to create your mosaic datasets) with limited modifications. Any parameters entered in the Source Mosaic Dataset or Derived Mosaic Dataset tool dialog will take precedence over the parameters in the configuration file.

See the table below for descriptions of the available parameters in the Managing Elevation geoprocessing tools.

Parameter	Description
Configuration File
Path to the configuration file used to build this mosaic dataset. (Parameters set with this tool will take precedence.)
Command
List of two-letter codes representing commands that need to be run on the newly created mosaic dataset. These can be combined using a plus sign (CM+AR+BF, for example), and will be run in the order listed.
Note:
Source and derived mosaic datasets take slightly different input commands from reference mosaic datasets; see the tool dialog boxes for more information about available commands.
Path to the geodatabase
Path and name of the geodatabase where the output mosaic dataset will be created
Note:
This tool will not create a geodatabase; it must exist before you start.
Mosaic Dataset Name
The name of your output mosaic dataset
Input Data Path
Path and name of the rasters or mosaic dataset(s) used as input
Identify the source and derived mosaic datasets you plan to create for your project.
Locate the sample configuration file from the downloaded workflow files that is closest to what you need for your project's first mosaic dataset.
In ArcGIS Pro, create a project and add the Managing Elevation workflow tools as you did in Using the geoprocessing tools.
In the Catalog pane, double click the appropriate tool for the mosaic dataset you're creating (Source Mosaic Dataset or Derived Mosaic Dataset).
In the first field, enter the path to the configuration file you wish to use for the first mosaic dataset.
Fill in the geoprocessing tool dialog box with the parameters for your mosaic dataset. Any fields left blank will default to the value stored in the input configuration file.
Click OK to run the geoprocessing tool.
Repeat steps 4 through 7 for all mosaic datasets needed for your project.
Creating custom configuration files

The Managing Elevation geoprocessing tools and batch files rely on xml configuration files to set essential input parameters. You will need one configuration file for each source and derived mosaic dataset you plan to create.

The workflow GP tools allow you tweak existing configuration files, but if you wish to automate, scale up, or repeat your data processing, you will likely want to create configuration files for your specific project. To create custom configuration files, follow these steps.

Navigate to the …ElevationScript\Elevation\Parameter\Config\ArcGISPro\ directory and open the XML configuration file you wish to edit in your preferred text editor.
Edit fields as necessary, keeping the formatting the same. The fields you are most likely to edit in the XML configuration files for source and derived mosaic datasets are listed in the tables below.
In the XML file for source mosaic datasets, you are most likely to edit these fields:
Heading (in XML file)	Tag to edit: Description
<Name>
Name of your project
<Command>
List of two-letter codes representing commands that need to be run on the newly created mosaic dataset. These can be combined using a plus sign and will be run in the order listed.
Note:
Source and derived mosaic datasets take slightly different input commands; see the tool dialog boxes for more information about available commands.
<Workspace>
<WorkspacePath>: Path to the directory that contains your geodatabase
<Geodatabase>: Name of your geodatabase
<MosaicDataset>
<Name>: Name of your mosaic dataset
<SRS>: Projection
<AddRasters><AddRaster>
<dataset_id>: A unique identifier (text string) for the input dataset. This label is entered into the mosaic dataset Attribute Table for all the rasters added in one Add Raster operation.
<Sources><data_path>: Path to the directory that contains your input data
<CalculateValues>
(<FieldName>: ProductName) <Expression>: Enter a unique identifier in double quotes
(<FieldName>: LE90) <Expression>: Enter vertical accuracy of elevation data at a 90% confidence level
(<FieldName>: CE90) <Expression>: Enter horizontal accuracy of the input data at a 90% confidence level
(<FieldName>: Date_Start ) <Expression>: Enter the start date for the creation of the source data being added to the mosaic dataset in double quotes
(<FieldName>: Date_End ) <Expression>: Enter the end date for the creation of the source data being added to the mosaic dataset in double quotes
(<FieldName>: Source_URL) <Expression>: Enter the URL for the original source of the data being added into the mosaic dataset in double quotes. This could be the source organization, or alternatively a server where the original source data can be downloaded.
(<FieldName>: VerticalDatum) <Expression>: Enter the name of the vertical datum (in the case of elevation data) for the data being added into the mosaic dataset in double quotes, if available
(<FieldName>: Metadata_URL) <Expression>: If your metadata is hosted online, enter the URL here in double quotes
(<FieldName>: DEM_Type) <Expression>: Enter the identifier to be set in the Attribute Table for any elevation data being entered into the mosaic dataset.
Note:
Most elevation data will be "bare earth" (dem_type = 2) but others are possible:
Undefined = 0
DSM (first return surface, e.g. buildings, tree canopy) = 1
DTM (bare earth) = 2
Bathymetry = 3
Ice (e.g. ETOPO, GTOPO) = 4
Ellipsoid = 5
Geoid = 6
In the XML file for derived mosaic datasets, you are most likely to edit these fields:

Heading (in XML file)	Tag to edit: Description
<Name>
Name of your project
<Command>
List of two-letter codes representing commands that need to be run on the newly created mosaic dataset. These can be combined using a plus sign and will be run in the order listed.
Note:
Source and derived mosaic datasets take slightly different input commands; see the tool dialog boxes for more information about available commands.
<Workspace>
<WorkspacePath>: Path to the directory that contains your geodatabase
<Geodatabase>: Name of your geodatabase
<MosaicDataset>
<Name>: Name of your mosaic dataset
<SRS>: Projection
<processing_templates>: list of the filenames of the .rft.xml raster function template files you wish to make available to end users
<AddRasters><AddRaster>
<dataset_id>: ID of the raster you'll use to manage your source mosaic datasets
<Sources><data_path>: Names of the mosaic datasets you wish to add (list as many as desired)
Save the new version of the XML configuration file to your project's ../Parameter/Config/ directory using an appropriate name. These can be selected when using the GP tools, or deployed using batch files (as described in the next section).
Repeat this process to generate xml configuration files for each source and derived mosaic dataset you will create as a part of your project.

Using the batch files with your data

To adapt the batch files to your data, follow these steps. You will probably need to create two new batch files: one for creating source mosaic datasets and one for creating a derived mosaic dataset.

Note:
Be sure to create XML configuration files for each mosaic dataset you will create before you begin.

Navigate to the …\ElevationScript\elevation\batchfiles\ArcGISPro\ directory and open Generate_Source_MD_sample1_ArcGISPro.bat in your preferred text editor.
You will call the MDCS script, using your configuration files as input, for each source mosaic dataset you need to create. Ensure that the batch file is pointing to the instance of MDCS you wish to use, and change the XML file paths to point to the XML configuration files for your project's source mosaic datasets.
Save your edited batch file to your project's batchfile directory using an appropriate name.
Repeat this process to edit the batch file that will create your derived mosaic dataset.
To run each batch file, locate the file in the directory where you saved it and double click the file.
After reading this section, you should have the information you need to use the workflow tools and scripts with your own data. If you have additional questions not addressed here, check out the Workflow tab for a deeper dive into what's happening under the hood of the Managing Elevation workflow.