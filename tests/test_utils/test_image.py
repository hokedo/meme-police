from pathlib import Path

import pytest
from PIL import Image

from meme_police.env import IMAGE_SIMILARITY_THRESHOLD
from meme_police.utils.image import calculate_image_hash, calculate_image_hash_similarity


class TestCalculateImageHashSimalirity():
    IMAGES_FOLDER = Path('tests') / 'data' / 'images'
    TRADE_OFFER_MEME_FOLDER = IMAGES_FOLDER / 'trade_offer_meme'
    DISTRACTED_BOYFRIEND_MEME_FOLDER = IMAGES_FOLDER / 'distracted_boyfriend'

    def test_trade_offer_meme_original_not_similar_to_edited(self):
        similarity = self.load_and_calculate_similarity(
            self.TRADE_OFFER_MEME_FOLDER / 'original.png',
            self.TRADE_OFFER_MEME_FOLDER / 'text_and_edit.jpg',
        )

        assert similarity < IMAGE_SIMILARITY_THRESHOLD

    @pytest.mark.skip("Not handling this case well but it should")
    def test_trade_offer_meme_similarity_with_extra_border(self):
        similarity = self.load_and_calculate_similarity(
            self.TRADE_OFFER_MEME_FOLDER / 'original.png',
            self.TRADE_OFFER_MEME_FOLDER / 'original_extra_border.jpg',
        )

        assert similarity >= IMAGE_SIMILARITY_THRESHOLD

    def test_trade_offer_meme_not_similar_with_distracted_boyfriend(self):
        similarity = self.load_and_calculate_similarity(
            self.TRADE_OFFER_MEME_FOLDER / 'original.png',
            self.DISTRACTED_BOYFRIEND_MEME_FOLDER / 'cute_memes.jpg',
        )

        assert similarity <= IMAGE_SIMILARITY_THRESHOLD

    def load_and_calculate_similarity(self, image_a_path, image_b_path):
        with Image.open(image_a_path) as image_a:
            with Image.open(image_b_path) as image_b:
                image_a_hash = calculate_image_hash(image_a)
                image_b_hash = calculate_image_hash(image_b)

                return calculate_image_hash_similarity(image_a_hash, image_b_hash)
