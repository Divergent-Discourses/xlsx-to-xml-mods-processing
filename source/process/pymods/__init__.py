from lxml import etree
from lxml.builder import ElementMaker
from ._custom_lxml import makeelement

XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'

MODS_NAMESPACE = 'http://www.loc.gov/mods/v3'
MODS_SCHEMA_LOC = 'http://www.loc.gov/standards/mods/v3/mods-3-4.xsd'
MODS_NAMESPACE_MAP = {
    'mods': MODS_NAMESPACE,
    'xsi': XSI_NAMESPACE,
    'xlink': XLINK_NAMESPACE
}

class ModsRoot(object):

    def __init__(self, collection=False):
        self._me = ElementMaker(
            namespace=MODS_NAMESPACE,
            nsmap=MODS_NAMESPACE_MAP,
            makeelement=makeelement
        )
        if collection:
            self._root = self._me.modsCollection()
        else:
            self._root = self._me.mods()
        self._root.set(
            '{{{}}}schemaLocation'.format(XSI_NAMESPACE),
            '{} {}'.format(MODS_NAMESPACE, MODS_SCHEMA_LOC)
        )

    @property
    def etree(self):
        return self._root

    def as_xml(self, xml_declaration=False, pretty_print=True):
        return etree.tostring(
            self._root,
            xml_declaration=xml_declaration,
            pretty_print=pretty_print,
            encoding='utf-8'
        )


class ModsCollection(ModsRoot):

    def __init__(self):
        super(ModsCollection, self).__init__(True)

    def add_mods(self, mods):
        ''' Adds another Mods record as an embedded related item
        @param mods: This should be an instance of asurepo.metadata.Mods
        '''
        if not isinstance(mods, Mods):
            raise TypeError('You should only be supplying this method an ' +
                            'instance of asurepo.metadata.Mods')
        self._root.append(mods.etree)


