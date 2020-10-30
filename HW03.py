import numpy as np
import pandas as pd

from pprint import pprint

def critic_rater(name, critic_score,  threshold):
    return [name[i] for i in range(len(critic_score)) if critic_score[i] >= threshold]

def missing_data(user_score, critic_score):
    return sum(np.isnan(np.concatenate((user_score, critic_score), axis = 0)))
    
def purchase_games(name, price, tax, quantity, budget):
    return [name[i] for i in range(len(price)) if (price[i] * (1 + tax[i]) * quantity) <= budget]

# name = np.array(['Minecraft', 'Animal Crossing', 'Breath of the Wild', 'Genshin Impact', 'Tetris', 'The Last of Us II'])
# price = np.array([14.99, 24.99, 39.99, 0.99, 0.49, 59.99])
# tax = np.array([0.01, 0.07, 0.05, 0.09, 0.1, 0.07])

# purchase_games(name, price, tax, 2, 59.99)


def developer_validator(developer, publisher):
    return np.where((developer == publisher),'valid', 'invalid')

# developer = np.array(['Nintendo', 'Treyarch', 'Infinity Ward', 'Ubisoft', 'Capcom'])
# publisher = np.array(['Nintendo', 'Microsoft Games', 'Activision', 'Ubisoft', 'Nintendo'])
# developer_validator(developer, publisher)

def csv_parser(filename):
    return pd.read_csv(filename + '.csv')


# df = csv_parser("video_games")
# df.head()
    
def critic_grade(df):
    
    df['Critic_Grade'] = df.apply(lambda x: 'N' if pd.isnull(x.Critic_Score) else ('A' if x.Critic_Score >= 90 else ('B' if 90 > x.Critic_Score >= 80 else ('C' if 80 > x.Critic_Score >= 70 else ('F')))), axis=1) 

    return df

# df = csv_parser("video_games")
# df = critic_grade(df) 
# df[['Name', 'Critic_Score', 'Critic_Grade']].head()


def publisher_sales(df):
    
    n_df = df[['Publisher', 'Global_Sales', 'User_Count']]

    s_n_df = n_df.groupby(['Publisher']).sum()
    s_n_df.loc['Total']= s_n_df.sum(numeric_only=True, axis=0)
    
    # Rounding all values to 2 decimal places:
    s_n_df = s_n_df.round(decimals=2)
    
    return s_n_df

# df = csv_parser("video_games")
# publisher_sales(df)
    

def platform_stats(df):
    
    n_df = df[['Platform', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales', 'Critic_Score']]

    s_n_df = n_df.groupby(['Platform']).agg({'NA_Sales':'sum', 'EU_Sales':'sum','JP_Sales':'sum', 'Other_Sales':'sum', 'Global_Sales':'sum', 'Critic_Score':'mean'}).round(decimals=2)
    
    r_df = s_n_df.sort_values(by = 'Global_Sales', ascending = False) 
    
    return r_df
    
# df = csv_parser("video_games")
# df = platform_stats(df)
# df.head()
    

def popular_developer(df, year):
    
    n_df = df[['Developer', 'Critic_Score', 'User_Score']]
    
    r = n_df.copy()
    
    r['Average_Score'] = n_df.apply(lambda row: ((row.User_Score * 10) + row.Critic_Score) / 2, axis =1)
   
    mask = df['Year_of_Release'] == int(year)

    i = r[mask]
    
    i=i.groupby(['Developer']).max()
    
    return i
    
    
df = csv_parser("video_games")
popular_developer(df, 2008)

