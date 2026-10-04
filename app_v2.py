import csv
import json
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

# path ของไฟล์ข้อมูล — ค่าคงที่ระดับโมดูล (ไม่ใช่ global state ที่ถูกแก้ระหว่างรัน)
# test ใช้ monkeypatch เปลี่ยนค่านี้ได้ เพราะทุกคลาสอ่านค่าตอนสร้าง instance
db = "data.json"

SAVE_FAILED_MESSAGE = "Error: could not save data to disk. No changes were made."
ENV_FILE = ".env"


def _parse_env_line(line):
    """คืน (key, value) จากบรรทัด KEY=VALUE หรือ None ถ้าเป็นบรรทัดว่าง/คอมเมนต์/ไม่มี ="""
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        return None
    key, value = (part.strip() for part in line.split("=", 1))
    return (key, value.strip("\"'")) if key else None


def load_env_file(path=ENV_FILE):
    """
    [W13] อ่านไฟล์ .env (บรรทัดละ KEY=VALUE) เข้า os.environ — ไม่ใช้ไลบรารีภายนอก
    ค่าที่ตั้งไว้ใน environment อยู่แล้วจะไม่ถูกทับ เพื่อให้สั่งค่าชั่วคราวจาก command line ได้
    """
    env_path = Path(path)
    if not env_path.is_file():
        return {}
    loaded = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        pair = _parse_env_line(line)
        if pair is not None and pair[0] not in os.environ:
            key, value = pair
            os.environ[key] = value
            loaded[key] = value
    return loaded


