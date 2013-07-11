import os.path
import unittest

from mandrill_inbound import MandrillInbound


class MandrillInboundTest(unittest.TestCase):

    def setUp(self):
        json_data = open('tests/fixtures/valid_http_post.json').read()
        self.inbound = MandrillInbound(json=json_data)

    def tearDown(self):
        if os.path.exists('./tests/equal.jpg'):
            os.remove('./tests/equal.jpg')

    def test_should_have_a_subject(self):
        assert 'Testing' == self.inbound.subject

    def test_should_have_a_cc(self):
        name, email = self.inbound.cc[0]

        assert 'Bob Johnson' == name
        assert 'bob@example.com' == email

    def test_should_have_a_message_id(self):
        message_id = '<54C9A31C34DF40409355EC9BB763EF15@example.com>'
        assert message_id == self.inbound.message_id

    def test_should_be_from_someone(self):
        name, email = self.inbound.sender

        assert name == 'John Smith'
        assert email == 'john@example.com'

    def test_should_have_a_html_body(self):
        assert '<p>We no speak americano</p>' == self.inbound.html_body

    def test_should_have_a_text_body(self):
        assert '\nThis is awesome!\n\n' == self.inbound.text_body

    def test_should_be_to_someone(self):
        name, email = self.inbound.to[0]

        assert 'testing+123testing@example.com' == email
        assert 'Testing Staging' == name

    def test_should_have_header_mime_version(self):
        assert '1.0' == self.inbound.headers['Mime-Version']

    def test_should_have_one_attachment(self):
        assert 1 == len(self.inbound.attachments)

    def test_should_have_attachment(self):
        assert True == self.inbound.has_attachments

    def test_attachment_should_have_content_type(self):
        for a in self.inbound.attachments:
            assert a.content_type is not None

    def test_attachment_should_have_name(self):
        for a in self.inbound.attachments:
            assert a.name is not None

    def test_attachment_should_download(self):
        for a in self.inbound.attachments:
            a.download('./tests/')

        assert True == os.path.exists('./tests/equal.jpg')

    def test_send_date(self):
        assert 2013 == self.inbound.send_date.year

    def test_mailbox_hash(self):
        assert '123testing' == self.inbound.mailbox_hash

    def test_ts(self):
        assert 2013 == self.inbound.ts.year

    def test_recipients(self):
        recip = self.inbound.recipients

        assert 'Testing Staging' == recip[0][0]
        assert 'testing+123testing@example.com' == recip[0][1]
        assert 'Bob Johnson' == recip[1][0]
        assert 'bob@example.com' == recip[1][1]


class MandrillInboundNoCcTest(unittest.TestCase):

    def setUp(self):
        json_data = open('tests/fixtures/valid_http_post_no_cc.json').read()
        self.inbound = MandrillInbound(json=json_data)

    def test_can_handle_no_cc(self):
        cc = self.inbound.cc
        assert [] == cc


if __name__ == "__main__":
    unittest.main()
