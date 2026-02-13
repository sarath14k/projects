from dataclasses import dataclass

@dataclass
class Theme:
    name: str
    bg_color: str
    fg_color: str
    card_bg: str
    accent_color: str
    accent_hover: str
    destructive_color: str
    destructive_hover: str
    warning_color: str
    warning_hover: str
    success_color: str
    info_color: str
    border_color: str
    shadow_color: str

THEMES = {
    "Modern (System)": Theme(
        name="Modern (System)",
        bg_color="#131318",
        fg_color="#E5E1E9",
        card_bg="#201F25",
        accent_color="#C3C0FF",
        accent_hover="#D2D0FF",
        destructive_color="#FFB4AB",
        destructive_hover="#FFDAD6",
        warning_color="#F39C12",
        warning_hover="#E67E22",
        success_color="#27AE60",
        info_color="#3498DB",
        border_color="#47464F",
        shadow_color="rgba(0, 0, 0, 0.4)"
    ),
    "Aura": Theme(
        name="Aura",
        bg_color="#151515",
        fg_color="#EDECEE",
        card_bg="#1E1E1E",
        accent_color="#A277FF",
        accent_hover="#B794FF",
        destructive_color="#FF6767",
        destructive_hover="#FF8A8A",
        warning_color="#FFCA3A",
        warning_hover="#FFD45E",
        success_color="#61FFCA",
        info_color="#82E3FF",
        border_color="#333333",
        shadow_color="rgba(0, 0, 0, 0.5)"
    ),
    "Tokyo Night": Theme(
        name="Tokyo Night",
        bg_color="#1A1B26",
        fg_color="#A9B1D6",
        card_bg="#24283B",
        accent_color="#7AA2F7",
        accent_hover="#89B4FA",
        destructive_color="#F7768E",
        destructive_hover="#FF8EAB",
        warning_color="#E0AF68",
        warning_hover="#FFC777",
        success_color="#9ECE6A",
        info_color="#7DCFFF",
        border_color="#414868",
        shadow_color="rgba(0, 0, 0, 0.6)"
    ),
    "Catppuccin": Theme(
        name="Catppuccin",
        bg_color="#1E1E2E",
        fg_color="#CDD6F4",
        card_bg="#181825",
        accent_color="#F5C2E7",
        accent_hover="#F5E0DC",
        destructive_color="#F38BA8",
        destructive_hover="#EBA0AC",
        warning_color="#FAB387",
        warning_hover="#F9E2AF",
        success_color="#A6E3A1",
        info_color="#89B4FA",
        border_color="#313244",
        shadow_color="rgba(0, 0, 0, 0.5)"
    ),
    "Nord": Theme(
        name="Nord",
        bg_color="#2E3440",
        fg_color="#D8DEE9",
        card_bg="#3B4252",
        accent_color="#88C0D0",
        accent_hover="#8FBCBB",
        destructive_color="#BF616A",
        destructive_hover="#D08770",
        warning_color="#EBCB8B",
        warning_hover="#D08770",
        success_color="#A3BE8C",
        info_color="#81A1C1",
        border_color="#4C566A",
        shadow_color="rgba(0, 0, 0, 0.3)"
    ),
    "Pitch Black": Theme(
        name="Pitch Black",
        bg_color="#000000",
        fg_color="#FFFFFF",
        card_bg="#080808",
        accent_color="#2EC27E",
        accent_hover="#3AD68E",
        destructive_color="#E74C3C",
        destructive_hover="#FF6B6B",
        warning_color="#F1C40F",
        warning_hover="#F39C12",
        success_color="#2ECC71",
        info_color="#3498DB",
        border_color="#333333",
        shadow_color="rgba(0, 0, 0, 0.8)"
    )
}
