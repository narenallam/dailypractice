g = 9.8

def fun3(x):
    print ('fun3 start')
    # print 'stack frame of fun3: ', locals()
    print ('fun3 end')

def fun2(n):
    print ('fun2 start')
    y = 30
    n = n + 1
    # print 'stack frame of fun2: ', locals()
    fun3(n)
    print ('fun2 end')

def fun1(n):
    print ('fun1 start')
    n = n + 1
    x = 20
    # print 'stack frame of fun1: ', locals()
    fun2(n)
    print ('fun1 end')

def main():
    print ('main starts here')
    a = 100
    b = 200
    # print 'stack frame of fun: ', locals()
    fun1(a)
    print ('main ends here')

if __name__ == '__main__':
    main()