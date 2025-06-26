import os
import shutil
import json

# Paths
parent_folder = os.path.dirname(__file__)
in_dir = os.path.join(parent_folder, "IN")
out_dir = os.path.join(parent_folder, "OUT")
template_dir = os.path.join(parent_folder, "Playground Template")

# Data to save
importSettings = {
    "includeDefaultPlanets": False,
    "includeDefaultHeightmaps": True,
    "includeDefaultTextures": True,
    "hideStarsInAtmosphere": True
}

spaceCenter = {
    "address": "Earth",
    "angle": 90.0,
    "position_LaunchPad": {
        "horizontalPosition": 365.0,
        "height": 26.2
    }
}

version = "1.5.10.2"

# Mappings: from IN/[x]/subfolder -> OUT/[x]/destination
mappings = [
    ["GENERATED", "Planet Data"],
    ["TEXTURES", "Texture Data"],
    ["HEIGHTMAPS", "Heightmap Data"]
]

# Scan IN directory
for folder_name in os.listdir(in_dir):
    source_path = os.path.join(in_dir, folder_name)
    if not os.path.isdir(source_path):
        continue

    target_path = os.path.join(out_dir, folder_name)
    os.makedirs(target_path, exist_ok=True)

    # Create mapped subfolders
    for _, target_subfolder in mappings:
        os.makedirs(os.path.join(target_path, target_subfolder), exist_ok=True)

    # Copy IN contents
    for src_sub, dest_sub in mappings:
        src_full = os.path.join(source_path, src_sub)
        dest_full = os.path.join(target_path, dest_sub)
        if os.path.exists(src_full):
            for file in os.listdir(src_full):
                src_file = os.path.join(src_full, file)
                if os.path.isfile(src_file):
                    shutil.copy2(src_file, os.path.join(dest_full, file))

    # Copy from Playground Template into OUT folders
    for _, dest_sub in mappings:
        template_sub = os.path.join(template_dir, dest_sub)
        dest_folder = os.path.join(target_path, dest_sub)
        if os.path.exists(template_sub):
            for file in os.listdir(template_sub):
                template_file = os.path.join(template_sub, file)
                if os.path.isfile(template_file):
                    shutil.copy2(template_file, os.path.join(dest_folder, file))

    # Write config files
    with open(os.path.join(target_path, "Import_Settings.txt"), "w") as f:
        json.dump(importSettings, f, indent=2)

    with open(os.path.join(target_path, "Space_Center_Data.txt"), "w") as f:
        json.dump(spaceCenter, f, indent=2)

    with open(os.path.join(target_path, "Version.txt"), "w") as f:
        f.write(version)
