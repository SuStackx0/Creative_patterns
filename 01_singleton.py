"""
PATTERN 1: SINGLETON
====================
Goal: a class that can only EVER have ONE instance.
No matter how many times you "create" it, you always get the same object back.

Classic use cases: a Logger, app Configuration, a database connection.

PYTHON CONCEPT YOU MUST UNDERSTAND FIRST: __new__ vs __init__
-------------------------------------------------------------
When you write  Logger()  Python actually does TWO steps:

    1. __new__(cls)        -> CREATES the raw object in memory (the "birth")
    2. __init__(self)      -> INITIALIZES it, i.e. fills in attributes (the "setup")

99% of the time you only ever write __init__ and let Python handle __new__.
Singleton is the classic case where we hijack __new__: if an instance
already exists, we return THAT instead of creating a new one.
"""


class Logger:
    # This is a CLASS attribute (note: defined on the class, not inside a
    # method). It is shared by the class itself — there is exactly one
    # `_instance` for the whole class, not one per object.
    # The leading underscore is a Python convention meaning "private-ish,
    # don't touch this from outside".
    _instance = None

    def __new__(cls):
        # `cls` is the class itself (Logger), like `self` but for the class.
        # __new__ receives the class because its job is to produce an
        # instance OF that class.
        if cls._instance is None:
            print("(creating the one and only Logger instance)")
            # super() here is `object`, the ultimate base class.
            # object.__new__(cls) is the normal "allocate a new object"
            # machinery we are wrapping.
            cls._instance = super().__new__(cls)
        return cls._instance  # always the SAME object after the first call

    def __init__(self):
        # ⚠️ THE CLASSIC SINGLETON GOTCHA ⚠️
        # __init__ runs EVERY time you write Logger() — even when __new__
        # returned the already-existing instance! Without the guard below,
        # calling Logger() a second time would WIPE self.history clean.
        #
        # hasattr(obj, name) asks: "does this object have that attribute?"
        if not hasattr(self, "history"):
            self.history = []  # instance attribute: the log messages so far

    def log(self, message: str) -> None:
        self.history.append(message)
        print(f"[LOG] {message}")


# ---------------------------------------------------------------------------
# DEMO — run me with:  python3 01_singleton.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- Creating 'two' loggers ---")
    logger_a = Logger()
    logger_b = Logger()   # no "creating..." print this time — why? (see __new__)

    # `is` checks IDENTITY: are these literally the same object in memory?
    # (== checks equality of value; `is` checks same-object.)
    print(f"\nlogger_a is logger_b?  {logger_a is logger_b}")
    print(f"id(logger_a) = {id(logger_a)}")
    print(f"id(logger_b) = {id(logger_b)}   <- identical memory address")

    print("\n--- Logging from 'different' loggers ---")
    logger_a.log("User signed in")
    logger_b.log("User clicked a button")

    # Both messages live in ONE shared history, because there is one object.
    print(f"\nlogger_a.history = {logger_a.history}")
    print(f"logger_b.history = {logger_b.history}   <- same list!")

    # EXERCISE: comment out the `if not hasattr(...)` guard in __init__
    # (keep `self.history = []` unguarded) and re-run. Watch the history
    # get destroyed when logger_b is "created". That bug is THE reason
    # the guard exists.
