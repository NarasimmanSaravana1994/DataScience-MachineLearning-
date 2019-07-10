



def process():
    try:
        x=1/0
        f=open("C:\\Users\\mirra.balaji\\Music\\Training Doc\\Python_Sripts\\Temp\\first.txt","r")
           
    except ZeroDivisionError as e:
        print("inside except")

    finally:
        f.close()
        print("closed")

process()
