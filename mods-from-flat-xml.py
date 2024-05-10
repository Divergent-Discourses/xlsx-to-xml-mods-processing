import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import lxml.etree as etree

#Code starts here

def safe_set_text(parent, tag, text, attributes=None):
    if text: 
        elem = ET.SubElement(parent, tag)
        elem.text = text
        if attributes:
            for key, value in attributes.items():
                if value is not None:
                    elem.set(key, value)
    return None


def add_title_info(mods_root, record):
    titles = {
        'Title_English': {'lang': 'eng'},
        'Title_Tibetan': {'lang': 'tib', 'script': 'Tibt'},
        'Title_Wylie': {'lang': 'tib', 'script': 'Latn'}, 
        'Title_Chinese': {'lang': 'chi', 'script': 'Hant'}, 
        'Title_pinyin': {'lang': 'chi', 'script': 'Latn'},  
    }

    for title_key, attrs in titles.items():
        title_element = record.find(title_key)
        if title_element is not None and title_element.text:
            title_info = ET.SubElement(mods_root, 'titleInfo', lang=attrs['lang'], script=attrs['script'] if attrs['script'] else {})
            safe_set_text(title_info, 'title', title_element.text)
    
    translated_title = record.find('Translated_title')
    if translated_title is not None and translated_title.text and translated_title.text.strip():
        title_info_translated = ET.SubElement(mods_root, 'titleInfo', type='translated')
        safe_set_text(title_info_translated, 'title', translated_title.text.strip())


def add_location_info(mods_root, record):
    origin_info = ET.SubElement(mods_root, 'originInfo')
    
    primary_place = ET.SubElement(origin_info, 'place')

    city_terms = {
        'Place_name_Tibetan': {'lang': 'tib', 'script': 'Tibt'},
        'Place_Wylie': {'lang': 'tib', 'script': 'Latn'},
        'Place_Chinese': {'lang': 'chi', 'script': 'Hant'},
        'Place_pinyin': {'lang': 'chi', 'script': 'Latn'},
        'Place_English': {'lang': 'eng'}
    }

    province_terms = {
        'Province_English': {'lang': 'eng'},
        'Province_Tibetan': {'lang': 'tib', 'script': 'Tibt'},
        'Province_Chinese': {'lang': 'zho', 'script': 'Hant'},
        'Province_pinyin': {'lang': 'zho', 'script': 'Latn'},
        'Province_Wylie': {'lang': 'tib', 'script': 'Latn'}
    }

    district_terms = {
        'Prefectur_District_Tibetan': {'lang': 'tib', 'script': 'Tibt'},
        'Prefecture_District_Wylie': {'lang': 'tib', 'script': 'Latn'},
        'Prefecture_District_English': {'lang': 'eng'},
        'Prefectur_District_Chinese': {'lang': 'chi', 'script': 'Hant'}
    }

    for key, attrs in city_terms.items():
        text = record.find(key).text if record.find(key) is not None else None
        safe_set_text(primary_place, 'placeTerm', text, {'type': "text", 'authority': "marc", **attrs})

    country_place = ET.SubElement(primary_place, 'place')
    country_text = record.find('Country_SO_3166-1_alpha-3').text if record.find('Country_SO_3166-1_alpha-3') is not None else None
    safe_set_text(country_place, 'placeTerm', country_text, {'type': "text", 'authority': "marc", 'lang': 'eng'})

    province_place = ET.SubElement(country_place, 'place')
    for key, attrs in province_terms.items():
        text = record.find(key).text if record.find(key) is not None else None
        safe_set_text(province_place, 'placeTerm', text, {'type': "text", 'authority': "marc", **attrs})

    # Adding district information
    district_place = ET.SubElement(province_place, 'place')
    for key, attrs in district_terms.items():
        text = record.find(key).text if record.find(key) is not None else None
        safe_set_text(district_place, 'placeTerm', text, {'type': "text", 'authority': "marc", **attrs})


