import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Argument parser
parser = argparse.ArgumentParser(description='Generate admixture plots.')
parser.add_argument('--fam', type=str, help='Path to the FAM file.')
parser.add_argument('--Q', type=str, help='Path to the Q file.')
parser.add_argument('--df_csv', type=str, help='Output CSV file name.')
parser.add_argument('--out_pdf', type=str, help='Output PDF file name.')
args = parser.parse_args()

# Read in fam file as dataframe
df_fam = pd.read_csv(args.fam, delim_whitespace=True, header=None)

# Read in the Q file, which is also whitespace delimited
df_q = pd.read_csv(args.Q, delim_whitespace=True, header=None)

# Sample IDs are in the second column of the fam file
sample_ids = df_fam[1].tolist()

# Add column names to the Q dataframe
names = ["pop{}".format(i) for i in range(1, df_q.shape[1] + 1)]
df_q.columns = names

# Insert the sample IDs into the first column position
df_q.insert(0, 'Sample', sample_ids)

# Insert population labels from the fam file as the first column
df_q.insert(0, 'Pop_Label', df_fam[0])

# Sort the rows alphabetically by population labels
df_q.sort_values('Pop_Label', inplace=True)

# Set the dataframe index to the sample IDs
df_q.set_index('Sample', inplace=True)

# Assign each individual to a population based on the highest proportion of ancestry
# Exclude non-numeric columns (Pop_Label, Sample) when finding the max value
if 'Sample' in df_q.columns:
    df_q['assignment'] = df_q.drop(['Pop_Label', 'Sample'], axis=1).idxmax(axis=1)
else:
    df_q['assignment'] = df_q.drop(['Pop_Label'], axis=1).idxmax(axis=1)

# Set the color palette
pal = sns.color_palette(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1b9e77', '#e7298a', '#66a61e', '#e6ab02', '#a6761d'])

# Create the stacked bar plot
ax = df_q.plot.bar(stacked=True,
                   figsize=(25, 5),
                   width=1,
                   color=pal,
                   fontsize='x-small',
                   edgecolor=None)  # Remove the default edgecolor

# Clean up the plot
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xticks([])
ax.set_xlabel('')
ax.legend(bbox_to_anchor=(1, 1), fontsize='medium', labelspacing=0.5, frameon=False)

# Set Y-axis scale
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])

# Ensure that df_q is sorted based on the order of df_fam
df_fam_sorted = df_fam.set_index(1).loc[df_q.index].reset_index()

# Calculate the position for each population label
pop_labels = df_fam_sorted[0].unique()
pop_label_positions = {}
pop_label_boundaries = []
for pop_label in pop_labels:
    indices = df_fam_sorted[df_fam_sorted[0] == pop_label].index
    center_index = (indices[0] + indices[-1]) / 2
    pop_label_positions[pop_label] = center_index
    pop_label_boundaries.append(indices[-1] + 0.5)

# Adjust plot margins to make space for the labels
plt.subplots_adjust(bottom=0.2)

# Place population labels below the center of the group of bars for each pop label
for pop_label, center_index in pop_label_positions.items():
    ax.text(center_index, -0.05, pop_label, ha='center', va='top', fontsize=6, rotation=90, transform=ax.get_xaxis_transform())

# Add black lines between different population labels
for boundary in pop_label_boundaries:
    ax.vlines(x=boundary, ymin=0, ymax=1, color='black', linewidth=0.5)

# Add a black line on Y-axis at x = -0.5 with the calculated height
ax.axvline(x=-0.5, ymin=0, ymax=0.95121, color='black', linewidth=0.5)

# Display the value of K at the top of the plot
K = df_q.shape[1] - 2  # Subtracting 2 to exclude 'Pop_Label' and 'assignment'
ax.text(0.5, 1.1, f'K = {K}', ha='center', va='center', fontsize=14, transform=ax.transAxes)

# Save the plot
ax.figure.savefig(args.out_pdf, bbox_inches='tight')

# Save the sorted Q dataframe
df_q.to_csv(args.df_csv, sep=",", index=True, float_format='%.6f')

plt.show()