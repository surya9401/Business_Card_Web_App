import re
import difflib


# Class with parser to extract fields from a text input
class ContactInfo:

    def __init__(self, document):

        # extracting phone number
        search = re.compile('^.*\\d?.*\\d{3}.*\\d{3}.*\\d{4}$', re.MULTILINE)
        match = re.search(search, document)
        if match and match.group(0):
            match = re.findall('\\d', match.group(0))
            self.m_phone = ''.join(match)

        # extracting email
        search = re.compile('\\S+@.+', re.MULTILINE)
        match = re.search(search, document)
        if match and match.group(0):
            self.m_email = match.group(0)

        # extracting name
        search = re.compile('^\\w+\\s+\\w+$', re.MULTILINE)
        match = re.findall(search, document)
        match = [x.lower() for x in match]
        if self:
            username = self.m_email[:self.m_email.find('@')]
            matches = difflib.get_close_matches(username, match)
            if matches and matches[0] is not None:
                self.m_name = matches[0].title()

    # Respective getters for each field
    @property
    def getName(self):
        return self.m_name

    @property
    def getPhoneNumber(self):
        return self.m_phone

    @property
    def getEmailAddress(self):
        return self.m_email
