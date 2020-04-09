import unittest
from ignite.engine import Engine
from ignite.contrib.metrics import CharacterErrorRate, WordErrorRate


class CERTestCase(unittest.TestCase):
    def setUp(self):
        self.cer = CharacterErrorRate()

    def test_cer_0(self):
        self.cer.update((["abc"], ["abc"]))
        self.assertEqual(self.cer.compute(), 0)

    def test_cer_1(self):
        self.cer.update((["abc"], ["ab"]))
        self.assertEqual(self.cer.compute(), 1 / 2)

    def test_cer_2(self):
        self.cer.update((["ab"], ["ade"]))
        self.assertEqual(self.cer.compute(), 2 / 3)

    def test_cer_3(self):
        self.cer.update((["ab"], ["ade"]))
        self.assertEqual(self.cer.compute(), 2 / 3)
        self.cer.update((["a"], ["a"]))
        self.assertEqual(self.cer.compute(), (2 / 3 + 0 / 1) / 2)
        self.cer.update((["de"], ["fgh"]))
        self.assertEqual(self.cer.compute(), (2 / 3 + 0 / 1 + 3 / 3) / 3)

    def tearDown(self):
        self.cer.reset()


class WERWordTestCase(unittest.TestCase):
    def setUp(self):
        self.wer = WordErrorRate()

    def test_wer_0(self):
        self.wer.update((["abc"], ["abc"]))
        self.assertEqual(self.wer.compute(), 0)

    def test_wer_1(self):
        self.wer.update((["abc"], ["ab"]))
        self.assertEqual(self.wer.compute(), 1)

    def test_wer_2(self):
        self.wer.update((["ab"], ["ade"]))
        self.assertEqual(self.wer.compute(), 1)

    def test_wer_3(self):
        self.wer.update((["ab"], ["ade"]))
        self.assertEqual(self.wer.compute(), 1)
        self.wer.update((["a"], ["a"]))
        self.assertEqual(self.wer.compute(), (1 + 0) / 2)
        self.wer.update((["de"], ["fgh"]))
        self.assertEqual(self.wer.compute(), (1 + 0 + 1) / 3)

    def test_wer_4(self):
        self.wer.update((["word0 word1 word2"], ["word1 word2 word3"]))
        self.assertEqual(self.wer.compute(), 2 / 3)

    def test_wer_5(self):
        self.wer.update((["word1"], ["word0"]))
        self.assertEqual(self.wer.compute(), 1 / 1)

    def test_wer_6(self):
        self.wer.update((["word1 word2 word3"], ["word1 word2 word3"]))
        self.assertEqual(self.wer.compute(), 0 / 3)

    def test_wer_7(self):
        self.wer.update((["word2 word3 "], ["word2 word1"]))
        self.assertEqual(self.wer.compute(), 2 / 2)

    def tearDown(self):
        self.wer.reset()


if __name__ == "__main__":
    unittest.main()
