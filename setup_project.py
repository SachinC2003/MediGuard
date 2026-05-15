"""
Setup script to install all dependencies and verify the system
"""
import subprocess
import sys
import os

def run_command(cmd, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] {cmd}")
            return True
        else:
            print(f"[FAIL] {cmd}")
            if result.stderr:
                print(result.stderr[:500])
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    base_dir = "c:\\Users\\Sachin\\Desktop\\New folder"
    
    print("=" * 60)
    print("SETTING UP FEDERATED LEARNING + FLASK + REACT PROJECT")
    print("=" * 60)
    
    # 1. Install Flask backend dependencies
    print("\n[1] Installing Flask Backend dependencies...")
    flask_path = os.path.join(base_dir, "flask-backend")
    run_command("pip install Flask Flask-CORS scikit-learn pandas tensorflow numpy", cwd=flask_path)
    
    # 2. Install MegaProject (Federated Learning) dependencies
    print("\n[2] Installing MegaProject (Federated Learning) dependencies...")
    mega_path = os.path.join(base_dir, "megaProject")
    run_command("pip install flwr scikit-learn pandas tensorflow numpy", cwd=mega_path)
    
    # 3. Install Frontend dependencies
    print("\n[3] Installing Frontend dependencies...")
    frontend_path = os.path.join(base_dir, "megaProject-Frontend")
    run_command("npm install", cwd=frontend_path)
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nNEXT STEPS:")
    print("[Step 1] Start Federated Learning Server (in megaProject/)")
    print("   python server.py")
    print("\n[Step 2] Start Federated Learning Clients (open 3 terminals)")
    print("   python client.py --client-id 0 --num-clients 3")
    print("   python client.py --client-id 1 --num-clients 3")
    print("   python client.py --client-id 2 --num-clients 3")
    print("\n[Step 3] Start Flask Backend (in flask-backend/)")
    print("   python app.py")
    print("\n[Step 4] Start React Frontend (in megaProject-Frontend/)")
    print("   npm run dev")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

