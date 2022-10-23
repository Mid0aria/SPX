try:
    import threading, os, time, urllib, colorama, requests, random, string, names, urllib.request, http.client as httplib, sys
except ImportError:
    input("Error while importing modules. Please install the modules in requirements.txt")
    exit()

colorama.init(convert=True)

lock = threading.Lock()
counter = 0
errorcounter = 0
proxyfilelines = 0
proxies = []
proxy_counter = 0
name = "Spotify X"
owner = "Mido"
module = "main ;)"
rawrepo = "https://raw.githubusercontent.com/Mid0aria/SPX/main"

alert = colorama.Fore.RED + "[!] " + colorama.Fore.MAGENTA
info = colorama.Fore.YELLOW + "[!] " + colorama.Fore.MAGENTA
white = colorama.Fore.WHITE
green = colorama.Fore.GREEN
red = colorama.Fore.RED
magenta = colorama.Fore.MAGENTA


        
if (sys.version_info < (3, 10)):
    print(alert + 'This program only works with Python 3.10+.')
    print(info + f'Your current Python version : {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}' + white)
    sys.exit(1)

def connection():
    conn = httplib.HTTPConnection("www.google.com", timeout=3)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        return False

if (connection() == False):
	if(os.name == "nt"):
		os.system("cls")
	print(alert + "You do not have an internet connection!!!" + white)
	os._exit(1) 
 
def checkupdate():
    r = requests.get(rawrepo + "/version")
    gitver = r.text
    with open('version') as f:
        curver = f.readline()
    if(gitver != curver):
        print(info + "New update available. " + red + curver + white + " -> " + green + gitver)
        print(info + "Downloading update.")
        urllib.request.urlretrieve(rawrepo + '/main.py', 'main.py')
        urllib.request.urlretrieve(rawrepo + '/requirements.txt', 'requirements.txt')
        urllib.request.urlretrieve(rawrepo + '/version', 'version')
        print(info + "Update completed successfully please restart the program.")
        time.sleep(5)
        os._exit(1)
    else:
        return


class followclass:

    def __init__(self, mtype, profile, proxytype = None, proxy = None):
        self.session = requests.Session()
        self.profile = profile
        self.proxy = proxy
        self.proxytype = proxytype
        self.moduletype = mtype
    
    def register_account(self):
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.spotify.com/"
        }
        email = ("").join(random.choices(string.ascii_letters + string.digits, k = 8)) + "@gmail.com"
        password = ("").join(random.choices(string.ascii_letters + string.digits, k = 8))
        proxies = None
        if self.proxy != None:
            if self.proxytype == 1:
                proxies = {"http": f"http://{self.proxy}","https": f"http://{self.proxy}"}
            if self.proxytype == 2:
                proxies = {"http": f"socks4://{self.proxy}","https": f"socks4://{self.proxy}"}
            if self.proxytype == 3:
                proxies = {"http": f"socks5://{self.proxy}","https": f"socks5://{self.proxy}"}
        data = f"birth_day=1&birth_month=01&birth_year=1970&collect_personal_info=undefined&creation_flow=&creation_point=https://www.spotify.com/uk/&displayname={names.get_full_name()}&email={email}&gender=neutral&iagree=1&key=a1e486e2729f46d6bb368d6b2bcda326&password={password}&password_repeat={password}&platform=www&referrer=&send-email=1&thirdpartyemail=0&fb=0"
        try:
            create = self.session.post("https://spclient.wg.spotify.com/signup/public/v1/account", headers = headers, data = data, proxies = proxies)
            if "login_token" in create.text:
                login_token = create.json()['login_token']
                return login_token
            else:
                return None
        except:
            return False

    def get_csrf_token(self):
        try:
            r = self.session.get("https://www.spotify.com/uk/signup/?forward_url=https://accounts.spotify.com/en/status&sp_t_counter=1")
            return r.text.split('csrfToken":"')[1].split('"')[0]
        except:
            return None
        
    def get_token(self, login_token):
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRF-Token": self.get_csrf_token(),
            "Host": "www.spotify.com"
        }
        self.session.post("https://www.spotify.com/api/signup/authenticate", headers = headers, data = "splot=" + login_token)
        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Spotify/1.1.91.824 Safari/537.36",
            "spotify-app-version": "1.1.52.204.ge43bc405",
            "app-platform": "Windows",
            "Host": "open.spotify.com",
            "Referer": "https://open.spotify.com/"
        }
        try:
            r = self.session.get(
                "https://open.spotify.com/get_access_token?reason=transport&productType=web_player",
                headers = headers
            )
            return r.json()["accessToken"]
        except:
            return None

    def follow(self):
        if "/user/" in self.profile:
            self.profile = self.profile.split("/user/")[1]
        if "/playlist" in self.profile:
            self.profile = self.profile.split("/playlist/")[1]
        if "?" in self.profile:
            self.profile = self.profile.split("?")[0]
                         
        login_token = self.register_account()
        if login_token == None:
            return None, "while registering, ratelimit"
        elif login_token == False:
            if self.proxy == None:
                return None, f"unable to send request on register"
            return None, f"bad proxy on register {self.proxy}"
        auth_token = self.get_token(login_token)
        if auth_token == None:
            return None, "while getting auth token"
        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Spotify/1.1.91.824 Safari/537.36",
            "app-platform": "Windows",
            "Referer": "https://open.spotify.com/",
            "spotify-app-version": "1.1.52.204.ge43bc405",
            "authorization": "Bearer {}".format(auth_token),
        }
        if self.moduletype == "spotify_profile":
            try:
                self.session.put(
                    "https://api.spotify.com/v1/me/following?type=user&ids=" + self.profile,
                    headers = headers
                )
                return True, None
            except:
                return False, "while following"
        else:
            try:
                self.session.put(
                    f"https://api.spotify.com/v1/playlists/{self.profile}/followers",
                    headers = headers
                )    
                return True, None
            except:
                return False, "while following"


