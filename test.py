from twDAO import truckwashDAO as DAO
import pandas as pd

def test1():
    df=pd.DataFrame(DAO.getWashSum())
    #print(df)
    import calendar

    # Convert 'Rate' column to float
    df['Rate'] = df['Rate'].astype(float)

    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract Year and Month from 'Date'
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # Map month numbers to month names
    df['Month'] = df['Month'].apply(lambda x: calendar.month_name[x])

    # Group by 'Year', 'Month', and 'Customer', and aggregate 'Rate'
    summary_df = df.groupby(['Year', 'Month', 'Customer'])['Rate'].sum().reset_index()
    print(DAO.getWashSum())

def test2():
    df=pd.DataFrame(DAO.getWashSumMonth())
    print(df)

test2()



