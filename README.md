# crypfolio
Cryptocurrency portfolio

Each time the script is executed, a line wiht the prices and ammounts of currencies in the input file is added to a pandas dataframe.
It uses coinmarketcap api. Fiat and crypto symbols should be the ones used by coinmarketcap. If other fiat that EUR is used, script should be modified.
Input file has currency symbol followed by amount. It admits fiat for daytraders :)
Example:

BTC 0.025\n
ETH 1.245\n
NEO 17.52\n
EUR 105.25\n

Functions are provided for updating, ploting and portfolio value calculation.
