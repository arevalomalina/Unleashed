import unittest
import walker

class unleashed_test(unittest.TestCase):

	def test_sha1(self):
		self.assertEqual(walker.sha1('string'), 'ecb252044b5ea0f679ee78ec1a12904739e2904d')


if __name__=='__main__':
	unittest.main()