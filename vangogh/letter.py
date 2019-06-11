from lxml import etree
import re
import string
import sys
import unicodedata

class Letter:

    def __init__(self, xml, parser=etree.XMLParser(attribute_defaults=True)):
        self.xml = etree.parse(xml, parser)

    def people(self):
        """
        Extract names of people mentioned in the letters
        """
        names = {}
        find_names = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}rs")
        for e in find_names(self.xml):
            names[re.sub(r'\s+', r' ', e.text)] = e.get('key')
        return names

    def original_text(self):
        """
        Return transcription (without textual notes)
        """
        find_textual_notes = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}div[@type=\"textualNotes\"]")
        for e in find_textual_notes(self.xml):
            e.getparent().remove(e)

        find = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}div[@type=\"original\"]//text()")
        text = ''.join(find(self.xml))
        return text

    def _whitespace(self, text):
        return re.sub("\s+", " ", text)

    def _punctuation(self, text):
        """
        remove unicode & ascii punctuation, except for apostrophes
        """
        unicode_punct = [
            '\u00a0', # NO-BREAK SPACE
            '\u00a3', # POUND SIGN
            '\u00b0', # DEGREE SIGN
            '\u00b1', # PLUS-MINUS SIGN
            '\u00b4', # ACUTE ACCENT
            '\u00b7', # MIDDLE DOT
            '\u00bb', # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
            '\u00bd', # VULGAR FRACTION ONE HALF
            '\u2013', # EN DASH
            '\u2014', # EM DASH
            '\u2018', # LEFT SINGLE QUOTATION MARK
            '\u201c', # LEFT DOUBLE QUOTATION MARK
            '\u201d', # RIGHT DOUBLE QUOTATION MARK
            '\u2026', # HORIZONTAL ELLIPSIS
            '\u2500', # BOX DRAWINGS LIGHT HORIZONTAL
            '\u25a1', # WHITE SQUARE
            # '\u2019', # RIGHT SINGLE QUOTATION MARK
        ]
        string_punct = list(string.punctuation)
        return re.sub(rf"[{''.join(unicode_punct + string_punct)}]", "", text)

    def _apostrophes(self, text):
        """
        Replace RIGHT SINGLE QUOTATION MARK with ascii apostrophe
        """
        return re.sub('\u2019', '\'', text)

    def _diacritics(self, text):
        """
        Replace characters with diacritical marks with their ascii equivalents
        """
        return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))

    def preprocess(self, levels=['whitespace', 'punctuation', 'apostrophes', 'diacritics']):
        """
        preprocess the text,

        """
        dispatch = {'whitespace': self._whitespace,
                    'punctuation': self._punctuation,
                    'apostrophes': self._apostrophes,
                    'diacritics': self._diacritics}

        text = self.original_text()
        for l in levels:
            text = dispatch[l](text)
        # text = self._whitespace(text)
        # text = self._punctuation(text)
        # text = self._apostrophes(text)
        # text = self._diacritics(text)
        return text
