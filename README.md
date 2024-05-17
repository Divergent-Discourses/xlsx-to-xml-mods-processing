This repository contains two functions for converting our project-internal metadata spreadsheets to MODS-formatted XML. Note that these scripts are for project use only, and will not work outside of the Diverge project, because the conversion process from Excel to XML requires hard-coding of column names. 

The workflow is executed in two steps. First, the python programs must be stored hierarchically at or above the level where the raw data and the target directory is stored, in the same hierarchy. Then, in the command line interface, run the following command:

``` python -m flat-xml.py ```

You will then be prompted for the relevant filepath inputs. This script generates “flat” XML for each record in the spreadsheet, where each column corresponds to a unique field in the XML.

Once the “flat” XML files have been generated, run the second script, which converts “flat” XML to MODS format, compliant with the Berlin State Library’s metadata storage standards, with the command prompt:

``` python -m mods-from-flat-xml.py ```

As before, you will receive prompts to input your paths to files or folders for conversion. The MODS converter can handle single records or a directory containing only XML files. 

