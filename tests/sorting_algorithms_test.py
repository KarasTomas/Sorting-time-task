import unittest
import sys
import os

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from sorting_algorithms import sorting


# Class for testing sorting algorithms that inherit from unittest.TestCase
class TestSortingAlgorithms(unittest.TestCase):

    # Method that is called before each test - provided by unittest
    def setUp(self):
        self.unsorted_list = [64, 34, 25, 12, 22, 11, 90]
        self.sorted_list = [11, 12, 22, 25, 34, 64, 90]

    # test case method must start with test_
    def test_selection_sort(self):
        # assertEqual checks if the two arguments are equal - inherited from unittest.TestCase
        self.assertEqual(
            sorting.selection_sort(self.unsorted_list.copy()), self.sorted_list
        )

    def test_bubble_sort(self):
        self.assertEqual(
            sorting.bubble_sort(self.unsorted_list.copy()), self.sorted_list
        )

    def test_merge_sort(self):
        self.assertEqual(
            sorting.merge_sort(self.unsorted_list.copy()), self.sorted_list
        )


if __name__ == "__main__":
    # this finds all setups and test cases in the class and runs them
    unittest.main()
