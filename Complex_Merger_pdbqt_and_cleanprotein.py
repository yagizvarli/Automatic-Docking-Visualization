import os
import glob
import subprocess
import shutil
import tempfile

# ==========================================
# CONFIGURATION & PATH SETTINGS
# ==========================================
PROTEIN_FILE = "protein_clean.pdb"          
LIGANDS_DIR = "."                           
OUTPUT_BASE_DIR = "Interaction_Maps"        
LIGAND_EXT = ".pdbqt"                       

# PyMOL executable path:
# 1. Checks 'PYMOL_BIN_PATH' environment variable if set.
# 2. Checks if 'pymol' is accessible globally in system PATH.
# 3. Falls back to a standard user installation path.
DEFAULT_PYMOL_PATH = os.path.expanduser("~/anaconda3/bin/pymol")
PYMOL_BIN = os.getenv("PYMOL_BIN_PATH", shutil.which("pymol") or DEFAULT_PYMOL_PATH)

# ==========================================
# MAIN EXECUTION PIPELINE
# ==========================================
def main():
    # Verify receptor existence
    if not os.path.exists(PROTEIN_FILE):
        print(f"[ERROR] Target receptor file '{PROTEIN_FILE}' not found in the current directory.")
        return

    # Verify PyMOL executable
    if not os.path.exists(PYMOL_BIN) and not shutil.which(PYMOL_BIN):
        print(f"[ERROR] PyMOL executable not found at: {PYMOL_BIN}")
        print("Please ensure PyMOL is in your PATH or set the 'PYMOL_BIN_PATH' environment variable.")
        return

    # Scan for docking poses
    ligand_files = sorted(glob.glob(os.path.join(LIGANDS_DIR, f"*{LIGAND_EXT}")))
    if not ligand_files:
        print(f"[WARNING] No files with extension '{LIGAND_EXT}' found in '{LIGANDS_DIR}'.")
        return

    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    print(f"Found {len(ligand_files)} files. Merging into complexes using: {PYMOL_BIN}")

    # Use a secure temporary file to pass commands to PyMOL headless mode
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pml", delete=False) as temp_pml:
        temp_script_path = temp_pml.name

    try:
        for idx, lig_path in enumerate(ligand_files, 1):
            full_lig_name = os.path.splitext(os.path.basename(lig_path))[0]
            base_mol_name = full_lig_name.split('_')[0]
            
            # Create target folder for molecule cluster
            complex_dir = os.path.join(OUTPUT_BASE_DIR, f"{base_mol_name}_complex_interaction")
            os.makedirs(complex_dir, exist_ok=True)
            
            complex_pdb_path = os.path.join(complex_dir, f"protein_{full_lig_name}_complex.pdb")
            
            # PyMOL batch commands
            pymol_commands = f"""
load {PROTEIN_FILE}, protein
load {lig_path}, ligand_{full_lig_name}
create complex, protein or ligand_{full_lig_name}
save {complex_pdb_path}, complex
quit
"""
            with open(temp_script_path, "w") as f:
                f.write(pymol_commands)
                
            print(f"[{idx}/{len(ligand_files)}] Building complex: {full_lig_name} -> {base_mol_name}_complex_interaction/")
            subprocess.run(
                [PYMOL_BIN, "-c", "-q", temp_script_path], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                check=False
            )

        print(f"\nSuccessfully processed and organized {len(ligand_files)} complex files into '{OUTPUT_BASE_DIR}/'.")

    finally:
        # Guarantee cleanup of temporary file even if execution is interrupted
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)

if __name__ == "__main__":
    main()
