--// =============================================================================
--// [0] INITIAL IDENTITY INJECTION (BACKGROUND PIPELINE)
--// =============================================================================
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local reFolder = ReplicatedStorage:WaitForChild("RE", 5)

if reFolder then
    local nameRemote = reFolder:WaitForChild("1RPNam1eTex1t", 3)
    local colorRemote = reFolder:WaitForChild("1RPNam1eColo1r", 3)
    
    if nameRemote then
        pcall(function()
            nameRemote:FireServer("RolePlayName", "RXO HUB V2.1")
            task.wait(0.2)
            nameRemote:FireServer("RolePlayBio", "SPEICAL--MEMBERS ONLY HUB👉🔥")
        end)
    end

    if colorRemote then
        task.spawn(function()
            while true do
                local color = Color3.fromHSV(math.random(), 1, 1)
                pcall(function()
                    colorRemote:FireServer("PickingRPNameColor", color)
                    colorRemote:FireServer("PickingRPBioColor", color)
                end)
                task.wait(0.05)
            end
        end)
    end
end

--// =============================================================================
--// [[ RxO HUB - ARCTIC PREMIUM EDITION (V1.7) ]] --
--// =============================================================================
local CoreGui = game:GetService("CoreGui")
local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local Players = game:GetService("Players")

if CoreGui:FindFirstChild("RxOHub_Core") then
    CoreGui.RxOHub_Core:Destroy()
end

local RxOHub = Instance.new("ScreenGui")
RxOHub.Name = "RxOHub_Core"
RxOHub.Parent = CoreGui
RxOHub.ResetOnSpawn = false

local ARCTIC_DARK   = Color3.fromRGB(10, 16, 26)   
local ARCTIC_LIGHT  = Color3.fromRGB(20, 32, 50)   
local ARCTIC_CONTENT = Color3.fromRGB(14, 22, 34)  
local ARCTIC_GLOW   = Color3.fromRGB(0, 210, 255)  
local ARCTIC_WHITE  = Color3.fromRGB(235, 245, 255) 
local ARCTIC_MUTED  = Color3.fromRGB(120, 140, 160) 

