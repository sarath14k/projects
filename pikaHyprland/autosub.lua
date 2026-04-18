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
}

local logins = {}
local bools = {
    auto = true,   
    force = true,  
    utf8 = true,   
}

-- Download function
function download_subs(language)
    language = language or languages[1]
    mp.osd_message('🔍 Searching ' .. language[1] .. ' subtitles...', 10)

    local table = { args = { subliminal } }
    local a = table.args
    a[#a + 1] = 'download'
    if bools.force then a[#a + 1] = '-f' end
    if bools.utf8 then a[#a + 1] = '-e'; a[#a + 1] = 'utf-8' end

    a[#a + 1] = '-l'; a[#a + 1] = language[2]
    a[#a + 1] = '-d'; a[#a + 1] = directory
    a[#a + 1] = filename 

    -- DEBUG: Print full command to terminal
    print("RUNNING: " .. table.concat(a, " "))

    local result = utils.subprocess({ args = a, cwd = directory })

    if result.status == 0 and result.stdout and string.find(result.stdout, 'Downloaded 1 subtitle') then
        mp.set_property('slang', language[2])
        mp.commandv('rescan_external_files')
        mp.osd_message('✅ ' .. language[1] .. ' subtitles ready!')
        return true
    else
        local err_msg = "❌ No subtitles found"
        if result.status ~= 0 then
            err_msg = "⚠️ Error: " .. (result.stderr or "Unknown Error")
        end
        mp.osd_message(err_msg, 5)
        print("RESULT: " .. (result.stdout or "") .. " | ERR: " .. (result.stderr or ""))
        return false
    end
end

function download_subs2() download_subs(languages[2]) end

function control_downloads()
    mp.set_property('sub-auto', 'fuzzy')
    local path = mp.get_property('path')
    if not path or path:find('^http') then return end
    
    if not path:find('^/') then
        path = utils.join_path(utils.getcwd(), path)
    end
    directory, filename = utils.split_path(path)

    sub_tracks = {}
    for _, track in ipairs(mp.get_property_native('track-list')) do
        if track['type'] == 'sub' then sub_tracks[#sub_tracks + 1] = track end
    end

    for _, language in ipairs(languages) do
        local found = false
        for _, track in ipairs(sub_tracks) do
            if track['lang'] == language[2] or track['lang'] == language[3] then
                found = true; break
            end
        end
        if not found then
            if download_subs(language) then return end
        end
    end
end

mp.add_key_binding('b', 'download_subs', download_subs)
mp.add_key_binding('n', 'download_subs2', download_subs2)
mp.register_event('file-loaded', control_downloads)
