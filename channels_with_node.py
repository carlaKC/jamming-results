import json
import sys

def find_channels_with_alias(file_path, alias):
    with open(file_path, "r") as file:
        data = json.load(file)
    
    channels = []
    
    for channel in data.get("sim_network", []):
        node_1, node_2 = channel["node_1"], channel["node_2"]
        scid = channel["scid"]
        
        if node_1["alias"] == alias:
            channels.append(f"{alias} -> {node_2['alias']}: {scid}")
        elif node_2["alias"] == alias:
            channels.append(f"{alias} -> {node_1['alias']}: {scid}")
    
    for entry in channels:
        print(entry)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <alias>")
        sys.exit(1)
    
    file_path, alias = sys.argv[1], sys.argv[2]
    find_channels_with_alias(file_path, alias)
