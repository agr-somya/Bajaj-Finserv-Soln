#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json


# In[2]:


file_path = r'C:\Users\somya\OneDrive\Desktop\DataEngineeringQ2.json'
with open(file_path, 'r') as file:  # Use 'r' mode explicitly
    data = json.load(file)
print(data[:5])


# In[3]:


df_patient_details = pd.json_normalize(data, sep='_', max_level=2)
df_medicines = pd.json_normalize(data, record_path=['consultationData', 'medicines'], 
                                 meta=['_id', 'appointmentId'], sep='_', errors='ignore')


# In[4]:


df_patient_details.head(5)


# In[5]:


df_medicines.head(5)


# In[6]:


missing_values = {
    'firstName': df_patient_details['patientDetails_firstName'].isna().sum() +
                 (df_patient_details['patientDetails_firstName'] == '').sum(),
    'lastName': df_patient_details['patientDetails_lastName'].isna().sum() +
                (df_patient_details['patientDetails_lastName'] == '').sum(),
    'DOB': df_patient_details['patientDetails_birthDate'].isna().sum() +
           (df_patient_details['patientDetails_birthDate'] == '').sum()
}

total_rows = len(df_patient_details)

missing_percentages = {col: round((count / total_rows) * 100, 2) for col, count in missing_values.items()}


# In[7]:


print(missing_percentages)


# In[8]:


gender_mode = df_patient_details['patientDetails_gender'].mode()[0]
df_patient_details['patientDetails_gender'].fillna(gender_mode, inplace=True)

female_percentage = round((df_patient_details[df_patient_details['patientDetails_gender'] == 'Female'].shape[0] / total_rows) * 100, 2)


# In[9]:


print(female_percentage)


# In[10]:


medicine_counts = df_medicines.groupby('appointmentId').size().reset_index(name='total_medicines')

active_inactive_counts = df_medicines.groupby(['appointmentId', 'isActive']).size().unstack(fill_value=0).reset_index()
active_inactive_counts.columns = ['appointmentId', 'inactive_medicines', 'active_medicines']


# In[11]:


df_patient_details['birth_year'] = pd.to_datetime(df_patient_details['patientDetails_birthDate'], errors='coerce').dt.year
df_patient_details['age'] = 2024 - df_patient_details['birth_year']
age_20_59_count = df_patient_details[(df_patient_details['age'] >= 20) & (df_patient_details['age'] <= 59)].shape[0]


# In[12]:


print(age_20_59_count)


# In[14]:


df_patient_details = df_patient_details.merge(medicine_counts, on='appointmentId', how='left').merge(
    active_inactive_counts, on='appointmentId', how='left')
total_active = df_medicines[df_medicines['isActive'] == True].shape[0]
total_inactive = df_medicines[df_medicines['isActive'] == False].shape[0]
total_medicines = total_active + total_inactive
active_percentage = round((total_active / total_medicines) * 100, 2)
inactive_percentage = round((total_inactive / total_medicines) * 100, 2)

print(active_percentage,inactive_percentage )


# In[15]:


average_medicines = round(df_medicines.shape[0] / df_patient_details.shape[0], 2)
print(average_medicines)


# In[16]:


medicine_frequency = df_medicines['medicineName'].value_counts().reset_index()
medicine_frequency.columns = ['medicineName', 'frequency']
third_most_frequent_medicine = medicine_frequency.iloc[2]['medicineName']
print(third_most_frequent_medicine)


# In[17]:


df_patient_details['total_medicines'] = df_patient_details['total_medicines'].fillna(0)
pearson_correlation = df_patient_details[['total_medicines', 'age']].corr(method='pearson').iloc[0, 1]
print(round(pearson_correlation,2))


# In[19]:


def is_valid_phone_number(phone):
    phone_str = str(phone)
    if phone_str.startswith('+91'):
        phone_str = phone_str[3:]
    elif phone_str.startswith('91'):
        phone_str = phone_str[2:]
    return phone_str.isdigit() and 6000000000 <= int(phone_str) <= 9999999999

df_patient_details['isValidMobile'] = df_patient_details['phoneNumber'].apply(is_valid_phone_number)

valid_phone_numbers_count = df_patient_details['isValidMobile'].sum()
print(valid_phone_numbers_count)


# In[20]:


print("Missing Value Percentages:", missing_percentages)
print("Percentage of Female Gender after Imputation:", female_percentage)
print("Number of records for ages 20-59:", age_20_59_count)
print("Average number of medicines prescribed:", average_medicines)
print("3rd Most Frequently Prescribed Medicine:", third_most_frequent_medicine)
print("Active Medicines Percentage:", active_percentage)
print("Inactive Medicines Percentage:", inactive_percentage)
print("Pearson Correlation between total medicines and age:", pearson_correlation)
print("Number of valid phn no.s:", valid_phone_numbers_count)


# In[ ]:




