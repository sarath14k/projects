STANDARD_CSS = """
    /* --- Premium Obsidian Dark Design System --- */
    @define-color primary #818cf8;
    @define-color primary-hover #6366f1;
    @define-color success #34d399;
    @define-color danger #fb7185;
    @define-color warning #fbbf24;
    
    @define-color bg-app #000000;
    @define-color bg-surface #0a0a0a;
    @define-color bg-card #111111;
    @define-color text-main #f8fafc;
    @define-color text-muted #94a3b8;
    @define-color border-ui #1e293b;

    * {
        font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
        color: @text-main;
        outline-width: 0;
    }

    window, .background, scrolledwindow, viewport, list {
        background-color: @bg-app;
        border: none;
    }

    headerbar {
        background-image: none;
        background-color: @bg-surface;
        border-bottom: 1px solid @border-ui;
    }

    .status-bar {
        background-color: @bg-app;
        border-top: 1px solid @border-ui;
        padding: 8px 20px;
        font-size: 11px;
        color: @text-muted;
    }

    .sidebar-header {
        background-color: @bg-surface;
        border-bottom: 1px solid @border-ui;
        padding: 14px 24px;
        font-weight: 700;
        font-size: 18px;
    }

    list row {
        background-color: transparent;
        padding: 0;
        margin: 0;
    }
    list row:selected { background-color: transparent; }

    .video-card {
        background-color: @bg-card;
        border: 1px solid @border-ui;
        border-radius: 12px;
        margin: 6px 16px;
        padding: 12px;
    }
    .video-card:hover { background-color: #1a1a1a; }
    .active-card {
        border-color: @primary;
        background-color: alpha(@primary, 0.05);
    }

    .inspector-pane {
        background-color: @bg-surface;
        border-left: 1px solid @border-ui;
    }

    .inspector-filename {
        font-weight: 700;
        font-size: 20px;
    }

    .studio-preview-frame {
        background-color: #000;
        border-radius: 12px;
        border: 4px solid #1e293b;
    }
    .studio-preview-frame image { border-radius: 8px; }
    .immersive-preview-bg { background-color: transparent; padding: 20px 10px; }

    .btn {
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        border: 1px solid transparent;
        background-image: none;
    }
    
    .btn-primary { background-color: @primary; color: #000; }
    .btn-success { background-color: @success; color: #000; }
    .btn-danger { background-color: @danger; color: #000; }
    .btn-outline-secondary { background-color: #222; border-color: @border-ui; color: #fff; }
    .btn-icon { padding: 6px; border-radius: 8px; background-color: transparent; }

    .text-primary { color: @primary; }
    .text-success { color: @success; }
    .text-danger { color: @danger; }
    .text-warning { color: @warning; }

    /* Tiny Window - Compact Everything */
    .tiny-window .sidebar-header { padding: 8px 12px; font-size: 14px; }
    .tiny-window .video-card { margin: 4px 8px; padding: 8px; }
    .tiny-window .inspector-pane { padding: 0; }
    .tiny-window .immersive-preview-bg { padding: 8px 4px; }
    .tiny-window .studio-preview-frame { border-width: 2px; border-radius: 8px; }
    .tiny-window .inspector-filename { font-size: 14px; }
    .tiny-window .dim-label { font-size: 10px; }
    .tiny-window .btn { padding: 4px 8px; font-size: 11px; }
    .tiny-window combobox { min-width: 60px; }
    
    .small-window .inspector-pane { border-left: none; border-top: 4px solid @primary; }
"""

PITCH_BLACK_CSS = (
    STANDARD_CSS.replace("@define-color bg-surface #0a0a0a;", "@define-color bg-surface #000000;")
    .replace("@define-color bg-card #111111;", "@define-color bg-card #000000;")
    .replace("@define-color border-ui #1e293b;", "@define-color border-ui #111111;")
    .replace("background-color: #1a1a1a;", "background-color: #050505;")
)
