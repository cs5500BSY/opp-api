## payment service:
Core module of the system. Responsible for handling payment requests from users and storing transaction data into db.
### logic
Upon auth, call card validation service. If card is valid then proceed. Otherwise return.<br>
Then if is credit card: save the transaction into account receivable db(peeding db).
If is debit card: save save the transaction into transaction db and update the the credit of the business owner.

## card validation service:
Use some algorithm to determine if the card is fraudulant or the transaction is fraudulant.
## credit card relay service:
Read receivable db(peeding db). If an record exceeds the waiting time(e.g. 2 calender days):
delete it in receivable db(peeding db), insert transaction into transaction db, update business owner's credit.