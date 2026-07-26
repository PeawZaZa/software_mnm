import json
import os

# global variables
db = "data.json"
LOW_STOCK = 10 # แก้ไข: เพิ่มตัวแปรคงที่สำหรับกำหนดเกณฑ์สต๊อกต่ำ (ใช้ร่วมกันทั้งเมนู 3 และเมนู 4 เพื่อแก้ INV-9)

def load(inventory):
    """โหลดข้อมูลจากไฟล์ JSON หากไฟล์เสียหรือไม่มีจะโหลดค่าเริ่มต้น"""
    if os.path.exists(db):
        try: # [INV-10] เพิ่ม try/except สำหรับอ่านไฟล์
            with open(db, 'r') as f:
                inventory.update(json.load(f))
        except Exception: # [INV-10] ถ้าไฟล์เสียหรืออ่านไม่ได้ ให้โหลด default แทน
            print("Warning: Database file is corrupted. Loading default data.")
            default_data = {
                "101": {"n": "Mama Noodles", "q": 50, "p": 6.0, "c": "Food"},
                "102": {"n": "Lactasoy Milk", "q": 20, "p": 12.0, "c": "Drink"},
                "103": {"n": "Singha Water", "q": 100, "p": 10.0, "c": "Drink"}
            }
            inventory.update(default_data)
    else:
        # default data if file not found
        default_data = {
            "101": {"n": "Mama Noodles", "q": 50, "p": 6.0, "c": "Food"},
            "102": {"n": "Lactasoy Milk", "q": 20, "p": 12.0, "c": "Drink"},
            "103": {"n": "Singha Water", "q": 100, "p": 10.0, "c": "Drink"}
        }
        inventory.update(default_data)

def save(inventory):
    """[INV-11] ทำ Atomic write ผ่าน tmp file เพื่อป้องกันไฟล์เสียระหว่างเซฟ"""
    temp_db = db + ".tmp"
    try:
        with open(temp_db, 'w') as f:
            json.dump(inventory, f)
        os.replace(temp_db, db) # [INV-11] replace ไฟล์ต้นฉบับเมื่อเขียนเสร็จสมบูรณ์
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    inventory = {} # ประกาศตัวแปรรับข้อมูลแทนการใช้ global x
    load(inventory)
    
    while True:
        print("\n=== INVENTORY SYSTEM v1.0 ===")
        print("1. Show all")
        print("2. Add or Update")
        print("3. Out")
        print("4. Inventory Summary") # [INV-12] เปลี่ยนชื่อจาก Check Check เป็น Inventory Summary
        print("5. Exit")
        choice = input("Select menu: ")
        
        if choice == "1":
            print("-" * 50)
            for k in inventory:
                print(f"ID: {k} | Name: {inventory[k]['n']} | Stock: {inventory[k]['q']} | Price: {inventory[k]['p']} THB | Type: {inventory[k]['c']}")
            print("-" * 50)
            
        elif choice == "2":
            a = input("Enter ID: ")
            b = input("Enter Name: ")
            
            # [INV-6] เพิ่ม try/except ดักผู้ใช้พิมพ์ผิด & [INV-5] ใช้ตัวแปร qty แทน c
            try:
                qty = int(input("Enter Qty: ")) 
                d = float(input("Enter Price: "))
            except ValueError:
                print("Invalid input: Qty and Price must be numbers.")
                continue
                
            e = input("Enter Category: ")
            
            # This logic updates or creates
            # แก้ไข: ลบ if/else ที่ทำงานเหมือนกันทิ้ง (INV-8) และเขียนทับ/สร้างใหม่ไปเลย
            inventory[a] = {"n": b, "q": qty, "p": d, "c": e}
            save(inventory)
            print("Done.")
            
        elif choice == "3":
            # Cut stock
            id_to_cut = input("Enter product ID to cut stock: ")
            if id_to_cut in inventory:
                # [INV-6] ดักการรับค่าตัวอักษร
                try:
                    amt = int(input("How many items out?: "))
                except ValueError:
                    print("Invalid input: Amount must be a number.")
                    continue
                
                # fix(menu3): reject negative and zero amount input [INV-7]
                if amt <= 0:
                    print("Error: Amount must be greater than zero!")
                    continue
                    
                if inventory[id_to_cut]['q'] >= amt:
                    inventory[id_to_cut]['q'] -= amt
                    save(inventory)
                    print("Stock updated.")
                    # Check if running low
                    if inventory[id_to_cut]['q'] < LOW_STOCK: # แก้ไข: ใช้ค่าคงที่ LOW_STOCK แทนตัวเลข 5 (แก้ INV-9: เกณฑ์ไม่ตรงกันระหว่างเมนู 3 และเมนู 4)
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
            
            for k in inventory:
                total_items += 1
                total_val += inventory[k]['q'] * inventory[k]['p']
                if inventory[k]['q'] < LOW_STOCK: # แก้ไข: ใช้ค่าคงที่ LOW_STOCK แทนตัวเลข 10
                    low_stock_list.append(inventory[k]['n'])
                    
            print(f"Total product types: {total_items}")
            print(f"Total inventory value: {total_val} THB")
            print(f"Alert low stock (<{LOW_STOCK}): {', '.join(low_stock_list)}") # แก้ไข: ดึงค่า LOW_STOCK มาแสดงในข้อความแจ้งเตือน
            
        elif choice == "5":
            print("Bye")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()