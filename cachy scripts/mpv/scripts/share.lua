-- mpv screen sharing script
-- Press Ctrl+Shift+S to enable audio sharing for Google Meet

local utils = require 'mp.utils'

function enable_sharing()
    mp.osd_message("Opening audio setup window...", 3)
    
    -- Open terminal with the audio setup script
    -- The script itself will handle keeping terminal open
    utils.subprocess({
        args = {"kitty", "--title", "MPV Share Audio", "-e", "mpv-share-audio"},
        playback_only = false,
    })
end

-- Bind Ctrl+Shift+S to enable sharing
mp.add_key_binding("Ctrl+Shift+s", "enable-sharing", enable_sharing)

mp.msg.info("Screen sharing keybind loaded: Ctrl+Shift+S")
