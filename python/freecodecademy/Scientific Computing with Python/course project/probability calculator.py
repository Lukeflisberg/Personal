import copy
import random

class Hat:
    def __init__(self, **balls):
        self.contents = []

        for color, count in balls.items():
            self.contents.extend([color] * count)

    def draw(self, num_balls):
        drawn_balls = []

        # Removing more balls than there are available
        if num_balls > len(self.contents):
            drawn_balls = self.contents.copy()
            self.contents.clear()
            return drawn_balls
        
        # Remove balls
        for _ in range(num_balls):
            chosen_ball = random.choice(self.contents)
            drawn_balls.append(chosen_ball)
            self.contents.remove(chosen_ball)
        return drawn_balls

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    num_succeeded = 0

    # Loop through num experiments
    for _ in range(1, num_experiments+1):
        # Create a deep copy of hat
        hat_copy = copy.deepcopy(hat)
        drawn_balls = hat_copy.draw(num_balls_drawn)

        # Loop through results, checking each color
        success = True
        for color, count in expected_balls.items():
            if (drawn_balls.count(color) < count):
                success = False
                break
        
        if success:
            num_succeeded += 1

    return (num_succeeded / num_experiments)

hat = Hat(black=6, red=4, green=3)
probability = experiment(hat=hat,
                  expected_balls={'red':2,'green':1},
                  num_balls_drawn=5,
                  num_experiments=2000)