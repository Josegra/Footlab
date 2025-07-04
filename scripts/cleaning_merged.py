
import pandas as pd
import os

df = pd.read_csv("https://raw.githubusercontent.com/Josegra/Footlab/refs/heads/main/data/all_leagues_stats.csv")

df = df[df['Pos'] != 'GK']

df['Pos'].value_counts()

"""#### Replace positions and add primary and secondary positions"""

pos_map = {
    'DF': 'Defender',
    'MF': 'Midfielder',
    'FW': 'Forward',
    'GK': 'Goalkeeper'  # por si aparece
}

# Corregir errores como 'FW,D' antes de reemplazar
df['Pos'] = df['Pos'].str.replace(r'\bD\b', 'DF', regex=True)

# Reemplazar abreviaturas por nombres completos
def expand_positions(pos_str):
    parts = pos_str.split(',')
    full_parts = [pos_map.get(p.strip(), p.strip()) for p in parts]
    return ','.join(full_parts)

df['Pos'] = df['Pos'].apply(expand_positions)

# Crear columnas de posición primaria y secundaria
df['primary_pos'] = df['Pos'].apply(lambda x: x.split(',')[0])
df['secondary_pos'] = df['Pos'].apply(lambda x: x.split(',')[1] if ',' in x else None)

df['secondary_pos'].value_counts()

"""#### Replace nations names"""

nation_mapping = {
    'ENG': 'England', 'ESP': 'Spain', 'IRL': 'Ireland', 'FRA': 'France', 'MAR': 'Morocco',
    'ALG': 'Algeria', 'EGY': 'Egypt', 'TUN': 'Tunisia', 'KSA': 'Saudi Arabia', 'DEN': 'Denmark',
    'BRA': 'Brazil', 'ITA': 'Italy', 'NGA': 'Nigeria', 'SCO': 'Scotland', 'USA': 'USA',
    'AUT': 'Austria', 'GER': 'Germany', 'CIV': 'Ivory Coast', 'MNE': 'Montenegro', 'SUI': 'Switzerland',
    'SWE': 'Sweden', 'GHA': 'Ghana', 'NOR': 'Norway', 'ROU': 'Romania', 'NED': 'Netherlands',
    'ARG': 'Argentina', 'PAR': 'Paraguay', 'GAB': 'Gabon', 'POR': 'Portugal', 'MEX': 'Mexico',
    'SEN': 'Senegal', 'PAN': 'Panama', 'PUR': 'Puerto Rico', 'JAM': 'Jamaica', 'URU': 'Uruguay',
    'VEN': 'Venezuela', 'HAI': 'Haiti', 'ISL': 'Iceland', 'JPN': 'Japan', 'ALB': 'Albania',
    'COL': 'Colombia', 'TOG': 'Togo', 'GUI': 'Guinea', 'CRO': 'Croatia', 'SLE': 'Sierra Leone',
    'CAN': 'Canada', 'COD': 'Congo (DR)', 'CMR': 'Cameroon', 'HUN': 'Hungary', 'ZAM': 'Zambia',
    'CZE': 'Czech Republic', 'BEL': 'Belgium', 'SUR': 'Suriname', 'POL': 'Poland', 'SVK': 'Slovakia',
    'GNB': 'Guinea-Bissau', 'SVN': 'Slovenia', 'MLI': 'Mali', 'NIR': 'Northern Ireland', 'SRB': 'Serbia',
    'CHI': 'Chile', 'WAL': 'Wales', 'AUS': 'Australia', 'NZL': 'New Zealand', 'ECU': 'Ecuador',
    'TUR': 'Turkey', 'GAM': 'Gambia', 'CGO': 'Congo', 'BAN': 'Bangladesh', 'EQG': 'Equatorial Guinea',
    'CPV': 'Cape Verde', 'GEO': 'Georgia', 'BIH': 'Bosnia and Herzegovina', 'BFA': 'Burkina Faso',
    'GRE': 'Greece', 'UKR': 'Ukraine', 'MKD': 'North Macedonia', 'CRC': 'Costa Rica', 'MAS': 'Malaysia',
    'LTU': 'Lithuania', 'RUS': 'Russia', 'DOM': 'Dominican Republic', 'IRQ': 'Iraq', 'KOR': 'South Korea',
    'PHI': 'Philippines', 'BEN': 'Benin', 'IDN': 'Indonesia', 'FIN': 'Finland', 'ZIM': 'Zimbabwe',
    'ISR': 'Israel', 'CYP': 'Cyprus', 'UZB': 'Uzbekistan', 'ANG': 'Angola', 'CTA': 'Central African Republic',
    'GLP': 'Guadeloupe', 'MAD': 'Madagascar', 'PER': 'Peru', 'MOZ': 'Mozambique', 'EST': 'Estonia',
    'ARM': 'Armenia', 'KVX': 'Kosovo', 'LBY': 'Libya', 'BDI': 'Burundi', 'KEN': 'Kenya',
    'COM': 'Comoros', 'MDA': 'Moldova', 'GUF': 'French Guiana', 'MTQ': 'Martinique', 'MSR': 'Montserrat',
    'LUX': 'Luxembourg', 'JOR': 'Jordan', 'IRN': 'Iran', 'MLT': 'Malta', 'CUW': 'Curaçao',
    'PLE': 'Palestine', 'BUL': 'Bulgaria', 'BOE': 'Bonaire', 'CUB': 'Cuba', 'BLR': 'Belarus',
    'RSA': 'South Africa', 'AND': 'Andorra', 'LBR': 'Liberia', 'THA': 'Thailand', 'SYR': 'Syria',
    'RWA': 'Rwanda', 'UGA': 'Uganda', 'HON': 'Honduras', 'GUA': 'Guatemala', 'GUY': 'Guyana',
    'TRI': 'Trinidad and Tobago', 'SLV': 'El Salvador', 'GRN': 'Grenada', 'NAM': 'Namibia', 'BER': 'Bermuda'
}
df['Nation'] = df['Nation'].replace(nation_mapping)

