### PersonalFi
PersonalFi is a web game to teach the basics of personal finance, with an emphasis on budgeting and credit.

#### Running PersonalFi

* Install Django: `pip3 install django`
* Build the database: from the root of the repo, `python3 manage.py migrate`
* Create an admin user: `python3 manage.py createsuperuser`
* Run the development server: `python3 manage.py runserver`.
* Access the [admin site](http://localhost:8000/admin) or [main app](http://localhost:8000).

#### Main Menu
Balances: Top right, updates whenever their is a user action

Always Available Buttons:
* Transactions 
* Investments/Savings
* Job 

Transactions Buttons: (will include property)
* Buy Items
* Sell Items

Job Buttons:
* Change Hours
* Apply for/Change job

Savings and Investments Buttons:
* Move between accounts
* Rates/Explanations of accounts


#### Secondary Menus
Payment Options (need for transactions, property)
* Credit
* Cash
* Loans (can't use for transactions)






