import robot
import unittest
import test_base
from io import StringIO

class Robot_Tests(unittest.TestCase):

    def test_forward_right_left(self):
        robot.world.obstacles.random.randint = lambda a, b: 0
        self.maxDiff = None
        intro = "What do you want to name your robot? Bomba: Hello kiddo!\nBomba: Loaded obstacles.\nBomba: What must I do next? "
        off = "Bomba: Shutting down.."
        next = "Bomba: What must I do next? "
        with test_base.captured_io(StringIO('Bomba\nforward 5\nright\nforward 10\nleft\nforward 5\noff')) as (out, err):
            robot.robot_start()
            output = out.getvalue().strip()
            self.assertEqual(f"{intro} > Bomba moved forward by 5 steps.\n > Bomba now at position (0,5).\n{next} > Bomba turned right.\n > Bomba now at position (0,5).\n{next} > Bomba moved forward by 10 steps.\n > Bomba now at position (10,5).\n{next} > Bomba turned left.\n > Bomba now at position (10,5).\n{next} > Bomba moved forward by 5 steps.\n > Bomba now at position (10,10).\n{next}{off}", output)


    def test_sprint(self):
        self.maxDiff = None
        with test_base.captured_io(StringIO('Bongo\nsprint 3\noff')) as (out, err):
            robot.world.obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
            output = out.getvalue().strip()
            self.assertEqual('''What do you want to name your robot? Bongo: Hello kiddo!
Bongo: Loaded obstacles.
Bongo: What must I do next?  > Bongo moved forward by 3 steps.
 > Bongo moved forward by 2 steps.
 > Bongo moved forward by 1 steps.
 > Bongo now at position (0,6).
Bongo: What must I do next? Bongo: Shutting down..''',output)


    def test_back_limit(self):
        self.maxDiff = None
        with test_base.captured_io(StringIO('Bomba\nforward 200\nforward 1\nright\nback 100\nback 1\noff')) as (out, err):
            robot.world.obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
            output = out.getvalue().strip()
            self.assertEqual('''What do you want to name your robot? Bomba: Hello kiddo!
Bomba: Loaded obstacles.
Bomba: What must I do next?  > Bomba moved forward by 200 steps.
 > Bomba now at position (0,200).
Bomba: What must I do next? Bomba: Sorry, I cannot go outside my safe zone.
 > Bomba now at position (0,200).
Bomba: What must I do next?  > Bomba turned right.
 > Bomba now at position (0,200).
Bomba: What must I do next?  > Bomba moved back by 100 steps.
 > Bomba now at position (-100,200).
Bomba: What must I do next? Bomba: Sorry, I cannot go outside my safe zone.
 > Bomba now at position (-100,200).
Bomba: What must I do next? Bomba: Shutting down..''',output)


    def test_correct_replay_flags(self):
        correct_flags = robot.correct_replay_flags("silent reversed 6-5")
        self.assertEqual(correct_flags, True)
        correct_flags = robot.correct_replay_flags("silent reversed 6-4 16")
        self.assertEqual(correct_flags, False)
        correct_flags = robot.correct_replay_flags("1")
        self.assertEqual(correct_flags, True)
        correct_flags = robot.correct_replay_flags("")
        self.assertEqual(correct_flags, True)


if __name__ == "__main__":
    unittest.main()