import random 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
methylation_values = [round(random.random(), 10) for _ in range(100)]
# methylation_values = [0.8, 0.2, 0.9, 0.1, 0.75, 0.4, 0.6, 0.3, 0.88, 0.05]
df = pd.DataFrame(methylation_values, columns=["Site_Score"])

avg = df['Site_Score'].mean()

above_avg = df[df['Site_Score'] > avg]

sortedtable = df.sort_values(by='Site_Score', ascending=False)

print("Average: ", avg)
print("Above Average: ", above_avg)
print(sortedtable)


plt.hist(df['Site_Score'], bins=10, color='skyblue', edgecolor='black')
plt.title("Distribution of Methylation Scores")
plt.xlabel("Methylation Level (0 to 1)")
plt.ylabel("Number of Sites")

plt.show()

'''
# 1. Create two empty lists: high_sites and low_sites
high_sites = []
low_sites = []
not_binded = []

# 2. Loop through methylation_values
for x in methylation_values:
    if x>0.7:
        high_sites.append(x)
    elif x<0.3:
        low_sites.append(x)
    else:
        not_binded.append(x)

high_sites_total_sum = sum(high_sites)
low_sites_total_sum = sum(low_sites)

high_sites_number_items = len(high_sites)
low_sites_number_items = len(low_sites)

average_high = round((high_sites_total_sum / high_sites_number_items)*100)/100
average_low = round((low_sites_total_sum / low_sites_number_items)*100)/100


for i in range(high_sites_number_items):
     hmin_index = i

     for j in range(i+1, high_sites_number_items):
         if high_sites[j]<high_sites[hmin_index]:
             hmin_index = j
             
     high_sites[i], high_sites[hmin_index] = high_sites[hmin_index], high_sites[i]

for k in range(low_sites_number_items):
     lmin_index = k

     for l in range(k+1, low_sites_number_items):
         if low_sites[l]<low_sites[lmin_index]:
             lmin_index = l
             
     low_sites[k], low_sites[lmin_index] = low_sites[lmin_index], low_sites[k]
    

print("High Sites ", high_sites)
print("Low Sites ", low_sites)
print("Count (high): ", high_sites_number_items)
print("Count (Low): ", low_sites_number_items)
print("Unsorted: ", len(not_binded))
print("Average (high): ", average_high)
print("Average (Low): ", average_low)
'''