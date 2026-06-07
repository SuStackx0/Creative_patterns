"""
PATTERN 2: FACTORY METHOD
=========================
Goal: a base class defines an algorithm that needs *a* product, but lets
SUBCLASSES decide *which concrete* product to create.

Classic GoF example: a logistics company plans deliveries. Planning is the
same everywhere, but RoadLogistics delivers by Truck and SeaLogistics by Ship.

⚠️ COMMON CONFUSION — this is NOT the "simple factory":
    def make_transport(kind):
        if kind == "truck": return Truck()
        if kind == "ship":  return Ship()
That if/else helper is called a SIMPLE FACTORY (not one of the 5 GoF
patterns). The real Factory Method pattern uses INHERITANCE: the creator
class has an abstract create method that each subclass overrides.

PYTHON CONCEPTS YOU'LL LEARN HERE
---------------------------------
1. ABC (Abstract Base Class): a class that CANNOT be instantiated directly;
   it only exists to be inherited from. Python's version of an "interface".
2. @abstractmethod: marks a method that subclasses MUST implement.
3. Polymorphism: code written against the base type (Transport) works with
   any subclass (Truck, Ship) without changes.
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# THE PRODUCTS — the things being created
# ---------------------------------------------------------------------------
class Transport(ABC):
    """Abstract product. Inheriting from ABC + having an @abstractmethod
    makes this class un-instantiable: Transport() raises TypeError."""

    @abstractmethod
    def deliver(self) -> str:
        """Every concrete transport MUST provide this method.
        (No body needed here — `...` or `pass` is the whole point.)"""
        ...


class Truck(Transport):
    def deliver(self) -> str:           # overriding the abstract method
        return "Delivering by land in a box truck 🚚"


class Ship(Transport):
    def deliver(self) -> str:
        return "Delivering by sea in a container ship 🚢"


# ---------------------------------------------------------------------------
# THE CREATORS — this is where the actual "Factory Method" lives
# ---------------------------------------------------------------------------
class Logistics(ABC):
    """Abstract creator. Notice it contains real business logic
    (plan_delivery) that USES the product without knowing its concrete type."""

    @abstractmethod
    def create_transport(self) -> Transport:
        """<-- THIS is the factory method. Subclasses decide what to build."""
        ...

    def plan_delivery(self) -> str:
        # This method is written ONCE in the base class, yet works for every
        # subclass, because create_transport() is "filled in" by them.
        # This is polymorphism doing the heavy lifting.
        transport = self.create_transport()
        return f"Delivery planned -> {transport.deliver()}"


class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


# ---------------------------------------------------------------------------
# DEMO — run me with:  python3 02_factory_method.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # The client code only deals with the abstract Logistics type.
    # It never writes Truck() or Ship() itself — that's the win.
    for company in (RoadLogistics(), SeaLogistics()):
        # type(x).__name__ gives the class name as a string — handy for demos
        print(f"{type(company).__name__:>14}: {company.plan_delivery()}")

    print()
    # Proof that ABCs protect you — you cannot instantiate the abstract class:
    try:
        Logistics()
    except TypeError as e:
        print(f"Logistics() failed as expected -> TypeError: {e}")

    # EXERCISE: add AirLogistics + Plane yourself. Notice you do NOT have to
    # touch any existing class — that's the Open/Closed Principle in action
    # (open for extension, closed for modification).
