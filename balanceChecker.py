import requests
import json
import os
import glob
import random
import winsound

watchList = []
goldList = []
frequency = 2500
duration = 500


def checkBalance(acctData, numbOfAccounts):

    url1 = "https://blockchain.info/balance?active={}".format(acctData[1].strip())
    url2 = "https://blockchain.info/balance?active={}".format(acctData[2].strip())
    r1 = requests.get(url1)
    r2 = requests.get(url2)
    final1 = 0
    final2 = 0
    tot1 = 0
    tot2 = 0

    if r1.status_code is not 200 or r2.status_code is not 200:
        print("cant look up bal, blockchain api issue")

    if r1.status_code == 200:
        acctCheck1 = json.loads(r1.content)[acctData[1].strip()]
        final1 = acctCheck1['final_balance']
        tot1 = acctCheck1['total_received']

    if r2.status_code == 200:
        acctCheck2 = json.loads(r2.content)[acctData[2].strip()]
        final2 = acctCheck2['final_balance']
        tot2 = acctCheck2['total_received']

    print("{} {} {} {} -- {}".format(final1, final2, tot1, tot2, numbOfAccounts))

    if final1 > 0 or final2 > 0:
        print("GOT ONE!!!!!!!!!!!!!!!1")
        print("*"*100)
        print(acctData)
        print("*"*100)
        goldList.append(acctData)
        winsound.Beep(frequency, duration)
        winsound.Beep(frequency, duration)
        winsound.Beep(frequency, duration)

    if tot1 > 0 or tot2 > 0:
        print("WATCH OUT!!!!!!!!!!!!!!")
        print("*"*50)
        print(acctData)
        print("*"*50)
        watchList.append(acctData)
        winsound.Beep(frequency, duration)


directory = "C:\\Users\\n644d\\code\\accts"
acctDirectories = [x[0] for x in os.walk(directory)]
numberOfAccounts = 0
for acctDir in acctDirectories:
    acctFiles = glob.glob("{}\\*.txt".format(acctDir))
    if len(acctFiles) > 0:
        for acctFile in acctFiles:
            accts = []
            with open(acctFile) as f:
                accts = f.read().splitlines()
                for acct in accts:
                    acctData = acct.split(',')
                    numberOfAccounts = numberOfAccounts + 1
                    checkBalance(acctData, numberOfAccounts)

seed = random.getrandbits(128)

if len(goldList) > 0:
    with open("C:\\Users\\n644d\\code\\accts\\{}.gold.txt", "w".format(seed)) as f:
        for gold in goldList:
            f.write("{}\n".format(gold))

if len(watchList) > 0:
    with open("C:\\Users\\n644d\\code\\accts\\{}.watch.txt", "w".format(seed)) as f:
        for watch in watchList:
            f.write("{}\n".format(watch))
