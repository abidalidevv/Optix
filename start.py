import os
import sys
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def main():
    print("=" * 60)
    print("⚡ OPTIX — Speed & Optical Optimizer (Shopify Booster)")
    print("   Sibling Product of Clonix Labs")
    print("=" * 60)
    print("Starting FastAPI backend on http://localhost:8000 ...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.server:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=str(BASE_DIR)
    )

    time.sleep(2)

    print("Starting React + Vite frontend on http://localhost:5173 ...")
    frontend_proc = subprocess.Popen(
        ["npm.cmd", "run", "dev", "--", "--host", "127.0.0.1", "--port", "5173"],
        cwd=str(BASE_DIR / "frontend")
    )

    print("\n✅ Optix is RUNNING!")
    print("👉 App UI:  http://localhost:5173")
    print("👉 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to terminate both servers.")

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping Optix servers...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("Optix stopped cleanly.")

if __name__ == "__main__":
    main()
