import json
import os

# global variables
db = "data.json"
x = {}

def load():
    global x
    if os.path.exists(db):
        try: # [INV-10] เพิ่ม try/except สำหรับอ่านไฟล์
            with open(db, 'r') as f:
                x = json.load(f)
        except Exception: # [INV-10] ถ้าไฟล์เสียหรืออ่านไม่ได้ ให้โหลด default แทน
            x = {
                "101": {"n": "Mama Noodles", "q": 50, "p": 6.0, "c": "Food"},
                "102": {"n": "Lactasoy Milk", "q": 20, "p": 12.0, "c": "Drink"},
                "103": {"n": "Singha Water", "q": 100, "p": 10.0, "c": "Drink"}
            }
    else:
        # default data if file not found
        x = {
            "101": {"n": "Mama Noodles", "q": 50, "p": 6.0, "c": "Food"},
            "102": {"n": "Lactasoy Milk", "q": 20, "p": 12.0, "c": "Drink"},
            "103": {"n": "Singha Water", "q": 100, "p": 10.0, "c": "Drink"}
        }

def save():
    # [INV-11] ทำ Atomic write ผ่าน tmp file เพื่อป้องกันไฟล์เสียระหว่างเซฟ
    temp_db = db + ".tmp"
    with open(temp_db, 'w') as f:
        json.dump(x, f)
    os.replace(temp_db, db) # [INV-11] replace ไฟล์ต้นฉบับเมื่อเขียนเสร็จสมบูรณ์

def main():
    load()
    while True:
        print("\n=== INVENTORY SYSTEM v1.0 ===")
        print("1. Show all")
        print("2. Add or Update")
        print("3. Out")
        print("4. Check Check")
        print("5. Exit")
        choice = input("Select menu: ")
        
        if choice == "1":
            print("-" * 50)
            # Print everything in x
            for k in x:
                print(f"ID: {k} | Name: {x[k]['n']} | Stock: {x[k]['q']} | Price: {x[k]['p']} THB | Type: {x[k]['c']}")
            print("-" * 50)
            
        elif choice == "2":
            a = input("Enter ID: ")
            b = input("Enter Name: ")
            qty = int(input("Enter Qty: ")) # [INV-5] เปลี่ยนตัวแปร c เป็น qty เพื่อไม่ให้สับสนกับ key "c"
            d = float(input("Enter Price: "))
            e = input("Enter Category: ")
            
            # This logic updates or creates
            if a in x:
                # if already have, just add qty? or overwrite? Let's overwrite!
                x[a] = {"n": b, "q": qty, "p": d, "c": e} # [INV-5] ใช้ qty แทน c
            else:
                x[a] = {"n": b, "q": qty, "p": d, "c": e} # [INV-5] ใช้ qty แทน c
            save()
            print("Done.")
            
        elif choice == "3":
            # Cut stock
            id_to_cut = input("Enter product ID to cut stock: ")
            if id_to_cut in x:
                amt = int(input("How many items out?: "))
                if x[id_to_cut]['q'] >= amt:
                    x[id_to_cut]['q'] = x[id_to_cut]['q'] - amt
                    save()
                    print("Stock updated.")
                    # Check if running low
                    if x[id_to_cut]['q'] < 5:
                        print("!!! WARNING: ITEM IS RUNNING VERY LOW IN STOCK !!!")
                else:
                    print("Error: Not enough stock!")
            else:
                print("Product not found!")
                
        elif choice == "4":
            # Calculate total value and show some alert
            total_items = 0
            total_val = 0.0
            low_stock_list = []
            
            for k in x:
                total_items += 1
                total_val += x[k]['q'] * x[k]['p']
                if x[k]['q'] < 10:
                    low_stock_list.append(x[k]['n'])
                    
            print(f"Total product types: {total_items}")
            print(f"Total inventory value: {total_val} THB")
            print(f"Alert low stock (<10): {', '.join(low_stock_list)}")
            
        elif choice == "5":
            print("Bye")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()