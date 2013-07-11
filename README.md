# Mandrill Inbound Python Wrapper


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

```
from mandrill_inbound import MandrillInbound


# Load from JSON string
json_data = open('./tests/fixtures/valid_http_post.json').read()
inbound = MandrillInbound(json=json_data)

# Load Python dictionary
json_data = json.loads(open('./tests/fixtures/valid_http_post.json').read())
inbound = MandrillInbound(source=json_data)

# Content
inbound.subject
inbound.sender
inbound.to
inbound.cc
inbound.recipients
inbound.message_id
inbound.mailbox_hash
inbound.html_body
inbound.text_body
inbound.send_date
inbound.ts

# headers
inbound.headers  # default to get all headers
inbound.headers['MIME-Version']
inbound.headers['Received-SPF']

# attachments
inbound.has_attachments # boolean
attachments = inbound.attachments

first_attachment = attachments[0]
first_attachment.name

second_attachment = attachments[1]
second_attachment.content_length

for a in attachments:
  a.name
	a.content_type
	a.read()
	a.download('./tests/', ['image/png'])

# raw data
inbound.source
inbound.msg
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
