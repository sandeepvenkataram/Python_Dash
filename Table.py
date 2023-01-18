'''
    Table - module to generate the tables for the Dash visualization
    Sandeep Venkataram
    Jan 2023
'''

from dash.exceptions import PreventUpdate
import pandas as pd
import Data

Hover_Columns = [   
    "gene", 
    "mutType", 
    "mutImpact", 
    "mutIsAdaptive", 
    "AAPos", 
    "AAChange", 
    "chr", 
    "pos",
    "refBase",
    "derBase",
]

Hover_Column_Map = {
    "gene" : "Gene", 
    "mutType" : "Type", 
    "mutImpact" : "Impact", 
    "mutIsAdaptive" : "Adaptive?", 
    "AAPos" : "AA Pos", 
    "AAChange" : "AA Change", 
    "chr" : "Chr.", 
    "pos" : "Nucl. Pos.", 
    "refBase" : "Reference Base", 
    "derBase" : "Derived Base", 
}

Subset_Columns = ["Gene", "Alone", "Community", "Total"]

def generate_hover_table(barcode):
    """
        Generate table of mutations for the input barcode
    """
    if barcode in Data.mut_df.index:
        my_subset = Data.mut_df.loc[
            barcode, 
            Hover_Columns,
            ]
        if type(my_subset) == pd.Series:
            my_subset = my_subset.to_frame()
        my_subset.rename(mapper = Hover_Column_Map,inplace = True, axis=1)
        return my_subset.to_dict('records')
    raise PreventUpdate

def generate_subset_table(selected_barcodes):
    """
        Given a set of selected barcodes, return a table counting mutations in adaptive loci
    """
    if len(selected_barcodes) == 0:
        selected_barcodes = list(set(Data.mut_df.index))
    
    selected_barcodes = list(set(selected_barcodes).intersection(set(Data.mut_df.loc[Data.mut_df['mutIsAdaptive']].index)))
    my_loci = Data.adaptive_locus_df['Locus']
    mut_subset = Data.mut_df.loc[selected_barcodes]
    mut_subset = mut_subset[mut_subset['gene'].isin(my_loci)]

    """ At this point, we have a set of mutations"""

    if len(mut_subset)==0: #if there are no mutations here, prevent update
        raise PreventUpdate


    """
        Generate a table of gene counts in the dataset by clone type
    """
    occur = mut_subset.groupby(["gene","CloneSource"], as_index=False)
    occur_size = occur.size()
    gene_counts = pd.pivot_table(occur_size, index = "gene", columns = "CloneSource", values = "size", fill_value = 0)

    my_columns = list(set(["Alone","Community"]).intersection(set(gene_counts.columns)))
    gene_counts['Total'] = gene_counts.loc[:,my_columns].sum(axis=1)
    gene_counts = gene_counts.loc[gene_counts["Total"] > 0]
    if "Ancestor" in gene_counts.columns:
        gene_counts.drop("Ancestor", axis=1, inplace = True)
    gene_counts.reset_index(inplace=True)
    gene_counts.rename(columns = {"gene": "Gene"},inplace=True)
    gene_counts.sort_values(["Total","Gene"],ascending=[False,True],inplace=True)

    if type(gene_counts) == pd.Series:
            gene_counts = gene_counts.to_frame()
    
    return gene_counts.to_dict('records')