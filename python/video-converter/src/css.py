PITCH_BLACK_CSS = """
            @define-color theme_bg_color #000000;
            @define-color theme_base_color #000000;
            @define-color theme_fg_color #ffffff;
            @define-color card_bg_color #121212; 
            @define-color accent_color #2ec27e;
            @define-color accent_hover #3ad68e;
            @define-color destructive_color #e74c3c;
            
            * {
                -gtk-icon-style: symbolic;
            }

            window, .background, headerbar, list, treeview, textview, eventbox, scrolledwindow, viewport, box {
                background-color: #000000;
                background-image: none;
                border-color: #333333;
            }
            
            .dim-label { 
                opacity: 0.6; 
                font-size: 11px; 
                margin-bottom: 2px; 
                font-weight: 600; 
                letter-spacing: 0.5px; 
            }
            
            .sidebar-bg { 
                background-color: #000000; 
                border-right: none; 
            }
            
            .row-card { 
                border-radius: 16px; 
                border: none; 
                background-color: #080808; 
                padding: 12px; 
            }
            
            .active-row .row-card { 
                border: 1px solid @accent_color; 
                background-color: alpha(@accent_color, 0.05); 
            }
            
            .row-card:hover { 
                background-color: #111111; 
                transition: background-color 0.2s ease; 
            }
            
            .file-list row { 
                padding-bottom: 12px; 
                margin-left: 4px;
                margin-right: 4px;
            }
            
            button image {
                background-color: transparent;
            }

            button:not(.suggested-action):not(.destructive-action):not(.flat-button) {
                background-color: #080808;
                background-image: none;
                border: none;
                border-radius: 8px;
                box-shadow: none;
                text-shadow: none;
                color: #ffffff;
                min-height: 38px;
                min-width: 38px;
                padding: 0 12px;
                font-weight: 500;
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
                border-radius: 8px;
                background-image: none;
                box-shadow: none;
                text-shadow: none;
                font-weight: 700;
                min-height: 38px;
                min-width: 38px;
                padding: 0 12px;
            }
            .suggested-action image, .suggested-action box {
                background-color: transparent;
                background-image: none;
                color: inherit;
            }
            .suggested-action:hover { background-color: @accent_hover; }

            .destructive-action {
                background-color: @destructive_color;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                background-image: none;
                box-shadow: none;
                text-shadow: none;
                min-height: 38px;
                min-width: 38px;
                padding: 0 12px;
            }
            .destructive-action image, .destructive-action box {
                background-color: transparent;
                background-image: none;
                color: inherit;
            }
            .destructive-action:hover { background-color: shade(@destructive_color, 1.1); }
            
            .flat-button {
                border-radius: 50%;
                color: #888888;
            }
            .flat-button:hover {
                background-color: #222222;
                color: @accent_color;
            }

            entry, combobox, spinbutton, treeview, textview, popover, menu, menubar, toolbar {
                background-color: #000000;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                box-shadow: none;
                outline-width: 0px;
                outline: none;
            }
            
            combobox button, 
            combobox > box.linked > button.combo {
                 background-color: #000000;
                 border: none;
                 border-radius: 6px;
                 padding-left: 8px;
                 box-shadow: none;
            }
            
            combobox box {
                 background-color: transparent;
            }
            combobox cellview {
                 background-color: transparent;
                 color: #ffffff;
            }

            menuitem, modelbutton {
                color: #ffffff;
                background-color: #000000;
            }
            menuitem:hover, modelbutton:hover {
                background-color: #111111;
            }
            
            scrollbar slider {
                background-color: #333333;
                border-radius: 4px;
            }
            
            progressbar trough { 
                min-height: 4px; 
                background-color: #222222; 
                border-radius: 2px;
            }
            progressbar progress { 
                min-height: 4px; 
                background-color: @accent_color; 
                border-radius: 2px;
            }
"""
