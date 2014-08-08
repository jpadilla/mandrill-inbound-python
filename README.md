# Mandrill Inbound Python Wrapper [![Build Status](https://travis-ci.org/jpadilla/mandrill-inbound-python.png?branch=master)](https://travis-ci.org/jpadilla/mandrill-inbound-python)


This is a simple API wrapper for [Mandrill's inbound email webhook](http://help.mandrill.com/entries/22092308-What-is-the-format-of-inbound-email-webhooks-)
in Python inspired by this other Python wrapper library I made for [Postmark Inbound](https://github.com/jpadilla/postmark-inbound-python).

## Install

Using Github:

```
git clone git://github.com/jpadilla/mandrill-inbound-python.git
```

Using pip:

```
pip install python-mandrill-inbound
```

Using easy_install:

```
easy_install python-mandrill-inbound
```


Usage
-----

```python
from mandrill_inbound import MandrillInbound


# Load from JSON string
json_data = open('./tests/fixtures/valid_http_post.json').read()
inbound = MandrillInbound(json=json_data)

# Load Python dictionary
json_data = json.loads(open('./tests/fixtures/valid_http_post.json').read())
inbound = MandrillInbound(source=json_data)

# Content
print inbound.subject
print inbound.sender
print inbound.to
print inbound.cc
print inbound.recipients
print inbound.message_id
print inbound.mailbox_hash
print inbound.html_body
print inbound.text_body
print inbound.send_date
print inbound.ts

# Spam and Spoofing Detection
print inbound.spf
print inbound.dkim
print inbound.spam_score

# headers
print inbound.headers  # default to get all headers
print inbound.headers['MIME-Version']
print inbound.headers['Received-SPF']

# attachments
print inbound.has_attachments # boolean
attachments = inbound.attachments

first_attachment = attachments[0]
print first_attachment.name

second_attachment = attachments[1]
print second_attachment.content_length

for a in attachments:
	print a.name
	print a.content_type
	print a.read()
	print a.download('./tests/', ['image/png'])

# raw data
print inbound.source
print inbound.msg
```

Bug tracker
-----------

Have a bug? Please create an issue here on GitHub!


Contributions
-------------

* Fork
* Write tests
* Write Code
* Pull request

Thanks for your help.


License
---------------------

MIT License
