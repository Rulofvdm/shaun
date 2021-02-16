import unittest
import maze.obstacles as obstacles

class test_obstacles(unittest.TestCase):
    def test_is_path_blocked(self):
        obstacles.obstacle_list = [(1, 1)]
        self.assertEqual(obstacles.is_path_blocked(0 , 2, 50, 2), True)

    def test_is_position_blocked(self):
        obstacles.create_random_obstacles()
        obstacles.obstacle_list = [(10,10), (100,100)]
        self.assertEqual(obstacles.is_position_blocked(11,11), True)
        self.assertEqual(obstacles.is_position_blocked(11,15), False)

if __name__ == "__main__":
    unittest.main()