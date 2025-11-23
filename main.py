input_file = "input.txt"
output_file = "output.txt"

def main():
    global results
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    results = create_results(lines)

    with open(output_file, "w", encoding="utf-8") as f:
        for result in results:
            print(result)
            f.write(result+"\n")

def total_executed_volume(time):
    my_line_list = results
    total = my_function1(time,my_line_list)
    return total

def executed_user_volume(user_id,time):
    my_line_list = results
    total = my_function2(my_line_list, user_id, time)
    return total

def total_remaining_volume(time):
    my_line_list = results
    total = my_function3(time,my_line_list)
    return total

def remaining_user_volume(user_id,time):
    my_line_list = results
    total = my_function4(my_line_list, user_id, time)
    return total

import copy
#commandreceived is used for indexing orders that are being processed. in commandnumber function it is going to be used
command_received = 0
#commandsbystock is a dictonary that is separtes sell orders and buy orders of the named stock with order indexes that are given for all commands individually
commandsbystock = dict()
#this all_commands list holds all the orders that are given and their currents status of order_amount. while transtactions are getting done, orders are picked from this list
all_commands = list()
#outputs which are going to be returned for results of create_results function
output = list()
#holds all the data of current time interval while getting changed by every new proccessed order in the function of create_results
executeddata = list()
#needed for alphabetical ordering of stocks
alphabet_upcase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
#all the history of transactions are in this dictionary with the key values of time
transaction_history = dict()

#this fnction gives words a alphabetical order priority number, if the number is higher, that means that word priorited alphabetically(be careful for the fact that higher in negative numbers means lower absolute value)
def alphabetical_ord_check(a):
    sum = int(0)
    for x in range(len(a)):
        sum = sum + (alphabet_upcase.index(a[x])+1) *30** (4-x)
    return -sum


#this function is used for giving individual numbers for every order that are in input list, numbers given by input list order.
def command_number():
    global command_received
    
    result = f"{command_received:06}"
    command_received = command_received + 1
    return result
#used as key for sorting executed data, in a x in executed data x[1] = transaction time x[2] = time of first given order in that transaction
def executeddatasorter(a):    
    return (a[1], a[2])
#converts data to a convinient format for output
def timeconverter(time):
    return f"{time[0:4]}-{time[4:6]}-{time[6:8]} at {time[8:10]}:{time[10:12]}:{time[12:14]}"
#gives bigger time because that time is the transaction time. in the give first order it gives the smaller time in a transaction because that time does not determine transaction time, however it is important in sorting
def givebuytime(za):
    if (all_commands[za[0]]["time"]) < (all_commands[za[1]]["time"]):
        return all_commands[za[1]]["time"]
    else:
        return all_commands[za[0]]["time"]
def givefirstorder(za):
    if (all_commands[za[0]]["time"]) > (all_commands[za[1]]["time"]):
        return all_commands[za[1]]["time"]
    else:
        return all_commands[za[0]]["time"]

#function for executed total volume function. to that time mark this function multiplies and sums all the values in executed data, which is list used for completed transatctions
def my_function1(time,my_line_list):
    time = time.replace("-","")
    sum = float(0)
    for ctrans in executeddata:
        if int(ctrans[1]) <= int(time):
            ctrans[0] = ctrans[0].split()
            sum = sum + int(ctrans[0][2])*float(ctrans[0][5])
    return round(sum)

#exetuced user volume function, same one, however we are chechking for user ids now
def my_function2(my_line_list,user_id, time):
    time = time.replace("-","")
    sum = float(0)
    for ctrans in executeddata:
        if (str(user_id) == str(ctrans[3])) or (str(user_id) == str(ctrans[4])):
            if int(ctrans[1]) <= int(time):
                ctrans[0] = ctrans[0].split()
                sum = sum + int(ctrans[0][2])*float(ctrans[0][5])
    return round(sum)
