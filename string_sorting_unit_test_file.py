import unittest

from string_sorting import sort_the_solution


class Testsorting(unittest.TestCase):
    def test_sorting_alphabets(self):
        """
        Test that it return sorted alphabets
        """
        string_input = 'Contrary to popular belief, the pink unicorn flies east.'
        result = sort_the_solution(string_input)
        print("displaying the result :",result)
        ouput = 'aaabcceeeeeffhiiiiklllnnnnooooppprrrrssttttuuy'
        self.assertEqual(result, ouput)

if __name__ == '__main__':
    unittest.main()