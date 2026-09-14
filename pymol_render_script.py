import os
import glob
from pymol import cmd

# ==========================================
# CONFIGURATION & CAMERA MATRICES
# ==========================================

# Target receptor filename (must be in the working directory)
PROTEIN_FILE = "protein_clean.pdb"

# Overview camera view matrix (Generated via PyMOL 'get_view')
VIEW_OVERVIEW = (
    -0.009963626,   -0.771724463,    0.635880411,
    -0.186651126,   -0.623298347,   -0.759382129,
     0.982374787,   -0.126254112,   -0.137833059,
    -0.000013791,    0.000009904, -145.988616943,
    12.036911011,   16.755558014,   14.761597633,
  -17580.246093750, 17872.222656250,  -20.000001907
)

# Close-up camera view matrix (Generated via PyMOL 'get_view')
VIEW_CLOSEUP = (
    -0.009963626,   -0.771724463,    0.635880411,
    -0.186651126,   -0.623298347,   -0.759382129,
     0.982374787,   -0.126254112,   -0.137833059,
    -0.000030216,    0.000008561,  -60.038463593,
    11.030479431,   14.619016647,   21.891202927,
  -17666.189453125, 17786.279296875,  -20.000001907
)

# Color mapping for poses 1 through 5
LIGAND_COLORS = ["oxygen", "violet", "deepsalmon", "hotpink", "lightpink"]

# Output resolution settings
RENDER_WIDTH = 1920
RENDER_HEIGHT = 1080
RENDER_DPI = 600

# ==========================================
# RENDER PIPELINE
# ==========================================

def render_clusters():
    """Scans for docking poses, aligns with receptor, and exports ray-traced figures."""
    if not os.path.exists(PROTEIN_FILE):
        print(f"[ERROR] Target receptor '{PROTEIN_FILE}' not found in the current directory.")
        return

    # Find primary pose files (*_1_best.pdbqt) to determine molecule IDs
    ligand_1_files = sorted(glob.glob("*_1_best.pdbqt"))

    if not ligand_1_files:
        print("[WARNING] No '*_1_best.pdbqt' files found. Please verify file naming.")
        return

    print(f"Found {len(ligand_1_files)} molecule clusters to process.")

    for l1 in ligand_1_files:
        base_name = l1.replace("_1_best.pdbqt", "")
        
        # Reset session to avoid memory bloat and visual artifacts
        cmd.reinitialize()

        # Global Render Settings
        cmd.bg_color("white")
        cmd.space("cmyk")
        cmd.set("antialias", 2)
        cmd.set("ray_shadows", 1)
        cmd.set("surface_quality", 1)
        cmd.set("ray_trace_mode", 0)

        # Load and style receptor
        cmd.load(PROTEIN_FILE, "protein_clean")
        cmd.color("hydrogen", "protein_clean")
        cmd.hide("everything", "protein_clean")
        cmd.show("surface", "protein_clean")
        cmd.set("transparency", 0.4, "protein_clean")
        cmd.show("wire", "protein_clean")

        # Load replicate poses (1 to 5)
        for i in range(1, 6):
            ligand_filename = f"{base_name}_{i}_best.pdbqt"
            ligand_obj_name = f"ligand_{i}"

            if os.path.exists(ligand_filename):
                cmd.load(ligand_filename, ligand_obj_name)
                cmd.color(LIGAND_COLORS[i - 1], ligand_obj_name)
                cmd.show("sticks", ligand_obj_name)
            else:
                print(f"[INFO] Missing {ligand_filename}, skipping this pose.")

        # --- Overview Render ---
        cmd.set_view(VIEW_OVERVIEW)
        out_overview = f"{base_name}_uzak.png"
        print(f"Rendering overview ({RENDER_DPI} DPI) -> {out_overview}")
        cmd.png(out_overview, width=RENDER_WIDTH, height=RENDER_HEIGHT, dpi=RENDER_DPI, ray=1)

        # --- Close-up Render ---
        cmd.set_view(VIEW_CLOSEUP)
        out_closeup = f"{base_name}_yakin.png"
        print(f"Rendering close-up ({RENDER_DPI} DPI) -> {out_closeup}")
        cmd.png(out_closeup, width=RENDER_WIDTH, height=RENDER_HEIGHT, dpi=RENDER_DPI, ray=1)

        print(f"Cluster '{base_name}' finished.")

if __name__ == "__main__":
    print("Initializing automated PyMOL rendering pipeline...")
    render_clusters()
    print("All tasks completed.")
