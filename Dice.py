import random


class ActionDice(object):
    class RESULT:
        FAIL = 0
        SUCCESS = 1
        CRIT = 2

        @staticmethod
        def get_roll_counter(faces=None, **kwargs):
            """Get a dict set up to track/count a series of rolls."""
            if faces is None:
                faces = (0, 0, 0)
            return {
                ActionDice.RESULT.FAIL: faces[0],
                ActionDice.RESULT.SUCCESS: faces[1],
                ActionDice.RESULT.CRIT: faces[2],
            }

    def __init__(self, faces=None, **kwargs):
        if faces is None:
            faces = (1, 1, 1)

        self._fail, self._success, self._crit = faces
        self.faces = self._fail + self._success + self._crit

    def get_roll(self):
        roll = random.randint(0, self.faces - 1)
        if roll < self._fail:  # When there are no fails, it's zero, auto pass.
            return self.RESULT.FAIL
        elif self._success > 0 and roll < self._fail + self._success:
            return self.RESULT.SUCCESS
        elif self._crit > 0:  # Technically a redundant check. This method could probably be simplified.
            return self.RESULT.CRIT
        # This should never happen without deliberate interference.
        raise IndexError(f"Rolled an invalid face value: {roll}")


class Dice(object):

    def __init__(self, faces=6):
        self._faces = faces

    def get_roll(self):
        """Return a number between 1 and faces, inclusive"""
        return random.randint(1, self._faces)

    def get_rolls(self, rolls):
        """Return an array of numbers between 1 and faces, inclusive"""
        return [random.randint(1, self._faces) for _ in range(0, rolls)]

    def check_roll(self, score_check, modifier=0, beat=False):
        """
        Return a tuple representing a scored roll.

        Roll the dice, then compare to the value score_check.
        Tuple is a boolean followed by the roll value.

        The roll passes when it + the bonus value is higher than the score_check.

        When beat is false, the value may be greater than or equal to the score_check.
        """
        roll = self.get_roll()
        return (roll + modifier > score_check if beat else roll + modifier >= score_check), roll


if __name__ == '__main__':
    a = ActionDice()

    results = ActionDice.RESULT.get_roll_counter()

    for _ in range(0, 100):
        results[a.get_roll()] += 1
    print(results)
