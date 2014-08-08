import json
import re
from base64 import b64decode
from datetime import datetime
from email.utils import mktime_tz, parsedate_tz


class MandrillInbound(object):

    def __init__(self, *args, **kwargs):
        if not kwargs.get('json') and not kwargs.get('source'):
            raise Exception('Mandrill Inbound Error: you must \
                            provide json or source')

        if kwargs.get('source'):
            self.source = kwargs.get('source')
        else:
            self.source = json.loads(kwargs.get('json'))[0]

        self.msg = self.source.get('msg')

        if self.source['event'] != 'inbound':
            raise Exception('Mandrill event not inbound')

        if not self.msg:
            raise Exception('Mandrill msg not found')

    def _normalize_addresses(self, addresses):
        recipients = []

        for email, name in addresses:
            recipients.append((name, email))

        return recipients
    
    @property
    def subject(self):
        """
        The subject line of the message 
        """
        return self.msg.get('subject')
    
    @property
    def sender(self):
        """
        An array of the From Name and Email.
        """
        return (self.msg.get('from_name'), self.msg.get('from_email'))
        
    @property
    def cc(self):
        """
        All names and emails the email was indirectly sent to (cc'd)
        """
        return self._normalize_addresses(self.msg.get('cc', []))
        
    @property
    def to(self):
        """
        All names and emails the email was directly sent to (to)
        """
        return self._normalize_addresses(self.msg.get('to', []))

    @property
    def recipients(self):
        """
        All recipients of the message, both to'd and cc'd
        """
        return self.to + self.cc

    @property
    def headers(self):
        """
        A dictionary of all headers recieved for the message.
        """
        headers = self.msg.get('headers')
        return headers

    @property
    def message_id(self):
        return self.headers['Message-Id']

    @property
    def attachments(self):
        """
        All attachments for this email.
        """
        attachments = []
        for name, attachment in self.msg.get('attachments', {}).items():
            attachments.append(Attachment(attachment))
        return attachments

    @property
    def has_attachments(self):
        """
        A boolean of the attachment type.
        """
        if not self.attachments:
            return False
        return True

    @property
    def html_body(self):
        """
        The body of the email in html form.
        """
        return self.msg.get('html')

    @property
    def text_body(self):
        """
        The body of the email in text form.
        """
        return self.msg.get('text')
        
    @property
    def tags(self):
        """
        Included for completeness, but "but inbound messages generally won't have tags since they're being received instead of sent, and the sender is null since the event is for a message not being sent by Mandrill"
        According to http://help.mandrill.com/entries/22092308-What-is-the-format-of-inbound-email-webhooks-
        """
        return self.msg.get('tags')
        
    @property
    def dkim(self):
        """
        Returns a boolean, if True, DKIM was present and valid.
        If False, DKIM was not valid.
        DomainKeys Identified Mail(DKIM) protects against email spoofing.
        Yahoo, Gmail, AOL, and various others should use DKIM.
        DKIM lets you verify an email came on behalf of the claimed domain.
        """
        return self.msg.get('dkim').get('valid')
        
    @property
    def spf(self):
        """
        Returns a string of the the spf validation result. One of: pass, neutral, fail, softfail, temperror, permerror, none.
        Sender Policy Framework (SPF), is a tool to detect email spoofing by verifying sender IP addresses.
        """
        return self.msg.get('spf').get('result')
        
    @property
    def spam_score(self):
        """
        Returns a SpamAssassin score (float/int)
        The lower a score, the less likely the message is spam.
        """
        return self.msg.get('spam_report').get('score')

    @property
    def mailbox_hash(self):
        matches = re.search(r"\+(\S+)\@", self.msg.get('email'))

        if matches:
            return matches.group(1)

        return None

    @property
    def send_date(self):
        """
        Returns a date object of when the email was sent.
        """
        date = None
        rfc_2822 = self.headers['Date']
        if rfc_2822:
            try:
                date = datetime.fromtimestamp(mktime_tz(parsedate_tz(rfc_2822)))
            except:
                pass
        return date

    @property
    def ts(self):
        """
        UTC unix timestamp when that the event occurred
        """
        return datetime.fromtimestamp(self.source.get('ts'))


class Attachment(object):

    def __init__(self, attachment, **kwargs):
        self.attachment = attachment

    @property
    def name(self):
        """
        The name of the attachent.
        """
        return self.attachment.get('name')

    @property
    def content_type(self):
        """
        The MIME type of the attachment.
        """
        return self.attachment.get('type')

    def read(self):
        """
        Provides the raw binary content of the attachment file.
        """
        return b64decode(self.attachment.get('content'))

    def download(self, directory='', allowed_types=[]):
        """
        Download attachments into a directory.
        """
        if len(directory) == 0:
            raise Exception('Mandrill Inbound Error: you must provide \
                            the upload path')

        if allowed_types and self.content_type not in allowed_types:
            raise Exception('Mandrill Inbound Error: the file type %s is \
                            not allowed' % self.content_type)

        try:
            attachment = open('%s%s' % (directory, self.name), 'w')
            attachment.write(self.read())
        except IOError:
            raise Exception('Mandrill Inbound Error: cannot save the file, \
                            check path and rights.')
        else:
            attachment.close()
