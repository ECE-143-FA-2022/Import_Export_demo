import pandas as pd

# reading in the Import Export dataset
master_df = pd.read_csv("National_Import_Export.csv")

# assembling a list of countries.
countries = master_df["country"].unique()
# This will be the string appended to the end of the relevant coumns fo which I am taking the difference of.
diff_str = "_yearly_difference"
# these are the relevant columns that I will be operating on.
columns = ["imports","exports","net(exports-imports)"]
# Since I have grown older I know that if you want to make a pandas dataframe, you should just assemble it into a dictionary first.
difference_dict = {}
# looping throught the relevant columns
for column in columns:
    # initializing the key-value string-list pair that will be used to add to the pandas dataframe.
    difference_dict[column+diff_str] = []
    # looping through the countries.
    for country in countries:
        # narrowing down the scope of the master dataframe
        country_df = master_df[master_df["country"]==country]
        # assembling a list of the relevant years that the dataset has for the current country.
        relevant_years_for_country = country_df["year"].unique()
        # I need to have a separate counter in order to make sure that I don't take a difference for the first year.
        year_count = 0
        prev_year = 0
        for year in relevant_years_for_country:
            if year_count == 0:
                year_count += 1
                difference_dict[column+diff_str].append(0.0)
                prev_year = year
                continue
            # Subtracting the value of this year from the previous year
            current_difference = country_df[country_df["year"]==year][column].iloc[0] - country_df[country_df["year"]==prev_year][column].iloc[0]
            print(country,year,current_difference)
            difference_dict[column+diff_str].append(current_difference)
            prev_year = year
            
output_df = pd.DataFrame.from_dict(difference_dict)
output_df = output_df.fillna(method="ffill")
output_df.to_csv("difference_test.csv",index=False)
