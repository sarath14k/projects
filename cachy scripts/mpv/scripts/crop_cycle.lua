-- Cycle through crop ratios (VLC style)
-- Keybinding: 'c' (default)

local crop_ratios = {
    {name = "Disable", vf = ""},
    {name = "16:9", vf = "crop=iw:iw/1.7777"},
    {name = "4:3", vf = "crop=ih*1.3333:ih"},
    {name = "1:1", vf = "crop=ih:ih"},
    {name = "2.35:1", vf = "crop=iw:iw/2.35"}
}

local current_index = 1

function cycle_crop()
    current_index = current_index + 1
    if current_index > #crop_ratios then
        current_index = 1
    end

    local crop = crop_ratios[current_index]
    
    if crop.vf == "" then
        mp.command("set vf \"\"")
        mp.osd_message("Crop: Disabled")
    else
        -- Need to handle video dimensions properly, but simple vf set works for basic cases
        -- A more robust way is to use video-pan/align or just raw ffmpeg filters
        -- For 'crop', usually we want to center the crop.
        -- We can just set the vf property directly.
        mp.command("set vf " .. crop.vf)
        mp.osd_message("Crop: " .. crop.name)
    end
end

mp.add_key_binding("c", "cycle_crop", cycle_crop)
