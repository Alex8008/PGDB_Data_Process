import requests
import pandas as pd
from tqdm import tqdm

n = 1  # Specify to start downloading from g000n, inclusive

# Read the CSV file
df = pd.read_csv("2.csv")

# Get the data from the second column
gene_ids = df.iloc[:, 1].tolist()

# Create a tqdm object to display the progress bar
pbar = tqdm(gene_ids[n - 1:], desc="Download Progress", unit="gene")  # Iterate from the skipped row

# Update gene name and function description directly in the DataFrame
for gene_id in pbar:
    url = f'https://rest.uniprot.org/uniprotkb/{gene_id}'
    response = requests.get(url)
    if response.ok:
        data = response.json()

        if 'genes' in data and data['genes']:
            genename = data['genes'][0]['geneName']['value'] if 'geneName' in data['genes'][0] else ' '
        else:
            genename = ' '

        if 'proteinDescription' in data and data['proteinDescription']:
            protein = ' '
            protein = data['proteinDescription']['submissionNames'][0]['fullName']['value'] if 'submissionNames' in data['proteinDescription'] else protein
            protein = data['proteinDescription']['recommendedName']['fullName']['value'] if 'recommendedName' in data['proteinDescription'] else protein
        else:
            protein = ' '

        # Process gene_name, add a vertical bar separator, no spaces
        gene_name_parts = [genename]
        gene_name = ''.join(gene_name_parts)

        df.loc[df.iloc[:, 1] == gene_id, 'gene_name'] = gene_name
        df.loc[df.iloc[:, 1] == gene_id, 'function_description'] = protein

# Close the progress bar
pbar.close()

# Save the updated DataFrame to a CSV file
df.to_csv("new_2.csv", index=False)

# Update gene_id

# Read the user-uploaded CSV file
df = pd.read_csv("new_2.csv")

# Generate a new gene_id sequence in the format g00001, g00002, ...
df['gene_id'] = [f'g{str(i).zfill(5)}' for i in range(1, len(df) + 1)]

# Save the modified DataFrame to a new CSV file
updated_file_path = 'new_2.csv'
df.to_csv(updated_file_path, index=False)
