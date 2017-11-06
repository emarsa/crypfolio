# crypfolio
Cryptocurrency portfolio

Each time the script is executed, a line wiht the prices and ammounts of currencies in the input file is added to a pandas dataframe.
It uses coinmarketcap api. Fiat and crypto symbols should be the ones used by coinmarketcap. If other fiat that EUR is used, script should be modified.
Input file has currency symbol followed by amount. One currency per line. It admits fiat for daytraders :)
Example:

BTC 0.025

ETH 1.245

NEO 17.52

EUR 105.25

Functions are provided for updating, ploting and portfolio value calculation.
