import json
import os
from dataclasses import dataclass
from pathlib import Path

# global variables
db = "data.json"


@dataclass
class Product:
    """[SAM1-28] สินค้า 1 รายการ — แทนที่ dict {"n","q","p","c"} แบบเดิม"""

    id: str
    name: str
    qty: int
    price: float
    category: str

    def to_dict(self):
        """คืนรูปแบบ key ย่อเดิม เพื่อให้ data.json ที่มีอยู่ยังใช้ได้ ไม่ต้อง migrate"""
        return {"n": self.name, "q": self.qty, "p": self.price, "c": self.category}

    @classmethod
    def from_dict(cls, product_id, data):
        """
        สร้าง Product จาก dict รูปแบบเดิม
        key ที่ขาดใช้ค่า default (กัน KeyError จาก legacy data ที่ไม่ครบ)
        แต่ค่าที่แปลงชนิดไม่ได้จะปล่อย ValueError ให้ชั้นบนจัดการ
        """
        return cls(
            id=str(product_id),
            name=str(data.get("n", "")),
            qty=int(data.get("q", 0)),
            price=float(data.get("p", 0.0)),
            category=str(data.get("c", "")),
        )


class InventoryRepository:
    """[SAM1-31] รับผิดชอบการอ่าน/เขียน data.json เพียงอย่างเดียว"""

    # ย้าย default data มาไว้ที่เดียว (เดิมเขียนซ้ำ 2 ที่ใน load())
    DEFAULT_DATA = {
        "101": {"n": "Mama Noodles", "q": 50, "p": 6.0, "c": "Food"},
        "102": {"n": "Lactasoy Milk", "q": 20, "p": 12.0, "c": "Drink"},
        "103": {"n": "Singha Water", "q": 100, "p": 10.0, "c": "Drink"}
    }

    def __init__(self, path=None):
        # อ่านค่า db ตอนถูกเรียก ไม่ใช่ตอนนิยามคลาส เพื่อให้ monkeypatch ใน test ทำงานได้
        self.path = Path(path if path is not None else db)

    def load(self):
        """โหลดข้อมูลเป็น dict[str, Product] หากไฟล์เสียหรือไม่มีจะใช้ค่าเริ่มต้น"""
        if self.path.exists():
            try: # [INV-10] เพิ่ม try/except สำหรับอ่านไฟล์
                raw = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception: # [INV-10] ถ้าไฟล์เสียหรืออ่านไม่ได้ ให้โหลด default แทน
                print("Warning: Database file is corrupted. Loading default data.")
                raw = self.DEFAULT_DATA
        else:
            raw = self.DEFAULT_DATA
        return {pid: Product.from_dict(pid, item) for pid, item in raw.items()}

    def save(self, inventory):
        """[INV-11] ทำ Atomic write ผ่าน tmp file เพื่อป้องกันไฟล์เสียระหว่างเซฟ"""
        temp_path = Path(str(self.path) + ".tmp")
        try:
            payload = {pid: product.to_dict() for pid, product in inventory.items()}
            temp_path.write_text(json.dumps(payload), encoding="utf-8")
            os.replace(temp_path, self.path) # [INV-11] replace ไฟล์ต้นฉบับเมื่อเขียนเสร็จสมบูรณ์
        except Exception as e:
            print(f"Error saving data: {e}")


class InventoryService:
    """[SAM1-34] business logic ทั้งหมด — ไม่ยุ่งกับ input/print และไม่ยุ่งกับไฟล์โดยตรง"""

    LOW_STOCK = 10 # [INV-9] เกณฑ์เดียวใช้ร่วมกันทั้งเมนู 3 และเมนู 4

    def __init__(self, repository):
        self.repository = repository
        self.inventory = repository.load()

    def validate(self, qty, price):
        """ตรวจค่าก่อนบันทึก คืน (ok, error_message)"""
        if qty < 0:
            return False, "Invalid input: Qty must not be negative."
        if price < 0:
            return False, "Invalid input: Price must not be negative."
        return True, ""

    def add_update(self, product_id, name, qty, price, category):
        """[INV-8] เพิ่มหรือแก้ไขสินค้า — เขียนทับเสมอ ไม่บวกสะสม"""
        ok, message = self.validate(qty, price)
        if not ok:
            return False, message
        self.inventory[product_id] = Product(product_id, name, qty, price, category)
        self.repository.save(self.inventory)
        return True, "Done."

    def stock_out(self, product_id, amt):
        """ตัดสต๊อกออก คืน (success, message)"""
        product = self.inventory.get(product_id)
        if product is None:
            return False, "Product not found!"
        # [INV-7] ปฏิเสธจำนวนที่เป็นลบหรือศูนย์ ก่อนเทียบกับสต๊อกที่มี
        if amt <= 0:
            return False, "Error: Amount must be greater than zero!"
        if product.qty < amt:
            return False, "Error: Not enough stock!"

        product.qty -= amt
        self.repository.save(self.inventory)
        if product.qty < self.LOW_STOCK:
            return True, "Stock updated. !!! WARNING: ITEM IS RUNNING VERY LOW IN STOCK !!!"
        return True, "Stock updated."

    def get_summary(self):
        """คืน (จำนวนชนิดสินค้า, มูลค่ารวม, รายชื่อสินค้าที่สต๊อกต่ำ)"""
        total_items = len(self.inventory)
        total_val = sum(p.qty * p.price for p in self.inventory.values())
        low_stock_list = [p.name for p in self.inventory.values() if p.qty < self.LOW_STOCK]
        return total_items, float(total_val), low_stock_list


