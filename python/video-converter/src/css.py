STANDARD_CSS = """
    @define-color bg_color #242424;
    @define-color fg_color #eeeeee;
    @define-color card_bg #323232;
    @define-color accent_color #2ec27e;
    @define-color accent_hover #3ad68e;
    @define-color destructive_color #e74c3c;
    @define-color destructive_hover #ff6b6b;

    * {
        font-family: "Inter", "Roboto", "Segoe UI", "Cantarell", "Ubuntu", sans-serif;
    }

    window, textview, .background {
        background-color: @bg_color;
        color: @fg_color;
    }

    .dim-label {
        opacity: 0.6;
        font-size: 10px;
        margin-bottom: 2px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .sidebar-bg {
        background-color: alpha(#000000, 0.1);
        border-right: 1px solid alpha(#ffffff, 0.05);
        font-size: 13px;
    }

    .row-card {
        border-radius: 6px;
        border: 1px solid alpha(#ffffff, 0.05);
        background-color: @card_bg;
        padding: 18px;
        margin-bottom: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }

    .row-card:hover {
        background-color: shade(@card_bg, 1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border-color: alpha(@ffffff, 0.1);
    }

    .file-list { background: transparent; }
    .file-list row {
        padding-bottom: 12px;
        background: transparent;
        margin-left: 4px;
        margin-right: 4px;
    }
    .file-list row:last-child { padding-bottom: 0; }
    .file-list row:hover { background: transparent; }

    .active-row .row-card {
        border: 1px solid @accent_color;
        background-color: alpha(@accent_color, 0.08);
    }

    .thumbnail {
        border-radius: 6px;
        background-color: #000000;
        border: 3px solid #222222;
        box-shadow: 0 2px 5px rgba(0,0,0,0.4);
    }

    .filename-label {
        font-weight: 800;
        font-size: 13px;
        color: @fg_color;
        margin-top: 4px;
    }

    .empty-icon {
        background-color: transparent;
        background-image: none;
        border: none;
        box-shadow: none;
    }

    .drag-active {
        border: 2px dashed @accent_color;
        background-color: alpha(@accent_color, 0.1);
        border-radius: 16px;
    }

    .drag-active .empty-icon,
    .drag-active image,
    .drag-active box {
        background-color: transparent;
        background-image: none;
    }

    button {
        min-height: 34px;
        min-width: 34px;
        padding: 0 8px;
        border-radius: 8px;
        font-weight: 500;
        transition: background-color 0.15s ease;
    }

    .destructive-action {
        background-image: none;
        background-color: @destructive_color;
        color: white;
        border: none;
        min-height: 34px;
        min-width: 34px;
        padding: 0 8px;
    }
    .destructive-action image, .destructive-action box {
        background-color: transparent;
        background-image: none;
        color: inherit;
    }
    .destructive-action:hover { background-color: @destructive_hover; }

    .flat-button {
        min-height: 28px;
        min-width: 28px;
        padding: 4px;
        margin: 0px;
        border: none;
        background: transparent;
        box-shadow: none;
        color: alpha(@fg_color, 0.6);
        border-radius: 50%;
    }
    .flat-button:hover {
        background-color: alpha(@fg_color, 0.1);
        color: @accent_color;
    }
    .flat-button:active { background-color: alpha(@fg_color, 0.2); }

    .suggested-action {
        background-image: none;
        background-color: @accent_color;
        color: #000000;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0 8px;
        min-height: 34px;
        min-width: 34px;
    }
    .suggested-action label { background-color: transparent; color: inherit; }
    .suggested-action:hover { background-color: @accent_hover; }
    .suggested-action:disabled {
        background-color: alpha(@fg_color, 0.1);
        color: alpha(@fg_color, 0.4);
    }

    .row-remove-btn {
        color: alpha(@fg_color, 0.5);
        margin-right: 12px;
    }
    .row-remove-btn:hover {
        color: @destructive_hover;
        background-color: alpha(@destructive_color, 0.15);
        border-radius: 50%;
    }

    progressbar {
        margin-bottom: 4px;
    }

    progressbar trough {
        min-height: 6px;
        border-radius: 3px;
        background-color: alpha(#000000, 0.3);
    }
    progressbar progress {
        min-height: 6px;
        border-radius: 3px;
        background-color: @accent_color;
        background-image: none;
        border: none;
    }

    .success-bar progress {
        background-color: @accent_color;
    }

    /* Small Window Overrides */
    .small-window .filename-label { font-size: 11px; }
    .small-window .dim-label { font-size: 11px; }
"""

PITCH_BLACK_CSS = """
    @define-color bg_color #000000;
    @define-color fg_color #ffffff;
    @define-color card_bg #080808;

    * {
        -gtk-icon-style: symbolic;
    }

    window, .background, headerbar, list, treeview, textview, eventbox, scrolledwindow, viewport, box {
        background-color: @bg_color;
        background-image: none;
        border-color: #333333;
        color: @fg_color;
    }

    .sidebar-bg {
        background-color: @bg_color;
        border-right: none;
        font-size: 13px;
    }

    .row-card {
        background-color: @card_bg;
        border: 1px solid #181818;
        padding: 18px;
        margin-bottom: 8px;
        border-radius: 10px;
        transition: all 0.2s ease;
    }
    .row-card:hover {
        background-color: #121212;
        border-color: #333333;
    }
    .active-row .row-card {
        border: 1px solid @accent_color;
        background-color: alpha(@accent_color, 0.05);
    }

    .thumbnail {
        border-radius: 6px;
        border: 3px solid #333333;
    }

    button:not(.suggested-action):not(.destructive-action):not(.flat-button) {
        background-color: @card_bg;
        background-image: none;
        border: none;
        box-shadow: none;
        text-shadow: none;
        color: @fg_color;
    }
    button:not(.suggested-action):not(.destructive-action):not(.flat-button):hover {
        background-color: #161616;
    }
    button:not(.suggested-action):not(.destructive-action):not(.flat-button):active {
        background-color: #222222;
    }

    .suggested-action {
        background-color: #2ec27e;
        color: #000000;
        border: none;
    }
    .suggested-action:hover {
        background-color: #3ad68e;
    }

    button image, button box, button > * {
        background-color: transparent;
        background-image: none;
        border: none;
        box-shadow: none;
    }

    entry, combobox, spinbutton, treeview, textview, popover, menu, menubar, toolbar {
        background-color: @bg_color;
        color: @fg_color;
        border: none;
        box-shadow: none;
    }

    combobox button,
    combobox > box.linked > button.combo {
         background-color: @bg_color;
         border: none;
         box-shadow: none;
    }
    combobox box, combobox cellview {
         background-color: transparent;
         color: @fg_color;
    }

    menuitem, modelbutton {
        color: @fg_color;
        background-color: @bg_color;
    }
    menuitem:hover, modelbutton:hover {
        background-color: #111111;
    }

    scrollbar slider {
        background-color: #333333;
    }
    progressbar trough {
        background-color: #222222;
    }

    .empty-icon,
    .drag-active .empty-icon,
    .drag-active image,
    .drag-active box,
    .drag-active label {
        background-color: transparent;
        background-image: none;
    }

    .row-remove-btn {
        margin-right: 12px;
    }

    .drag-active {
        background-color: alpha(#2ec27e, 0.05);
    }

    progressbar progress {
        background-color: @accent_color;
        background-image: none;
        border: none;
    }

    .success-bar progress {

        background-color: @accent_color;
    }

    /* Small Window Overrides */
    .small-window .filename-label { font-size: 12px; }
    .small-window .dim-label { font-size: 12px; }
"""
