-- Our Own Simple Subtitle Downloader
local utils = require 'mp.utils'
local engine = os.getenv("HOME") .. '/projects/pikaHyprland/sub_selector.sh'

function download_subs()
    local path = mp.get_property('path')
    if not path or path:find('^http') then return end

    -- Run our custom engine
    utils.subprocess_detached({ args = { 'bash', engine, path } })
end

-- Hook it up to Shift+S and the menu
mp.add_key_binding('S', 'download', download_subs)
