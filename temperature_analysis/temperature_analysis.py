import pandas as pd
import matplotlib.pyplot as plt


temperature = pd.read_csv('Average_Temperature_1900-2023.csv')

print(temperature.head())
print(temperature.isnull().sum())
print(temperature.duplicated().sum())

temperature['Average_Celsius_Temperature'] = ((temperature['Average_Fahrenheit_Temperature'] - 32) * 5/9).round(1)

temperature.to_csv('processed_data.csv', index=False)

plt.figure(figsize=(12, 6))
plt.plot(temperature.Year, temperature.Average_Celsius_Temperature)
plt.title('Temperature change during the years 1900-2023')
plt.xlabel('Year')
plt.ylabel('Celsius Temperature')
plt.show()

temperature['Smoothed_Temperature'] = temperature['Average_Celsius_Temperature'].rolling(window=10).mean()

plt.plot(temperature['Year'], temperature['Smoothed_Temperature'], label='Smoothed')
plt.plot(temperature['Year'], temperature['Average_Celsius_Temperature'], alpha=0.5, label='Original')
plt.xlabel('Year')
plt.ylabel('Average temperature')
plt.title('Average temperature dynamics over 100 years')
plt.legend()
plt.show()

plt.hist(temperature['Average_Celsius_Temperature'], bins=20, edgecolor='black')
plt.xlabel('Average temperature')
plt.ylabel('Number of years')
plt.title('Distribution of average temperature for 100 years')
plt.show()

plt.scatter(temperature['Year'], temperature['Average_Celsius_Temperature'],
            c=temperature['Average_Celsius_Temperature'], cmap='viridis', s=50)
plt.colorbar(label='Average temperature')
plt.xlabel('Year')
plt.ylabel('Average temperature')
plt.title('Dynamics of average temperature changes over 100 years')
plt.show()
