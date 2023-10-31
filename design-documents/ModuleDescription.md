## payment service:
Core module of the system. Responsible for handling payment requests from users and storing transaction data into db.
## card validation service:
Responsible for debit/credit card validation.
## credit card relay service:
Responsible for handling 2 calender day delay of credit card payments. Scheduled once (flexible) per day to read pending transactions that has passed 2 days.
## banking API
Some banking api for deducting money from debit/credit card.
## transaction db:
Stores all finished and rejected transactions.
## account receivable db:
Stores all pending transactions from credit cards.
## business owner db:
Stores all info of business owners. E.g. current balance received..