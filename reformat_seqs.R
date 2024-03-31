# Load jsonlite library
library(jsonlite)

# Function to reformat a single sequence entry
reformat_sequence <- function(sequence) {
  # Extract the identifier and JSON part from the sequence
  parts <- strsplit(sub(">", "", sequence), " ", fixed = TRUE)[[1]]
  identifier <- parts[1]  # Keep the original identifier as is
  json_part <- paste(parts[-1], collapse=" ")
  
  # Parse the JSON to extract the gene ID
  json_data <- fromJSON(json_part)
  gene_id <- json_data$pub_og_id
  
  # Construct the new sequence header with the original ID, pub_gene_id, and the entire JSON
  new_header <- paste(">", paste(identifier, gene_id, json_part, sep=" "), sep="")
  return(new_header)
}

# Specify the input file name
infile <- "beetle_ogs_from_orthodb.fa"

# Use commandArgs to capture command line arguments
args <- commandArgs(trailingOnly = TRUE)
if(length(args) != 2) {
  stop("Insufficient arguments. Please provide input and output file names.")
}
infile <- args[1]  # The first argument is the input file name
outfile <- args[2]  # The second argument is the output file name

# Read the OrthoDB sequences from the file
sequences <- readLines(infile)

# Initialize a vector to hold the reformatted sequences
reformatted_sequences <- vector("character", length(sequences))

# Loop through the sequences, reformatting each one
for (i in seq_along(sequences)) {
  sequence <- sequences[i]
  if (startsWith(sequence, ">")) {
    # Process sequence headers
    reformatted_sequences[i] <- reformat_sequence(sequence)
  } else {
    # Directly add sequence data
    reformatted_sequences[i] <- sequence
  }
}

# Write the reformatted sequences to the new file
writeLines(reformatted_sequences, outfile)
