import unittest
from limerick import LimerickDetector

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.ld = LimerickDetector()

    def test_syllables(self):
        s = []
        try: self.assertEqual(self.ld.num_syllables("dog"), 1)
        except: s.append(1)
        try: self.assertEqual(self.ld.num_syllables("asdf"), 1)
        except: s.append(2)
        try: self.assertEqual(self.ld.num_syllables("letter"), 2)
        except: s.append(3)
        try: self.assertEqual(self.ld.num_syllables("washington"), 3)
        except: s.append(4)
        try: self.assertEqual(self.ld.num_syllables("dock"), 1)
        except: s.append(5)
        try: self.assertEqual(self.ld.num_syllables("dangle"), 2)
        except: s.append(6)
        try: self.assertEqual(self.ld.num_syllables("thrive"), 1)
        except: s.append(7)
        try: self.assertEqual(self.ld.num_syllables("fly"), 1)
        except: s.append(8)
        try: self.assertEqual(self.ld.num_syllables("placate"), 2)
        except: s.append(9)
        try: self.assertEqual(self.ld.num_syllables("renege"), 2)
        except: s.append(10)
        try: self.assertEqual(self.ld.num_syllables("reluctant"), 3)
        except: s.append(11)

        print '\nNumber of failed syllables tests:', str(len(s))
        if len(s)!=0: print 'Failed syllables tests:', ','.join([str(x) for x in s])

if __name__ == '__main__':
    unittest.main()
