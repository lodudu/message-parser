import re
import logging
import requests

from lxml import html

logger = logging.getLogger(__name__)
REGEX_USERNAME = '@[a-zA-Z0-9_]+'
REGEX_EMOTICON = '\([a-zA-Z]+\)'
REGEX_URL = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


class Message(object):

    def __init__(self, message):
        self.message = message
        self.supported_emoticons = self._get_supported_emoticons()

    @property
    def mentions(self):
        """Parsed list of mentioned user names of the message"""
        mentions = re.findall(REGEX_USERNAME, self.message)
        logging.debug("Matched mentions: {}".format(mentions))
        return [item.replace('@', '').strip() for item in mentions]

    @property
    def emoticons(self):
        """Parsed emoticons of the message"""
        emoticons = re.findall(REGEX_EMOTICON, self.message)
        logging.debug("Matched emoticons: {}".format(emoticons))
        raw_list = [item[1: -1] for item in emoticons]

        # Checking if the emoticon is supported is not required per description
        # but nice to have. This probably can also be loaded from a persistent
        # datastore, and saved as a global context.
        return [item for item in raw_list if self._is_valid_emoticon(item)]

    @property
    def links(self):
        """Parsed links of the message"""
        links = re.findall(REGEX_URL, self.message)
        logging.debug("Matched links: {}".format(links))

        link_list = []
        for link in links:
            result = {}
            result['url'] = link
            result['title'] = self._get_title(link)
            link_list.append(result)

        return link_list

    def _get_title(self, link):
        """Retrieve title for given link"""
        title = None
        res = requests.get(link)
        if res.status_code == 200:
            tree = html.fromstring(res.content)
            title = tree.xpath('//title/text()')[0]
            logger.info("Title for {}: {}".format(link, title))
        else:
            logger.error("Unable to get title for link {}".format(link))

        return title

    def _is_valid_emoticon(self, emoji):
        """Return if the specified emoticon is supported"""
        return emoji in self.supported_emoticons

    def _get_supported_emoticons(self):
        """Get the list of supported emoticons from hipchat.com/emoticons"""
        res = requests.get("https://www.hipchat.com/emoticons")
        tree = html.fromstring(res.content)
        raw_list = tree.xpath('//div[@class="emoticon-block"]')
        supported_emoticons = [item.attrib['data-clipboard-text'][1:-1] for item in raw_list]

        logger.debug("All supported emoticons: {}".format(supported_emoticons))
        return supported_emoticons