@dataclass
class Settings:
    """[W13] ค่าที่ผันแปรตามเครื่อง แยกออกจากโค้ด (Twelve-Factor App ข้อ III: Config)"""

    db_path: Path
    export_dir: Path | None = None

    @classmethod
    def from_env(cls, environ=None):
        environ = os.environ if environ is None else environ
        export_dir = environ.get("REPORT_EXPORT_DIR")
        return cls(
            db_path=Path(environ.get("INVENTORY_DB_PATH") or db),
            export_dir=Path(export_dir) if export_dir else None,
        )

    def prepare_directories(self):
        """สร้างโฟลเดอร์ข้อมูลและโฟลเดอร์รายงานถ้ายังไม่มี (ทำครั้งเดียวตอนเปิดโปรแกรม)"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if self.export_dir is not None:
            self.export_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class Product:
    """[SAM1-28] สินค้า 1 รายการ — แทนที่ dict {"n","q","p","c"} แบบเดิม"""

    id: str
    name: str
    qty: int
    price: float
    category: str
    barcode: str = ""       # [CR-01] รหัสบาร์โค้ด — ว่างได้ สินค้าเดิมยังไม่มี
    reorder_point: int = 0  # [CR-01] จุดสั่งซื้อซ้ำ เกณฑ์รายชิ้น

    def to_dict(self):
        """คืนรูปแบบ key ย่อเดิม เพื่อให้ data.json ที่มีอยู่ยังใช้ได้ ไม่ต้อง migrate"""
        return {
            "n": self.name, "q": self.qty, "p": self.price, "c": self.category,
            "b": self.barcode, "r": self.reorder_point,  # [CR-01]
        }

    @property
    def stock_value(self):
        """[W11 Feature Envy] มูลค่าคงคลังของสินค้าชิ้นนี้ — คำนวณที่เจ้าของข้อมูล"""
        return self.qty * self.price

    def needs_reorder(self):
        """[W11 Feature Envy] ถึงจุดสั่งซื้อซ้ำหรือยัง (reorder_point = 0 คือไม่ได้ตั้งค่า)"""
        return self.reorder_point > 0 and self.qty <= self.reorder_point

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
            # [CR-01] key b/r ไม่มีใน data.json เดิม จึงต้องมีค่า default
            barcode=str(data.get("b", "")),
            reorder_point=int(data.get("r", 0)),
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

    @property
    def backup_path(self):
        """[W14] สำเนาสำรองย้อนหลัง 1 ก้าว — ถูกเขียนก่อนบันทึกทุกครั้ง"""
        return self.path.with_name(self.path.name + ".bak")

    @staticmethod
    def _read_json_object(path):
        """อ่านไฟล์ที่ต้องเป็น JSON object คืน dict หรือ None ถ้าไม่มีไฟล์/อ่านไม่ได้/ผิดรูปแบบ"""
        # [W11] ระบุ exception ให้เจาะจง — json.JSONDecodeError เป็น subclass ของ ValueError
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            return None
        return raw if isinstance(raw, dict) else None

    def _load_raw(self):
        """
        [INV-10] ไฟล์เสียต้องไม่ทำให้โปรแกรมตาย
        [W14] ไฟล์หลักเสียหรือหายไป → กู้จาก .bak อัตโนมัติก่อน ค่อยถอยไปใช้ข้อมูลตั้งต้น
        """
        if not self.path.exists() and not self.backup_path.exists():
            return self.DEFAULT_DATA  # เปิดครั้งแรก ยังไม่เคยมีข้อมูล
        raw = self._read_json_object(self.path)
        if raw is not None:
            return raw
        problem = "is corrupted" if self.path.exists() else "is missing"
        backup = self._read_json_object(self.backup_path)
        if backup is not None:
            print(f"Warning: Database file {problem}. "
                  f"Restored data from backup {self.backup_path.name}.")
            return backup
        print(f"Warning: Database file {problem}. Loading default data.")
        return self.DEFAULT_DATA

    def load(self):
        """โหลดข้อมูลเป็น dict[str, Product]"""
        raw = self._load_raw()
        inventory = {}
        for pid, item in raw.items():
            try:
                inventory[pid] = Product.from_dict(pid, item)
            except (ValueError, TypeError, AttributeError):
                # [#22] ข้อมูลเสียแถวเดียวต้องไม่ทำให้เปิดโปรแกรมไม่ได้ทั้งระบบ
                print(f"Warning: skipping corrupted row '{pid}' in {self.path.name}.")
        return inventory

    def save(self, inventory):
        """
        [INV-11] Atomic write: เขียนลงไฟล์ชั่วคราวให้เสร็จก่อน แล้วสลับด้วย os.replace()
        ผลคือไฟล์จริงจะเป็นข้อมูลใหม่ทั้งหมด หรือข้อมูลเดิมทั้งหมด ไม่มีสภาพครึ่ง ๆ กลาง ๆ

        [W11] คืนค่า True/False แทนการกลืน error เงียบ ๆ เพื่อให้ชั้น service รู้ว่าบันทึกไม่สำเร็จ
        """
        payload = {pid: product.to_dict() for pid, product in inventory.items()}
        directory = self.path.parent
        temp_name = None
        try:
            # ไฟล์ชั่วคราวต้องอยู่โฟลเดอร์เดียวกับไฟล์จริง os.replace() จึงเป็น atomic
            fd, temp_name = tempfile.mkstemp(
                prefix=self.path.name + ".", suffix=".tmp", dir=directory
            )
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())  # ให้ข้อมูลลงดิสก์จริงก่อนสลับไฟล์
            # [W14] Rolling backup: เก็บไฟล์เดิมไว้ 1 ก้าว — ข้ามถ้าไฟล์เดิมเสีย
            # เพื่อไม่ให้ไฟล์เสียไปทับสำเนาดีที่เพิ่งใช้กู้ข้อมูล
            if self._read_json_object(self.path) is not None:
                shutil.copy2(self.path, self.backup_path)
            os.replace(temp_name, self.path)
            return True
        except OSError as e:
            print(f"Error saving data: {e}")
            if temp_name and os.path.exists(temp_name):
                os.remove(temp_name)  # ไม่ทิ้งไฟล์ .tmp ค้างไว้
            return False


class InventoryService:
    """[SAM1-34] business logic ทั้งหมด — ไม่ยุ่งกับ input/print และไม่ยุ่งกับไฟล์โดยตรง"""

    LOW_STOCK = 10  # [INV-9] เกณฑ์เดียวใช้ร่วมกันทั้งเมนู 3 และเมนู 4

    def __init__(self, repository):
        self.repository = repository
        self.inventory = repository.load()

    def validate(self, qty, price, reorder_point=0):
        """ตรวจค่าก่อนบันทึก คืน (ok, error_message)"""
        if qty < 0:
            return False, "Invalid input: Qty must not be negative."
        if price < 0:
            return False, "Invalid input: Price must not be negative."
        # [#21] จุดสั่งซื้อซ้ำติดลบไม่มีความหมาย และเคยถูกบันทึกแล้วละเลยเงียบๆ
        if reorder_point < 0:
            return False, "Invalid input: Reorder Point must not be negative."
        return True, ""

    def _products_with_barcode(self, barcode):
        """[W11 Duplicate Code] จุดเดียวที่วนหาสินค้าจากบาร์โค้ด (บาร์โค้ดว่างไม่นับว่าตรงกัน)"""
        if not barcode:
            return []
        return [p for p in self.inventory.values() if p.barcode == barcode]

    def _barcode_owner(self, barcode, exclude_id):
        """[#20] คืน id ของสินค้าตัวอื่นที่ใช้บาร์โค้ดนี้อยู่"""
        for product in self._products_with_barcode(barcode):
            if product.id != exclude_id:
                return product.id
        return None

    def add_update(self, product_id, name, qty, price, category,
                   barcode="", reorder_point=0):
        """[INV-8] เพิ่มหรือแก้ไขสินค้า — เขียนทับเสมอ ไม่บวกสะสม"""
        ok, message = self.validate(qty, price, reorder_point)
        if not ok:
            return False, message
        # [#20] กันสินค้าคนละตัวใช้บาร์โค้ดเดียวกัน จนค้นหาแล้วเจอผิดตัว
        owner = self._barcode_owner(barcode, product_id)
        if owner is not None:
            return False, f"Error: Barcode {barcode} is already used by product {owner}."
        previous = self.inventory.get(product_id)
        self.inventory[product_id] = Product(
            product_id, name, qty, price, category, barcode, reorder_point
        )
        if not self.repository.save(self.inventory):
            # [W11] บันทึกไม่สำเร็จ → ย้อนข้อมูลในหน่วยความจำ ให้ตรงกับไฟล์บนดิสก์
            if previous is None:
                del self.inventory[product_id]
            else:
                self.inventory[product_id] = previous
            return False, SAVE_FAILED_MESSAGE
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
        if not self.repository.save(self.inventory):
            product.qty += amt  # [W11] ย้อนกลับ เพราะไฟล์บนดิสก์ยังเป็นค่าเดิม
            return False, SAVE_FAILED_MESSAGE
        message = "Stock updated."
        if product.qty < self.LOW_STOCK:
            message += " !!! WARNING: ITEM IS RUNNING VERY LOW IN STOCK !!!"
        # [UAT-DEF-01] เดิมเตือนแค่เกณฑ์รวม LOW_STOCK สินค้าขายเร็วที่ตั้ง reorder point
        # สูงกว่า 10 จึงไม่เคยถูกเตือนตอนขาย ต้องเตือนตามเกณฑ์รายชิ้นด้วย
        if product.needs_reorder():
            message += (f" !!! REORDER POINT REACHED: {product.qty} left "
                        f"(reorder point {product.reorder_point}) !!!")
        return True, message

    def find_by_barcode(self, barcode):
        """[CR-01] ค้นสินค้าจากบาร์โค้ด คืน None ถ้าไม่เจอ"""
        matches = self._products_with_barcode(barcode)
        return matches[0] if matches else None

    def get_reorder_list(self):
        """[CR-01] สินค้าที่ถึงจุดสั่งซื้อซ้ำแล้ว (qty <= reorder_point ของชิ้นนั้น)"""
        return [p for p in self.inventory.values() if p.needs_reorder()]

    def get_summary(self):
        """คืน (จำนวนชนิดสินค้า, มูลค่ารวม, รายชื่อสินค้าที่สต๊อกต่ำ)"""
        total_items = len(self.inventory)
        total_val = sum(p.stock_value for p in self.inventory.values())
        low_stock_list = [p.name for p in self.inventory.values() if p.qty < self.LOW_STOCK]
        return total_items, float(total_val), low_stock_list


class CsvReportExporter:
    """[CR-02] ส่งออกรายงานสต๊อกเป็นไฟล์ CSV"""

    HEADERS = ["id", "name", "qty", "price", "category", "barcode", "reorder_point"]

    def export(self, inventory, path):
        """เขียน inventory ลงไฟล์ CSV คืนจำนวนแถวข้อมูล (ไม่นับ header)"""
        # newline="" กัน Windows แทรกบรรทัดว่างคั่นทุกแถว
        # utf-8-sig ใส่ BOM ให้ Excel อ่านภาษาไทยได้ถูกต้อง
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADERS)
            for product in inventory.values():
                writer.writerow([
                    product.id, product.name, product.qty, product.price,
                    product.category, product.barcode, product.reorder_point,
                ])
        return len(inventory)


