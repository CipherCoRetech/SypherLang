class Staking:
    def __init__(self):
        self.stakeholders = {}

    def add_stake(self, address, amount):
        if address in self.stakeholders:
            self.stakeholders[address] += amount
        else:
            self.stakeholders[address] = amount

    def get_stake(self, address):
        return self.stakeholders.get(address, 0)

    def select_validator(self):
        if not self.stakeholders:
            return None

        total_stake = sum(self.stakeholders.values())
        choice = random.uniform(0, total_stake)

        current = 0
        for address, stake in self.stakeholders.items():
            current += stake
            if current >= choice:
                return address
