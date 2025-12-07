class SBD:
    s_list= []
    b_list= []
    d_list= []
    
    
    while True:
        choice = input("create?")
        if choice == "yes":
            s = input("Enter Squat PR")
            b = input("Enter Bench PR")
            d = input("Enter Deadlift PR")

            s_list.append(s)
            b_list.append(b)
            d_list.append(d)
            
        
        elif choice == "no":
            break
        else :
            print("no such thing brah!")
            continue
    
    
    
    print(f"this is your squat PRs: {s_list}")
    print(f"this is your bench PRs: {b_list}")
    print(f"this is your deadlift PRs: {d_list}")

        