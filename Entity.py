from Wounds import WoundManager
from Dice import ActionDice


class Entity(object):
    COUNT = 1

    def __init__(self, wounds, defense, damage, name=None):
        if name is None:
            name = f'Entity-{self.__class__.COUNT}'
            self.__class__.COUNT += 1
        self._name = name
        self._wounds = WoundManager(wounds=wounds, defense=defense)
        self._damage = damage

        self._damage_inflicted = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def wounds(self) -> WoundManager:
        return self._wounds

    def _count_damage(self, target):
        print(f'{self.name} does {self._damage} damage to {target.name}')
        self._damage_inflicted += self._damage

    def attack(self, target):
        # Keeping this simple for testing
        a = ActionDice((3, 5, 2))

        result = a.get_roll()
        if result == ActionDice.RESULT.FAIL:
            print(f'{self.name} misses {target.name}')
            return  # Early exit
        print(f'{self.name} hits {target.name}')
        on_hit = lambda entity=target: self._count_damage(target=entity)  # This will be called when a hit causes damage
        args = dict(damage=self._damage, on_hit=on_hit, crit=False)
        if result == ActionDice.RESULT.CRIT:
            args['crit'] = True
        target.wounds.check_hit(**args)
        if not target.wounds.active:
            print(f'{self.name} kills {target.name}')


import random

if __name__ == '__main__':
    player = Entity(wounds=4, defense=50, damage=15, name='Smackers')
    monster1 = Entity(wounds=2, defense=35, damage=7)
    monster2 = Entity(wounds=2, defense=35, damage=7)

    entities = [player, monster1, monster2]
    count = 1
    while player.wounds.active and (monster1.wounds.active or monster2.wounds.active):
        print(f'--- Round {count}---')
        health_bars = [f'{_entity.name}: {_entity.wounds.wound_string}' for _entity in [player, monster1, monster2]]
        print(' '.join(health_bars))
        print()
        target = random.randint(0, 1)
        if target % 2 == 0:
            player.attack(monster1)
        else:
            player.attack(monster2)
        monster1.attack(player)
        monster2.attack(player)
        count += 1
        print()
