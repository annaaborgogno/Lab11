from dataclasses import dataclass


@dataclass
class Arco:
    p1ID: int
    p2ID: int
    peso: int

    def __str__(self):
        return f"I prodotti {self.p1ID} e {self.p2ID} sono collegati con peso {self.peso}"