def add_publication_info(mods_root, record):
    origin_info = ET.SubElement(mods_root, 'originInfo')

    frequency_text = record.find('Frequency').text if record.find('Frequency') is not None else None
    if frequency_text:
        frequency = ET.SubElement(origin_info, 'frequency')
        frequency.text = frequency_text

    roles = {
        'Publisher': ['_Tibetan', '_Wylie', '_Chinese', '_pinyin', '_English'],
        'Editor_Person': ['_English', '_Tibetan', '_Wylie', '_Chinese', '_pinyin']
    }

    for role_type, suffixes in roles.items():
        for suffix in suffixes:
            field_name = f"{role_type}{suffix}"
            person_text = record.find(field_name).text if record.find(field_name) is not None else None
            if person_text:
                name = ET.SubElement(mods_root, 'name')
                safe_set_text(name, 'namePart', person_text)
                role = ET.SubElement(name, 'role')
                safe_set_text(role, 'roleTerm', role_type.lower(), {'type': "text"})

    ids = {
        'IN_Registration_Number': None,
        'CN_Newspaper_Code': None
    }

    for id_field, id_text in ids.items():
        id_text = record.find(id_field).text if record.find(id_field) is not None else None
        if id_text:
            identifier = ET.SubElement(mods_root, 'identifier', type="local")
            identifier.text = id_text

    format_text = record.find('Format').text if record.find('Format') is not None else None
    if format_text:
        physical_description = ET.SubElement(mods_root, 'physicalDescription')
        form = ET.SubElement(physical_description, 'form')
        form.text = format_text

    languages = ['_1st_Language_ISO_639-2', '_2nd_Language_ISO_639-2', '_3rd_Language_ISO_639-2']
    for lang_field in languages:
        lang_code = record.find(lang_field).text if record.find(lang_field) is not None else None
        if lang_code:
            language = ET.SubElement(mods_root, 'language')
            language_term = ET.SubElement(language, 'languageTerm', type="code", authority="iso639-2")
            language_term.text = lang_code

    dates = {
        'First_Issue': 'start',
        'last_issue': 'end'
    }
    for date_field, point in dates.items():
        date_text = record.find(date_field).text if record.find(date_field) is not None else None
        if date_text:
            date_issued = ET.SubElement(origin_info, 'dateIssued', encoding="w3cdtf", point=point)
            date_issued.text = date_text

    
    notes_fields = ['description', 'Donor_Code', 'Places_of_distribution', 'Holdings_in_other_collections_w_o_xml_sources', 'Diverge_digital_holdings']
    for note_field in notes_fields:
        note_text = record.find(note_field).text if record.find(note_field) is not None else None
        if note_text:
            note = ET.SubElement(mods_root, 'note')
            note.text = note_text

    library_links_text = record.find('Library_links').text if record.find('Library_links') is not None else None
    if library_links_text:
        related_item = ET.SubElement(mods_root, 'relatedItem', type="host")
        location = ET.SubElement(related_item, 'location')
        url = ET.SubElement(location, 'url')
        url.text = library_links_text

def initialize_mods_root():
    mods_root = ET.Element('mods', xmlns="http://www.loc.gov/mods/v3")
    return mods_root
        
def process_single_record(record, destination):
    mods_root = initialize_mods_root()
    add_title_info(mods_root, record)
    add_location_info(mods_root, record)
    add_publication_info(mods_root, record)

    if not destination.endswith('.xml'):
        destination += '.xml'

    tree = ET.ElementTree(mods_root)
    tree.write(destination, encoding='utf-8', xml_declaration=True)

def process_directory(source_directory, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    for filename in os.listdir(source_directory):
        if filename.endswith('.xml'):
            source_file = os.path.join(source_directory, filename)
            destination_file = os.path.join(destination_directory, os.path.splitext(filename)[0] + "_mods.xml")

            record = ET.parse(source_file).getroot()
            process_single_record(record, destination_file)
