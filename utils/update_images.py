import json
import os

def update_image_paths(json_file_path, output_file_path=None):
    # Load the JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # The root key is "arbol"
    if "arbol" not in data:
        print("Error: JSON structure is invalid. Root key 'arbol' not found.")
        return

    # Iterate through each branch in the tree
    for branch in data["arbol"]:
        branch_id = branch.get("id")
        opciones = branch.get("opciones", [])

        if not branch_id:
            continue

        print(f"Updating images for branch: {branch_id}")

        # Iterate through options and update the 'imagen' property
        for i, option in enumerate(opciones, start=1):
            # Using .jpg as the default extension as per user example
            # If the user wants to keep original extension, we'd need more logic,
            # but the request specified "i" as the iteration.
            new_path = f"/imgs/{branch_id}/{i}.jpg"
            option["imagen"] = new_path

    # Save the updated data
    save_path = output_file_path if output_file_path else json_file_path
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully updated and saved to: {save_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    input_json = "arbol_conocimiento.json"
    # You can specify a different output path if you don't want to overwrite the original
    # e.g., update_image_paths(input_json, "arbol_conocimiento_updated.json")
    update_image_paths(input_json)
