-- Simple-Subs: THE LIST EDITION
local utils = require 'mp.utils'
local engine = os.getenv("HOME") .. '/projects/pikaHyprland/sub_list.py'

function download_subs()
    local path = mp.get_property('path')
    if not path or path:find('^http') then return end

    -- Run our new List Selector
    utils.subprocess_detached({ args = { 'python3', engine, path } })
end

mp.add_key_binding('S', 'download', download_subs)
