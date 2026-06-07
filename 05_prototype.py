"""
PATTERN 5: PROTOTYPE
====================
Goal: create new objects by CLONING an existing object (the "prototype")
instead of building from scratch with a constructor.

When is cloning better than constructing?
  - the object was EXPENSIVE to set up (loaded from DB / network / big file)
  - you want many near-identical copies with tiny differences
  - client code shouldn't need to know the object's concrete class

THE python CONCEPT THAT *IS* THIS PATTERN: shallow vs deep copy
---------------------------------------------------------------
import copy
  copy.copy(x)      -> SHALLOW copy: new outer object, but inner mutable
                       objects (lists, dicts...) are SHARED with the original
  copy.deepcopy(x)  -> DEEP copy: recursively copies everything; the clone
                       is fully independent

Getting this wrong causes one of the most common bug families in Python
("why did changing the copy change the original?!") — so the demo below
shows the bug on purpose.
"""

import copy


class Document:
    """Imagine this was loaded from a slow database — we don't want to
    re-run that work for every variant, so we clone instead."""

    def __init__(self, title: str, author: str, tags: list[str]):
        self.title = title          # str is immutable -> copy-safe either way
        self.author = author
        self.tags = tags            # list is MUTABLE -> this is the danger zone

    def clone(self, **overrides) -> "Document":
        """The Prototype method: deep-copy myself, then apply tweaks.

        **overrides collects keyword args into a dict, so callers can write
        doc.clone(title="New title") and change only what they need."""
        new_doc = copy.deepcopy(self)        # fully independent copy
        for attr_name, value in overrides.items():
            # setattr(obj, "title", v) is the same as obj.title = v,
            # but works when the attribute NAME is only known at runtime.
            setattr(new_doc, attr_name, value)
        return new_doc

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author}, tags={self.tags}"


# ---------------------------------------------------------------------------
# DEMO — run me with:  python3 05_prototype.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    original = Document("Design Patterns", "Gamma et al.", ["oop", "classic"])

    print("=== 1. THE SHALLOW-COPY TRAP (the bug) ===")
    shallow = copy.copy(original)        # NOT what clone() uses — on purpose
    shallow.title = "Shallow Copy"       # reassigning an attr: safe ✅
    shallow.tags.append("HACKED")        # mutating a shared list: DANGER ❌

    print(f"original: {original}   <- 'HACKED' leaked into the original!")
    print(f"shallow : {shallow}")
    # Why: copy.copy made a new Document, but both .tags point at the SAME
    # list object in memory:
    print(f"same tags list? {original.tags is shallow.tags}")

    print("\n=== 2. THE PATTERN DONE RIGHT (deepcopy via clone) ===")
    original.tags.remove("HACKED")       # undo the damage from the demo

    sequel = original.clone(title="Design Patterns Vol. 2")
    sequel.tags.append("sequel")         # safe now — it's an independent list

    print(f"original: {original}   <- untouched this time")
    print(f"sequel  : {sequel}")
    print(f"same tags list? {original.tags is sequel.tags}")

    print("\n=== 3. Why this beats constructing from scratch ===")
    # One expensive object -> many cheap variants, one line each:
    drafts = [original.clone(title=f"Draft {n}") for n in range(1, 4)]
    for d in drafts:
        print(f"  {d}")

    # EXERCISE: change clone() to use copy.copy instead of copy.deepcopy and
    # re-run. Watch section 2 start leaking tags just like section 1.
