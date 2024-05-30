import time

__doc = '1234'
__doc = "2345"
DOC = "2345"
DOC = "1234"

print(__doc)

money = 100
def addmoney(m):
    global money
    money += m

print(money)

tup = (1)

# tup[0]=100

print(tup)

tinydict = {'name': 'john', 'code': 6734, 'dept': 'sales'}

print(tinydict)

tinydict['age'] = 7  # Add new entry

print(tinydict)

tinydict[(1, 2, 3)] = "hello"  # Add entry with tuple key

print(tinydict)

times = time.time()
localtime = time.localtime(times).tm_hour, ':', time.localtime(times).tm_min
localtime2 = f"{time.localtime(times).tm_hour}:{time.localtime(times).tm_min}"

print(localtime)
print(localtime2)

