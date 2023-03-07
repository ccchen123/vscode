from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
from collections import OrderedDict

app = Flask(__name__)


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
#date = "20221231"
#VA= "VA"
#shock="up"

@app.route('/term_structure', methods=['GET'])
def get_ccurrency_data():
    type = request.args.get('type')
    date = request.args.get('date')
    VA = request.args.get('VA')
    shock = request.args.get('shock')
    currency = request.args.get('currency')
    tenor = request.args.get('tenor')

    filename = "EIOPA_RFR_"+date+"_Term_Structures"+".xlsx"
    sheetname= pd_excel(VA,shock)
    excel_file = pd.read_excel(filename,sheet_name=None)
    
    if type !="EIOPA":
       return jsonify({'error': 'type not found'}), 404
    if sheetname in excel_file:
       df = excel_file[sheetname]
       df = df.drop(columns=df.columns[0])
       df.columns = df.iloc[0] 
       #df = df.drop(labels=0,axis=0)
       df['Main menu'][6]="alpha"
      #df = df.rename({'Euro': 'EUR','Austria': 'EUR','Belgium': 'EUR','Bulgaria': 'BGN','Croatia': 'HRK','Cyprus': 'EUR','Czech Republic': 'CZK','Denmark': 'DKK','Estonia': 'EUR','Finland': 'EUR', 'France': 'EUR','Germany': 'EUR','Greece': 'EUR','Hungary': 'HUF','Iceland': 'ISK','Ireland': 'EUR','Italy': 'EUR','Latvia': 'LVL','Liechtenstein': 'CHF','Lithuania': 'EUR','Luxembourg': 'EUR','Malta': 'MTL','Netherlands': 'EUR','Norway': 'NOK','Poland': 'PLN','Portugal': 'EUR','Romania': 'RON','Russia': 'RUB','Slovakia': 'EUR','Slovenia': 'SIT','Spain': 'EUR','Sweden': 'SEK','Switzerland': 'CHF','United Kingdom': 'GBP','Australia': 'AUD','Brazil': 'BRL','Canada': 'CAD','Chile': 'CLP','China': 'CNY','Colombia': 'COP','Hong Kong': 'HKD','India': 'INR','Japan': 'JPY','Malaysia': 'MYR','Mexico': 'MXN','New Zealand': 'NZD','Singapore': 'SGD','South Africa': 'ZAR','South Korea': 'KRW','Taiwan': 'TWD','Thailand': 'THB','Turkey': 'TRY','United States': 'USD'}, axis=1)
       df = df.rename({'Euro': 'EUR','Bulgaria': 'BGN','Croatia': 'HRK','Czech Republic': 'CZK','Denmark': 'DKK','Hungary': 'HUF','Iceland': 'ISK','Latvia': 'LVL','Malta': 'MTL','Norway': 'NOK','Poland': 'PLN','Romania': 'RON','Russia': 'RUB','Slovenia': 'SIT','Sweden': 'SEK','Switzerland': 'CHF','United Kingdom': 'GBP','Australia': 'AUD','Brazil': 'BRL','Canada': 'CAD','Chile': 'CLP','China': 'CNY','Colombia': 'COP','Hong Kong': 'HKD','India': 'INR','Japan': 'JPY','Malaysia': 'MYR','Mexico': 'MXN','New Zealand': 'NZD','Singapore': 'SGD','South Africa': 'ZAR','South Korea': 'KRW','Taiwan': 'TWD','Thailand': 'THB','Turkey': 'TRY','United States': 'USD'}, axis=1)
       df = df.set_index('Main menu').rename_axis('currency', axis=1)
       df.index.names = [None]
       jsonStr = df.to_json()
       jsonStr = json.loads(jsonStr)
       if currency not in jsonStr:
         return jsonify({'error': 'Currency not found'}), 404       
       if tenor is not None:
         if tenor not in jsonStr[currency]:
            return jsonify({'error': 'Tenor not found'}), 404
         return jsonify(jsonStr[currency][tenor])
       my_dict = OrderedDict(jsonStr[currency])
       return json.dumps(my_dict, indent=4)
       #sorted_keys = sorted(my_dict.keys(), key=lambda x: int(x) if x.isdigit() else x)
       #sorted_json_str = json.dumps(sorted_dict)
       #print(sorted_json_str)
       #new= OrderedDict(my_dict)
       #print(new)
       #currency = "GBP"
       #print(jsonStr["GBP"])
       
    return jsonify({'error': 'Sheet_name not found, VA can be chosen as VA or no, shock can be chosen as no, up or down'}), 404   
     

if __name__ == '__main__':
    app.run(debug=True)