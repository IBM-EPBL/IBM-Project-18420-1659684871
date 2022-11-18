from flask import Flask,render_template,request,url_for,redirect
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account.html')    

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/productdetails')
def productdetails():
    return render_template('product-details.html')

@app.route('/productdetails1')
def productdetails1():
    return render_template('product-details1.html') 

@app.route('/productdetails2')
def productdetails2():
    return render_template('product-details2.html')

@app.route('/productdetails3')
def productdetails3():
    return render_template('product-details3.html')



@app.route('/cart')
def cart():
    return render_template('cart.html')        





if __name__ == "__main__":
   app.run(debug=True)

   