class ConsoleUI:
    """[SAM1-37] ชั้นติดต่อผู้ใช้ — รับ input, พิมพ์ผล และ route ไปยัง service เท่านั้น"""

    def __init__(self, service, input_fn=input, print_fn=print):
        # inject input/print เพื่อให้เขียน unit test ได้โดยไม่ต้อง monkeypatch builtins
        self.service = service
        self.input = input_fn
        self.print = print_fn

    def run(self):
        while True:
            self.print("")
            self.print("=== INVENTORY SYSTEM v2.0 ===")
            self.print("1. Show all")
            self.print("2. Add or Update")
            self.print("3. Out")
            self.print("4. Inventory Summary") # [INV-12] เปลี่ยนชื่อจาก Check Check
            self.print("5. Exit")
            choice = self.input("Select menu: ")

            if choice == "1":
                self.handle_show()
            elif choice == "2":
                self.handle_add()
            elif choice == "3":
                self.handle_out()
            elif choice == "4":
                self.handle_summary()
            elif choice == "5":
                self.print("Bye")
                break
            else:
                self.print("Invalid choice, try again.")

    def handle_show(self):
        self.print("-" * 50)
        for product in self.service.inventory.values():
            self.print(
                f"ID: {product.id} | Name: {product.name} | Stock: {product.qty} "
                f"| Price: {product.price} THB | Type: {product.category}"
            )
        self.print("-" * 50)

    def handle_add(self):
        product_id = self.input("Enter ID: ")
        name = self.input("Enter Name: ")
        try: # [INV-6] ดักผู้ใช้พิมพ์ตัวอักษรในช่องตัวเลข
            qty = int(self.input("Enter Qty: "))
            price = float(self.input("Enter Price: "))
        except ValueError:
            self.print("Invalid input: Qty and Price must be numbers.")
            return
        category = self.input("Enter Category: ")
        _, message = self.service.add_update(product_id, name, qty, price, category)
        self.print(message)

    def handle_out(self):
        product_id = self.input("Enter product ID to cut stock: ")
        try: # [INV-6] ดักการรับค่าตัวอักษร
            amt = int(self.input("How many items out?: "))
        except ValueError:
            self.print("Invalid input: Amount must be a number.")
            return
        _, message = self.service.stock_out(product_id, amt)
        self.print(message)

    def handle_summary(self):
        total_items, total_val, low_stock_list = self.service.get_summary()
        self.print(f"Total product types: {total_items}")
        self.print(f"Total inventory value: {total_val} THB")
        self.print(f"Alert low stock (<{self.service.LOW_STOCK}): {', '.join(low_stock_list)}")


# ── Backward-compatible wrappers ──
# test_app.py (regression suite ของ Sprint 1) ยังเรียก API ระดับโมดูลอยู่
# จึงคง signature เดิมไว้ แล้ว delegate ให้ InventoryRepository

LOW_STOCK = InventoryService.LOW_STOCK # alias ให้โค้ด/เทสต์เดิมที่อ้าง app_v2.LOW_STOCK

def load(inventory):
    """โหลดข้อมูลเข้า dict รูปแบบเดิม (key ย่อ n/q/p/c)"""
    loaded = InventoryRepository(db).load()
    inventory.update({pid: product.to_dict() for pid, product in loaded.items()})

def save(inventory):
    """บันทึก dict รูปแบบเดิมลงไฟล์"""
    products = {pid: Product.from_dict(pid, item) for pid, item in inventory.items()}
    InventoryRepository(db).save(products)

def main():
    ConsoleUI(InventoryService(InventoryRepository(db))).run()


if __name__ == "__main__":
    main()