local function quickTween(obj, duration, properties)
    local info = TweenInfo.new(duration, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
    local tween = TweenService:Create(obj, info, properties)
    tween:Play()
    return tween
end

local ToggleBtn = Instance.new("TextButton")
ToggleBtn.Name = "HubToggle"
ToggleBtn.Parent = RxOHub
ToggleBtn.Position = UDim2.new(0.03, 0, 0.2, 0)
ToggleBtn.Size = UDim2.new(0, 50, 0, 50)
ToggleBtn.BackgroundColor3 = ARCTIC_DARK
ToggleBtn.Text = "RxO"
ToggleBtn.Font = Enum.Font.GothamBold
ToggleBtn.TextSize = 14
ToggleBtn.TextColor3 = ARCTIC_GLOW

local ToggleCorner = Instance.new("UICorner")
ToggleCorner.CornerRadius = UDim.new(1, 0)
ToggleCorner.Parent = ToggleBtn

local ToggleStroke = Instance.new("UIStroke")
ToggleStroke.Thickness = 2
ToggleStroke.Color = ARCTIC_LIGHT
ToggleStroke.Parent = ToggleBtn

local MainFrame = Instance.new("Frame")
MainFrame.Name = "MainConsole"
MainFrame.Parent = RxOHub
MainFrame.Position = UDim2.new(0.5, -175, 0.5, -125)
MainFrame.Size = UDim2.new(0, 350, 0, 250)
MainFrame.BackgroundColor3 = ARCTIC_DARK
MainFrame.Active = true
MainFrame.Draggable = true

local MainCorner = Instance.new("UICorner")
MainCorner.CornerRadius = UDim.new(0, 14)
MainCorner.Parent = MainFrame

local MainStroke = Instance.new("UIStroke")
MainStroke.Thickness = 1.5
MainStroke.Color = ARCTIC_LIGHT
MainStroke.Parent = MainFrame

local TopBar = Instance.new("Frame")
TopBar.Name = "TopBar"
TopBar.Size = UDim2.new(1, 0, 0, 40)
TopBar.BackgroundTransparency = 1
TopBar.Parent = MainFrame

local HubTitle = Instance.new("TextLabel")
HubTitle.Size = UDim2.new(1, -20, 1, 0)
HubTitle.Position = UDim2.new(0, 15, 0, 0)
HubTitle.BackgroundTransparency = 1
HubTitle.Text = "RxO HUB <font color='rgb(0, 210, 255)'>ARCTIC</font>"
HubTitle.RichText = true
HubTitle.Font = Enum.Font.GothamBold
HubTitle.TextSize = 14
HubTitle.TextColor3 = ARCTIC_WHITE
HubTitle.TextXAlignment = Enum.TextXAlignment.Left
HubTitle.Parent = TopBar

local Navigation = Instance.new("Frame")
Navigation.Name = "Navigation"
Navigation.Position = UDim2.new(0, 12, 0, 45)
Navigation.Size = UDim2.new(0, 100, 1, -60)
Navigation.BackgroundTransparency = 1
Navigation.Parent = MainFrame

local TabButton = Instance.new("TextButton")
TabButton.Size = UDim2.new(1, 0, 0, 32)
TabButton.BackgroundColor3 = ARCTIC_LIGHT
TabButton.Text = "RxO sCripTs!"
TabButton.Font = Enum.Font.GothamBold
TabButton.TextSize = 11
TabButton.TextColor3 = ARCTIC_GLOW
TabButton.Parent = Navigation

local TabCorner = Instance.new("UICorner")
TabCorner.CornerRadius = UDim.new(0, 6)
TabCorner.Parent = TabButton

local ContentFrame = Instance.new("ScrollingFrame")
ContentFrame.Name = "ContentFrame"
ContentFrame.Position = UDim2.new(0, 122, 0, 45)
ContentFrame.Size = UDim2.new(1, -134, 1, -60)
ContentFrame.BackgroundColor3 = ARCTIC_CONTENT
ContentFrame.BorderSizePixel = 0
ContentFrame.ScrollBarThickness = 3
ContentFrame.ScrollBarImageColor3 = ARCTIC_MUTED
ContentFrame.Parent = MainFrame
Instance.new("UICorner", ContentFrame).CornerRadius = UDim.new(0, 8)

local ListLayout = Instance.new("UIListLayout")
ListLayout.Padding = UDim.new(0, 8)
ListLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center
ListLayout.SortOrder = Enum.SortOrder.LayoutOrder
ListLayout.Parent = ContentFrame
Instance.new("UIPadding", ContentFrame).PaddingTop = UDim.new(0, 6)

local VersionTag = Instance.new("TextLabel")
VersionTag.Position = UDim2.new(0, 15, 1, -18)
VersionTag.Size = UDim2.new(1, -30, 0, 15)
VersionTag.BackgroundTransparency = 1
VersionTag.Text = "MOBILE ENGINE COMPATIBLE v1.7"
VersionTag.Font = Enum.Font.Code
VersionTag.TextSize = 8
VersionTag.TextColor3 = ARCTIC_MUTED
VersionTag.TextXAlignment = Enum.TextXAlignment.Right
VersionTag.Parent = MainFrame

local function createScriptCard(name, executionString)
    local Card = Instance.new("Frame")
    Card.Name = "ScriptCard"
    Card.Size = UDim2.new(0.92, 0, 0, 50)
    Card.BackgroundColor3 = ARCTIC_LIGHT
    Card.Parent = ContentFrame

    local CardCorner = Instance.new("UICorner")
    CardCorner.CornerRadius = UDim.new(0, 8)
    CardCorner.Parent = Card

    local CardStroke = Instance.new("UIStroke")
    CardStroke.Thickness = 1
    CardStroke.Color = Color3.fromRGB(30, 45, 65)
    CardStroke.Parent = Card

    local Title = Instance.new("TextLabel")
    Title.Size = UDim2.new(0.65, 0, 1, 0)
    Title.Position = UDim2.new(0, 10, 0, 0)
    Title.BackgroundTransparency = 1
    Title.Text = name
    Title.Font = Enum.Font.GothamBold
    Title.TextSize = 11
    Title.TextColor3 = ARCTIC_WHITE
    Title.TextXAlignment = Enum.TextXAlignment.Left
    Title.Parent = Card

    local ExecBtn = Instance.new("TextButton")
    ExecBtn.Name = "ExecBtn"
    ExecBtn.Size = UDim2.new(0.28, 0, 0, 26)
    ExecBtn.Position = UDim2.new(0.68, 0, 0.5, -13)
    ExecBtn.BackgroundColor3 = Color3.fromRGB(24, 42, 68)
    ExecBtn.Text = "RUN"
    ExecBtn.Font = Enum.Font.GothamBold
    ExecBtn.TextSize = 10
    ExecBtn.TextColor3 = ARCTIC_GLOW
    ExecBtn.Parent = Card
    Instance.new("UICorner", ExecBtn).CornerRadius = UDim.new(0, 6)
    local ExecStroke = Instance.new("UIStroke", ExecBtn)
    ExecStroke.Color = Color3.fromRGB(0, 140, 200)

    ExecBtn.MouseEnter:Connect(function()
        quickTween(ExecBtn, 0.2, {BackgroundColor3 = Color3.fromRGB(0, 150, 200), TextColor3 = ARCTIC_WHITE})
    end)
    ExecBtn.MouseLeave:Connect(function()
        quickTween(ExecBtn, 0.2, {BackgroundColor3 = Color3.fromRGB(24, 42, 68), TextColor3 = ARCTIC_GLOW})
    end)

    ExecBtn.MouseButton1Click:Connect(function()
        ExecBtn.Text = "RUNNING..."
        task.wait(0.15)
        ExecBtn.Text = "RUN"

        task.spawn(function()    
            local func, err = loadstring(executionString)    
            if func then func() else warn("RxO Hub Execution Error: " .. tostring(err)) end    
        end)
    end)
end

--// DEFAULT CARDS
createScriptCard("RxO rechat delayed bug", [[loadstring(game:HttpGet("https://pastefy.app/J3Y1rYGi/raw"))()]])
createScriptCard("Spammer Best v4", [[loadstring(game:HttpGet("https://pastefy.app/qWlpfhRW/raw"))()]])
createScriptCard("Prop Rep", [[loadstring(game:HttpGet("https://pastefy.app/I2hBqplP/raw"))()]])
createScriptCard("RxO emotes", [[loadstring(game:HttpGet("https://pastefy.app/UoLJfIsI/raw"))()]])
createScriptCard("RxO PlaYeR banger", [[loadstring(game:HttpGet("https://pastefy.app/IRPZn64G/raw"))()]])
createScriptCard("RxO proP trOll {little bugged}", [[loadstring(game:HttpGet("https://pastefy.app/uQUAFTgc/raw"))()]])
createScriptCard("RxO Anti Bang v1.1", [[loadstring(game:HttpGet("https://pastefy.app/rqdjH79c/raw"))()]])
createScriptCard("RxO foNtz", [[loadstring(game:HttpGet("https://pastefy.app/9w4IcvkO/raw"))()]])
createScriptCard("RxO bOt sCript Best", [[loadstring(game:HttpGet("https://pastefy.app/4dR91XZe/raw", true))()]])

--// CORRECTLY INSTANTIATED INTERACTIVE CARDS
createScriptCard("SIGN TROLL OP", [[loadstring(game:HttpGet("https://pastefy.app/RJ6xRwTn/raw"))()]])
createScriptCard("Identity Spammer", [[loadstring(game:HttpGet("https://pastefy.app/k6Ussa4x/raw"))()]])

ContentFrame.CanvasSize = UDim2.new(0, 0, 0, ListLayout.AbsoluteContentSize.Y + 15)
ListLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
    ContentFrame.CanvasSize = UDim2.new(0, 0, 0, ListLayout.AbsoluteContentSize.Y + 15)
end)

