"""
PATTERN 3: ABSTRACT FACTORY
===========================
Goal: create whole FAMILIES of related products that must be used together,
without ever naming their concrete classes in client code.

Classic GoF example: a cross-platform GUI toolkit. A Mac app must use a
MacButton AND a MacCheckbox — mixing a MacButton with a WindowsCheckbox
would look broken. The factory guarantees the family stays consistent.

FACTORY METHOD vs ABSTRACT FACTORY (the #1 interview question)
--------------------------------------------------------------
- Factory Method  = ONE method, creates ONE product, varies by subclassing
                    the creator. (02_factory_method.py)
- Abstract Factory = an OBJECT with MULTIPLE factory methods that produce a
                     matching SET of products. It's basically a collection
                     of factory methods grouped into one family.

No new Python syntax here — this file deliberately reuses everything from
file 02 (ABC, @abstractmethod, polymorphism) so you can focus on the
pattern's structure. Notice how many small classes cooperate.
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# ABSTRACT PRODUCTS — one ABC per product *kind*
# ---------------------------------------------------------------------------
class Button(ABC):
    @abstractmethod
    def render(self) -> str: ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str: ...


# ---------------------------------------------------------------------------
# CONCRETE PRODUCTS — one row per *family* (Windows family, Mac family)
# ---------------------------------------------------------------------------
class WindowsButton(Button):
    def render(self) -> str:
        return "[ Windows-style button ]"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "[x] Windows-style checkbox"


class MacButton(Button):
    def render(self) -> str:
        return "( Mac-style button )"


class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "(•) Mac-style checkbox"


# ---------------------------------------------------------------------------
# THE ABSTRACT FACTORY — one create_* method per product kind
# ---------------------------------------------------------------------------
class GUIFactory(ABC):
    """Each concrete factory below produces one complete, matching family."""

    @abstractmethod
    def create_button(self) -> Button: ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...


class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


# ---------------------------------------------------------------------------
# CLIENT CODE — knows ONLY the abstract types. Search this class for the
# words "Windows" or "Mac": you won't find them. That's the whole point.
# ---------------------------------------------------------------------------
class Application:
    def __init__(self, factory: GUIFactory):
        # The factory is INJECTED (passed in), so this class works with any
        # current or future family (LinuxFactory?) without modification.
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def render_ui(self) -> str:
        return f"{self.button.render()}\n{self.checkbox.render()}"


# ---------------------------------------------------------------------------
# DEMO — run me with:  python3 03_abstract_factory.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    # The ONE place a concrete family is chosen — usually from config/env.
    # This dict maps a string to a factory CLASS (classes are objects in
    # Python — you can store them in dicts and call them later!).
    factories = {"windows": WindowsFactory, "mac": MacFactory}

    platform = "mac" if sys.platform == "darwin" else "windows"
    print(f"Detected platform -> using {platform!r} family\n")

    app = Application(factories[platform]())   # note the () — instantiate it
    print(app.render_ui())

    print("\nSame Application class, other family:")
    other = Application(WindowsFactory() if platform == "mac" else MacFactory())
    print(other.render_ui())

    # EXERCISE: add a LinuxFactory with LinuxButton/LinuxCheckbox.
    # Count how many existing classes you had to edit. (Answer: zero —
    # except adding one entry to the `factories` dict.)
