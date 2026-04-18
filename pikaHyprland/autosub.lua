local utils = require 'mp.utils'

-- Dynamic Path Resolution
local subliminal = os.getenv("HOME") .. '/.local/bin/subliminal'

-- Self-Healing Function (Runs only when needed)
local function check_engine()
    local check = os.execute(subliminal .. " --version > /dev/null 2>&1")
    if not check then
        -- Try global command as fallback
        check = os.execute("subliminal --version > /dev/null 2>&1")
        if check then 
            subliminal = "subliminal" 
            return true
        end
        
        mp.osd_message("⚠️ Subliminal missing! Installing...", 5)
        os.execute("python3 -m pip install --user subliminal --break-system-packages")
        return os.execute(os.getenv("HOME") .. "/.local/bin/subliminal --version > /dev/null 2>&1")
    end
    return true
end

--=============================================================================
-->>    CONFIG:
--=============================================================================
local languages = {
    { 'Malayalam', 'ml', 'mal' },
    { 'English', 'en', 'eng' },
}

-- Core Download Engine
function download_subs(language)
    if not check_engine() then
        mp.osd_message("❌ Error: Subliminal engine failed to start", 5)
        return false
    end

    language = language or languages[1]
    mp.osd_message('🔍 Searching ' .. language[1] .. ' subtitles...', 10)

    local path = mp.get_property('path')
    if not path or path:find('^http') then 
        mp.osd_message("❌ Cannot search for streams/urls", 5)
        return false 
    end
    
    local dir, file = utils.split_path(path)
    if not dir:find('^/') then dir = utils.join_path(utils.getcwd(), dir) end

    local args = { subliminal, 'download', '-f', '-e', 'utf-8', '-l', language[2], '-d', dir, file }

    print("ENGINE RUNNING: " .. table.concat(args, " "))
    local result = utils.subprocess({ args = args, cwd = dir })

    if result.status == 0 and result.stdout and string.find(result.stdout, 'Downloaded 1 subtitle') then
        mp.set_property('slang', language[2])
        mp.commandv('rescan_external_files')
        mp.osd_message('✅ ' .. language[1] .. ' subtitles ready!')
        return true
    else
        mp.osd_message('❌ No subtitles found', 5)
        return false
    end
end

-- Key Bindings (Required for uosc to see the command)
mp.add_key_binding('b', 'download_subs', download_subs)

-- Auto-download on file load
mp.register_event('file-loaded', function()
    -- Only auto-download if no subtitles exist
    local tracks = mp.get_property_native('track-list')
    local has_sub = false
    for _, t in ipairs(tracks) do
        if t.type == 'sub' then has_sub = true; break end
    end
    
    if not has_sub then
        download_subs(languages[1])
    end
end)
