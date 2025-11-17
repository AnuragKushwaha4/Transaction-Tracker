#import modules
from flask import Flask,request,url_for,render_template,redirect

#initiate
app=Flask(__name__)
#Sample Data
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

#Read :
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


#create:
@app.route("/add",methods=["GET","POST"])
def add_transaction():
    if request.method=="GET":
        return render_template("form.html")
    if request.method=="POST":
        transation = {
              'id': len(transactions)+1,
              'date': request.form['date'],
              'amount': float(request.form['amount'])
             }
        transactions.append(transation)
        return redirect(url_for("get_transactions"))


#update:
@app.route("/edit/<int:transaction_id>",methods=["GET","POST"])
def edit_transaction(transaction_id):
    if request.method=="POST":
        date=request.form["date"]  
        amount=float(request.form["amount"])
        for transaction in transactions:
            if transaction["id"]==transaction_id:
                transaction["date"]=date
                transaction["amount"]=amount
                break
        return redirect(url_for("get_transactions"))
    if request.method=="GET":
        for transaction in transactions:
            if transaction["id"]==transaction_id:
                return render_template("edit.html",transaction=transaction)
    return {"message": "Transaction not found"}, 404


#delete:
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction["id"]==transaction_id:
            transactions.remove(transaction)
            break

    return redirect(url_for("get_transactions"))

#Search:
@app.route("/search",methods=["GET",'POST'])
def search_transactions():
    if request.method=="POST":
        minimum=float(request.form["min_amount"])
        maximum=float(request.form["max_amount"])
        filtered_list=[]
        for transaction in transactions:
            if transaction["amount"]>minimum and transaction["amount"]<maximum:
                filtered_list.append(transaction)
        return render_template("transactions.html",transactions=filtered_list)
    if request.method=="GET":
        return render_template("search.html")

#total:
@app.route("/balance")
def total_balance():
    balance=0
    for transaction in transactions:
        balance+=transaction["amount"]
    return {"Total balance" : balance}

if __name__=="__main__":

    app.run(debug=True)

