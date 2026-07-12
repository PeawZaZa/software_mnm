# System Architecture Document
## Project: Inventory System
**Version:** 1.1

----

### 1. ภาพรวมของระบบ (System Overview)
ระบบ Inventory System เป็นแอปพลิเคชันประเภท Command Line Interface (CLI) ที่พัฒนาด้วยภาษา Python เพื่อใช้จัดการคลังสินค้าขนาดเล็ก ตัวระบบเน้นความเรียบง่ายและทำงานแบบ Standalone รองรับการทำงานพื้นฐาน เช่น การดูรายการสินค้า, การเพิ่ม/แก้ไขข้อมูล, การตัดสต๊อก, และการสรุปมูลค่าคลังสินค้า

### 2. สถาปัตยกรรมข้อมูล (Data Architecture)
* **Data Structure:** ข้อมูลจะถูกโหลดขึ้นมาทำงานในหน่วยความจำ (In-Memory) ด้วยโครงสร้างข้อมูลแบบ Dictionary (`dict`) โดยใช้รหัสสินค้า (Product ID) เป็น Key หลัก
* **Data Schema:** ```json
  "Product_ID": {
      "n": "ชื่อสินค้า (Name)",
      "q": จำนวนคงเหลือ (Quantity - Int),
      "p": ราคา (Price - Float),
      "c": หมวดหมู่ (Category)
  }
Data Persistence: ระบบใช้ Text-based storage โดยเขียน/อ่านข้อมูลจากไฟล์ data.json โดยตรง

3. โครงสร้างคอมโพเนนต์ (System Components)
ระบบถูกออกแบบให้ลดการพึ่งพาสถานะส่วนกลาง (Global State) โดยแบ่งการทำงานออกเป็น 3 ส่วนหลัก:

State & Event Controller (main)

ทำหน้าที่เป็น Application Entry Point และจัดการ Event Loop (UI/Menu)

เป็นจุดประกาศตัวแปร State หลัก (inventory = {}) และส่งผ่านพารามิเตอร์ตัวนี้ไปยังฟังก์ชันอื่นๆ (Dependency Injection) เพื่อป้องกัน Side Effects

File I/O Services (load, save)

load(inventory): ดึงข้อมูลจากไฟล์ data.json หากไม่พบไฟล์จะทำการ Inject ข้อมูลพื้นฐาน (Default Data) เข้าไปในระบบแทน

save(inventory): อัปเดตสถานะของ Inventory จากหน่วยความจำลงสู่ไฟล์ JSON (ทำงานแบบ Overwrite)

Business Logic Layer (ภายในเมนูย่อย)

Stock Management: จัดการคำนวณการบวก/ลบสินค้าแบบ Real-time พร้อม Validation แจ้งเตือนเมื่อสต๊อกไม่พอ

Alert System: ระบบแจ้งเตือนสต๊อกต่ำ ควบคุมด้วยค่าคงที่ส่วนกลาง LOW_STOCK = 10 เพื่อให้ทุกโมดูลประเมินผลผ่านเกณฑ์เดียวกัน

4. สรุปการปรับปรุงจากเวอร์ชันก่อนหน้า (v1.1 Changes)
Eliminate Global State: ยกเลิกการใช้ global x และปรับให้ฟังก์ชันรับพารามิเตอร์แทน เพิ่มความปลอดภัยให้กับข้อมูลในระบบ

Logic Streamlining: แก้ไขปัญหาการใช้เงื่อนไขแบบ Dead Code ในระบบ Add/Update สินค้า

Single Source of Truth: รวมศูนย์เกณฑ์การแจ้งเตือนสต๊อกต่ำให้เป็นมาตรฐานเดียวกันทั้งระบบ (INV-9)