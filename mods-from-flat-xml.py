from xml.etree import ElementTree as ET
from datetime import date
import os

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
        'Title_Tibetan': {'lang': 'tib'},
        'Title_Wylie': {'lang': 'tib', 'transliteration': 'Wylie'}, 
        'Title_Chinese': {'lang': 'chi'}, 
        'Title_Pinyin': {'lang': 'chi', 'transliteration': 'pinyin'}
    }

    for title_key, attrs in titles.items():
        title_element = record.find(title_key)
        if title_element is not None and title_element.text and title_element.text.strip():
            title_info = ET.SubElement(mods_root, 'titleInfo', lang=attrs['lang'])
            if 'transliteration' in attrs:
                title_info.set('transliteration', attrs['transliteration'])
            safe_set_text(title_info, 'title', title_element.text.strip())
    
    translated_title = record.find('Translated_title')
    if translated_title is not None and translated_title.text and translated_title.text.strip():
        title_info_translated = ET.SubElement(mods_root, 'titleInfo', type='translated')
        safe_set_text(title_info_translated, 'title', translated_title.text.strip())

def add_location_info(mods_root, record):
    origin_info = ET.SubElement(mods_root, 'originInfo')
    place_added = False

def add_location_info(mods_root, record):
    origin_info = ET.SubElement(mods_root, 'originInfo')
    place_added = False

    place_terms = OrderedDict()
    
    def collect_place_term(record, field_name, lang, transliteration=None):
        element = record.find(field_name)
        if element is not None and element.text:
            key = (element.text.strip(), lang, transliteration)
            place_terms[key] = element.text.strip()

    # Collect all place terms
    collect_place_term(record, 'Place_name_Tibetan', 'tib', 'Wylie')
    collect_place_term(record, 'Place_Wylie', 'tib', 'Wylie')
    collect_place_term(record, 'Place_Chinese', 'chi', 'pinyin')
    collect_place_term(record, 'Place_pinyin', 'chi', 'pinyin')
    collect_place_term(record, 'Place_English', 'eng')
    collect_place_term(record, 'Province_English', 'eng')
    collect_place_term(record, 'Province_Tibetan', 'tib', 'Wylie')
    collect_place_term(record, 'Prefectur_District_Tibetan', 'tib', 'Wylie')
    collect_place_term(record, 'Prefecture_District_Wylie', 'tib', 'Wylie')
    collect_place_term(record, 'Prefectur_District_Chinese', 'chi', 'pinyin')
    collect_place_term(record, 'Prefecture_District_English', 'eng')
    collect_place_term(record, 'Country_SO_3166-1_alpha-3', 'eng')


    if place_terms:
        place = ET.SubElement(origin_info, 'place')
        for (text, lang, transliteration), value in place_terms.items():
            attrs = {'type': "text", 'authority': "marc", 'lang': lang}
            if transliteration:
                attrs['transliteration'] = transliteration
            term = ET.SubElement(place, 'placeTerm', **attrs)
            term.text = value
            place_added = True

    place_identifier = record.find('PlaceIdentifier')
    if place_identifier is not None and place_identifier.text:
        place_id_elem = ET.SubElement(place, 'placeIdentifier', type="local")
        place_id_elem.text = place_identifier.text.strip()

    if not place_added:
        mods_root.remove(origin_info)

def add_publication_info(mods_root, record):
    origin_info = ET.SubElement(mods_root, 'originInfo')
    origin_info_added = False

    frequency_text = record.find('Frequency').text if record.find('Frequency') is not None else None
    if frequency_text:
        frequency = ET.SubElement(origin_info, 'frequency')
        frequency.text = frequency_text
        origin_info_added = True

    roles = {
        'Publisher': ['_Tibetan', '_Wylie', '_Chinese', '_pinyin', '_English'],
        'Editor_Person': ['_English', '_Tibetan', '_Wylie', '_Chinese', '_pinyin']
    }

    for role_type, suffixes in roles.items():
        for suffix in suffixes:
            field_name = f"{role_type}{suffix}"
            person_text = record.find(field_name).text if record.find(field_name) is not None else None
            if person_text:
                transliteration = None
                if 'Wylie' in suffix:
                    transliteration = 'Wylie'
                elif 'pinyin' in suffix:
                    transliteration = 'pinyin'
                lang = suffix.split('_')[1].lower()
                name = ET.SubElement(mods_root, 'name', lang=lang)
                safe_set_text(name, 'namePart', person_text.strip())
                role = ET.SubElement(name, 'role')
                safe_set_text(role, 'roleTerm', role_type.lower(), {'type': "text"})

    ids = {
        'IN_Registration_Number': None,
        'CN_Newspaper_Code': None
    }

    for id_field in ids.keys():
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
        'Last_Issue': 'end'
    }
    for date_field, point in dates.items():
        date_text = record.find(date_field).text if record.find(date_field) is not None else None
        if date_text:
            date_issued = ET.SubElement(origin_info, 'dateIssued', encoding="w3cdtf", point=point)
            date_issued.text = date_text
            origin_info_added = True

    notes_fields = ['Description', 'Donor_Code', 'Places_of_distribution', 'Holdings_in_other_collections_w_o_xml_sources', 'Diverge_digital_holdings']
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

    if not origin_info_added:
        mods_root.remove(origin_info)

def add_record_info(mods_root):
    record_info = ET.SubElement(mods_root, 'recordInfo')
    
    record_origin = ET.SubElement(record_info, 'recordOrigin')
    record_origin.text = 'Automatically generated by script (author Engels, James J.)'
    
    record_creation = ET.SubElement(record_info, 'recordCreationDate', encoding="w3cdtf")
    today = date.today()
    record_creation.text = today.strftime('%Y-%m-%d')

    language_of_cataloging = ET.SubElement(record_info, 'languageOfCataloging')
    language_term = ET.SubElement(language_of_cataloging, 'languageTerm', type="code", authority="iso639-2")
    language_term.text = 'eng'

def initialize_mods_root():
    attrs = {
        'xmlns': "http://www.loc.gov/mods/v3",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'version': "3.8",
        'xsi:schemaLocation': "http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-8.xsd"
    }
    mods_root = ET.Element('mods', attrib=attrs)
    return mods_root

def process_single_record(record, destination):
    mods_root = initialize_mods_root()
    add_title_info(mods_root, record)
    add_location_info(mods_root, record)
    add_publication_info(mods_root, record)
    add_record_info(mods_root)

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
