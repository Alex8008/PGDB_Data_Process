import requests
import pandas as pd
from tqdm import tqdm

n = 1  # Specify to start downloading from g000n, inclusive

skip_rows = n - 1 

# Read the CSV file
df = pd.read_csv("new_2.csv")

# Get the data from the second column
protein_ids = df.iloc[:, 1].tolist()

# Create a tqdm object to display the progress bar
pbar = tqdm(protein_ids, desc="Download Progress", unit="protein")

# Create a new list to save the scraped protein sequences
amino_acid_sequences = []

for index, protein_id in enumerate(pbar):
    if index < skip_rows:
        # Skip the preceding rows, do not scrape
        amino_acid_sequences.append(None)
        continue
    
    url = f'https://www.uniprot.org/uniprot/{protein_id}.fasta'
    response = requests.get(url)
    if response.ok:
        data = response.text
        try:
            sequence = data[data.index('\n') + 1:].replace('\n', '')
            df.loc[df.iloc[:, 1] == protein_id, 'amino_acid_sequence'] = sequence
        except IndexError:
            print(f"Unable to process protein ID: {protein_id}")

# Close the progress bar
pbar.close()

# Save the updated DataFrame back to the original CSV file
df.to_csv("new_new_2.csv", index=False)
