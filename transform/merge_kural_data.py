# /transform/merge_kural_data.py
# This script flattens the detail.json file and adds "paal" and "adhikaram" metadata fields to each kural.

import json

# configuration
# Define the names of input and output files
DETAILS_FILE_PATH = 'json/detail.json'
KURAL_FILE_PATH = 'json/thirukkural.json'
UNIFIED_OUTPUT_FILE_PATH = 'json/thirukkural_data.json'

def create_kural_lookup(details_data: dict) -> dict:
    """
    Parses the complex, nexted details JSON and creates a simple lookup dictionary
    mapping each kural number to its details
    """

    print("Flattening the heierarchical details data...")
    lookup_table = {}

    # The top-level JSON is a list with one item
    for paal in details_data[0]["section"]["detail"]:
        for iyal in paal["chapterGroup"]["detail"]:
            for adhikram in iyal["chapters"]["detail"]:
                # For each chapter, create an entry for every kural number in its range
                for kuram_num in range(adhikram["start"], adhikram["end"] + 1):
                    lookup_table[kuram_num] = {
                        "kural_number": kuram_num,
                        "paal_name_tamil": paal["name"],
                        "paal_translation_english": paal["translation"],
                        "adhikaram_name_tamil": adhikram["name"],
                        "adhikaram_translation_english": adhikram["translation"]
                    }

    return lookup_table


def main():
    """
    Main function to read the details and kural files, merge them, and write the output.
    """
    # Read the details JSON file
    with open(DETAILS_FILE_PATH, 'r', encoding='utf-8') as details_file:
        details_data = json.load(details_file)

    # Read the kural JSON file
    with open(KURAL_FILE_PATH, 'r', encoding='utf-8') as kural_file:
        kural_data = json.load(kural_file)

    # Create a lookup table for kural details
    kural_details_lookup = create_kural_lookup(details_data)

    # Merge the kural data with the lookup table
    print("Merging kural data with metadata...")
    for kural in kural_data["kural"]:
        kural_number = kural.get("Number")

        # Check if kural number exists in our lookup table
        if kural_number in kural_details_lookup:
            # Get the details from the lookup table
            details_to_add = kural_details_lookup[kural_number]
            # Merge the details into the kural dictionary
            kural.update(details_to_add)

    # Write the merged data to the output file
    print(f"Writing merged data to {UNIFIED_OUTPUT_FILE_PATH}...")
    with open(UNIFIED_OUTPUT_FILE_PATH, 'w', encoding='utf-8') as output_file:
        json.dump(kural_data, output_file, ensure_ascii=False, indent=4)

    print("Merging completed successfully!")    
    print("The new file contains kural data with metadata fields 'paal' and 'adhikaram'.")

if __name__ == "__main__":
    main()
