# xlsx-to-mods-xml conversion tool for Tibetan newspaper metadata 
This repository contains two functions for converting our project-internal metadata spreadsheets [Diverge_Tibetan Newspaper Metadata for XML v2.xlsx](https://github.com/Divergent-Discourses/xml-processing/blob/91c1011ad867a31e79be4a91fbfab6fac2a32ed2/Diverge_Newspaper%20Metadata%20for%20XML%20v2.xlsx) to MODS-formatted XML. 

Note that these scripts are for project use only, and will not work outside of the Diverge project, because the conversion process from Excel to XML requires hard-coding of column names. Generally, columns and column names cannot be modified. However, new newspaper records (rows) can be added and information updated. To add, alter, or delete columns get in touch with the developers.

The spreadsheet [Diverge_Tibetan Newspaper Metadata for XML v2.xlsx](https://github.com/Divergent-Discourses/xml-processing/blob/91c1011ad867a31e79be4a91fbfab6fac2a32ed2/Diverge_Newspaper%20Metadata%20for%20XML%20v2.xlsx) contains the metadata for the newspapers in the Diverge corpus. It includes links to the original holdings and aggregates information from various sources, including the newspapers, the catalogue entries of the libraries, where original copies are held and from previous research:
- Schubert, J. 1935. ["Tibetische Literatur in modernem Gewande](https://www.jstor.org/stable/3250338) (Mit einem Exkurs über tibetische Zeitungen)." Artibus Asiae 5(1), 95–98.
- Schubert, J. 1958. [*Publikationen des modernen chinesisch-tibetischen Schrifttums.*](https://www.degruyter.com/document/doi/10.1515/9783112539729/html)/ Veröffentlichung / Deutsche Akademie der Wissenschaften, Institut für Orientforschung 39. Berlin: Akademie-Verlag.
- Kolmaš, J. 1962. ["Tibetan Literature in China."](https://ceskadigitalniknihovna.cz/uuid/uuid:83d6711e-3e45-11e1-bdd3-005056a60003) Archív Orientální 30, 638–44.
- Kolmaš, J. 1978. [*Tibetan Books and Newspapers (Chinese collection): With Bibliographical Notes.*](https://pahar.in/pahar/Books%20and%20Articles/Tibet%20and%20China/1978%20Tibetan%20Books%20and%20Newspapers%20(Chinese%20Collection%20)%20with%20bibliographical%20notes%20by%20Kolmas%20s.pdf) Asiatische Forschungen 62. Wiesbaden: Harrassowitz.
- Erhard, F.X. 2015. ["Tibetan Mass Media. A Preliminary Survey of Tibetan Language Newspapers."](https://www.academia.edu/20285155/Tibetan_Mass_Media_A_Preliminary_Survey_of_Tibetan_Language_Newspapers) In O. Czaja and G. Hazod (eds.) *The Illuminating Mirror: Tibetan Studies in Honour of Per K. Sørensen on the Occasion of his 65th Birthday,* 155–171. Contributions to Tibetan Studies 12. Wiesbaden: Reichert.
- Erhard, F.X. and H. Hou 2018. ["The Melong in Context. A Survey of the Earliest Tibetan Language Newspapers 1904–1960."](https://www.academia.edu/38535397/The_Melong_in_Context_A_Survey_ofthe_Earliest_Tibetan_Language_Newspapers_1904_1960) In F. Wang-Toutain and M. Preziosi (eds.) *Cahiers du Mirror,* 1–40. Paris: Collège de France.

# How to use
The workflow is executed in two steps. First, the python programs must be stored hierarchically at or above the level where the raw data and the target directory is stored, in the same hierarchy. Then, in the command line interface, run the following command:

``` python -m flat-xml.py ```

You will then be prompted for the relevant file path inputs. This script generates “flat” XML for each record in the spreadsheet, where each column corresponds to a unique field in the XML.

Once the “flat” XML files have been generated, run the second script, which converts “flat” XML to MODS format, compliant with the Berlin State Library’s metadata storage standards, with the command prompt:

``` python -m mods-from-flat-xml.py ```

As before, you will receive prompts to input your paths to files or folders for conversion. The MODS converter can handle single records or a directory containing only XML files. 

