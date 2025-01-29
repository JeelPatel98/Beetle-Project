import os
import sys
from Bio import SeqIO

def modify_header(header, orthogroup):
    """
    Modify the FASTA header to match the CAPTUS format.
    - Moves species name to the beginning (if present).
    - Extracts relevant description (if present).
    - Ensures no leading underscores or empty brackets.
    """
    # Split the header into sequence name and description
    parts = header.split(maxsplit=1)
    sequence_name = parts[0]  # Example: "TRINITY_DN1046_c0_g1_i5.p1"
    description = parts[1] if len(parts) > 1 else ""  # The rest of the header (if exists)

    # Extract the necessary part of the description
    description_parts = description.split(' ')

    # Check if species name exists (last part), otherwise leave it empty
    species = ""
    if len(description_parts) > 0 and "_nostop.pep" in description_parts[-1]:
        species = description_parts[-1].replace("_nostop.pep", "")

    # Extract relevant description (excluding the species)
    relevant_description = ""
    if len(description_parts) > 2:
        relevant_description = ' '.join(description_parts[2:-1])  # Extract ORF type, score, len, etc.

    # Construct the new Sequence ID
    new_sequence_id = f"{species}_{sequence_name}" if species else sequence_name  # No leading underscore if species is missing

    # Construct final header with or without description
    new_header = f"{new_sequence_id}-{orthogroup}"
    if relevant_description:
        new_header += f" [{relevant_description}]"

    return new_header

def convert_fasta_headers(input_file, output_file, orthogroup):
    """
    Reads a FASTA file, modifies the headers using `modify_header()`, 
    and writes the updated sequences to a new file.
    """
    records = []
    for record in SeqIO.parse(input_file, "fasta"):
        new_header = modify_header(record.description, orthogroup)
        record.id = new_header.split()[0]  # Update sequence ID
        record.description = new_header  # Update description
        records.append(record)
    
    # Write all records to the output file
    with open(output_file, "w") as out_f:
        SeqIO.write(records, out_f, "fasta")

def batch_convert_fasta_files(input_folder, output_folder):
    """
    Processes all `.fasta` files in the given input folder, modifies headers, 
    and saves the modified files to the output folder.
    """
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists
    
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".fa"):  # Process only fa files
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            
            # Extract Orthogroup from the file name
            orthogroup = filename.split('.')[-2]  # Extracting 'OrthoGroupX' from the filename
            
            # Convert the file
            convert_fasta_headers(input_file_path, output_file_path, orthogroup)

if __name__ == "__main__":
    """
    Command-line execution: Provide input and output directories as arguments.
    """
    if len(sys.argv) != 3:
        print("Usage: python convert_to_captus.py <input_folder> <output_folder>")
        sys.exit(1)

    input_dir = sys.argv[1]  # Get input directory
    output_dir = sys.argv[2]  # Get output directory

    # Run batch processing
    batch_convert_fasta_files(input_dir, output_dir)

    print(f"Batch conversion complete! All converted files are saved in {output_dir}.")
