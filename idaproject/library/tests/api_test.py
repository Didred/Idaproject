import os
import io
import unittest
from PIL import Image
from library.api.api import API

TEST_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Inkscape_vectorisation_test.svg/1280px-Inkscape_vectorisation_test.svg.png"
TEST_BAD_URL = "bad_url.ru"
TEST_NAME = "test_name"
TEST_WIDTH = 100
TEST_HEIGHT = 100

DATABASE_NAME = "database_test"
CONNECTION_STRING = "sqlite:///" + DATABASE_NAME


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = API(CONNECTION_STRING)

    def tearDown(self):
        os.remove(DATABASE_NAME)

    def add_pictire(self, url, name, picture):
        picture_id = self.api.add(url, name, picture)

        return picture_id

    def test_add_picture_by_link(self):
        picture_id = self.add_pictire(TEST_URL, TEST_NAME, None)

        self.assertEqual(picture_id, 1)
        self.assertRaises(Exception, self.add_pictire, TEST_BAD_URL, TEST_NAME, None)

    def test_get_picture(self):
        picture_id = self.add_pictire(TEST_URL, None, None)
        picture = self.api.get(picture_id)
        w, h = Image.open(io.BytesIO(picture.picture)).size

        self.assertEqual(picture.name, TEST_URL)
        self.assertEqual(picture.width, w)
        self.assertEqual(picture.height, h)
        self.assertIsNotNone(picture.picture)

    def test_get_pictures(self):
        self.add_pictire(TEST_URL, None, None)

        pictures = self.api.get_pictures()
        self.assertEqual(len(pictures), 1)

        self.add_pictire(TEST_URL, None, None)

        pictures = self.api.get_pictures()
        self.assertEqual(len(pictures), 2)

    def test_resize(self):
        picture_id = self.add_pictire(TEST_URL, None, None)
        picture = self.api.get(picture_id)
        image = Image.open(io.BytesIO(picture.picture))
        w, h = image.size

        new_picture = self.api.resize(picture_id, TEST_WIDTH, None)
        self.assertEqual(new_picture.width, TEST_WIDTH)
        self.assertEqual(new_picture.height, int(TEST_WIDTH / w * h))

        new_picture = self.api.resize(picture_id, None, TEST_HEIGHT)
        self.assertEqual(new_picture.height, TEST_HEIGHT)
        self.assertEqual(new_picture.width, int(TEST_HEIGHT / h * w))

        new_picture = self.api.resize(picture_id, TEST_WIDTH, TEST_HEIGHT)
        self.assertEqual(new_picture.height, TEST_HEIGHT)
        self.assertEqual(new_picture.width, TEST_WIDTH)


if __name__ == "__main__":
    unittest.main()
