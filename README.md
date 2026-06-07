# Creational Design Patterns in Python

Creational patterns answer one question: **"How should objects get created?"**
Instead of scattering `SomeClass()` calls everywhere, these patterns give you
controlled, flexible ways to create objects.

## Learning order (do them in this order!)

| # | File                       | Pattern          | One-line idea                                                             | Python concepts you'll learn                        |
| - | -------------------------- | ---------------- | ------------------------------------------------------------------------- | --------------------------------------------------- |
| 1 | `01_singleton.py`        | Singleton        | Only ONE instance of a class can ever exist                               | `__new__` vs `__init__`, class attributes       |
| 2 | `02_factory_method.py`   | Factory Method   | A base class declares "make the product", subclasses decide WHICH product | ABCs,`@abstractmethod`, inheritance, polymorphism |
| 3 | `03_abstract_factory.py` | Abstract Factory | A factory that creates a whole FAMILY of related products                 | Multiple ABCs working together                      |
| 4 | `04_builder.py`          | Builder          | Construct a complex object step by step                                   | Method chaining (`return self`), `__str__`      |
| 5 | `05_prototype.py`        | Prototype        | Create new objects by CLONING an existing one                             | `copy` vs `deepcopy`, `__dict__`              |

## How to use this repo

1. Open the file and read it top to bottom (comments explain everything).
2. Run it: `python3 01_singleton.py` — every file has a demo at the bottom.
3. Predict the output BEFORE running. If you're surprised, re-read.
4. Break it on purpose (delete a line, change a value) and see what happens.

## Quick mental models

- **Singleton** → "There can be only one." (app config, logger)
- **Factory Method** → "I know I need *a* transport, the subclass knows *which*."
- **Abstract Factory** → "Give me a matching SET of things." (Mac button + Mac checkbox)
- **Builder** → "Too many constructor arguments — build it piece by piece instead."
- **Prototype** → "Copying this object is easier/cheaper than building a new one."
