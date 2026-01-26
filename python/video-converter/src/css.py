PITCH_BLACK_CSS = """
            @define-color theme_bg_color #000000;
            @define-color theme_base_color #000000;
            @define-color theme_fg_color #ffffff;
            @define-color window_bg_color #000000;
            @define-color window_fg_color #ffffff;
            
            window, .background, headerbar, list, treeview, textview, eventbox, scrolledwindow, viewport, box {
                background-color: #000000;
                background-image: none;
                border-color: #333333;
            }
            .dim-label { 
                opacity: 0.8; 
                font-size: 10px; 
                margin-bottom: 2px; 
                font-weight: bolder; 
                letter-spacing: 0.5px; 
            }
            
            .sidebar-bg { 
                background-color: alpha(currentColor, 0.03); 
                border-right: 1px solid alpha(currentColor, 0.1); 
            }
            .row-card { 
                border-radius: 12px; 
                border: 1px solid alpha(currentColor, 0.08); 
                background-color: alpha(currentColor, 0.03); 
                padding: 8px; 
            }
            .active-row .row-card { 
                border: 1px solid #2ec27e; 
                background-color: alpha(#2ec27e, 0.08); 
            }
            .row-card:hover { 
                background-color: alpha(currentColor, 0.08); 
                transition: background-color 0.2s ease; 
            }
            button:not(.suggested-action):not(.destructive-action):not(.flat-button) {
                background-color: #000000;
                background-image: none;
                border: 1px solid #222222; 
                border-radius: 4px;
                box-shadow: none;
                text-shadow: none;
                color: #ffffff;
            }
            
            button:not(.suggested-action):not(.destructive-action):not(.flat-button):hover {
                background-color: #111111;
                border-color: #444444;
            }
            button:not(.suggested-action):not(.destructive-action):not(.flat-button):active {
                background-color: #222222;
            }
            
            /* Explicitly preserve/fix suggested action */
            .suggested-action {
                background-color: #2ec27e;
                color: #000000;
                border: none;
                border-radius: 4px;
                background-image: none;
                box-shadow: none;
                text-shadow: none;
                -gtk-icon-shadow: none;
            }
            .suggested-action image, .suggested-action box {
                background-color: transparent;
                background-image: none;
                color: inherit;
            }
            .suggested-action:hover { background-color: #3ad68e; }

            /* Explicitly preserve/fix destructive action */
            .destructive-action {
                background-color: #e74c3c;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                background-image: none;
                box-shadow: none;
                text-shadow: none;
                -gtk-icon-shadow: none;
            }
            .destructive-action image, .destructive-action box {
                background-color: transparent;
                background-image: none;
                color: inherit;
            }
            .destructive-action:hover { background-color: #ff6b6b; }

            entry, combobox, spinbutton, treeview, textview, popover, menu, menubar, toolbar {
                background-color: #000000;
                color: #ffffff;
                border: none;
                border-radius: 0;
                box-shadow: none;
                outline-width: 0px;
                outline: none;
                -gtk-outline-radius: 0;
            }

            /* Deep targeting for combobox internals */
            combobox *, 
            combobox button, 
            combobox button.combo,
            combobox > box.linked > button.combo {
               background-color: #000000;
               background-image: none;
               border: none;
               border-image: none;
               border-radius: 0;
               box-shadow: none;
               outline: none;
               text-shadow: none;
            }
            
            /* Remove the dashed focus ring */
            entry, combobox, list, row, treeview, textview, scrolledwindow, iconview {
               outline-width: 0px;
            }

            combobox window {
                background-color: #000000;
            }
            
            /* Target internal entry of combobox if present */
            combobox entry {
                background-color: #000000;
                color: #ffffff;
            }

            /* Fix dropdown menus */
            menuitem, modelbutton {
                color: #ffffff;
                background-color: #000000;
            }
            menuitem:hover, modelbutton:hover {
                background-color: #222222;
            }
            
            /* Scrollbars */
            scrollbar slider {
                background-color: #333333;
            }
"""
