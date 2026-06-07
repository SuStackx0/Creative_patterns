"""
PATTERN 4: BUILDER
==================
Goal: construct a complex object STEP BY STEP instead of through one giant
constructor call.

The problem it solves ("telescoping constructor"):
    Pizza("large", True, False, True, True, False, True)   # what is this?!
Seven positional booleans — unreadable, error-prone, and you need every
combination. Builder replaces it with readable, optional, ordered steps:
    PizzaBuilder("large").add_cheese().add_mushrooms().build()

PYTHON CONCEPTS YOU'LL LEARN HERE
---------------------------------
1. Method chaining: each builder method ends with `return self`, so calls
   can be glued together with dots (this style is called a "fluent API").
2. __str__: the dunder method print() uses to display your object nicely.
3. Keeping a "product" class dumb/simple while the builder holds the
   construction smarts.
"""


# ---------------------------------------------------------------------------
# THE PRODUCT — deliberately simple; it just holds the final state
# ---------------------------------------------------------------------------
class Pizza:
    def __init__(self, size: str, toppings: list[str]):
        self.size = size
        self.toppings = toppings

    def __str__(self) -> str:
        # __str__ must RETURN a string (never print!). print(pizza) calls it.
        toppings = ", ".join(self.toppings) if self.toppings else "plain"
        return f"{self.size} pizza with: {toppings}"


# ---------------------------------------------------------------------------
# THE BUILDER — collects choices step by step, then produces the product
# ---------------------------------------------------------------------------
class PizzaBuilder:
    def __init__(self, size: str = "medium"):
        self.size = size
        self.toppings: list[str] = []   # accumulates as steps are called

    # Each step returns `self` — THAT is what makes chaining work:
    # builder.add_cheese() evaluates to the builder itself, so you can
    # immediately call .add_mushrooms() on the result, and so on.
    def add_cheese(self) -> "PizzaBuilder":
        self.toppings.append("cheese")
        return self

    def add_pepperoni(self) -> "PizzaBuilder":
        self.toppings.append("pepperoni")
        return self

    def add_mushrooms(self) -> "PizzaBuilder":
        self.toppings.append("mushrooms")
        return self

    def add_olives(self) -> "PizzaBuilder":
        self.toppings.append("olives")
        return self

    def build(self) -> Pizza:
        # The final step hands over a finished, immutable-ish product.
        # list(...) makes a COPY so the pizza isn't affected if the
        # builder is reused afterwards. (Foreshadowing file 05!)
        return Pizza(self.size, list(self.toppings))


# ---------------------------------------------------------------------------
# OPTIONAL EXTRA: THE DIRECTOR
# A director stores well-known "recipes" — fixed sequences of builder steps.
# Use it when the same construction order is needed in many places.
# ---------------------------------------------------------------------------
class PizzaDirector:
    @staticmethod   # no self needed — this is just a namespaced function
    def make_margherita() -> Pizza:
        return PizzaBuilder("medium").add_cheese().build()

    @staticmethod
    def make_supreme() -> Pizza:
        return (
            PizzaBuilder("large")     # wrapping in (...) lets you split
            .add_cheese()             # a long chain across lines nicely
            .add_pepperoni()
            .add_mushrooms()
            .add_olives()
            .build()
        )


# ---------------------------------------------------------------------------
# DEMO — run me with:  python3 04_builder.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Free-form building — caller picks any combination, any order
    custom = PizzaBuilder("small").add_mushrooms().add_olives().build()
    print(f"Custom   : {custom}")

    # 2. Step-by-step building — chaining is optional, this also works:
    builder = PizzaBuilder("large")
    builder.add_cheese()
    if input("Add pepperoni? (y/n) ").strip().lower() == "y":
        builder.add_pepperoni()      # <- steps can be CONDITIONAL — try doing
    print(f"Yours    : {builder.build()}")  # that with a single constructor!

    # 3. Director recipes
    print(f"Margherita: {PizzaDirector.make_margherita()}")
    print(f"Supreme   : {PizzaDirector.make_supreme()}")

    # EXERCISE: remove `return self` from add_cheese() and re-run.
    # The chained call in make_margherita() will crash with
    # AttributeError: 'NoneType' object has no attribute 'build' — because a
    # method with no return statement returns None. Understand why!
