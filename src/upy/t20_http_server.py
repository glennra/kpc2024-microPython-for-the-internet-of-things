import wifi
from microdot import Microdot

wifi.create_ap()

app = Microdot()

# default port is 5000
# e.g. curl 192.168.2.155:500

@app.route('/')
async def index(request):
    return 'Hello, world!'
print("Running app")
app.run()
