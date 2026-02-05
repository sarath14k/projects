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
        font-size: 9px;
        margin-bottom: 2px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .sidebar-bg {
        background-color: alpha(#000000, 0.1);
        border-right: 1px solid alpha(#ffffff, 0.05);
        min-width: 200px;
    }

    /* Responsive Scaling */
    .compact-ui label, .compact-ui combobox *, .compact-ui button label { font-size: 10px; }
    .compact-ui .dim-label { font-size: 9px; }
    .compact-ui .font-bold { font-size: 10px; }
    .compact-ui button { min-height: 28px; padding: 0 6px; }
    .compact-ui combobox { min-height: 28px; }
    .compact-ui .sidebar-bg { min-width: 160px; }

    .narrow-ui label, .narrow-ui combobox *, .narrow-ui button label { font-size: 9px; }
    .narrow-ui .dim-label { font-size: 8px; }
    .narrow-ui .font-bold { font-size: 9px; }
    .narrow-ui button { min-height: 24px; padding: 0 4px; }
    .narrow-ui combobox { min-height: 24px; }
    .narrow-ui .sidebar-bg { min-width: 130px; }
    .narrow-ui .row-card { padding: 4px; }


    .main-gutter {
        padding: 20px;
    }

    .compact-ui .main-gutter { padding: 12px; }
    .narrow-ui .main-gutter { padding: 6px; }

    .font-bold {
        font-weight: bold;
    }

    .row-card {
        border-radius: 16px;
        border: 1px solid alpha(#ffffff, 0.05);
        background-color: @card_bg;
        padding: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    .row-card:hover {
        background-color: shade(@card_bg, 1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

    .file-list { 
        background: transparent;
        padding: 4px; /* Give some room for shadows/selection outlines */
    }
    .file-list row {
        padding-bottom: 8px; /* Slightly tighter spacing for modern look */
        background: transparent;
        margin: 2px 4px;
        border-radius: 16px; /* Match card radius for selection highlight */
    }
    .file-list row:selected {
        background-color: alpha(@accent_color, 0.12);
        outline: 2px solid alpha(@accent_color, 0.5);
        outline-offset: -2px;
    }
    .file-list row:hover { background: transparent; }
 
    .main-area, .main-area scrolledwindow, .main-area viewport, .main-area list, .main-area stack, .main-area listbox, .main-area listrow {
        background-color: transparent;
        background-image: none;
        box-shadow: none;
    }

    .active-row .row-card {
        border: 1px solid @accent_color;
        background-color: alpha(@accent_color, 0.05);
        box-shadow: 0 0 15px alpha(@accent_color, 0.15);
    }

    .thumbnail {
        border-radius: 8px;
        background-color: #000000;
    }

    .drag-active {
        border: none;
        background-color: alpha(@accent_color, 0.05);
        border-radius: 16px;
    }

    button {
        min-height: 38px;
        min-width: 38px;
        padding: 0 12px;
        border-radius: 8px;
        font-weight: 500;
    }

    .destructive-action {
        background-image: none;
        background-color: @destructive_color;
        color: white;
        border: none;
        min-height: 38px;
        min-width: 38px;
        padding: 0 12px;
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
        padding: 0 12px;
        min-height: 38px;
        min-width: 38px;
    }
    .suggested-action label { background-color: transparent; color: inherit; }
    .suggested-action:hover { background-color: @accent_hover; }
    .suggested-action:disabled {
        background-color: alpha(@fg_color, 0.1);
        color: alpha(@fg_color, 0.4);
    }

    .row-remove-btn { color: alpha(@fg_color, 0.5); }
    .row-remove-btn:hover {
        color: @destructive_hover;
        background-color: alpha(@destructive_color, 0.15);
        border-radius: 50%;
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
    }
    .small-row-btn {
        min-height: 28px;
        min-width: 28px;
        padding: 0 4px;
        border-radius: 6px;
    }
    .small-row-btn image {
         -gtk-icon-transform: scale(0.7);
    }

"""

PITCH_BLACK_CSS = """
    /* Color Palette - Pitch Black Theme */
    @define-color bg_color #000000;
    @define-color fg_color #ffffff;
    @define-color card_bg #080808;
    @define-color accent_color #2ec27e;
    @define-color accent_hover #3ad68e;
    @define-color destructive_color #e74c3c;
    @define-color destructive_hover #ff6b6b;
    @define-color warning_color #f39c12;
    @define-color warning_hover #e67e22;
    @define-color success_color #27ae60;
    @define-color info_color #3498db;
    @define-color border_color #333333;
    @define-color shadow_color rgba(0, 0, 0, 0.5);

    * {
        -gtk-icon-style: symbolic;
        font-family: "Inter", "Roboto", "Segoe UI", "Cantarell", "Ubuntu", sans-serif;
    }

    window, .background, headerbar, list, treeview, textview, eventbox, scrolledwindow, viewport {
        background-color: @bg_color;
        background-image: none;
        border-color: @border_color;
        color: @fg_color;
    }
    
    box { background-color: transparent; } /* Default boxes to transparent */
 
    .main-area, .main-area scrolledwindow, .main-area viewport, .main-area list, .main-area stack, .main-area listbox, .main-area listrow {
        background-color: transparent;
        background-image: none;
        box-shadow: none;
    }

    .sidebar-bg {
        background-color: @bg_color;
        border-right: none;
        min-width: 200px;
    }

    /* Responsive Scaling */
    .compact-ui label, .compact-ui combobox *, .compact-ui button label { font-size: 10px; }
    .compact-ui .dim-label { font-size: 9px; }
    .compact-ui .font-bold { font-size: 10px; }
    .compact-ui button { min-height: 28px; padding: 0 6px; }
    .compact-ui combobox { min-height: 28px; }
    .compact-ui .sidebar-bg { min-width: 160px; }

    .narrow-ui label, .narrow-ui combobox *, .narrow-ui button label { font-size: 9px; }
    .narrow-ui .dim-label { font-size: 8px; }
    .narrow-ui .font-bold { font-size: 9px; }
    .narrow-ui button { min-height: 24px; padding: 0 4px; }
    .narrow-ui combobox { min-height: 24px; }
    .narrow-ui .sidebar-bg { min-width: 130px; }
    .narrow-ui .row-card { padding: 4px; }


    .main-gutter {
        padding: 20px;
    }

    .compact-ui .main-gutter { padding: 12px; }
    .narrow-ui .main-gutter { padding: 6px; }

    .font-bold {
        font-weight: bold;
    }

    .row-card {
        background-color: @card_bg;
        border: 1px solid @border_color;
        border-radius: 16px;
        padding: 12px;
    }
    
    .row-card:hover {
        background-color: #111111;
        box-shadow: 0 4px 12px @shadow_color;
    }
    
    .row-card:active {
        background-color: shade(@card_bg, 0.9);
    }
    
    .row-card.disabled {
        opacity: 0.5;
    }
    
    .row-card.error {
        border-color: @destructive_color;
        background-color: alpha(@destructive_color, 0.05);
    }
    
    .row-card.warning {
        border-color: @warning_color;
        background-color: alpha(@warning_color, 0.05);
    }
    
    .row-card.success {
        border-color: @success_color;
        background-color: alpha(@success_color, 0.05);
    }
    .file-list row:selected {
        background-color: alpha(@accent_color, 0.15);
        outline: 2px solid @accent_color;
        outline-offset: -2px;
    }
    
    .active-row .row-card {
        border: 1px solid @accent_color;
        background-color: alpha(@accent_color, 0.08);
        box-shadow: 0 0 20px alpha(@accent_color, 0.2);
    }

    button:not(.suggested-action):not(.destructive-action):not(.flat-button) {
        background-color: #121212;
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
        background-color: @accent_color;
        color: #000000;
        border: none;
    }
    .suggested-action:hover {
        background-color: @accent_hover;
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

    .glass-section {
        background-color: alpha(@fg_color, 0.03);
        border: 1px solid alpha(@fg_color, 0.05);
        border-radius: 12px;
        margin-bottom: 8px;
    }

    .accordion-header {
        min-height: 48px;
        padding: 0 12px;
        background: transparent;
        border: none;
        border-radius: 8px;
        transition: all 0.25s ease;
    }
    .accordion-header:hover {
        background-color: alpha(@fg_color, 0.05);
    }
    .accordion-header label {
        font-weight: 800;
        font-size: 8px;
        letter-spacing: 1px;
        opacity: 0.8;
    }

    .fab-button {
        background-color: @accent_color;
        color: #000000;
        border-radius: 50%;
        min-width: 64px;
        min-height: 64px;
        box-shadow: 0 4px 16px rgba(46, 194, 126, 0.4);
    }
    .fab-button:hover {
        background-color: @accent_hover;
        box-shadow: 0 6px 20px rgba(46, 194, 126, 0.6);
    }

    .skeleton {
        background-color: alpha(@fg_color, 0.05);
        opacity: 0.6;
    }
    .skeleton-text {
        min-width: 100px;
        min-height: 12px;
        border-radius: 4px;
    }

    .active-row .row-card {
        border: 2px solid @accent_color;
        background-color: alpha(@accent_color, 0.08);
        box-shadow: 0 0 15px alpha(@accent_color, 0.3);
    }
    .small-row-btn {
        min-height: 28px;
        min-width: 28px;
        padding: 0 4px;
        border-radius: 6px;
        background-color: alpha(#ffffff, 0.05);
    }
    .small-row-btn image {
         -gtk-icon-transform: scale(0.7);
    }
"""