#this is a little bit more complicated, transaction history is needed for this function. transaction history is dict in a format time:allcodes in that time interval. so finds the key needed with historyremarkindex, then uses that key to reach for finding remaining volume by multplying and summnig ordersthat are not executed in that time mark
def my_function3(time,my_line_list):
    time = time.replace("-","")
    babu = list()
    for a in transaction_history:
        babu.append([a, transaction_history[a]]) 
    for x in babu:
        if x[0] == time:
            historyremarkindex = x[0]
            break
        else:
            if x[0] < time:
                historyremarkindex = x[0]  
    sum= float()
    for x in transaction_history[historyremarkindex]:
            if int(transaction_history[historyremarkindex][x]["order_amount"]) > 0:
                sum = sum + int(transaction_history[historyremarkindex][x]["order_amount"])*round(transaction_history[historyremarkindex][x]["order_price"],1)
    return round(sum)
#same one with a user_id twist, now we are checking for user ids
def my_function4(my_line_list,user_id, time):
    time = time.replace("-","")
    babu = list()
    for a in transaction_history:
        babu.append([a, transaction_history[a]]) 
    for x in babu:
        if x[0] == time:
            historyremarkindex = x[0]
            break
        else:
            if x[0] < time:
                historyremarkindex = x[0]  
    sum= float()
    for x in transaction_history[historyremarkindex]:
        if str(transaction_history[historyremarkindex][x]["user_id"]) == str(user_id):
            if int(transaction_history[historyremarkindex][x]["order_amount"]) > 0:
                sum = sum + int(transaction_history[historyremarkindex][x]["order_amount"])*round(transaction_history[historyremarkindex][x]["order_price"],1)
    return round(sum)