os.system(f"title {name}/{module} by {owner}")
os.system("cls")
checkupdate()

print(magenta + "[1] " + white + "Profile Follower Bot" + magenta + "\n[2] " + white + "Playlist Follower Bot")
moduleinput = int(input(green + f"\n[{name}] " + white + "Select Module > "))

if moduleinput == 1:
    module = "User"
else:
    module = "Playlist"    
    
os.system(f"title {name}/{module} by {owner}")

spotify_profile = str(input(green + f"\n[{name}/{module}] " + white + f"Spotify {module} Link > "))

threads = int(input(green + f"\n[{name}/{module}] " + white + "Threads > "))
os.system("cls")

print(magenta + "[1] " + white + "Proxies" + magenta + "\n[2] " + white + "Get Free Proxies(Maybe you get bad proxies)" + magenta + "\n[3] " + white + "Proxyless")
proxyinput = int(input(green + f"\n[{name}/{module}] " + white + "Select Proxy Preference > "))

if proxyinput == 1 or proxyinput == 2:
    print(magenta + "\n[1] " + white + "Http" + magenta + "\n[2] " + white + "Socks4" + magenta + "\n[3] " + white + "Socks5")
    proxytype = int(input(green + f"\n[{name}/{module}] " + white +"Select Proxy Type > "))
os.system("cls")

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../../../proxies.txt"
proxiesdir = os.path.join(script_dir, rel_path)
           
def load_proxies():
        global proxyfilelines
        if not os.path.exists(proxiesdir):
            os.system("cls")
            print(info + "File proxies.txt not found")
            time.sleep(5)
            os._exit(0)
        with open(proxiesdir, "r", encoding = "UTF-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                proxyfilelines = len(proxies)
                proxyfilelines += 1
                proxies.append(line)            
            if not len(proxies):
                os.system("cls")
                print(info + "No proxies loaded in proxies.txt")
                time.sleep(5)
                os._exit(0)
    

def getfreeproxy():
    if proxytype == 1:
       # HTTP Proxies
       urllib.request.urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", proxiesdir)
    if proxytype == 2:
       # Socks4 Proxies
       urllib.request.urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all", proxiesdir)
    if proxytype == 3:           
       # Socks5 Proxies
       urllib.request.urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all", proxiesdir)

if proxyinput == 2:
        getfreeproxy()
        time.sleep(1)
        load_proxies()

if proxyinput == 1:
        load_proxies()

def safe_print(arg):
        lock.acquire()
        print(arg)
        lock.release()

def count():
        os.system(f'title [{name}/{module} by {owner}] Followed = {counter} / Error = {errorcounter} / Proxy = {proxyfilelines}')

def thread_starter():
    global counter, errorcounter
    if moduleinput == 1:
        spmoduletype = "spotify_profile"
    else:
        spmoduletype = "spotify_playlist"
    if proxyinput == 1:
           obj = followclass(spmoduletype, spotify_profile, proxytype, proxies[proxy_counter])
    if proxyinput == 2:
            obj = followclass(spmoduletype, spotify_profile, proxytype, proxies[proxy_counter])
    else:
            obj = followclass(spmoduletype, spotify_profile)
    result, error = obj.follow()
    if result == True:
            counter += 1
            safe_print(magenta + f"[{name}/{module}] " + green + "Follower Sended")
            count()
    else:
            errorcounter += 1
            safe_print(magenta + f"[{name}/{module}] " + red + f"Error {error}")
            count()
 
while True:
    if threading.active_count() <= threads:
        try:
            threading.Thread(target = thread_starter).start()
            proxy_counter += 1
        except:
            pass
        if len(proxies) <= proxy_counter:
            proxy_counter = 0
