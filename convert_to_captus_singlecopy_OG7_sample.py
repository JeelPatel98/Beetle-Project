import os
import sys
from Bio import SeqIO

def modify_header(header, orthogroup):
    # Split the header into sequence name and description
    parts = header.split(maxsplit=1)
    sequence_name = parts[0]  # TRINITY_DN1046_c0_g1_i5.p1
    description = parts[1] if len(parts) > 1 else ""  # The rest of the header
    
    # Extract the necessary part of the description excluding the species part
    description_parts = description.split(' ')
    relevant_description = ' '.join(description_parts[2:-1])  # Extract the ORF type, score, len, and coordinates, exclude the last part (species)

    # Extract species name by removing '_nostop.pep'
    species = description_parts[-1].replace('_nostop.pep', '')  # apiarius
    
    # Construct the new Sequence ID with species at the beginning
    new_sequence_id = f"{species}_{sequence_name}"
    
   # Format the new header as required by CAPTUS 
    new_header = f"{new_sequence_id}-{orthogroup} [{relevant_description}]"
    
    return new_header

def convert_fasta_headers(input_file, output_file, orthogroup):
    records = []
    for record in SeqIO.parse(input_file, "fasta"):
        # Modify the header
        new_header = modify_header(record.description, orthogroup)
        record.id = new_header.split()[0]  # Update the record ID
        record.description = new_header  # Set the new header as description
        records.append(record)
    
    # Write all records to the output file using SeqIO.write()
    with open(output_file, "w") as out_f:
        SeqIO.write(records, out_f, "fasta")

def batch_convert_fasta_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".fasta"):  # Check if the file is a FASTA file
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            
            # Extract Orthogroup from the file name
            orthogroup = filename.split('.')[-2]  # Extracting 'OrthoGroupX' from the filename
            
            # Convert the file
            convert_fasta_headers(input_file_path, output_file_path, orthogroup)
            

if __name__ == "__main__":
    # Get input and output directories from command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_folder> <output_folder>")
        sys.exit(1)

    input_dir = sys.argv[1]  # Get the input directory path
    output_dir = sys.argv[2]  # Get the output directory path
    
    # Run the batch conversion
    batch_convert_fasta_files(input_dir, output_dir)

    print(f"Batch conversion complete! All converted files are saved in {output_dir}.")
