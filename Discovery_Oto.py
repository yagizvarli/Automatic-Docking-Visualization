import os
import glob
import subprocess
import time
import shutil
import pyautogui
import pyperclip

# ==========================================
# CONFIGURATION & PATH SETTINGS
# ==========================================
BASE_DIR = "Interaction_Maps"
CONFIDENCE_LEVEL = 0.75  
pyautogui.FAILSAFE = True 

# Set your Discovery Studio executable path.
# Can be overridden via environment variable: export DS_BIN_PATH="/path/to/DiscoveryStudio"
DEFAULT_DS_PATH = os.path.expanduser("~/BIOVIA/DiscoveryStudio2024/bin/DiscoveryStudio2024")
DS_BIN = os.getenv("DS_BIN_PATH", DEFAULT_DS_PATH)

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def click_on_image(image_name, max_retries=5, delay_between_retries=1, offset_x=0, offset_y=0):
    """Locate an image on screen with retries and click it."""
    for attempt in range(max_retries):
        try:
            location = pyautogui.locateCenterOnScreen(image_name, confidence=CONFIDENCE_LEVEL)
            if location is not None:
                click_x = location.x + offset_x
                click_y = location.y + offset_y
                pyautogui.click(x=click_x, y=click_y)
                
                # Move cursor down to break hover state without triggering top-left FAILSAFE
                pyautogui.move(0, 100)
                return True
        except pyautogui.ImageNotFoundException:
            pass 
        time.sleep(delay_between_retries)
    
    print(f"\n[ERROR] Template '{image_name}' not found on screen.")
    return False

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    # Verify executable existence
    if not os.path.exists(DS_BIN) and not shutil.which(DS_BIN):
        print(f"[ERROR] Discovery Studio executable not found at: {DS_BIN}")
        print("Please update 'DS_BIN' or set the 'DS_BIN_PATH' environment variable.")
        return

    complex_files = glob.glob(os.path.join(BASE_DIR, "*_complex_interaction", "protein_*_complex.pdb"))

    if not complex_files:
        print(f"[WARNING] No complex files found under '{BASE_DIR}'. Check directory structure.")
        return

    print(f"Found {len(complex_files)} complex files to process.")
    print("Starting process in 4 seconds. Switch to your working workspace if needed...")
    time.sleep(4)

    # Launch Discovery Studio
    print(f"Launching Discovery Studio: {DS_BIN}")
    subprocess.Popen([DS_BIN])
    time.sleep(15) 

    for pdb_path in complex_files:
        pdb_path = os.path.abspath(pdb_path)
        filename = os.path.basename(pdb_path)
        full_lig_name = filename.replace("protein_", "").replace("_complex.pdb", "")
        png_path = os.path.abspath(os.path.join(os.path.dirname(pdb_path), f"{full_lig_name}_interaction_map.png"))
        
        print(f"\nProcessing: {full_lig_name}")
        
        # 1. Open File
        pyautogui.hotkey('ctrl', 'o')
        time.sleep(1.5)
        pyperclip.copy(pdb_path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(6) 
        
        # 2. Switch to Interactions Tab
        if not click_on_image('interactions_tab.png'):
            print("[ABORT] Interactions tab not found.")
            break
        time.sleep(1)

        # 3. Define Receptor
        if not click_on_image('define_receptor_anchor.png', offset_y=30):
            print("[ABORT] Could not define receptor.")
            break 
        time.sleep(1)
        
        # 4. Open Hierarchy Panel and Select Ligand
        pyautogui.hotkey('ctrl', 'h')
        time.sleep(1.5)
        
        try:
            ligand_loc = pyautogui.locateCenterOnScreen('ligand_icon.png', confidence=CONFIDENCE_LEVEL)
            if ligand_loc is None:
                raise pyautogui.ImageNotFoundException
            pyautogui.doubleClick(ligand_loc)
        except pyautogui.ImageNotFoundException:
            print("[ABORT] Ligand icon not found in hierarchy panel.")
            break
        time.sleep(1)
        
        # 5. Define Ligand
        if not click_on_image('define_ligand_btn.png'):
            print("[ABORT] Define ligand button not found.")
            break
        time.sleep(1)
        
        # 6. Generate 2D Diagram
        if not click_on_image('show_2d_btn.png'):
            print("[ABORT] Show 2D Diagram button not found.")
            break
        time.sleep(4) 
        
        # 7. Export PNG (Custom shortcut: Ctrl+Shift+S)
        pyautogui.hotkey('ctrl', 'shift', 's')
        time.sleep(1.5)
        
        pyperclip.copy(png_path)
        
        # Clear default text buffer
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('backspace')
        time.sleep(0.2)
        
        # Paste output path and confirm Save As
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        
        # Wait for and confirm 'Save Image' dialog (Pixels/Dimensions)
        time.sleep(1.5) 
        pyautogui.press('enter')
        time.sleep(2)  # Allow buffer write to disk
        
        # 8. Close Tabs (Discard changes)
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(1)
        pyautogui.hotkey('alt', 'n') 
        time.sleep(1)
        
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(1)
        pyautogui.hotkey('alt', 'n') 
        time.sleep(1)

    print("\nBatch processing completed successfully.")

if __name__ == "__main__":
    main()
