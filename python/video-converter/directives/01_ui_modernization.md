# UI Modernization Plan

## Goal
Make the UI "much more beautiful" by adopting modern design principles:
-   **Flat & Clean**: Minimalist aesthetic with subtle depth.
-   **Spacing**: Increased "breathing room" (padding/margins).
-   **Typography**: Clearer hierarchy, better weights.
-   **Visual Cues**: Better hover states, focus indicators, and active states.

## 1. CSS Overhaul (`src/utils.py`) - Standard "Gray" Theme
The current `load_static_css` in `src/utils.py` defines the base look. We will enhance it:
-   **Global Font**: Ensure `Inter` or `Roboto` is prioritized.
-   **Backgrounds**: Use a curated dark gray palette (e.g., `#1e1e1e` for background, `#2d2d2d` for cards) instead of `alpha(currentColor)`.
-   **Cards (`.row-card`)**:
    -   Increase border radius to `16px`.
    -   Add subtle shadow: `box-shadow: 0 4px 12px rgba(0,0,0,0.2)`.
    -   Remove border generally, rely on background separation.
-   **Buttons**:
    -   Pill-shaped or softer rounded corners (`8px` or `20px` for pills).
    -   Hover effects with slight lift (transform isn't supported in Gtk3 CSS, so use brightness).
    -   Transition effects (opacity, background) where valid.

## 2. Pitch Black Theme (`src/css.py`) - "Black" Theme
Refine `PITCH_BLACK_CSS`:
-   Keep true black `#000000` background.
-   Use slightly lighter black `#111111` or `#1a1a1a` for `row-card` to give *visible* separation without breaking the OLED benefit.
-   Neon accents: Ensure `#2ec27e` (Green) pops against the black.

## 3. UI Builder Adjustments
-   **Spacing**: Increase spacing in `Gtk.Box` containers in `sidebar_builder` and `main_area_builder` (from `10` to `16` or `20`).
-   **Sidebar**: Add more padding around the sidebar itself.
-   **Header**: Make it cleaner, possibly blend with the window background.

## 4. Specific Component Improvements
-   **Empty State**: Add a distinct illustration or larger icon with better typography.
-   **Progress Bar**: Make it thinner (4px or 6px) and sleek.
-   **Status Labels**: Use specific colors for "Processing", "Paused", "Completed".

## Implementation Steps
1.  Modify `src/utils.py` to inject the new "Beautiful Gray" CSS.
2.  Modify `src/css.py` to refine the Pitch Black theme.
3.  Tweak spacing in `sidebar_builder.py` and `main_area_builder.py`.
