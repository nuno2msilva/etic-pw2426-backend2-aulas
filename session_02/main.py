import math
from abc import ABC, abstractmethod


# --- Tutorial: Singleton ---
# Guarantees only one instance of a class exists across the program
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


# Problem: Factory Pattern
# Abstract base ensures every shape exposes the same interface
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2


class Square(Shape):
    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side ** 2


# Factory function: caller specifies type, factory handles instantiation
def shape_factory(shape_type: str, **kwargs) -> Shape:
    shapes = {"circle": Circle, "square": Square}
    if shape_type not in shapes:
        raise ValueError(f"Unknown shape: '{shape_type}'")
    return shapes[shape_type](**kwargs)


# --- Challenge: Observer Pattern ---
# Subject broadcasts state changes to all registered observers
class Subject:
    def __init__(self):
        self._observers: list = []
        self._state = None

    def attach(self, observer) -> None:
        self._observers.append(observer)

    def detach(self, observer) -> None:
        self._observers.remove(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update(self._state)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self._notify()          # automatically notifies all observers on change


class Observer:
    def __init__(self, name: str):
        self.name = name

    def update(self, state) -> None:
        print(f"  [{self.name}] received state: {state}")


def main():
    # Tutorial: Singleton
    a = Singleton()
    b = Singleton()
    print("Singleton — same instance?", a is b)   # True

    # Problem: Factory
    circle = shape_factory("circle", radius=5)
    square = shape_factory("square", side=4)
    print(f"Circle area: {circle.area():.2f}")     # ~78.54
    print(f"Square area: {square.area():.2f}")     # 16.00

    # Challenge: Observer
    subject = Subject()
    subject.attach(Observer("Logger"))
    subject.attach(Observer("Dashboard"))

    print("Changing state to 'active':")
    subject.state = "active"
    print("Changing state to 'idle':")
    subject.state = "idle"


if __name__ == "__main__":
    main()
