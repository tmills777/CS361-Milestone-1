#!/usr/bin/env python3
"""
Galactic Adventure(Milestone #1)
A small, inclusive, interactive sci-fi terminal game designed to demo:
- 3 user stories with functional acceptance criteria
- 8 Inclusivity Heuristics (implemented in UI + flow)
- 3 Quality Attributes (with non-functional acceptance criteria)
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import time


# -----------------------------
# Data Models
# -----------------------------

@dataclass
class PlayerPrefs:
    """
    Player accessibility / preference settings.
    """
    text_size: str = "normal"          # normal | large
    high_contrast: bool = False        # True enables high-contrast styling
    reduced_motion: bool = False       # True disables delays/typing effects
    confirm_actions: bool = True       # True asks confirmation on risky actions
    show_tooltips: bool = True         # True shows extra help text


@dataclass
class GameState:
    """
    Tracks current game progress and meaningful choices.
    """
    ship_name: str = "Vanguard"
    callsign: str = "Pilot"
    chapter: int = 1
    power_cells: int = 3
    distress_packets_sent: int = 0
    last_choice: Optional[str] = None


# -----------------------------
# Inclusivity & UI Helpers
# -----------------------------

class UI:
    """
    UI helper that implements multiple inclusivity heuristics via:
    - flexible display options (text size, contrast)
    - clear language and consistent layout
    - choice confirmations and safe undo paths
    - respectful, neutral tone; no assumptions about identity
    """
    def __init__(self, prefs: PlayerPrefs):
        self.prefs = prefs

    def _style(self, text: str) -> str:
        """
        Applies simple high-contrast styling without relying on color alone.
        (We avoid fancy ASCII art that could reduce readability.)
        """
        if self.prefs.high_contrast:
            return f"=== {text.upper()} ==="
        return text

    def header(self, title: str) -> None:
        print()
        print(self._style(title))
        print("-" * max(10, min(70, len(title) + 6)))

    def body(self, text: str) -> None:
        """
        Supports 'large text' mode by adding line spacing.
        """
        if self.prefs.text_size == "large":
            for line in text.splitlines():
                print(line)
                print()
        else:
            print(text)

    def hint(self, text: str) -> None:
        """
        Optional tooltips.
        """
        if self.prefs.show_tooltips:
            prefix = "[Hint] "
            self.body(prefix + text)

    def wait(self, seconds: float) -> None:
        """
        Reduced-motion support (no artificial delays).
        """
        if self.prefs.reduced_motion:
            return
        time.sleep(seconds)

    def ask(self, prompt: str) -> str:
        """
        Input prompt with consistent pattern.
        """
        return input(self._style(prompt) + " ").strip()

    def confirm(self, prompt: str) -> bool:
        """
        Confirmation step for potentially irreversible actions.
        """
        if not self.prefs.confirm_actions:
            return True
        ans = self.ask(f"{prompt} (y/n):").lower()
        return ans in ("y", "yes")

    def error(self, text: str) -> None:
        """
        Friendly, non-blaming error messages.
        """
        self.body(f"[Notice] {text}")

    def success(self, text: str) -> None:
        self.body(f"[OK] {text}")


# -----------------------------
# Quality Attribute Checks
# -----------------------------

def validate_ship_name(name: str) -> Tuple[bool, str]:
    """
    Reliability: input validation for ship name.
    - Must be 1..24 chars
    - No control chars
    """
    if not name:
        return False, "Ship name can't be empty."
    if len(name) > 24:
        return False, "Ship name must be 24 characters or fewer."
    if any(ord(c) < 32 for c in name):
        return False, "Ship name contains invalid characters."
    return True, ""


def safe_int_choice(raw: str, valid: Dict[int, str]) -> Optional[int]:
    """
    Reliability: prevents crashes from invalid numeric input.
    Returns an int if valid, else None.
    """
    try:
        val = int(raw)
    except ValueError:
        return None
    return val if val in valid else None


# -----------------------------
# User Stories & Acceptance Criteria (for video)
# -----------------------------

USER_STORIES = [
    {
        "story": "As a player, I want to customize accessibility settings so that I can read and navigate the game comfortably.",
        "criteria": "Given I open Settings, when I enable large text and high-contrast mode, then the menus and story text display in the selected format."
    },
    {
        "story": "As a player, I want to make a mission choice that changes resources so that my decisions meaningfully affect the outcome.",
        "criteria": "Given I have 3 power cells, when I choose to boost the comms relay, then my power cells decrease by 1 and a distress packet is sent."
    },
    {
        "story": "As a player, I want a clear way to recover from mistakes so that I don’t get stuck after a wrong input or accidental selection.",
        "criteria": "Given I enter an invalid menu option, when the game detects the input, then it shows a helpful message and returns me to the same menu without crashing."
    }
]

QUALITY_ATTRIBUTES = [
    {
        "name": "Accessibility/Usability",
        "nfr": "The program must provide at least two readability options (large text and high-contrast) and a reduced-motion option, all toggleable from Settings without restarting.",
        "where": "Settings menu toggles text size, high-contrast headers, and reduced-motion delays."
    },
    {
        "name": "Reliability",
        "nfr": "The program must not crash on invalid menu input; it must detect invalid choices and recover by re-prompting the user.",
        "where": "safe_int_choice() and friendly error handling in menus."
    },
    {
        "name": "Maintainability",
        "nfr": "Game logic, UI, and data models must be separated into functions/classes so that adding a new chapter or menu option requires changing only one clearly-located section.",
        "where": "UI class, dataclasses, and isolated menu functions."
    }
]


# -----------------------------
# Inclusivity Heuristics (1..8)
# NOTE: Your course defines these; this implementation makes them demonstrable.
# -----------------------------

def show_inclusivity_map(ui: UI) -> None:
    ui.header("Inclusivity Heuristics (Where to show in your video)")
    ui.body(
        "H1: Provide choice & control -> Settings menu (text size, contrast, reduced motion, confirmations)\n"
        "H2: Support different abilities -> Large text + reduced motion + high contrast (not color-only)\n"
        "H3: Clear, consistent language -> Simple words, consistent menus, no jargon required\n"
        "H4: Prevent errors / easy recovery -> Validation + re-prompting + confirmations\n"
        "H5: Respectful, neutral tone -> No identity assumptions; inclusive terms (player/callsign)\n"
        "H6: Multiple ways to understand -> Optional hints/tooltips; short summaries of consequences\n"
        "H7: Privacy & safety -> No accounts, no tracking, no external APIs, no personal data needed\n"
        "H8: Transparent consequences -> Mission choices show what will change before you commit\n"
    )
    ui.hint("In your video, open Settings and toggle options, then show a mission choice with a consequence preview.")


# -----------------------------
# Menus / Game Flow
# -----------------------------

def show_user_stories(ui: UI) -> None:
    ui.header("User Stories + Acceptance Criteria (Read in your video)")
    for i, item in enumerate(USER_STORIES, start=1):
        ui.body(f"{i}) User Story:\n   {item['story']}\n")
        ui.body(f"   Acceptance Criterion (Given/When/Then):\n   {item['criteria']}\n")
    ui.hint("In the video, demonstrate each acceptance criterion in the same order.")


def show_quality_attributes(ui: UI) -> None:
    ui.header("Quality Attributes (Read + Show in your video)")
    for i, qa in enumerate(QUALITY_ATTRIBUTES, start=1):
        ui.body(f"{i}) Quality Attribute: {qa['name']}")
        ui.body(f"   Non-functional acceptance criterion: {qa['nfr']}")
        ui.body(f"   Where/how it's satisfied: {qa['where']}\n")


def settings_menu(ui: UI, prefs: PlayerPrefs) -> None:
    while True:
        ui.header("Settings")
        ui.body(f"1) Text size: {prefs.text_size}")
        ui.body(f"2) High contrast: {prefs.high_contrast}")
        ui.body(f"3) Reduced motion: {prefs.reduced_motion}")
        ui.body(f"4) Confirm actions: {prefs.confirm_actions}")
        ui.body(f"5) Show tooltips: {prefs.show_tooltips}")
        ui.body("6) Back")

        valid = {
            1: "text_size",
            2: "high_contrast",
            3: "reduced_motion",
            4: "confirm_actions",
            5: "show_tooltips",
            6: "back",
        }
        choice = safe_int_choice(ui.ask("Choose an option (1-6):"), valid)
        if choice is None:
            ui.error("I couldn't read that as a valid option. Please enter a number from 1 to 6.")
            continue

        if choice == 1:
            prefs.text_size = "large" if prefs.text_size == "normal" else "normal"
            ui.success(f"Text size set to: {prefs.text_size}")
        elif choice == 2:
            prefs.high_contrast = not prefs.high_contrast
            ui.success(f"High contrast set to: {prefs.high_contrast}")
        elif choice == 3:
            prefs.reduced_motion = not prefs.reduced_motion
            ui.success(f"Reduced motion set to: {prefs.reduced_motion}")
        elif choice == 4:
            prefs.confirm_actions = not prefs.confirm_actions
            ui.success(f"Confirm actions set to: {prefs.confirm_actions}")
        elif choice == 5:
            prefs.show_tooltips = not prefs.show_tooltips
            ui.success(f"Show tooltips set to: {prefs.show_tooltips}")
        else:
            return

        ui.wait(0.2)


def profile_menu(ui: UI, state: GameState) -> None:
    while True:
        ui.header("Profile")
        ui.body(f"Ship name: {state.ship_name}")
        ui.body(f"Callsign: {state.callsign}")
        ui.body("1) Edit ship name")
        ui.body("2) Edit callsign")
        ui.body("3) Back")

        valid = {1: "ship", 2: "callsign", 3: "back"}
        choice = safe_int_choice(ui.ask("Choose an option (1-3):"), valid)
        if choice is None:
            ui.error("Please enter 1, 2, or 3.")
            continue

        if choice == 1:
            new_name = ui.ask("Enter a new ship name (1-24 chars):")
            ok, msg = validate_ship_name(new_name)
            if not ok:
                ui.error(msg)
                continue
            state.ship_name = new_name
            ui.success("Ship name updated.")
        elif choice == 2:
            new_callsign = ui.ask("Enter a new callsign (1-24 chars):")
            ok, msg = validate_ship_name(new_callsign)
            if not ok:
                ui.error(msg)
                continue
            state.callsign = new_callsign
            ui.success("Callsign updated.")
        else:
            return


def mission_brief(ui: UI, state: GameState) -> None:
    ui.header("Mission Brief: The Nebula Relay")
    ui.body(
        f"Ship: {state.ship_name}\n"
        f"Operator: {state.callsign}\n\n"
        "A communications relay is failing inside the Vesper Nebula.\n"
        "You can spend power to boost the relay, or conserve power and attempt a manual reroute.\n"
    )
    ui.hint("Your choice will change your resources. This is intentional (meaningful decisions).")
    ui.wait(0.4)


def mission_choice(ui: UI, state: GameState) -> None:
    while True:
        ui.header("Decision Point")
        ui.body(f"Power cells available: {state.power_cells}")
        ui.body(f"Distress packets sent: {state.distress_packets_sent}\n")
        ui.body("1) Boost the comms relay (Costs 1 power cell; sends 1 distress packet)")
        ui.body("2) Manual reroute (No cost; lower success chance)")
        ui.body("3) Back")

        ui.hint("Transparent consequences: Option 1 costs power but increases communication reliability.")

        valid = {1: "boost", 2: "reroute", 3: "back"}
        choice = safe_int_choice(ui.ask("Choose an option (1-3):"), valid)
        if choice is None:
            ui.error("That option isn't recognized. Enter 1, 2, or 3.")
            continue

        if choice == 3:
            return

        if choice == 1:
            if state.power_cells <= 0:
                ui.error("You don't have any power cells left to boost the relay.")
                continue

            # Confirm irreversible-ish action (error prevention + control)
            if not ui.confirm("This will spend 1 power cell. Proceed?"):
                ui.success("Cancelled. No resources spent.")
                continue

            state.power_cells -= 1
            state.distress_packets_sent += 1
            state.last_choice = "boost"
            ui.success("Boost successful. Distress packet transmitted.")
            ui.wait(0.4)
            return

        if choice == 2:
            if ui.confirm("Manual reroute can be risky. Proceed?"):
                state.last_choice = "reroute"
                ui.success("You attempt a manual reroute… signal stabilizing (barely).")
                ui.wait(0.4)
                return
            ui.success("Cancelled. Returning to decision menu.")


def status_screen(ui: UI, state: GameState) -> None:
    ui.header("Status")
    ui.body(
        f"Ship: {state.ship_name}\n"
        f"Callsign: {state.callsign}\n"
        f"Chapter: {state.chapter}\n"
        f"Power cells: {state.power_cells}\n"
        f"Distress packets sent: {state.distress_packets_sent}\n"
        f"Last choice: {state.last_choice}\n"
    )
    ui.hint("This screen makes game state visible and understandable (transparency).")


def help_menu(ui: UI) -> None:
    ui.header("Help")
    ui.body(
        "How to play:\n"
        "- Use numbers to choose menu options.\n"
        "- You can adjust readability and motion in Settings.\n"
        "- If you enter an invalid option, the game will guide you back.\n"
        "- Nothing is uploaded anywhere; this runs locally.\n"
    )


def main_menu(ui: UI, prefs: PlayerPrefs, state: GameState) -> None:
    while True:
        ui.header("Nebula Relay — Milestone #1")
        ui.body("1) Show User Stories + Acceptance Criteria")
        ui.body("2) Show Inclusivity Heuristics Map")
        ui.body("3) Show Quality Attributes")
        ui.body("4) Start Mission (interactive)")
        ui.body("5) Status")
        ui.body("6) Profile")
        ui.body("7) Settings")
        ui.body("8) Help")
        ui.body("9) Exit")

        valid = {1: "stories", 2: "heuristics", 3: "qa", 4: "mission", 5: "status",
                 6: "profile", 7: "settings", 8: "help", 9: "exit"}

        raw = ui.ask("Choose an option (1-9):")
        choice = safe_int_choice(raw, valid)

        if choice is None:
            # User story #3 acceptance criterion + reliability QA
            ui.error("Invalid input. Please type a number from 1 to 9. (No worries — try again.)")
            continue

        if choice == 1:
            show_user_stories(ui)
        elif choice == 2:
            show_inclusivity_map(ui)
        elif choice == 3:
            show_quality_attributes(ui)
        elif choice == 4:
            mission_brief(ui, state)
            mission_choice(ui, state)
        elif choice == 5:
            status_screen(ui, state)
        elif choice == 6:
            profile_menu(ui, state)
        elif choice == 7:
            settings_menu(ui, prefs)
        elif choice == 8:
            help_menu(ui)
        else:
            ui.header("Exit")
            ui.body("Thanks for playing Nebula Relay. Good luck with your Milestone #1 video!")
            return

        ui.wait(0.2)


def main() -> None:
    prefs = PlayerPrefs()
    ui = UI(prefs)
    state = GameState()

    # Friendly onboarding (no identity assumptions, clear language)
    ui.header("Welcome")
    ui.body(
        "This is a small sci-fi interactive program built to demonstrate Milestone #1.\n"
        "Tip: Open Settings if you want large text, high contrast, or reduced motion.\n"
    )
    ui.wait(0.4)

    main_menu(ui, prefs, state)


if __name__ == "__main__":
    main()

