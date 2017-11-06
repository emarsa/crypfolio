import pandas as pd
import numpy as np
import urllib.request, json
import matplotlib.pyplot as plt

api_url = "https://api.coinmarketcap.com/v1/ticker/?convert=EUR"
fiat_u = 'EUR'
fiat_v = '_' + fiat_u.lower()
pf_input = 'my_portfolio.txt'
pf_file = 'history_pf.csv'

def curr_ordered(curr_df, curr_in):
    for i in range(0,len(curr_df)):
        try:
            if curr_df[i][-4:] == fiat_v:
                del curr_df[i]
        except IndexError:
            pass
    del curr_df[-1]
    try:
        eurin=curr_in.index(fiat_u)
        del curr_in[eurin]
    except:
        pass
    tlist=curr_in + curr_df
    tset = list(set(tlist))
    curr_sort=sorted(tset, key= lambda x: tlist.index(x))
    df_order=[]
    for i in curr_sort:
        df_order.append(i)
        df_order.append(i+fiat_v)
    df_order.append(fiat_u)
    return df_order, curr_sort
    
def update_df(inp_file, pf_file):
    
    with urllib.request.urlopen(api_url) as url:
        data = json.loads(url.read().decode())
    
    first_entry=False
    try:
        df=pd.read_csv(pf_file, parse_dates=True, index_col=0)        
    except FileNotFoundError:
        print(pf_file + ' not found. It will be created')
        first_entry=True

    with open(inp_file, 'r') as file:
        # crea list (per mantnir ordre) y dic amb el input
        lines = file.readlines()
        inp_dic = {}
        inp_order = []
        for line in lines:
            words = line.split()
            inp_order.append(words[0])
            inp_dic[words[0]] = float(words[1])
    
    def api_update(inp_dic, inp_order, data):
        val_str = 'price' + fiat_v
        for coin in data:
            if coin['symbol'] in inp_order:
                inp_dic[coin['symbol'] + fiat_v] = float(coin[val_str])
        return inp_dic
    
    if first_entry:
        inp_dic = api_update(inp_dic, inp_order, data)
        if fiat_u not in inp_dic.keys():
            inp_dic[fiat_u] = np.nan
        # order for df
        order = []
        for item in inp_order:
            if item != fiat_u:
                order.append(item)
                order.append(item+fiat_v)
        order.append(fiat_u)
        df = pd.DataFrame(inp_dic, [pd.Timestamp('now')])
    if not first_entry:
        order, to_update = curr_ordered(df.columns.tolist(), inp_order)
        inp_dic = api_update(inp_dic, to_update, data)
        df_new = pd.DataFrame(inp_dic, [pd.Timestamp('now')])
        df = df.append(df_new)
    df = df[order]
    df.to_csv(pf_file)
    return df


def calc_val(df):
    df = df.fillna(value=0.0)
    df['cry_total'] = 0
    for cur in df.columns:
        try:
            if cur[-4:] == fiat_v:
                df[cur[:-4] + '_val'] = df[cur]*df[cur[:-4]]
                df['cry_total'] += df[cur[:-4] + '_val']
        except IndexError:
            pass
    df['total'] = df['cry_total'] + df[fiat_u]
    return df

def plot_pf(df, fiat = False):
    data = df.iloc[-1]
    values = []
    legend = []
    total = 0
    for item in data.index:
        try:
            if item[-4:] == '_val':
                values.append(data[item])
                legend.append(item[:-4] + ' ' +  '%.2f' % data[item] + ' €')
                total += data[item]
        except IndexError:
                pass
    if fiat and not pd.isnull(data[fiat_u]):
        values.append(data[fiat_u])
        legend.append(fiat_u + str(data[fiat_u]))
        total += data[fiat_u]
        
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=legend, autopct='%1.1f%%', 
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.set_title('Total portfolio value: ' + '%.2f' % total + ' €')

    plt.show()

def plot_evo(df, fiat=False):
    x_ax = df.index
    values = []
    legend = []
    for item in df.columns:
        try:
            if item[-4:] == '_val':
                values.append(list(df[item]))
                legend.append(item[:-4])
        except IndexError:
            pass
    if fiat:
        values.append(list(df[fiat_u]))
        legend.append(fiat_u)
    fig, ax = plt.subplots()
    ax.stackplot(x_ax, *values, labels=legend)
    ax.legend(loc=2)
    fig.autofmt_xdate()
    plt.show()

if __name__ == "__main__":
    pf = update_df(pf_input, pf_file)
    print ('Portfolio status:')
    print (pf.tail())
    fiat = input('Want to plot with fiat if available? (y/n)')
    pfiat = fiat == 'y'
    plot_pf(calc_val(pf), fiat=pfiat)

