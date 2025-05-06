#!/usr/bin/python3
import json
import os  # Import os module for file checking
from sys import argv 

def json_to_fasta(project_file):
    file = open(project_file, 'r')
    jr = json.load(file)

    output = "kunitz.fasta"
    fasta_file = open(output, "w")  # Use the output variable for consistency
    
    for entry in jr:
        if "data" in entry and "rcsb_entry_container_identifiers" in entry["data"]:
            pdb_id = entry["data"]["rcsb_entry_container_identifiers"].get("entry_id", None)
            polymer_entities = entry["data"].get("polymer_entities", [])
                
            if pdb_id and polymer_entities:
                for protein in polymer_entities:
                    entity_poly = protein.get("entity_poly", {})
                    sequence = entity_poly.get("pdbx_seq_one_letter_code_can", None)
                        
                    instances = protein.get("polymer_entity_instances", [])
                        
                    if sequence and len(instances) > 0:
                        instance_id = instances[0].get("rcsb_polymer_entity_instance_container_identifiers", {})
                        chain_id = instance_id.get("auth_asym_id", None)
                            
                        if chain_id:
                            fasta_file.write(f">{pdb_id}_{chain_id}\n")
                            fasta_file.write(sequence + "\n")

    fasta_file.close()  # Close the FASTA file
    file.close()  # Close the JSON file

    # Check if the output file exists and print the first few lines
    if os.path.isfile(output):
        print(f"{output} file exists.")
        with open(output, 'r') as f:
            for _ in range(5):  # Print the first 5 lines
                line = f.readline()
                if not line:
                    break
                print(line.strip())
    else:
        print(f"{output} file does not exist.")

if __name__ == '__main__':
    project_file = argv[1]
    json_to_fasta(project_file)
