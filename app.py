from flask import Flask, render_template, url_for, request

#importing model and function
import pickle
transform=pickle.load(open('trasform.pkl','rb'))
model=pickle.load(open('model.pkl','rb'))


#function import for data cleaning
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

#data cleaning function
def clean(x):
  x = re.sub('[^a-zA-Z]', ' ', x)
  x = x.lower()
  x = x.split()
  x = [ps.stem(word) for word in x if not word in stopwords.words('english')]
  x = ' '.join(x)
  return x

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    
    if request.method=='POST':
        if (request.form['content']==""):
          return render_template('index.html',result="")
        input=request.form['content']
        input=clean(input)
        input=transform.transform([input]).toarray()
        
        result=model.predict(input)
        if(result[0]==1):
          finalresult="Positive"
        elif(result[0]==0):
          finalresult="Negative"
        else:
          finalresult=""

        return render_template('index.html',result=finalresult)
    else:
        return render_template('index.html',result="")

@app.route('/about/')
def about():
    return render_template('about.html')

if __name__=='__main__':
      app.run(debug=True)