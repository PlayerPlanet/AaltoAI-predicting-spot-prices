import pandas as pd
import json

# Load the CSV file
csv_file = 'tuulivoimalat.csv'  # Replace with your file name
df = pd.read_csv(csv_file)

# Sort by 'Vuosi' (Year Built) in ascending order to calculate cumulative totals
df = df.sort_values(by='Vuosi')

# Prepare a dictionary to hold the final JSON data
result = {}

# Initialize cumulative data
cumulative_data = {}

for year in sorted(df['Vuosi'].unique()):  # Loop through each unique year
    # Convert year to native Python type (str or int) to avoid JSON encoding issues
    year = int(year)
    
    # Filter data up to and including the current year
    data_up_to_year = df[df['Vuosi'] <= year]
    
    # Calculate total power (p_t) up to this year
    total_power = data_up_to_year['Teho'].sum()
    
    # Calculate power per municipality (p_m) up to this year
    power_by_municipality = data_up_to_year.groupby('Kunta')['Teho'].sum()
    
    # Create a list of municipalities with their power and percentage
    municipalities = []
    for municipality, power in power_by_municipality.items():
        percentage = round((power / total_power) * 100, 2)
        municipalities.append({
            "name": municipality,
            "power": power,
            "percentage": percentage
        })
    
    # Store the results for this year
    result[year] = {  # 'year' is now a native Python int
        "total_power": total_power,
        "municipalities": municipalities
    }

# Save the result to a JSON file
output_file = 'tuulivoimalat.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)  # Preserve Finnish characters

print(f"JSON file '{output_file}' created successfully!")
