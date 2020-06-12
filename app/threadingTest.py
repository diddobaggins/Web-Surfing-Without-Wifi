import threading

num = 1

def ok():
    global num
    num+=1

thread = threading.Thread(target=ok)
thread.start()
print(num)
