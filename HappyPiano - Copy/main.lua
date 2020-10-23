display.setStatusBar(display.HiddenStatusBar)

--廣告--
-- local admob = require( "plugin.admob" )
--[[
local ads = require "ads"
local appID = "pub-8648886451787745"
local function adListener(event)
	if event.isError then
		print(event.response)
	end
end
ads.init("admob", appID, adListener)
ads.show("banner", {x=0, y=250, interval=60})
]]--
-- AdMob listener function
--------------------------------------------------------------------------------
------------------------------------是廣告喔-------------------------------------
--------------------------------------------------------------------------------
--[[
local function adListener( event )
 
    if ( event.phase == "init" ) then  -- Successful initialization
        -- Load an AdMob interstitial ad
        admob.load( "interstitial", { adUnitId="ca-app-pub-8648886451787745/8818903575" } )
    end
end
 
-- Initialize the AdMob plugin
admob.init( adListener, { appId="ca-app-pub-8648886451787745~2051736123" } )
 
-- Sometime later, show the interstitial ad
if ( admob.isLoaded( "interstitial" ) ) then
    admob.show( "interstitial" )
end
]]--

 
local fbAudienceNetwork = require( "plugin.fbAudienceNetwork" )
local myPlacementID = "535096590590924_535097300590853"
 
local function adListener( event )
 
    if ( event.phase == "init" ) then  -- Successful initialization
        -- Load a banner ad
        fbAudienceNetwork.load( "banner", { placementId=myPlacementID, bannerSize="BANNER_320_50" } )
 
    elseif ( event.phase == "loaded" ) then  -- The ad was successfully loaded
        print( event.type )
        print( event.placementId )
    end
end
 
-- Initialize the Facebook Audience Network
fbAudienceNetwork.init( adListener )
 
-- Sometime later, check if the ad is loaded and display it
if ( fbAudienceNetwork.isLoaded( myPlacementID ) ) then
    fbAudienceNetwork.show( "banner", { placementId=myPlacementID, y="bottom" } )
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
local backgroundImage = display.newImageRect("Background03.png",960,640)
backgroundImage.x = 480
backgroundImage.y = 320

local widget = require("widget")

system.activate("multitouch")

mySoundList = {}
wordList = {"C", "D", "E", "F", "G", "A", "B", "C", "C#", "D#", "F#", "G#", "A#"}
local wordGroup = display.newGroup()
local text = display.newText("Kming的鋼琴",570,130,native.systemFont, 50)
text:setFillColor( 1, 0, 0.5 )
wordGroup:insert(text)
wordGroup.isVisible = true
--------------------------------
--[[
local keyWord = display.newGroup()
local theWord = display.newImageRect("k1.png", 1500, 200)
keyWord:insert(theWord)
keyWord.x = 1200
keyWord.y = 130
keyWord.isVisible = false
]]--
--------------------------------

for i=1,13 do
	mySoundList[i] = audio.loadSound(i..".mp3")

	local keyPressed = function(event)
		if ("began" == event.phase) then
			print("just pressed key")
			audio.play(mySoundList[i])
			--[[
			print(i)
			keyWord[1]:removeSelf()
			local theWord = display.newImageRect("k"..i..".png",1500, 200)
			keyWord:insert(theWord)
			keyWord.isVisible = true
			]]--
			wordGroup[1]:removeSelf()
			local text = display.newText(wordList[i],570,130,native.systemFont, 100)
			text:setFillColor( 1, 0, 0.5 )
			wordGroup:insert(text)
			wordGroup.isVisible = true

		end
	end

	if (i<9) then
		local key = widget.newButton{ --產生按鈕
			width = 115, 			  --寬度
			height = 340, 
			defaultFile = i..".png", 
			overFile = i.."P.png", 
			onEvent = keyPressed
		}
		key.x = 108+106*(i-1)
		key.y = 398
		
	--以下為黑鍵，分為兩部分做，#c#d跟#f#g#a
	elseif (i>=9 and i<11) then
		local key = widget.newButton{
			width = 65, 			  --寬度
			height = 164, 
			defaultFile = "BlackKey.png", 
			overFile = "BlackKeyPressed.png", 
			onEvent = keyPressed,
		}
		key.x = 108+53*(2*i-17) --- Key1跟key2相加除以二化簡而得
		key.y = 316
	else
		local key = widget.newButton{
			width = 65, 			  --寬度
			height = 164, 
			defaultFile = "BlackKey.png", 
			overFile = "BlackKeyPressed.png", 
			onEvent = keyPressed,
		}
		key.x = 108+53*(2*i-15) --- Key4跟key5相加除以二化簡而得
		key.y = 316
	end
end
----------------------------------------
--當按下琴鍵時產生的音名
--[[
local dispObj_2 = display.newImageRect( "k1.png", 1500, 200)
dispObj_2.x = 1200
dispObj_2.y = 130

local keyWord = display.newGroup()
local theWord = display.newImageRect("k1.png", 1500, 200)
keyWord:insert(theWord)
keyWord.x = 1200
keyWord.y = 130
keyWord.isVisible = false
]]--