-- [5] CORE RUNTIME INTERFACE TRANSITIONS
task.spawn(function()
    local clock = 0
    while true do
        local cycle = math.abs(math.sin(clock))
        local blendedColor = Color3.fromRGB(0, 120 + (cycle * 90), 180 + (cycle * 75))
        MainStroke.Color = blendedColor
        ToggleStroke.Color = blendedColor
        clock = clock + 0.04
        task.wait(0.04)
    end
end)

local uiVisible = true
ToggleBtn.MouseButton1Click:Connect(function()
    uiVisible = not uiVisible
    if uiVisible then
        MainFrame.Visible = true
        quickTween(MainFrame, 0.3, {Size = UDim2.new(0, 350, 0, 250), BackgroundTransparency = 0})

        for _, obj in ipairs(MainFrame:GetDescendants()) do
            if obj:IsA("Frame") or obj:IsA("ScrollingFrame") then
                local targetTransparency = 0
                if obj.Name == "TopBar" or obj.Name == "Navigation" then targetTransparency = 1 end
                quickTween(obj, 0.2, {BackgroundTransparency = targetTransparency})
            elseif obj:IsA("TextLabel") or obj:IsA("TextButton") then
                quickTween(obj, 0.2, {TextTransparency = 0, BackgroundTransparency = obj:IsA("TextButton") and 0 or 1})
            elseif obj:IsA("UIStroke") then
                quickTween(obj, 0.2, {Transparency = 0})
            end
        end
    else
        quickTween(MainFrame, 0.3, {Size = UDim2.new(0, 350, 0, 0), BackgroundTransparency = 1})
        for _, obj in ipairs(MainFrame:GetDescendants()) do
            if obj:IsA("Frame") or obj:IsA("ScrollingFrame") then
                quickTween(obj, 0.15, {BackgroundTransparency = 1})
            elseif obj:IsA("TextLabel") or obj:IsA("TextButton") then
                quickTween(obj, 0.15, {TextTransparency = 1, BackgroundTransparency = 1})
            elseif obj:IsA("UIStroke") then
                quickTween(obj, 0.15, {Transparency = 1})
            end
        end
        task.wait(0.3)
        if not uiVisible then MainFrame.Visible = false end
    end
end)
