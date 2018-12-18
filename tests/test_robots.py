import codecs
import unittest

from robotstxtparser import robotstxtparser


class RobotsTest(unittest.TestCase):

    def test_honors_specific_agent(self):
        """Honors the specific user agent if a match is found"""
        rp = robotstxtparser.RobotExclusionRulesParser()
        rp.parse('''
        User-agent: *
        Disallow: /tmp
        
        User-agent: agent
        Allow: /tmp
        ''')

        self.assertTrue(rp.is_allowed('agent', 'http://example.org/tmp'))
        self.assertTrue(rp.is_allowed('agent', 'http://example.org/path'))

    def test_grouping(self):
        """Multiple consecutive User-Agent lines are allowed."""
        rp = robotstxtparser.RobotExclusionRulesParser()
        rp.parse('''
            User-agent: one
            User-agent: two
            Disallow: /tmp
        ''')

        self.assertFalse(rp.is_allowed('one', 'http://example.org/tmp'))
        self.assertFalse(rp.is_allowed('two', 'http://example.org/tmp'))
        self.assertTrue(rp.is_allowed('agent', 'http://example.org/tmp'))

    def test_grouping_unknown_keys(self):
        """
        When we encounter unknown keys, we should disregard any grouping that may have
        happened between user agent rules.

        This is an example from the wild. Despite `Noindex` not being a valid directive,
        we'll not consider the '*' and 'ia_archiver' rules together.
        """
        rp = robotstxtparser.RobotExclusionRulesParser()
        rp.parse('''
            User-agent: *
            Disallow: /content/2/
            User-agent: *
            Noindex: /gb.html
            Noindex: /content/2/
            User-agent: ia_archiver
            Disallow: /
        ''')

        self.assertTrue(rp.is_allowed('agent', 'http://example.org/foo'))
        self.assertTrue(rp.is_allowed('ia_archiver', 'http://example.org/bar'))

    def test_case_insensitivity(self):
        """Make sure user agent matches are case insensitive"""
        rp = robotstxtparser.RobotExclusionRulesParser()
        rp.parse('''
            User-agent: Agent
            Disallow: /path
        ''')

        self.assertFalse(rp.is_allowed('agent', 'http://example.org/path'))
        self.assertFalse(rp.is_allowed('aGeNt', 'http://example.org/path'))

    def test_skip_malformed_line(self):
        """If there is no colon in a line, then we must skip it"""
        rp = robotstxtparser.RobotExclusionRulesParser()
        rp.parse('''
            User-Agent: agent
            Disallow /no/colon/in/this/line
        ''')

        self.assertTrue(rp.is_allowed('agent', 'http://example.org/no/colon/in/this/line'))

    def test_utf8_bom(self):
        """If there's a utf-8 BOM, we should parse it as such"""
        rp = robotstxtparser.RobotExclusionRulesParser()
        rp.parse(codecs.BOM_UTF8 + b'''
            User-Agent: agent
            Allow: /path
            User-Agent: other
            Disallow: /path
        ''')

        self.assertTrue(rp.is_allowed('agent', 'http://example.org/path'))
        self.assertFalse(rp.is_allowed('other', 'http://example.org/path'))

    def test_rfc_example(self):
        """Tests the example provided by the RFC"""
        rp = robotstxtparser.RobotExclusionRulesParser()
        rp.parse('''
            # /robots.txt for http://www.fict.org/
            # comments to webmaster@fict.org
            
            User-agent: unhipbot
            Disallow: /
            
            User-agent: webcrawler
            User-agent: excite
            Disallow:
            
            User-agent: *
            Disallow: /org/plans.html
            Allow: /org/
            Allow: /serv
            Allow: /~mak
            Disallow: /
        ''')

        # The unhipbot bot
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/'))
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/index.html'))
        self.assertTrue(rp.is_allowed('unhipbot', 'http://example.org/robots.txt'))
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/server.html'))
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/services/fast.html'))
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/services/slow.html'))
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/orgo.gif'))
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/org/about.html'))
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/org/plans.html'))
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/%7Ejim/jim.html'))
        self.assertFalse(rp.is_allowed('unhipbot', 'http://example.org/%7Emak/mak.html'))

        # The webcrawler bot
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/index.html'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/robots.txt'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/server.html'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/services/fast.html'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/services/slow.html'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/orgo.gif'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/org/about.html'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/org/plans.html'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/%7Ejim/jim.html'))
        self.assertTrue(rp.is_allowed('webcrawler', 'http://example.org/%7Emak/mak.html'))

        # The excite bot
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/index.html'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/robots.txt'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/server.html'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/services/fast.html'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/services/slow.html'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/orgo.gif'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/org/about.html'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/org/plans.html'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/%7Ejim/jim.html'))
        self.assertTrue(rp.is_allowed('excite', 'http://example.org/%7Emak/mak.html'))

        # All others
        self.assertFalse(rp.is_allowed('anything', 'http://example.org/'))
        self.assertFalse(rp.is_allowed('anything', 'http://example.org/index.html'))
        self.assertTrue(rp.is_allowed('anything', 'http://example.org/robots.txt'))
        self.assertTrue(rp.is_allowed('anything', 'http://example.org/server.html'))
        self.assertTrue(rp.is_allowed('anything', 'http://example.org/services/fast.html'))
        self.assertTrue(rp.is_allowed('anything', 'http://example.org/services/slow.html'))
        self.assertFalse(rp.is_allowed('anything', 'http://example.org/orgo.gif'))
        self.assertTrue(rp.is_allowed('anything', 'http://example.org/org/about.html'))
        self.assertFalse(rp.is_allowed('anything', 'http://example.org/org/plans.html'))
        self.assertFalse(rp.is_allowed('anything', 'http://example.org/%7Ejim/jim.html'))
        self.assertTrue(rp.is_allowed('anything', 'http://example.org/%7Emak/mak.html'))