class ConsoleUI:
    """[SAM1-37] ชั้นติดต่อผู้ใช้ — รับ input, พิมพ์ผล และ route ไปยัง service เท่านั้น"""

    def __init__(self, service, input_fn=None, print_fn=None, exporter=None,
                 export_dir=None):
        # inject input/print เพื่อให้เขียน unit test ได้โดยไม่ต้อง monkeypatch builtins
        self.service = service
        # ค่า default ผูกตอนสร้าง object ไม่ใช่ตอนนิยามคลาส — smoke test แทน input/print ได้
        self.input = input_fn if input_fn is not None else input
        self.print = print_fn if print_fn is not None else print
        self.exporter = exporter if exporter is not None else CsvReportExporter()
        self.export_dir = Path(export_dir) if export_dir is not None else None  # [W13]

    EXIT_CHOICE = "5"

    def menu(self):
        """
        [W11] ตารางเมนู เลข → (ชื่อ, handler) แทน if/elif 8 ชั้น
        ลด Cyclomatic Complexity ของ run() จาก 9 เหลือ 5
        """
        return {
            "1": ("Show all", self.handle_show),
            "2": ("Add or Update", self.handle_add),
            "3": ("Out", self.handle_out),
            "4": ("Inventory Summary", self.handle_summary),  # [INV-12] เดิมชื่อ Check Check
            self.EXIT_CHOICE: ("Exit", None),
            "6": ("Reorder List", self.handle_reorder),  # [CR-01]
            "7": ("Export CSV", self.handle_export),  # [CR-02]
        }

    def run(self):
        menu = self.menu()
        while True:
            self.print("")
            self.print("=== INVENTORY SYSTEM v2.0 ===")
            for key, (label, _) in menu.items():
                self.print(f"{key}. {label}")
            choice = self.input("Select menu: ")

            if choice == self.EXIT_CHOICE:
                self.print("Bye")
                break
            if choice in menu:
                menu[choice][1]()
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
        try:  # [INV-6] ดักผู้ใช้พิมพ์ตัวอักษรในช่องตัวเลข
            qty = int(self.input("Enter Qty: "))
            price = float(self.input("Enter Price: "))
        except ValueError:
            self.print("Invalid input: Qty and Price must be numbers.")
            return
        category = self.input("Enter Category: ")
        barcode = self.input("Enter Barcode (leave blank if none): ")  # [CR-01]
        try:
            reorder_point = int(self.input("Enter Reorder Point: "))
        except ValueError:
            self.print("Invalid input: Reorder Point must be a number.")
            return
        _, message = self.service.add_update(
            product_id, name, qty, price, category, barcode, reorder_point
        )
        self.print(message)

    def handle_out(self):
        product_id = self.input("Enter product ID to cut stock: ")
        try:  # [INV-6] ดักการรับค่าตัวอักษร
            amt = int(self.input("How many items out?: "))
        except ValueError:
            self.print("Invalid input: Amount must be a number.")
            return
        _, message = self.service.stock_out(product_id, amt)
        self.print(message)

    def handle_reorder(self):
        """[CR-01] แสดงรายการสินค้าที่ถึงจุดสั่งซื้อซ้ำ"""
        reorder_list = self.service.get_reorder_list()
        if not reorder_list:
            self.print("No product has reached its reorder point.")
            return
        self.print("-" * 50)
        for product in reorder_list:
            self.print(
                f"ID: {product.id} | Name: {product.name} "
                f"| Stock: {product.qty} | Reorder Point: {product.reorder_point}"
            )
        self.print("-" * 50)

    def export_path(self, raw):
        """
        [W13] ชื่อไฟล์เปล่า ๆ จะถูกวางในโฟลเดอร์รายงาน (REPORT_EXPORT_DIR)
        ส่วน path ที่ระบุโฟลเดอร์มาด้วยจะใช้ตามที่ผู้ใช้พิมพ์
        """
        path = Path(raw.strip())
        if self.export_dir is not None and path.parent == Path("."):
            return self.export_dir / path
        return path

    def handle_export(self):
        """[CR-02] ส่งออกรายงานเป็น CSV"""
        path = self.export_path(self.input("Enter output CSV path: "))
        try:
            rows = self.exporter.export(self.service.inventory, path)
        except OSError as e:
            self.print(f"Error: cannot write CSV file: {e}")
            return
        self.print(f"Exported {rows} products to {path}")

    def handle_summary(self):
        total_items, total_val, low_stock_list = self.service.get_summary()
        self.print(f"Total product types: {total_items}")
        self.print(f"Total inventory value: {total_val} THB")
        self.print(f"Alert low stock (<{self.service.LOW_STOCK}): {', '.join(low_stock_list)}")


# ── Backward-compatible wrappers ──
# test_app.py (regression suite ของ Sprint 1) ยังเรียก API ระดับโมดูลอยู่
# จึงคง signature เดิมไว้ แล้ว delegate ให้ InventoryRepository

LOW_STOCK = InventoryService.LOW_STOCK  # alias ให้โค้ด/เทสต์เดิมที่อ้าง app_v2.LOW_STOCK


def load(inventory):
    """โหลดข้อมูลเข้า dict รูปแบบเดิม (key ย่อ n/q/p/c)"""
    loaded = InventoryRepository(db).load()
    inventory.update({pid: product.to_dict() for pid, product in loaded.items()})


def save(inventory):
    """บันทึก dict รูปแบบเดิมลงไฟล์"""
    products = {pid: Product.from_dict(pid, item) for pid, item in inventory.items()}
    InventoryRepository(db).save(products)


def main():
    load_env_file()  # [W13] อ่าน .env ในโฟลเดอร์ที่สั่งรัน (ถ้ามี)
    settings = Settings.from_env()
    settings.prepare_directories()
    service = InventoryService(InventoryRepository(settings.db_path))
    ConsoleUI(service, export_dir=settings.export_dir).run()


if __name__ == "__main__":
    main()
