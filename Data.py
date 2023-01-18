'''
    Data - module to hold the data used for the dashboard visualization
    Sandeep Venkataram
    Jan 2023
'''


import pandas as pd
import re
from os import path
import random

root_dir = "Input_Data/"
master_df = pd.read_table(root_dir+"Data_S1.tab", sep = "\t")
master_df.set_index(['key'], inplace=True)
mut_df = pd.read_table(root_dir+"Data_S2.tab", sep = "\t")
mut_df.set_index(['key'], inplace=True)
adaptive_locus_df = pd.read_table(root_dir+"Data_S3.tab", sep = "\t")
population_list = ["A1","A2","A3","A4","A5","C1","C2","C3","C4","C5"]
num_neutrals = 500
population_types = ["Alone","Community"]
pop_type_map = {"Alone": "A", "Community": "C"}


master_name_map = {
    'Alone_fitness': 'Alone Fitness',
    'Community_fitness': 'Community Fitness',
    'YYA_Avg_rescaled': 'Normalized Yeast Yield Alone',
    'AYC_avg_rescaled': 'Normalized Algae Yield Community',
    'YYC_avg_rescaled': 'Normalized Yeast Yield Community',
    'r_Avg_rescaled': 'Normalized Growth Rate',
    'K_Avg_rescaled': 'Normalized Carrying Capacity',
}

master_err_map = {
    'Alone_fitness': 'Alone_stderr',
    'Community_fitness': 'Community_stderr',
    'YYA_Avg_rescaled': 'YYA_Stderr_rescaled',
    'AYC_avg_rescaled': 'AYC_stderr_rescaled',
    'YYC_avg_rescaled': 'YYC_stderr_rescaled',
    'r_Avg_rescaled': 'r_Stderr_rescaled',
    'K_Avg_rescaled': 'K_Stderr_rescaled',
}


"""
    Input data has removed 1 from normalized columns, so adding that back in
"""
for col in master_name_map:
    if "Normalized" in master_name_map[col]:
        master_df[col] = master_df[col].add(1)



def get_barcodes_to_highlight(selected_clones, selected_genes):
    """ 
        Get a set of barcodes to highlight
    """
    if len(selected_clones) == 0 and len(selected_genes) == 0: #if we haven't picked anything, highlight everything
        return []
    
    if len(selected_genes) == 0: #if we haven't picked any genes, show all highlighted clones
        return selected_clones
    
    mut_subset = mut_df.loc[
        list(set(selected_clones).intersection(set(mut_df.index.tolist())))
    ]
    mut_subset = mut_subset[mut_subset['gene'].isin(selected_genes)]
    
    return mut_subset.index.to_list()

