import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import textwrap
import numpy as np

class DataCleaning:
    def __init__(self, csv):
        self.df = pd.read_csv(csv)

    def drop(self):
        #dropping
        self.df = self.df.drop(columns=[
            'Timestamp',
            'CONFORME',
            'Are you:',
            'If answered "Other", please specify:',
            'If answered "Other", please specify:.1',
            'If answered "Other", please specify:.2'
        ])

        #renewing column names kay sigig daghan space
        new_column_names = {
            'Which mall(s) do you usually visit? (ex. MOA, SM Sta. Mesa, Robinsons Manila, etc.) (Can provide more than 1)': 'malls_visited',
            'Are you a Globe user?': 'globe_user',
            'What Globe services do you currently use? (Check all that apply)': 'globe_services',
            'Have you ever visited a Globe or other telco store (like Smart, DITO, etc.)?  ': 'visited_store_bool',
            'If yes, What are your usual reasons for visiting the store? (Check all that apply)': 'visit_reasons',
            'Have you encountered any challenges or difficulties when visiting a Globe / Telco store? ': 'encountered_challenges_bool',
            'What kind of challenges/difficulties have you experienced? (Check all that apply)': 'challenges_list',
            'What can telco companies do to serve Deaf customers better? (You can choose more than one.) ': 'suggested_improvements',
            'Have you ever met a Deaf staff working in mall stores?': 'met_deaf_staff_bool',
            'How would you feel if you saw Deaf people working at a Globe or telco store? ': 'feeling_about_deaf_staff',
            'Do you think having Deaf employees in stores can help Deaf and hard-of-hearing customers communicate better? ': 'believes_deaf_staff_help_bool',
            'Would you like to work for a telco company in the future? ': 'interest_in_working_bool',
            'Any other comments or suggestions for Globe or other telco companies? ': 'comments'
        }



        self.df.rename(columns=new_column_names, inplace=True)



        return self.df

    def indiv(self):

        results = {}

        if 'malls_visited' in self.df.columns:

            split_malls = self.df['malls_visited'].str.split(r'\s*,\s*|\s*&\s*|\s*/\s*|\s+and\s+|\s+AND\s+', regex=True)
            individual_malls = split_malls.explode().str.strip().str.lower()

            junk_answers = ['my apartment', 'csb', 'somewhere', 'malls', 'more', 'e', 'nan', 'none', '']
            individual_malls = individual_malls[~individual_malls.isin(junk_answers)]

            individual_malls = individual_malls.dropna()

            rename_map = {
                'moa': 'SM Mall of Asia',
                'sm moa': 'SM Mall of Asia',
                'mall of asia': 'SM Mall of Asia',
                'sm mall of asia': 'SM Mall of Asia',
                'sm megamall': 'SM Megamall',
                'megamall': 'SM Megamall',
                'megamll': 'SM Megamall',
                'sm mega mall': 'SM Megamall',
                'sm north': 'SM North EDSA',
                'sm north edsa': 'SM North EDSA',
                'robinsons manila': 'Robinsons Manila',
                'rob manila': 'Robinsons Manila'
            }

            results['malls'] = individual_malls.replace(rename_map).value_counts().head(10)

        if 'suggested_improvements' in self.df.columns:
            split_serve = self.df['suggested_improvements'].str.split(r',\s*', regex=True)
            individual_serve = split_serve.explode().str.strip().dropna()

            results['serve'] = individual_serve.value_counts()

        if 'challenges_list' in self.df.columns:
            split_challenges = self.df['challenges_list'].str.split(r',\s*', regex=True)
            individual_challenges = split_challenges.explode().str.strip().dropna()

            results['challenges'] = individual_challenges.value_counts()

        return results

    def yes_data(self):

        yes_df = self.df[self.df['globe_user'].str.lower() == 'yes'].copy()

        # 2. Split the services by commas, 'and', slashes, etc.
        split_gser = yes_df['globe_services'].str.split(r'\s*,\s*|\s*&\s*|\s*/\s*|\s+and\s+|\s+AND\s+', regex=True)

        # 3. Explode into individual rows, strip whitespace, and make lowercase
        ind_gser = split_gser.explode().str.strip().str.lower()

        # 4. Remove the junk words and drop NAs
        junk = ['data', 'wifi at home', 'pldt wifi']
        ind_gser = ind_gser[~ind_gser.isin(junk)]
        ind_gser = ind_gser.dropna()

        # 4. Count up the most popular services
        service_counts = ind_gser.value_counts().head(10)

        # 5. Return a dictionary containing both the dataframe AND the counts
        return {
            'dataframe': yes_df,
            'service_counts': service_counts
        }