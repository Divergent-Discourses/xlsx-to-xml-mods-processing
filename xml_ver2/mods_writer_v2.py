from pymods import Mods
import os
import pandas as pd
import sys

# Add pymods to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'source/Diverge_Newspaper Metadata for XML v2.xlsx')
resource = pd.read_excel(excel_path)
resource = resource.fillna('').astype(str)

for index, row in resource.iterrows():
    mods_record = Mods()
    # DIVERGE Local Code
    if row['DIVERGE Code']:
        code = row['DIVERGE Code']
        mods_record.add_identifier(row['DIVERGE Code'], 'local')

    # Add titles
    if row['Title (Tibetan)']:
        mods_record.add_title(row['Title (Tibetan)'], lang="tib")
    if row['Title (Wylie)']:
        mods_record.add_title(row['Title (Wylie)'], lang="tib-Latn")
    if row['Title (English)']:
        mods_record.add_title(row['Title (English)'], lang="eng")
    if row['Translated title']:
        mods_record.add_title(row['Translated title'], is_translated = True, lang="eng")
    if row['Title (pinyin)']:
        mods_record.add_title(row['Title (pinyin)'], lang="chi-Latn")
    if row['Title (Chinese)']:
        mods_record.add_title(row['Title (Chinese)'], lang="chi")
        
    # Add publisher
    if row['Publisher (Tibetan)']:
        mods_record.add_publisher(row['Publisher (Tibetan)'], lang="tib")
    if row['Publisher (Wylie)']:
        mods_record.add_publisher(row['Publisher (Wylie)'], lang="tib-Latn")
    if row['Publisher (English)']:
        mods_record.add_publisher(row['Publisher (English)'], lang="eng")
    if row['Publisher (Chinese)']:
        mods_record.add_publisher(row['Publisher (Chinese)'], lang="chi")
    if row['Publisher (pinyin)']:
        mods_record.add_publisher(row['Publisher (pinyin)'], lang="chi-Latn")
    if row['Publisher (GND-ID)']:
        mods_record.add_publisher(row['Publisher (GND-ID)'], authority="gnd")

    # Add languages
    if row['1st Language (ISO 639-2)']:
        mods_record.add_language(row['1st Language (ISO 639-2)'], type="code", authority="iso639-2b")
    if row['2nd Language (ISO 639-2)']:
        mods_record.add_language(row['2nd Language (ISO 639-2)'], type="code", authority="iso639-2b")
    if row['3rd Language (ISO 639-2)']:
        mods_record.add_language(row['3rd Language (ISO 639-2)'], type="code", authority="iso639-2b")

    # Add dates
    if row['First Issue']:
        if row['last issue']:
            mods_record.add_created_date(row['First Issue'] + ' – ' + row['last issue'])
        else:
            mods_record.add_created_date(row['First Issue'])

    # Add description
    if row['description']:
        mods_record.add_abstract(row['description'])

    # Add hierarchical geographic data
    if row['Country (SO 3166-1 alpha-3)'] or row['Province (English)'] or row['Prefecture/District (English)'] or row['Place (English)']:
        mods_record.add_hierarchical_geographic(
            country=row['Country (SO 3166-1 alpha-3)'],
            province=row['Province (English)'],
            district=row['Prefecture/District (English)'],
            place=row['Place (English)'],
            lang="eng",
            authority1="iso3166"
        )

    if row['Country (SO 3166-1 alpha-3)'] or row['Province (Tibetan)'] or row['Prefectur/District (Tibetan)'] or row['Place name (Tibetan)']:
        mods_record.add_hierarchical_geographic(
            country=row['Country (SO 3166-1 alpha-3)'],
            province=row['Province (Tibetan)'],
            district=row['Prefectur/District (Tibetan)'],
            place=row['Place name (Tibetan)'],
            lang="tib",
            authority1='iso3166'
        )

    if row['Country (SO 3166-1 alpha-3)'] or row['Prefecture/District (Wylie)'] or row['Place (Wylie)']:
        mods_record.add_hierarchical_geographic(
            country=row['Country (SO 3166-1 alpha-3)'],
            district=row['Prefecture/District (Wylie)'],
            province='',
            place=row['Place (Wylie)'],
            lang="tib-Latn",
            authority1='iso3166'
        )

    if row['Country (SO 3166-1 alpha-3)'] or row['Prefectur/District (Chinese)'] or row['Place (Chinese)']:
        mods_record.add_hierarchical_geographic(
            country=row['Country (SO 3166-1 alpha-3)'],
            district=row['Prefectur/District (Chinese)'],
            province='',
            place=row['Place (Chinese)'],
            lang="chi",
            authority1='iso3166'
        )

    if row['Country (SO 3166-1 alpha-3)'] or row['Prefecture/District (pinyin)'] or row['Place (pinyin)']:
        mods_record.add_hierarchical_geographic(
            country=row['Country (SO 3166-1 alpha-3)'],
            province='',
            district='',
            place=row['Place (pinyin)'],
            lang="chi-Latn",
            authority1='iso3166'
        )
        
    #Place GND
    if row['Place (GND-ID)']:
        mods_record.add_hierarchical_geographic(
            country=row['Country (SO 3166-1 alpha-3)'],
            district='',
            province='',
            place=row['Place (GND-ID)'],
            lang='',
            authority2='GND'
        )
        
    #Add editors
    if row['Editor (Person) English']:
        mods_record.add_name(row['Editor (Person) English'], lang="eng", roles=["editor"])
    if row['Editor (Person) Tibetan']:
        mods_record.add_name(row['Editor (Person) Tibetan'], lang="tib", roles=["editor"])
    if row['Editor (Person) Wylie']:
        mods_record.add_name(row['Editor (Person) Wylie'], lang="tib-Latn", roles=["editor"])
    if row['Editor (Person) Chinese']:
        mods_record.add_name(row['Editor (Person) Chinese'], lang="chi", roles=["editor"])
    if row['Editor (Person) pinyin']:
        mods_record.add_name(row['Editor (Person) pinyin'], lang="chi-Latn", roles=["editor"])
    if row['Editor (GND-ID)']:
        mods_record.add_name(row['Editor (GND-ID)'], authority="gnd", roles=["editor"])
        
    
    #Diverge digital holdings
    if row['Diverge digital holdings']:
        mods_record.add_note(row['Diverge digital holdings'], type="internal-holdings")
    
    #Holdings comment
    if row['Holdings comment']:
        mods_record.add_note(row['Holdings comment'], type="comment")
    
    #CN, IN codes
    if row['IN Registration Number']:
        mods_record.add_identifier(row['IN Registration Number'], 'IN-registration-number')
    if row['CN Newspaper Code']:
        mods_record.add_identifier(row['CN Newspaper Code'], 'CN-newspaper-code')
    
    #Donors
    for donor_col in ['Donor 1', 'Donor 2', 'Donor 3', 'Donor 4', 'Donor 5']:
        if row[donor_col]:
            mods_record.add_note(row[donor_col], type="donor")
    
    #External holdings
    if row['Holdings in other collections (w/o xml sources)']:
        mods_record.add_note(row['Holdings in other collections (w/o xml sources)'], type="external-holdings")
    
    #External links
    for link_col in ['Library link 1', 'Library link 2', 'Library link 3', 'Library link 4', 'Library link 5']:
        if row[link_col]:
            mods_record.add_location_url(row[link_col])
    
    #Format
    if row['Format']:
        mods_record._physical_description = row['Format']
    
    #Frequency
    if row['Frequency']:
        mods_record.add_frequency(row['Frequency'])
    
    #Distribution location
    if row['Place(s) of distribution']:
        mods_record.add_distribution(row['Place(s) of distribution'])   

    # Save the MODS record to a file
    with open(f'xml_records/record_{code}_mods.xml', 'wb') as f:
        f.write(mods_record.as_xml(xml_declaration=True, pretty_print=True))
