
import unittest
from dork_generator import generate_dorks

class TestDorkGenerator(unittest.TestCase):

    def test_basic_dork_generation(self):
        target_info = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "username": "johndoe_dev"
        }
        platforms = {
            "social_media": {"enabled": True, "specific_platforms": ["twitter"]},
            "code_repositories": {"enabled": True, "specific_platforms": ["github"]}
        }
        ai_integration = {"dork_generation": False}
        dorks = generate_dorks(target_info, platforms, ai_integration)
        
        expected_dorks = [
            '"John Doe"',
            'intitle:"John Doe"',
            '"john.doe@example.com"',
            'intext:"john.doe@example.com"',
            '"johndoe_dev"',
            'inurl:"johndoe_dev"',
            'site:twitter.com "John Doe"',
            'site:twitter.com "john.doe@example.com"',
            'site:twitter.com "johndoe_dev"',
            'site:github.com "John Doe"',
            'site:github.com "john.doe@example.com"',
            'site:github.com "johndoe_dev"'
        ]
        self.assertCountEqual(dorks, expected_dorks)

    def test_ai_dork_generation(self):
        target_info = {
            "name": "Jane Smith",
            "username": "janesmith_osint"
        }
        platforms = {"social_media": {"enabled": False}}
        ai_integration = {"dork_generation": True}
        dorks = generate_dorks(target_info, platforms, ai_integration)

        self.assertIn('"Jane Smith" filetype:pdf resume', dorks)
        self.assertIn('"Jane Smith" inurl:cv OR inurl:resume', dorks)
        self.assertIn('"janesmith_osint" password OR credentials', dorks)

    def test_empty_input(self):
        target_info = {}
        platforms = {}
        ai_integration = {}
        dorks = generate_dorks(target_info, platforms, ai_integration)
        self.assertEqual(dorks, [])

    def test_partial_input(self):
        target_info = {"name": "Alice"}
        platforms = {"social_media": {"enabled": True, "specific_platforms": ["facebook"]}}
        ai_integration = {"dork_generation": False}
        dorks = generate_dorks(target_info, platforms, ai_integration)
        expected_dorks = [
            '"Alice"',
            'intitle:"Alice"',
            'site:facebook.com "Alice"'
        ]
        self.assertCountEqual(dorks, expected_dorks)

if __name__ == '__main__':
    unittest.main()


