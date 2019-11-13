from Dice import Dice

WOUND_INTEGRITY_MAX = 100


class WoundManager(object):

    def __init__(self, wounds, defense, **kwargs):
        self._wounds = wounds
        self._wound_integrity_max = WOUND_INTEGRITY_MAX
        self._integrity_die = Dice(faces=self._wound_integrity_max)

        self.defense_buffer = defense

        # Would only be used for reloading, don't expose in the normal signature
        self._wounds_taken = kwargs.get('wounds_taken', 0)
        self._current_wound_integrity = kwargs.get('current_wound_integrity', WOUND_INTEGRITY_MAX)

        self._out_of_action = self._wounds_taken >= self._wounds

    @property
    def active(self) -> bool:
        return not self._out_of_action

    @property
    def wound_string(self):
        wounds_taken = ['[x]' for _ in range(0, self._wounds_taken)]
        wounds_remaining = ['[100%]' for _ in range(0, self._wounds - self._wounds_taken)]
        if len(wounds_remaining) > 0:
            wounds_remaining.pop(0)
        wounds_remaining.insert(0, f'[{self._current_wound_integrity + self.defense_buffer}/{self._wound_integrity_max}]')
        wounds_taken.extend(wounds_remaining)
        return ' '.join(wounds_taken)

    def _take_wound(self):
        """Add one to the wound counter and check out_of_action."""
        self._wounds_taken += 1
        self._current_wound_integrity = 0
        self._out_of_action = self._wounds_taken >= self._wounds
        if not self._out_of_action:
            self._current_wound_integrity = self._wound_integrity_max

    def _roll_for_wound(self):
        """
        Roll the integrity die to determine if a wound should be taken.

        Roll a Dice with _wound_integrity_max sides. A wound is taken based on the following expression
        Take wound: roll > current_wound_integrity + defense_buffer
        :return:
        """
        # This returns a tuple (bool, int), return the bool
        return self._integrity_die.check_roll(self._current_wound_integrity + self.defense_buffer)[0]

    def check_hit(self, damage, on_hit=None, crit=False):
        if not self._out_of_action:  # Check is skipped when already out of action.
            self._current_wound_integrity -= damage  # Immediately reduce integrity by damage.

            if self._roll_for_wound():
                self._take_wound()
                if on_hit and callable(on_hit):
                    on_hit()
            if crit:
                # When applying a crit, reduce the damage by half, truncating floats, and hit again.
                self.check_hit(damage // 2, crit=False)
