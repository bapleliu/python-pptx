# encoding: utf-8

"""Test data for presentation-related oxml unit tests"""

from __future__ import absolute_import, print_function, unicode_literals

from lxml import objectify

from pptx.oxml import parse_xml_bytes
from pptx.oxml.ns import nsdecls


class BaseBuilder(object):
    """
    Provides common behavior for all data builders.
    """
    nsdecls = ' %s' % nsdecls('p')

    def __init__(self):
        """Establish instance variables with default values"""
        self._empty = False
        self._indent = 0
        self._nsdecls = ''

    @property
    def element(self):
        """Return element based on XML generated by builder"""
        elm = parse_xml_bytes(self.xml)
        objectify.deannotate(elm, cleanup_namespaces=True)
        return elm

    @property
    def is_empty(self):
        return True

    def with_indent(self, indent):
        """Add integer *indent* spaces at beginning of element XML"""
        self._indent = indent
        return self

    def with_nsdecls(self):
        self._nsdecls = self.nsdecls
        return self

    @property
    def xml_bytes(self):
        return self.xml.encode('utf-8')


class CT_PresentationBuilder(BaseBuilder):
    """
    Test data builder for CT_Presentation (<p:presentation>) XML element that
    appears in presentation.xml files.
    """
    def __init__(self):
        """Establish instance variables with default values"""
        super(CT_PresentationBuilder, self).__init__()
        self._sldIdLst = None
        self._sldSz = None
        self._nsdecls = self.nsdecls

    @property
    def is_empty(self):
        return self._sldIdLst is None and self._sldSz is None

    def with_sldIdLst(self):
        """Add an empty slide id list element"""
        self._sldIdLst = a_sldIdLst()
        return self

    def with_sldSz(self):
        """Add an empty slide size element"""
        self._sldSz = a_sldSz()
        return self

    @property
    def xml(self):
        """Return element XML based on attribute settings"""
        indent = ' ' * self._indent
        if self.is_empty:
            xml = '%s<p:presentation%s/>\n' % (indent, self._nsdecls)
        else:
            xml = '%s<p:presentation%s>\n' % (indent, self._nsdecls)
            if self._sldIdLst:
                xml += self._sldIdLst.with_indent(self._indent+2).xml
            if self._sldSz:
                xml += self._sldSz.with_indent(self._indent+2).xml
            xml += '%s</p:presentation>\n' % indent
        return xml


class CT_SlideIdListBuilder(BaseBuilder):
    """
    Test data builder for CT_SlideIdList (<p:sldIdLst>) XML element that
    appears as a child of <p:presentation>.
    """
    def __init__(self):
        """Establish instance variables with default values"""
        super(CT_SlideIdListBuilder, self).__init__()

    @property
    def is_empty(self):
        return True

    @property
    def xml(self):
        """Return element XML based on attribute settings"""
        indent = ' ' * self._indent
        if self.is_empty:
            xml = '%s<p:sldIdLst%s/>\n' % (indent, self._nsdecls)
        else:
            xml = '%s<p:sldIdLst%s>\n' % (indent, self._nsdecls)
            xml += '%s</p:sldIdLst>\n' % indent
        return xml


class CT_SlideSizeBuilder(BaseBuilder):
    """
    Test data builder for CT_SlideSize (<p:sldSz>) XML element that
    appears as a child of <p:presentation>.
    """
    def __init__(self):
        """Establish instance variables with default values"""
        super(CT_SlideSizeBuilder, self).__init__()

    @property
    def is_empty(self):
        return True

    @property
    def xml(self):
        """Return element XML based on attribute settings"""
        indent = ' ' * self._indent
        if self.is_empty:
            xml = '%s<p:sldSz%s/>\n' % (indent, self._nsdecls)
        else:
            xml = '%s<p:sldSz%s>\n' % (indent, self._nsdecls)
            xml += '%s</p:sldSz>\n' % indent
        return xml


def a_presentation():
    """Return a CT_PresentationBuilder instance"""
    return CT_PresentationBuilder()


def a_sldIdLst():
    """Return a CT_SlideIdListBuilder instance"""
    return CT_SlideIdListBuilder()


def a_sldSz():
    """Return a CT_SlideSizeBuilder instance"""
    return CT_SlideSizeBuilder()
