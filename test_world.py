import unittest
from test_base import *
import world.text.world as text_world
# import world.turtle.world as turtle_world

class test_world(unittest.TestCase):
    def test_text_world(self):
        with captured_io(StringIO()) as (out, err):
            text_world.setup_world("Bongo")
            text_world.update_position(10)
            text_world.do_right()
            text_world.update_position(20)
            self.assertEqual(text_world.position_y, 10)
            self.assertEqual(text_world.position_x, 20)
    

    # def test_turtle_world(self):
    #     with captured_io(StringIO()) as (out, err):
    #         turtle_world.start()
    #         turtle_world.update_position(10)
    #         turtle_world.do_right()
    #         turtle_world.update_position(20)
    #         self.assertEqual(turtle_world.robo_turtle.ycor(), 10)
    #         self.assertEqual(turtle_world.robo_turtle.xcor(), 20)

if __name__ == "__main__":
    unittest.main()