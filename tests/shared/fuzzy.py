from unittest import TestCase

from ...coq.shared.fuzzy import dl_distance, metrics, multi_set_ratio, quick_ratio

_LOOK_AHEAD = 2


class MultiSetRatio(TestCase):
    def test_1(self) -> None:
        lhs = ""
        rhs = "a"
        ratio = multi_set_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 1)

    def test_2(self) -> None:
        lhs = "a"
        rhs = "ab"
        ratio = multi_set_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 1)

    def test_3(self) -> None:
        lhs = "ac"
        rhs = "ab"
        ratio = multi_set_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 1 / 2)

    def test_4(self) -> None:
        lhs = "acb"
        rhs = "abc"
        ratio = multi_set_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 1)

    def test_5(self) -> None:
        lhs = "abc"
        rhs = "abz"
        ratio = multi_set_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 2 / 3)


class QuickRatio(TestCase):
    def test_1(self) -> None:
        lhs = "a"
        rhs = "ab"
        ratio = quick_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 1)

    def test_2(self) -> None:
        lhs = "ac"
        rhs = "ab"
        ratio = quick_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 1 / 2)

    def test_3(self) -> None:
        lhs = "abc"
        rhs = "acb"
        ratio = quick_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 2 / 3)

    def test_4(self) -> None:
        lhs = "abcd"
        rhs = "abdc"
        ratio = quick_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 3 / 4)

    def test_5(self) -> None:
        lhs = "bcd"
        rhs = "cdb"
        ratio = quick_ratio(lhs, rhs, look_ahead=_LOOK_AHEAD)
        self.assertAlmostEqual(ratio, 1 / 2)


class EditD(TestCase):
    def test_1(self) -> None:
        lhs = ""
        rhs = ""
        d = dl_distance(lhs, rhs)
        self.assertEqual(d, 0)

    def test_2(self) -> None:
        lhs = "a"
        rhs = "b"
        d = dl_distance(lhs, rhs)
        self.assertEqual(d, 1)

    def test_3(self) -> None:
        lhs = "ca"
        rhs = "abc"
        d = dl_distance(lhs, rhs)
        self.assertEqual(d, 2)

    def test_4(self) -> None:
        lhs = "cac"
        rhs = "aca"
        d = dl_distance(lhs, rhs)
        self.assertEqual(d, 2)

    def test_5(self) -> None:
        lhs = "cacaca"
        rhs = "acacac"
        d = dl_distance(lhs, rhs)
        self.assertEqual(d, 2)

    def test_6(self) -> None:
        lhs = ""
        rhs = "abc"
        d = dl_distance(lhs, rhs)
        self.assertEqual(d, 3)

    def test_7(self) -> None:
        lhs = "ab"
        rhs = "bca"
        d = dl_distance(lhs, rhs)
        self.assertEqual(d, 2)

    def test_8(self) -> None:
        lhs = "badc"
        rhs = "abcd"
        d = dl_distance(lhs, rhs)
        self.assertEqual(d, 2)

    def test_9(self) -> None:
        lhs = "supervisor"
        rhs = "pervisor"
        d = dl_distance(lhs, rhs)
        self.assertEqual(d, 2)


class Metrics(TestCase):
    def test_1(self) -> None:
        cword = "ab"
        match = "abab"
        m = metrics(cword, match, look_ahead=_LOOK_AHEAD)
        self.assertEqual(m.prefix_matches, 2)
        self.assertEqual(m.edit_distance, 1)

    def test_2(self) -> None:
        cword = "ab"
        match = "ac"
        m = metrics(cword, match, look_ahead=_LOOK_AHEAD)
        self.assertEqual(m.prefix_matches, 1)
        self.assertAlmostEqual(m.edit_distance, 1 / 2)

    def test_3(self) -> None:
        cword = "abc"
        match = "abd"
        m = metrics(cword, match, look_ahead=_LOOK_AHEAD)
        self.assertEqual(m.prefix_matches, 2)
        self.assertAlmostEqual(m.edit_distance, 2 / 3)

    def test_4(self) -> None:
        cword = "per"
        match = "supervisor"
        m = metrics(cword, match, look_ahead=_LOOK_AHEAD)
        self.assertEqual(m.prefix_matches, 0)
        self.assertAlmostEqual(m.edit_distance, 1)

    def test_5(self) -> None:
        cword = "uper"
        match = "supervisor"
        m = metrics(cword, match, look_ahead=_LOOK_AHEAD)
        self.assertEqual(m.prefix_matches, 0)
        self.assertAlmostEqual(m.edit_distance, 1)

    def test_6(self) -> None:
        cword = "00"
        match = "11"
        m = metrics(cword, match, look_ahead=_LOOK_AHEAD)
        self.assertEqual(m.prefix_matches, 0)
        self.assertAlmostEqual(m.edit_distance, 0)
