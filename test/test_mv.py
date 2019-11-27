import unittest
from sympy import Symbol
from galgebra.ga import Ga
from galgebra import utils

class TestMv(unittest.TestCase):

    def test_is_base(self):
        """
        Various tests on several multivectors.
        """
        (_g3d, e_1, e_2, e_3) = Ga.build('e*1|2|3')

        self.assertTrue((e_1).is_base())
        self.assertTrue((e_2).is_base())
        self.assertTrue((e_3).is_base())
        self.assertTrue((e_1 ^ e_2).is_base())
        self.assertTrue((e_2 ^ e_3).is_base())
        self.assertTrue((e_1 ^ e_3).is_base())
        self.assertTrue((e_1 ^ e_2 ^ e_3).is_base())

        self.assertFalse((2 * e_1).is_base())
        self.assertFalse((e_1 + e_2).is_base())
        self.assertFalse((e_3 * 4).is_base())
        self.assertFalse(((3 * e_1) ^ e_2).is_base())
        self.assertFalse((2 * (e_2 ^ e_3)).is_base())
        self.assertFalse((e_3 ^ e_1).is_base())
        self.assertFalse((e_2 ^ e_1 ^ e_3).is_base())


    def test_blade_coefs(self):
        """
        Various tests on several multivectors.
        """
        (_g3d, e_1, e_2, e_3) = Ga.build('e*1|2|3')

        m0 =  2 * e_1 + e_2 - e_3 + 3 * (e_1 ^ e_3) + (e_1 ^ e_3) + (e_2 ^ (3 * e_3))
        self.assertTrue(m0.blade_coefs([e_1]) == [2])
        self.assertTrue(m0.blade_coefs([e_2]) == [1])
        self.assertTrue(m0.blade_coefs([e_1, e_2]) == [2, 1])
        self.assertTrue(m0.blade_coefs([e_1 ^ e_3]) == [4])
        self.assertTrue(m0.blade_coefs([e_1 ^ e_3, e_2 ^ e_3]) == [4, 3])
        self.assertTrue(m0.blade_coefs([e_2 ^ e_3, e_1 ^ e_3]) == [3, 4])
        self.assertTrue(m0.blade_coefs([e_1, e_2 ^ e_3]) == [2, 3])

        a = Symbol('a')
        b = Symbol('b')
        m1 = a * e_1 + e_2 - e_3 + b * (e_1 ^ e_2)
        self.assertTrue(m1.blade_coefs([e_1]) == [a])
        self.assertTrue(m1.blade_coefs([e_2]) == [1])
        self.assertTrue(m1.blade_coefs([e_3]) == [-1])
        self.assertTrue(m1.blade_coefs([e_1 ^ e_2]) == [b])
        self.assertTrue(m1.blade_coefs([e_2 ^ e_3]) == [0])
        self.assertTrue(m1.blade_coefs([e_1 ^ e_3]) == [0])
        self.assertTrue(m1.blade_coefs([e_1 ^ e_2 ^ e_3]) == [0])

        # Invalid parameters
        self.assertRaises(ValueError, lambda: m1.blade_coefs([e_1 + e_2]))
        self.assertRaises(ValueError, lambda: m1.blade_coefs([e_2 ^ e_1]))
        self.assertRaises(ValueError, lambda: m1.blade_coefs([e_1, e_2 ^ e_1]))
        self.assertRaises(ValueError, lambda: m1.blade_coefs([a * e_1]))
        self.assertRaises(ValueError, lambda: m1.blade_coefs([3 * e_3]))

    def test_rep_switching(self):
        # this ga has a non-diagonal metric
        (_g3d, e_1, e_2, e_3) = Ga.build('e*1|2|3')

        m0 =  2 * e_1 + e_2 - e_3 + 3 * (e_1 ^ e_3) + (e_1 ^ e_3) + (e_2 ^ (3 * e_3))
        m1 = (-4*(e_1 | e_3)-3*(e_2 | e_3))+2*e_1+e_2-e_3+4*e_1*e_3+3*e_2*e_3
        # m1 was chosen to make this true
        self.assertEqual(m0, m1)

        # all objects start off in blade rep
        self.assertTrue(m0.is_blade_rep)

        # convert to base rep
        m0_base = m0.base_rep()
        self.assertTrue(m0.is_blade_rep)  # original should not change
        self.assertFalse(m0_base.is_blade_rep)
        self.assertEqual(m0, m0_base)

        # convert back
        m0_base_blade = m0_base.blade_rep()
        self.assertFalse(m0_base.is_blade_rep)  # original should not change
        self.assertTrue(m0_base_blade.is_blade_rep)
        self.assertEqual(m0, m0_base_blade)

    def test_construction(self):
        (ga, e_1, e_2, e_3) = Ga.build('e*1|2|3')

        # non-function symbol construction
        self.assertEqual(ga.mv('A', 'scalar').grades, [0])
        self.assertEqual(ga.mv('A', 0).grades, [0])
        self.assertEqual(ga.mv('A', 'vector').grades, [1])
        self.assertEqual(ga.mv('A', 'grade', 1).grades, [1])
        self.assertEqual(ga.mv('A', 1).grades, [1])
        self.assertEqual(ga.mv('A', 'bivector').grades, [2])
        self.assertEqual(ga.mv('A', 'grade2').grades, [2])
        self.assertEqual(ga.mv('A', 2).grades, [2])
        self.assertEqual(ga.mv('A', 'pseudo').grades, [3])
        self.assertEqual(ga.mv('A', 'spinor').grades, [0, 2])
        self.assertEqual(ga.mv('A', 'even').grades, [0, 2])
        self.assertEqual(ga.mv('A', 'odd').grades, [1, 3])
        self.assertEqual(ga.mv('A', 'mv').grades, [0, 1, 2, 3])

        # illegal arguments
        with self.assertRaises(TypeError):
            ga.mv('A', 'vector', "too many arguments")
        with self.assertRaises(TypeError):
            ga.mv('A', 'grade')  # too few arguments
