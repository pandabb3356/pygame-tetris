from unittest import TestCase

from tetris.engine.texture import Texture


class TestTexture(TestCase):
    def test_init(self):
        content = "texture"

        texture = Texture(content)

        assert texture.content == content

    def test_load_pools(self):
        contents = ["content1", "content2"]
        Texture.load_pools(contents)

        assert "content1" in Texture.pools
        assert "content2" in Texture.pools
