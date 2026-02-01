import csv
import yaml
import os

def process_csv_to_yaml(csv_filename, output_folder="game_configs"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        with open(csv_filename, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            
            count = 0
            for row in reader:
                # Extract data
                game_name = row['name']
                app_id = row['steamappid']
                
                # Prepare YAML data structure
                yaml_data = {
                    "name": game_name,
                    "steamappid": int(app_id) if app_id.isdigit() else app_id
                }
                
                # Sanitize filename: replace spaces with underscores, remove special chars
                clean_name = "".join(c for c in game_name if c.isalnum() or c in (' ', '_')).strip()
                filename = f"{clean_name.replace(' ', '_').lower()}.yaml"
                file_path = os.path.join(output_folder, filename)
                
                # Write YAML file
                with open(file_path, 'w', encoding='utf-8') as yf:
                    yaml.dump(yaml_data, yf, default_flow_style=False, sort_keys=False)
                
                count += 1
            
            print(f"Done! Created {count} YAML files in '{output_folder}/'.")

    except FileNotFoundError:
        print(f"Error: The file '{csv_filename}' was not found.")

if __name__ == "__main__":
    # Ensure you have 'pip install pyyaml' installed
    process_csv_to_yaml('games.csv')