"""#### Merge with Salaries"""

df.shape

salaries = pd.read_csv("https://raw.githubusercontent.com/Josegra/Footlab/refs/heads/main/data/salaries.csv")

# Define las ligas que forman parte del Big 5
big5_leagues = ['Bundesliga', 'La Liga', 'Serie A', 'Premier League', 'Ligue']

# Filtra solo los de Big 5
df_big5 = df[df['Comp'].isin(big5_leagues)]

# Merge solo para Big 5
df_big5_merged = pd.merge(
    df_big5,
    salaries[['Weekly Wages', 'Annual Wages', 'Notes', 'Player']],
    on='Player',
    how='left'
)

# Dejar solo una fila por jugador con el salario más alto
salaries_clean = salaries.sort_values(by='Annual Wages', ascending=False).drop_duplicates(subset='Player')

# Hacer merge con df_big5
df_big5_merged = pd.merge(
    df_big5,
    salaries_clean[['Player', 'Weekly Wages', 'Annual Wages', 'Notes']],
    on='Player',
    how='left'
)

df.shape

# Dejar solo una fila por jugador con el salario más alto
salaries_clean = salaries.sort_values(by='Annual Wages', ascending=False).drop_duplicates(subset='Player')

# Hacer merge con df_big5
players_merged_salaries = pd.merge(
    df,
    salaries_clean[['Player', 'Weekly Wages', 'Annual Wages', 'Notes']],
    on='Player',
    how='left'
)

players_merged_salaries.shape

"""#### Merge with Transfermarkt"""

transfermarkt = pd.read_csv("https://raw.githubusercontent.com/Josegra/Footlab/refs/heads/main/players.csv")

transfermarkt.columns

from unidecode import unidecode

players_merged_salaries['player_code'] = (
    players_merged_salaries['Player'].apply(
        lambda x: unidecode(str(x).lower().strip().replace("'", "").replace(" ", "-"))
        if pd.notnull(x) and str(x).strip() else None
    ) if 'Player' in players_merged_salaries.columns else pd.Series(dtype='object')
)
# df_maestro['player_code'] = (
#     df_maestro['Player'].apply(
#         lambda x: unidecode(str(x).lower().strip().replace("'", "").replace(" ", "-"))
#         if pd.notnull(x) and str(x).strip() else None
#     ) if 'Player' in df_maestro.columns else pd.Series(dtype='object')
# )

columnas_maestro_seleccionadas = ['player_code', 'country_of_birth',
       'city_of_birth', 'country_of_citizenship', 'date_of_birth',
       'sub_position', 'position', 'foot', 'height_in_cm',
       'contract_expiration_date', 'agent_name', 'current_club_name',
       'market_value_in_eur', 'highest_market_value_in_eur']


players_merged_salaries.loc[:, 'Player'] = players_merged_salaries['Player'].apply(lambda x: unidecode(str(x)) if pd.notnull(x) else x)
players_merged_salaries.loc[:, 'Squad'] = players_merged_salaries['Squad'].apply(lambda x: unidecode(str(x)) if pd.notnull(x) else x)

players_merged_salaries['PlSqu'] = players_merged_salaries['Player'].astype(str) + players_merged_salaries['Squad'].astype(str)
df_maestro_filtrado = transfermarkt[columnas_maestro_seleccionadas]

final_merged_df = pd.merge(players_merged_salaries,
                        df_maestro_filtrado,
                        on='player_code',
                        how='left')

final_merged_df = final_merged_df.drop_duplicates(subset='PlSqu')

# Replace Ligue for Ligue 1
final_merged_df['Comp'] = final_merged_df['Comp'].replace('Ligue', 'Ligue 1')

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_dir = os.path.join(root_dir, 'data')
os.makedirs(output_dir, exist_ok=True)
final_merged_df.to_csv(os.path.join(output_dir, 'player_stats_cleaned_2024_2025.csv'), index=False)
