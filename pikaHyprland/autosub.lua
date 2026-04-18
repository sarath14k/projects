--=============================================================================
-->>    AUTO-HEALING SUBLIMINAL CONFIG:
--=============================================================================
local utils = require 'mp.utils'

-- 1. Find Subliminal Path
local subliminal = os.getenv("HOME") .. '/.local/bin/subliminal'

-- 2. Check and Auto-Install
local function ensure_subliminal()
    local check = os.execute(subliminal .. " --version > /dev/null 2>&1")
    if not check then
        mp.osd_message("⚠️ Subliminal missing! Attempting auto-install...", 5)
        mp.msg.warn("Subliminal not found. Attempting install...")
        os.execute("python3 -m pip install --user subliminal --break-system-packages")
    end
end

ensure_subliminal()

--=============================================================================
-->>    SUBTITLE LANGUAGE:
--=============================================================================
local languages = {
            { 'Malayalam', 'ml', 'mal' },
            { 'English', 'en', 'eng' },
            { 'Dutch', 'nl', 'dut' },
}

local logins = {}
local bools = {
    auto = true,   
    debug = false, 
    force = true,  
    utf8 = true,   
}
local excludes = { 'no-subs-dl' }
local includes = {}

-- Download function
function download_subs(language)
    language = language or languages[1]
    if #language == 0 then return false end
            
    mp.osd_message('🔍 Searching ' .. language[1] .. ' subtitles...', 30)

    local table = { args = { subliminal } }
    local a = table.args
    a[#a + 1] = 'download'
    if bools.force then a[#a + 1] = '-f' end
    if bools.utf8 then a[#a + 1] = '-e'; a[#a + 1] = 'utf-8' end

    a[#a + 1] = '-l'; a[#a + 1] = language[2]
    a[#a + 1] = '-d'; a[#a + 1] = directory
    a[#a + 1] = filename 

    local result = utils.subprocess({ args = a, cwd = directory })

    if result.stdout and string.find(result.stdout, 'Downloaded 1 subtitle') then
        mp.set_property('slang', language[2])
        mp.commandv('rescan_external_files')
        mp.osd_message('✅ ' .. language[1] .. ' subtitles ready!')
        return true
    else
        mp.osd_message('❌ No ' .. language[1] .. ' subtitles found')
        return false
    end
end

function download_subs2() download_subs(languages[2]) end

function control_downloads()
    mp.set_property('sub-auto', 'fuzzy')
    mp.set_property('slang', languages[1][2])
    mp.commandv('rescan_external_files')
    local path = mp.get_property('path')
    if not path then return end
    if not path:find('^/') and not path:find('^%w+://') then
        path = utils.join_path(utils.getcwd(), path)
    end
    directory, filename = utils.split_path(path)

    if not autosub_allowed() then return end

    sub_tracks = {}
    for _, track in ipairs(mp.get_property_native('track-list')) do
        if track['type'] == 'sub' then sub_tracks[#sub_tracks + 1] = track end
    end

    for _, language in ipairs(languages) do
        if should_download_subs_in(language) then
            if download_subs(language) then return end 
        else return end 
    end
end

function autosub_allowed()
    local duration = tonumber(mp.get_property('duration'))
    local active_format = mp.get_property('file-format')
    if not bools.auto or duration < 900 or directory:find('^http') then return false end
    return true
end

function should_download_subs_in(language)
    for i, track in ipairs(sub_tracks) do
        if track['lang'] == language[3] or track['lang'] == language[2] then
            if not track['selected'] then mp.set_property('sid', track['id']) end
            return false 
        end
    end
    return true
end

mp.add_key_binding('b', 'download_subs', download_subs)
mp.add_key_binding('n', 'download_subs2', download_subs2)
mp.register_event('file-loaded', control_downloads)
