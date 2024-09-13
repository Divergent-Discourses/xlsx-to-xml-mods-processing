This repository contains two functions for converting our project-internal metadata spreadsheets [Diverge_Tibetan Newspaper Metadata for XML v2.xlsx] to MODS-formatted XML. Note that these scripts are for project use only, and will not work outside of the Diverge project, because the conversion process from Excel to XML requires hard-coding of column names. Generally, columns and column names cannot be modified. However, new newspaper records (rows) can be added and information updated. To add, alter, or delete columns get in touch with the developers.

The spreadsheet [Diverge_Tibetan Newspaper Metadata for XML v2.xlsx] contains the metadata for the newspapers in the Diverge corpus. It includes information from various sources, including the newspapers, the catalogue entries of the libraries where original copies are held and from:
- Schubert, J. 1935. "Tibetische Literatur in modernem Gewande (Mit einem Exkurs über tibetische Zeitungen)." Artibus Asiae 5(1), 95–98.
- Schubert, J. 1958. *Publikationen des modernen chinesisch-tibetischen Schrifttums.*/ Veröffentlichung / Deutsche Akademie der Wissenschaften, Institut für Orientforschung 39. Berlin: Akademie-Verlag.
- Kolmaš, J. 1962. "Tibetan Literature in China." Archív Orientální 30, 638–44.
- Kolmaš, J. 1978. *Tibetan Books and Newspapers (Chinese collection): With Bibliographical Notes.* Asiatische Forschungen 62. Wiesbaden: Harrassowitz.
- Erhard, F.X. 2015. "Tibetan Mass Media. A Preliminary Survey of Tibetan Language Newspapers." In O. Czaja and G. Hazod (eds.) *The Illuminating Mirror: Tibetan Studies in Honour of Per K. Sørensen on the Occasion of his 65th Birthday,* 155–171. Contributions to Tibetan Studies 12. Wiesbaden: Reichert.
- Erhard, F.X. and H. Hou 2018. "The Melong in Context. A Survey of the Earliest Tibetan Language Newspapers 1904–1960." In F. Wang-Toutain and M. Preziosi (eds.) *Cahiers du Mirror,* 1–40. Paris: Collège de France.

# How to use
The workflow is executed in two steps. First, the python programs must be stored hierarchically at or above the level where the raw data and the target directory is stored, in the same hierarchy. Then, in the command line interface, run the following command:

``` python -m flat-xml.py ```

You will then be prompted for the relevant file path inputs. This script generates “flat” XML for each record in the spreadsheet, where each column corresponds to a unique field in the XML.

Once the “flat” XML files have been generated, run the second script, which converts “flat” XML to MODS format, compliant with the Berlin State Library’s metadata storage standards, with the command prompt:

``` python -m mods-from-flat-xml.py ```

As before, you will receive prompts to input your paths to files or folders for conversion. The MODS converter can handle single records or a directory containing only XML files. 

