from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/data",methods=['GET','POST'])
def data():
    if request.method == 'POST':
      row = request.form["input-maturity"]
      col = request.form["input-country"]
      sheet_name = request.form["input-sheet"]
    
      df = pd.read_excel('term_structure.xlsx',sheet_name=sheet_name)
      df = df.drop(columns=df.columns[0])
      df.columns = df.iloc[0]
      df = df.drop(labels=0,axis=0)
      df = df.set_index('Main menu')

      row= int(row)
      data = df[col][row]
      #data = pd_excel(pd=df,col=col,row=row )
         
    return render_template('data.html',data= data)

if __name__=='__main__':
    app.run(debug=True)









'''from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/data",methods=['GET','POST'])
def data():
    if request.method == 'POST':
      file = request.form["upload-file"]
      #def pd_excel(pd, col, row):
       #  print(pd[col][row])
      data = pd.read_excel(file)
      #data = pd_excel(pd=df,col=col,row=row )
      #return data.to_html
      return render_template('data.html',data=data.to_html())


if __name__=='__main__':
    app.run(debug=True)'''