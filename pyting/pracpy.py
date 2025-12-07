
# x = ["hello", "hi", "oten"]

# if "grrr" in x:
#     print (1)
# else:
#     print (2)

# y = ["heya", "heyo", "hola"]
# el = input("enter a num from 1-3") 
# el_int = int(el) #turn into int
# y[el_int] = "grrrr" 

# print(y)

# ins = ['a', 'b', 'c', 'd']

# ins.insert(1, 'y') #left is at what order, right is what you want

# print(ins)

# appe = [1,2,3,4]

# appe.append(6)

# print(appe)

# word = "I want to die die die"
# wordf = word.rfind("a")
# print(wordf)

# y.extend(appe) # merges lists

# print(y)

# rem = ['t', 'o', 'i']

# remx = input("Enter what you want to remove 1-3 : ")
# remx_int = int(remx)
# rem.pop(remx_int) #better than remove -> faster to type

# print(rem)

# loo = ["loop1", "loop2","loop3","loop4"]


# for l in range(len(loo)): #for loop
#     if l < 2 :
#         print(loo[l])

# loo2 = ["loop1", "loop2","loop3","loop4"]
# le = 0
# while le < len(loo2): #while loop
#     print(loo2[le])
#     le = le + 1

# loap = ['a', 'b', 'c']
# loaps = [1,2,3]

# for l in loaps:
#     if l <= 2:
#         loap.append(l)

# print(loap)

# loaps.extend(loap)

# print(loaps)

# loap.reverse()

# print(loap)

# x = range(4,12)

# print(x)

# print(list(x))

# iters = [1,2,3,4,5,6]

# iter_str = str(iters)
# x = iter(iter_str)

# for i in x:
#     print(next(i))

# class Myclass:
#     x = 5

# reuse = Myclass()
# print(reuse.x)

# class number1:
#     x = input("enter a number")
#     x_int = int(x)

# class number2:
#     x = input("Enter another number")
#     x_int = int(x)

# n1 = number1()
# n2 = number2()

# print(n1.x_int + n2.x_int)

# del number1

# print(number1.x)
# import sys
# # Add the directory containing 'mymodule.py' to the search path
# sys.path.append('d:/Coding/modules')

# import mymodule

# mymodule.greeting("jonathan")

# import myModule

# myModule.greeting("Jonathan")

# import datetime

# x = datetime.datetime(2025, 10, 7)

# print(x.month)
# print(x.strftime("%D")) #A -> day B -> month C -> year? idk D-> ?/?/?

# class Cla():
#     x = input("Enter a number")
#     x_int 

# class ():
#     pa = Cla()

#     print(pa.z)

# class Person():
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

# class List():
#     p = Person()

    

#     p_list = [p.name,p.age]

#     while(True):
#         print("Would you like to make a list?")
#         choice = input("Yes/No")
        
#         if choice == "yes":
#             p.name = input("Input Name")
#             p.age = input("Input age")

#             p_list.append(p.name)
#             p_list.append(p.age)
#         elif choice == "no":
#             break
#         else:
#             print("wrong!")
#             continue
    

# print(List.p_list)
# char = 'A'

# if char.isalpha():
#     print(ord(char))


def enc(text, key = 13):
    result = ""
    

    for char in text: # loop through all chars in text

        if char.isalpha(): # IF THEY ARE LETTERS ->
            start = ord('A') if char.isupper() else ord('a')  #Start Order at 'A' for all caps else 'a'

            shift = ord(char) - start #Since order is not all letters, First letter - Given letter (A-A = 0, A-B = 1)

            keying = (shift  + key) % 26 #To avoid passing over 26(since there is 26 letters in the alphabet)

            shifted = chr(keying + start) #lets say A in the order is 65 so chr(65) technically what order it is at(keying and start is numerical)

            result += shifted #(change the letter)
        else:
            result += char #if not letter, just stick with the letter
    return result


def dec(text, key=-13):
    return enc(text, key)
    

def blud():
    tex = input("Enter text")

    new_tex = enc(tex)
    org_text = dec(new_tex)

    print("This is your new text: ")

    print(new_tex)
    print(org_text)


blud()