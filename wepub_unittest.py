import unittest
import wepub

test_html = wepub.load_html("file:///~/git/web-epub-generator/test.html")

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
