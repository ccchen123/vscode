from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
from collections import OrderedDict



def pd_excel(VA,shock):
  if shock == "no":
    if VA == "VA":
       sheetname = "RFR_spot_with_VA"
    elif VA == "no":
       sheetname =  "RFR_spot_no_VA"
    else: print("error: wrong VA")
  elif shock == "up": 
    if VA == "VA":
       sheetname = "Spot_WITH_VA_shock_UP"
    elif VA == "no":
       sheetname =  "Spot_NO_VA_shock_UP"
    else: print("error: wrong VA")   
  elif shock == "down":  
     if VA == "VA":
       sheetname = "Spot_WITH_VA_shock_DOWN"
     elif VA == "no":
       sheetname =  "Spot_NO_VA_shock_DOWN"
     else: print("error: wrong VA") 
  else:
     print("error: wrong shock")   
  return sheetname      
date = "20221231"
VA= "VA"
shock="up"


filename = "EIOPA_RFR_"+date+"_Term_Structures"+".xlsx"
sheetname= pd_excel(VA,shock)
excel_file = pd.read_excel(filename,sheet_name=None)
    
df = excel_file[sheetname]
df = df.drop(columns=df.columns[0])
df.columns = df.iloc[0] 
       #df = df.drop(labels=0,axis=0)
df['Main menu'][6]="alpha"
      #df = df.rename({'Euro': 'EUR','Austria': 'EUR','Belgium': 'EUR','Bulgaria': 'BGN','Croatia': 'HRK','Cyprus': 'EUR','Czech Republic': 'CZK','Denmark': 'DKK','Estonia': 'EUR','Finland': 'EUR', 'France': 'EUR','Germany': 'EUR','Greece': 'EUR','Hungary': 'HUF','Iceland': 'ISK','Ireland': 'EUR','Italy': 'EUR','Latvia': 'LVL','Liechtenstein': 'CHF','Lithuania': 'EUR','Luxembourg': 'EUR','Malta': 'MTL','Netherlands': 'EUR','Norway': 'NOK','Poland': 'PLN','Portugal': 'EUR','Romania': 'RON','Russia': 'RUB','Slovakia': 'EUR','Slovenia': 'SIT','Spain': 'EUR','Sweden': 'SEK','Switzerland': 'CHF','United Kingdom': 'GBP','Australia': 'AUD','Brazil': 'BRL','Canada': 'CAD','Chile': 'CLP','China': 'CNY','Colombia': 'COP','Hong Kong': 'HKD','India': 'INR','Japan': 'JPY','Malaysia': 'MYR','Mexico': 'MXN','New Zealand': 'NZD','Singapore': 'SGD','South Africa': 'ZAR','South Korea': 'KRW','Taiwan': 'TWD','Thailand': 'THB','Turkey': 'TRY','United States': 'USD'}, axis=1)
df = df.rename({'Euro': 'EUR','Bulgaria': 'BGN','Croatia': 'HRK','Czech Republic': 'CZK','Denmark': 'DKK','Hungary': 'HUF','Iceland': 'ISK','Latvia': 'LVL','Malta': 'MTL','Norway': 'NOK','Poland': 'PLN','Romania': 'RON','Russia': 'RUB','Slovenia': 'SIT','Sweden': 'SEK','Switzerland': 'CHF','United Kingdom': 'GBP','Australia': 'AUD','Brazil': 'BRL','Canada': 'CAD','Chile': 'CLP','China': 'CNY','Colombia': 'COP','Hong Kong': 'HKD','India': 'INR','Japan': 'JPY','Malaysia': 'MYR','Mexico': 'MXN','New Zealand': 'NZD','Singapore': 'SGD','South Africa': 'ZAR','South Korea': 'KRW','Taiwan': 'TWD','Thailand': 'THB','Turkey': 'TRY','United States': 'USD'}, axis=1)
df = df.set_index('Main menu').rename_axis('currency', axis=1)
df.index.names = [None]
jsonStr1 = df.to_json()
jsonStr = json.loads(jsonStr1)
jsonStr = json.loads(jsonStr1)
print(df)
print(jsonStr)
currency = "GBP"
data_dict = jsonStr[currency]
data_dict = json.loads(data_dict)
print(data_dict)
#sorted_keys = sorted(data_dict.keys(), key=lambda x: int(x) if x.isdigit() else x)
sorted_keys = sorted(data_dict.keys(), key=lambda x: int(x) if x.isdigit() else str(x))
ordered_dict = OrderedDict()
for key in sorted_keys:
    ordered_dict[key] = data_dict[key]

# Print ordered dictionary
print(json.dumps(ordered_dict, indent=4))


dict = OrderedDict(jsonStr[currency])
print(dict)
print(json.dumps(dict, indent=4))
       #sorted_keys = sorted(my_dict.keys(), key=lambda x: int(x) if x.isdigit() else x)
       #sorted_json_str = json.dumps(sorted_dict)
       #print(sorted_json_str)
       #new= OrderedDict(my_dict)
       #print(new)
       #
       #print(jsonStr["GBP"])
       #return jsonify(my_dict)
   