#now this is the main function of this code, lets dive deeper
def create_results(txt):
    global command_received
    global commandsbystock
    global all_commands
    global output
    global executeddata
    global alphabet_upcase
    global transaction_history
    for a in range(len(txt)):
        txt[a] = txt[a].replace("\n","")
    all_commands= dict()
    completed_transactions = list()
    #we are preaping the input for procesising, if there is an empty line, pops it if not, splits it by spaces
    for linenumber in range(len(txt)):
        if len(txt[linenumber]) > 0:
            txt[linenumber] = txt[linenumber].split()
        else:
            txt[linenumber].pop(linenumber)
    #now we are orderirng inputs
    for b in range(len(txt)):
        for a in range(len(txt)-1):
            if txt[a][0] == txt[a+1][0]:
                
                #ordering for alphabetical order of stocks if the timestamps is same
                if alphabetical_ord_check(txt[a][3]) < alphabetical_ord_check(txt[a+1][3]):
                    temp = txt[a]
                    txt[a] = txt[a+1]
                    txt[a+1] = temp
                elif alphabetical_ord_check(txt[a][3]) == alphabetical_ord_check(txt[a+1][3]):
                    #if they are same too, we are looking for sell prices and ordering by that value
                    if txt[a][4] == txt[a][4] and txt[a][4] == "Sell":
                        if round(float(txt[a][6]),1) > round(float(txt[a+1][6]),1):
                            temp = txt[a]
                            txt[a] = txt[a+1]
                            txt[a+1] = temp
                        elif round(float(txt[a][6]),1) == round(float(txt[a+1][6]),1):
                            #if same, user id order
                            if int(txt[a][1]) > int(txt[a+1][1]):
                                temp = txt[a]
                                txt[a] = txt[a+1]
                                txt[a+1] = temp
                    #same but in reverse because of the buy command
                    elif txt[a][4] == txt[a][4] and txt[a][4] == "Buy":
                        if round(float(txt[a][6]),1) < round(float(txt[a+1][6]),1):
                            temp = txt[a]
                            txt[a] = txt[a+1]
                            txt[a+1] = temp
                        elif round(float(txt[a][6]),1) == round(float(txt[a+1][6]),1):
                            #if same, user id order
                            if int(txt[a][1]) > int(txt[a+1][1]):
                                temp = txt[a]
                                txt[a] = txt[a+1]
                                txt[a+1] = temp
                    #if they are not same, we are ordering with user ids
                    else:
                        if int(txt[a][1]) > int(txt[a+1][1]):
                            temp = txt[a]
                            txt[a] = txt[a+1]
                            txt[a+1] = temp
    for a in range(len(txt)):
        #active line cmd is the key of current lines order in all commands, and the individual number of the order
        activelinecmd= command_number()
        #order gets dictionaried by their spesific values for reacing easiser
        all_commands[activelinecmd] = {"time": txt[a][0].replace("-","") , "user_id": int(txt[a][1]) , "user_name": txt[a][2] , "stock_name": txt[a][3], "command": txt[a][4] , "order_amount": int(txt[a][5]) , "order_price": float(txt[a][6])}
        #if there is no key for that stock in commands by stock, we open a new one
        if all_commands[activelinecmd]["stock_name"] not in commandsbystock:
            commandsbystock[all_commands[activelinecmd]["stock_name"]] = {"BUY": [], "SELL" : [] }
        #separets the order for if it is sell or buy
        if all_commands[activelinecmd]["command"] == "Buy":
            commandsbystock[all_commands[activelinecmd]["stock_name"]]["BUY"].append(activelinecmd)
        else:
            commandsbystock[all_commands[activelinecmd]["stock_name"]]["SELL"].append(activelinecmd)
        #for every line, we are looking for is there any suitable matching that we can do by going stock by stock
        for cstock in commandsbystock:
            for buycode in commandsbystock[cstock]["BUY"]:
                #we are not using any order with zero order amount, so :
                if all_commands[buycode]["order_amount"] == 0:
                    continue
                possiblesellers = list()
                #looking for possible sellers we may need more than one seller for partial orders 
                for sellcode in commandsbystock[cstock]["SELL"]:
                    if all_commands[sellcode]["user_id"] != all_commands[buycode]["user_id"]:
                        if all_commands[sellcode]["order_price"] <= all_commands[buycode]["order_price"]:
                                if (all_commands[sellcode]["order_amount"]) != 0:
                                    possiblesellers.append(sellcode)
                #if there is no suitable seller:
                if len(possiblesellers) == 0:
                    continue
                #now we are making transactions with the sellers we founded, by using order of time we made earlier
                #these all boring mathematics, however it simply substracts the order amount that is transactined from both sides
                for x in range(len(possiblesellers)): 
                    properseller = possiblesellers[x]
                    if all_commands[buycode]["order_amount"] > 0:
                        if  int(all_commands[properseller]["order_amount"]) - int(all_commands[buycode]["order_amount"]) > 0:
                            all_commands[properseller]["order_amount"] = int(all_commands[properseller]["order_amount"]) - int(all_commands[buycode]["order_amount"])
                            completed_transactions.append((properseller,buycode, int(all_commands[buycode]["order_amount"],)))
                            all_commands[buycode]["order_amount"] = 0
                        elif int(all_commands[properseller]["order_amount"]) - int(all_commands[buycode]["order_amount"]) < 0:
                            all_commands[buycode]["order_amount"] = int(all_commands[buycode]["order_amount"]) - int(all_commands[properseller]["order_amount"])
                            completed_transactions.append((properseller,buycode, int(all_commands[properseller]["order_amount"])))
                            all_commands[properseller]["order_amount"] = 0
                        elif int(all_commands[properseller]["order_amount"]) - int(all_commands[buycode]["order_amount"]) == 0:
                            completed_transactions.append((properseller,buycode, int(all_commands[buycode]["order_amount"])))
                            all_commands[buycode]["order_amount"] = 0 
                            all_commands[properseller]["order_amount"] = 0
        #and we are adding this time interrvals's data to transaction history for further proccseing in functions
        transaction_history[all_commands[activelinecmd]["time"]] =((copy.deepcopy(all_commands)))
    #executed data is has the output message that is going to be given and some sorting values which going to be used...
    for trans in completed_transactions:
        executeddata.append([(f"{all_commands[trans[1]]["user_name"]} bought {trans[2]} {all_commands[trans[1]]["stock_name"]} for {all_commands[trans[0]]["order_price"]} USD from {all_commands[trans[0]]["user_name"]} on {f"{timeconverter(givebuytime(trans))}"}"),givebuytime(trans), givefirstorder(trans),all_commands[trans[1]]["user_id"],all_commands[trans[0]]["user_id"]])
    #RIGHT HERE! for further output sorting details look for function "executeddatasorter"
    executeddata = sorted(executeddata, key = executeddatasorter)
    for a in executeddata:
        output.append(a[0]) 
    return output


main()


#by calling the main function which looks for input and output file than proccesses it, we are ending this journey of stock orders...   