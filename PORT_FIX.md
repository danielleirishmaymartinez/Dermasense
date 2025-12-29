# Fixing Port 8000 Error

## Problem
The error `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)` means port 8000 is already in use.

## Solutions

### Option 1: Kill processes using port 8000 (Windows)

Run this command in PowerShell (as Administrator):
```powershell
netstat -ano | findstr :8000
```

Then kill each process ID (PID) shown:
```powershell
taskkill /PID <PID> /F
```

Or use the batch file:
```cmd
KILL_PORT.bat
```

### Option 2: Use the updated backend code

The backend code now automatically tries alternative ports (8001, 8002, 8003, 8080) if 8000 is busy.

**Important:** If the backend uses a different port, you need to update the frontend API client!

Edit `frontend/src/api/client.js` and change:
```javascript
baseURL: "http://127.0.0.1:8000",
```
to the port shown in the backend console (e.g., `8001`, `8002`, etc.).

### Option 3: Find and close the old backend

If you have an old backend server running:
1. Check your terminal windows for a running `python main.py` process
2. Press `Ctrl+C` to stop it
3. Then start the backend again

---

**After fixing, restart the backend and check the console output for the actual port number!**

