-- Simple-Subs: A minimal subtitle downloader for MPV
local utils = require 'mp.utils'
local subliminal = os.getenv("HOME") .. '/.local/bin/subliminal'

function download_subs()
    local path = mp.get_property('path')
    if not path or path:find('^http') then 
        mp.osd_message("❌ Cannot search streams")
        return 
    end

    local dir, file = utils.split_path(path)
    mp.osd_message("🔍 Searching subtitles...", 5)

    -- The one and only command: Simple and effective
    local args = { subliminal, 'download', '-l', 'en', '-d', dir, file }
    local result = utils.subprocess({ args = args, cwd = dir })

    if result.status == 0 and result.stdout and string.find(result.stdout, 'Downloaded 1 subtitle') then
        mp.commandv('rescan_external_files')
        mp.osd_message("✅ Subtitles Ready!")
    else
        mp.osd_message("❌ Not Found")
    end
end

-- 1 Method: Just press 'S' (Capital S) or use the menu
mp.add_key_binding('S', 'download', download_subs)