class Mods(ModsRoot):

    RESOURCE_TYPES = [
        'text',
        'cartographic',
        'notated music',
        'sound recording-musical',
        'sound recording-nonmusical',
        'sound recording',
        'still image',
        'moving image',
        'three dimensional object',
        'software, multimedia',
        'mixed material'
    ]

    def __init__(self):
        super(Mods, self).__init__()
        self._origin_info = None
        self._physical_description = None
        self._record_info = None

    @property
    def origin_info(self):
        if self._origin_info is None:
            self._origin_info = self._me.originInfo()
            self._root.append(self._origin_info)
        return self._origin_info

    @property
    def physical_description(self):
        if self._physical_description is None:
            self._physical_description = self._me.physicalDescription()
            self._root.append(self._physical_description)
        return self._physical_description

    @property
    def record_info(self):
        if self._record_info is None:
            self._record_info = self._me.recordInfo()
            self._root.append(self._record_info)
        return self._record_info

    def _create_date_elem(self, elem_name, date, encoding=None, point=None,
                          qualifier=None, is_key_date=False):

        date_elem = self._me(elem_name, date)

        if encoding in ['w3cdtf', 'iso8601', 'marc', 'edtf', 'temper']:
            date_elem.set('encoding', encoding)

        if point in ['start', 'end']:
            date_elem.set('point', point)

        if qualifier in ['approximate', 'inferred', 'questionable']:
            date_elem.set('qualifier', qualifier)

        if is_key_date:
            date_elem.set('keyDate', 'yes')

        return date_elem

    def add_title(self, title, is_translated=False, lang=None):
        ti = self._me.titleInfo()
        if is_translated:
            ti.set('type', 'translated')
        title_elem = self._me('title', title)
        if lang:
            title_elem.set('lang', lang)  # Add the lang attribute
        ti.append(title_elem)
        self._root.append(ti)

    def add_name(self, last, rest=None, roles=None, is_institution=False, lang=None):
        '''
        @param last: The 'family name' of a personal name or the institution
            or 'corporate name' of an institution
        @param rest: The given name (plus any other name info) of a personal
            name
        @param roles: a list of strings that designate this entity's relation
            to the resource
        @param is_institution: indicates whether this is a corporate name
        @param lang: The language of the name
        '''
        name = self._me.name()
        if is_institution:
            name.set('type', 'corporate')
            name_part = self._me.namePart(last)
            if lang:
                name_part.set('lang', lang)
            name.append(name_part)
        else:
            name.set('type', 'personal')
            family_name = self._me.namePart(last, {'type': 'family'})
            if lang:
                family_name.set('lang', lang)
            name.append(family_name)
            if rest:
                given_name = self._me.namePart(rest, {'type': 'given'})
                if lang:
                    given_name.set('lang', lang)
                name.append(given_name)

        if roles:
            role_elem = self._me.role()
            for role in roles:
                role_elem.append(self._me.roleTerm(role))
            name.append(role_elem)
        self._root.append(name)

    def add_subject(self, subject, lang=None):
        subject_elem = self._me.subject(self._me.topic(subject))
        if lang:
            subject_elem.set('lang', lang)  # Add the lang attribute
        self._root.append(subject_elem)

    def add_identifier(self, id, type=None):
        ident = self._me.identifier(id)
        if type:
            ident.set('type', type)
        self._root.append(ident)

    def add_abstract(self, abstract, lang=None):
        abstract_elem = self._me.abstract(abstract)
        if lang:
            abstract_elem.set('lang', lang)  # Add the lang attribute
        self._root.append(abstract_elem)

    def add_table_of_contents(self, toc, lang=None):
        toc_elem = self._me.tableOfContents(toc)
        if lang:
            toc_elem.set('lang', lang)  # Add the lang attribute
        self._root.append(toc_elem)

    def add_type(self, type):
        if type in self.RESOURCE_TYPES:
            self._root.append(self._me.typeOfResource(type))

    def add_genre(self, genre, lang=None):
        genre_elem = self._me.genre(genre)
        if lang:
            genre_elem.set('lang', lang)  # Add the lang attribute
        self._root.append(genre_elem)

    def add_mime(self, mime):
        self.physical_description.append(self._me.internetMediaType(mime))

    def add_extent(self, extent):
        self.physical_description.append(self._me.extent(extent))

    def add_note(self, note, type=None, lang=None):
        note_elem = self._me.note(note)
        if type:
            note_elem.set('type', type)
        if lang:
            note_elem.set('lang', lang)  # Add the lang attribute
        self._root.append(note_elem)

    def add_access_condition(self, cond, xlink=None, lang=None):
        access_elem = self._me.accessCondition(cond)
        if xlink:
            access_elem.set('{%s}href' % XLINK_NAMESPACE, xlink)
        if lang:
            access_elem.set('lang', lang)  # Add the lang attribute
        self._root.append(access_elem)

    def add_publisher(self, pub, lang=None):
        pub_elem = self._me.publisher(pub)
        if lang:
            pub_elem.set('lang', lang)  # Add the lang attribute
        self.origin_info.append(pub_elem)

    def add_created_date(self, date, encoding=None, point=None,
                         qualifier=None, is_key_date=False):
        self.origin_info.append(
            self._create_date_elem('dateCreated', date, encoding, point,
                                   qualifier, is_key_date))

    def add_language(self, lang, type=None, authority=None):
        '''
        @param lang: value of the element
        @param type: either 'code' or 'text'
        @param authority: one of 'iso639-2b', 'rfc3066', 'iso639-3', 'rfc4646'
        @see: http://www.loc.gov/standards/mods/mods-outline.html#language
        '''
        lt = self._me.languageTerm(lang)

        if type in ['code', 'text']:
            lt.set('type', type)

        if authority in ['iso639-2b', 'rfc3066', 'iso639-3', 'rfc4646']:
            lt.set('authority', authority)

        self._root.append(self._me.language(lt))

    def add_location_url(self, url, date_last_accessed=None,
                         access=None, usage=None):
        '''
        @see:
        http://www.loc.gov/standards/mods/v3/mods-userguide-elements.html#url
        '''

        url_elem = self._me.url(url)

        if date_last_accessed:
            url_elem.set('dateLastAccessed', date_last_accessed)

        if access in ['preview', 'raw object', 'object in context']:
            url_elem.set('access', access)

        if usage in ['primary display', 'primary']:
            url_elem.set('usage', usage)

        self._root.append(self._me.location(url_elem))

    def add_related_item(self, other_mods, type=None):
        ''' Adds another Mods record as an embedded related item
        @param other_mods: This should be another instance of
            asurepo.metadata.Mods
        @param type: one of the following values:
            'preceding', 'succeeding', 'original', 'host', 'constituent',
            'series', 'otherVersion', 'otherFormat', 'isReferencedBy',
            'references', 'reviewOf'
        '''
        if not isinstance(other_mods, Mods):
            raise TypeError('You should only be supplying this method an ' +
                            'instance of asurepo.metadata.Mods')
        ri = self._me.relatedItem()
        if type in ['preceding', 'succeeding', 'original', 'host',
                    'constituent', 'series', 'otherVersion', 'otherFormat',
                    'isReferencedBy', 'references', 'reviewOf']:
            ri.set('type', type)

        for child in other_mods.etree.getchildren():
            ri.append(child)

        self._root.append(ri)

    def add_record_content_source(self, source):
        self.record_info.append(self._me.recordContentSource(source))

    def add_record_creation_date(self, date, encoding=None, point=None,
                         qualifier=None, is_key_date=False):
        self.record_info.append(
            self._create_date_elem('recordCreationDate', date, encoding, point,
                                   qualifier, is_key_date))

    def add_record_identifier(self, ident):
        self.record_info.append(self._me.recordIdentifier(ident))

    def add_record_origin(self, origin):
        self.record_info.append(self._me.recordOrigin(origin))
    
    def add_hierarchical_geographic(self, country, province, district, place, lang=None, authority1=None, authority2=None):
        """
        Add hierarchical geographic information (country > province > district > place).
        @param country: The country name.
        @param province: The province name.
        @param district: The district/prefecture name.
        @param place: The place name.
        @param lang: The language of the place names.
        @param authority: The authority for the country (e.g., "iso3166").
        """
        hierarchical_geo = self._me.hierarchicalGeographic()

        # Add country
        country_elem = self._me.country(country)
        if authority1:
            country_elem.set('authority', authority1)
        hierarchical_geo.append(country_elem)

        # Add province
        province_elem = self._me.province(province)
        if lang:
            province_elem.set('lang', lang)
        hierarchical_geo.append(province_elem)

        # Add district
        district_elem = self._me.county(district)
        if lang:
            district_elem.set('lang', lang)
        hierarchical_geo.append(district_elem)

        # Add place
        place_elem = self._me.city(place)
        if authority2:
            place_elem.set('authority', authority2)
        if lang:
            place_elem.set('lang', lang)
        hierarchical_geo.append(place_elem)

        # Add to subject
        subject_elem = self._me.subject()
        subject_elem.append(hierarchical_geo)
        self._root.append(subject_elem)
    
    def add_frequency(self, frequency):
        """
        Add frequency information to the originInfo section.
        @param frequency: The frequency of the resource 
        """
        if frequency:
            frequency_elem = self._me.frequency(frequency)
            self.origin_info.append(frequency_elem)
    
    def add_distribution(self, dist):
        """
        Add distribution information to the originInfo section.
        @param dist: The distribution location of the resource 
        """
        if dist:
            dist_elem = self._me.dist(dist)
            self.origin_info.append(dist_elem)