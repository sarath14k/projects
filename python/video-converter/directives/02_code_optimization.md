# Code Optimization Plan

## Goal
Optimize the codebase by removing redundancy, consolidating utility modules, and refactoring the "God Class" (`VideoConverter` in `ui.py`) to delegate more logic to specialized components.

## 1. Module Consolidation
**Merge `src/helpers.py` into `src/utils.py`**.
-   `helpers.py` contains general file/system utilities that belong in `utils.py`.
-   **Action**: Move all functions from `helpers.py` to `utils.py`.
-   **Action**: Delete `src/helpers.py`.
-   **Action**: Update all imports in the project to use `src.utils`.

## 2. Refactoring `src/ui.py`
The `VideoConverter` class still holds logic that belongs elsewhere.
-   **Output Path Generation**:
    -   `_get_out_path` (lines 247-257) duplicates `helpers.generate_output_path`.
    -   **Action**: Delete `_get_out_path`. Update `ConversionManager` to call `utils.generate_output_path` directly.
-   **Render Devices**:
    -   `_get_render_devices` (lines 99-100) is a useless wrapper.
    -   **Action**: Delete `_get_render_devices`. Call `utils.get_render_devices` in `sidebar_builder.py`.
-   **Row UI Updates**:
    -   `_update_row_ui` (lines 258-276) constructs UI markup strings. This violates encapsulation of `FileRow`.
    -   **Action**: Move this logic into `FileRow.update_progress(pct, fps, speed, bitrate, rem, q_rem, init_size, est_size)`.
-   **Drag & Drop Logic**:
    -   `on_drag_data_received` (lines 200-221) contains directory walking logic.
    -   **Action**: Move path processing logic to `FileManager.process_dropped_uris`.

## 3. General Cleanup
-   **Unused Imports**: Scan files for unused key imports (`os`, `json`, `glob` in `ui.py` might be redundant after refactoring).
-   **Type Safety**: Add type hints to `utils.py` functions where obvious.

## Verification Plan
1.  **Manual Testing**:
    -   Launch app.
    -   Add files (Drag & Drop, Button).
    -   Check GPU device listing (Sidebar).
    -   Run conversion (Check output path generation).
    -   Check progress bar updates (Visual verification).
2.  **Automated Checks**:
    -   Run the app and check for `ImportError` (due to moved helpers).
