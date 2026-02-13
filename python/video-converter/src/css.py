BASE_CSS = """
    @define-color bg_color {bg_color};
    @define-color fg_color {fg_color};
    @define-color card_bg {card_bg};
    @define-color accent_color {accent_color};
    @define-color accent_hover {accent_hover};
    @define-color destructive_color {destructive_color};
    @define-color destructive_hover {destructive_hover};
    @define-color warning_color {warning_color};
    @define-color warning_hover {warning_hover};
    @define-color success_color {success_color};
    @define-color info_color {info_color};
    @define-color border_color {border_color};
    @define-color shadow_color {shadow_color};

    * {{
        font-family: "Google Sans", "Inter", "Roboto", "Segoe UI", sans-serif;
        -gtk-icon-style: symbolic;
    }}

    window, textview, .background, .sidebar-bg {{
        background-color: @bg_color;
        color: @fg_color;
    }}

    .dim-label {{
        opacity: 0.6;
        font-size: 11px;
        margin-bottom: 2px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    .row-card {{
        border-radius: 12px;
        border: 1px solid @border_color;
        background-color: @card_bg;
        padding: 12px;
        box-shadow: 0 2px 8px @shadow_color;
        transition: all 0.2s ease;
    }}

    .row-card:hover {{
        background-color: alpha(@fg_color, 0.05);
        border-color: @accent_color;
        box-shadow: 0 4px 12px @shadow_color;
    }}

    .active-row .row-card {{
        border: 1px solid @accent_color;
        background-color: alpha(@accent_color, 0.08);
    }}

    .thumbnail {{
        border-radius: 8px;
        background-color: #000000;
    }}

    .drag-active {{
        border: 2px dashed @accent_color;
        background-color: alpha(@accent_color, 0.05);
        border-radius: 16px;
    }}

    button {{
        min-height: 38px;
        min-width: 38px;
        padding: 0 12px;
        border-radius: 8px;
        font-weight: 500;
        background-color: @card_bg;
        border: 1px solid @border_color;
        color: @fg_color;
        transition: all 0.2s ease;
    }}
    
    button:hover {{
        background-color: alpha(@fg_color, 0.1);
    }}

    .suggested-action {{
        background-color: @accent_color;
        color: @bg_color;
        font-weight: 700;
        border: none;
    }}
    .suggested-action:hover {{ background-color: @accent_hover; }}
    
    .destructive-action {{
        background-color: @destructive_color;
        color: white;
        border: none;
    }}
    .destructive-action:hover {{ background-color: @destructive_hover; }}

    .flat-button {{
        border: none;
        background: transparent;
        box-shadow: none;
        color: alpha(@fg_color, 0.6);
        border-radius: 50%;
        min-height: 24px;
        min-width: 24px;
        padding: 4px;
    }}
    .flat-button:hover {{
        background-color: alpha(@fg_color, 0.1);
        color: @accent_color;
    }}

    progressbar trough {{
        min-height: 6px;
        border-radius: 3px;
        background-color: alpha(#000000, 0.3);
    }}
    progressbar progress {{
        min-height: 6px;
        border-radius: 3px;
        background-color: @accent_color;
    }}
    .success-bar progress {{ background-color: @success_color; }}
    .error-bar progress {{ background-color: @destructive_color; }}

    .header-area {{
        background-color: transparent;
    }}
    
    .compact-header {{
        padding: 4px 8px;
    }}
    
    .header-row {{
        margin-bottom: 4px;
    }}

    .bottom-bar {{
        background-color: @card_bg;
        border-top: 1px solid @border_color;
        margin-top: 4px;
    }}

    .accent-text {{ color: @accent_color; font-weight: bold; }}
    .success-text {{ color: @success_color; font-weight: bold; }}
    .warning-text {{ color: @warning_color; font-weight: bold; }}
    .error-text {{ color: @destructive_color; font-weight: bold; }}
    .info-text {{ color: @info_color; }}
"""
