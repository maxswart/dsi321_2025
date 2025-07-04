# DSI321: ระบบเตือนภัยไฟป่า (Wildfire Alert System)  
## โครงการร่วมรายวิชา DSI324: การจัดการข้อมูลเชิงปฏิบัติ

## บทนำโครงการ  
โครงการนี้มีวัตถุประสงค์เพื่อพัฒนาระบบตรวจจับและแจ้งเตือนไฟป่าในประเทศไทย โดยรวบรวมข้อมูลจากหลายแหล่งเพื่อช่วยสนับสนุนการตัดสินใจของหน่วยงานที่เกี่ยวข้องกับภัยพิบัติ ระบบนี้ออกแบบให้สามารถทำงานได้ใกล้เคียงแบบเรียลไทม์ และจัดการข้อมูลอย่างเป็นระบบตามแนวทางของ Data Governance พร้อมทั้งประยุกต์ใช้ Machine Learning เพื่อการวิเคราะห์ข้อมูลเชิงลึกและพยากรณ์ความเสี่ยงของไฟป่า

## โครงสร้างระบบโดยรวม
ระบบมีการทำงานแบบอัตโนมัติผ่านกระบวนการ ETL (Extract – Transform – Load) ซึ่งควบคุมด้วย Prefect โดยแบ่งออกเป็นขั้นตอนหลักดังนี้:

### ขั้นตอนที่ 1: ดึงข้อมูล (Extract)  
- OpenWeatherAPI: ใช้สำหรับดึงข้อมูลสภาพอากาศ เช่น อุณหภูมิ ความชื้น และความเร็วลม  
- NASA FIRMS: ให้ข้อมูลจุดความร้อนจากภาพถ่ายดาวเทียม ซึ่งสามารถใช้ในการคาดการณ์จุดที่มีแนวโน้มเกิดไฟป่า

### ขั้นตอนที่ 2: แปลงข้อมูล (Transform)  
- ทำความสะอาดข้อมูล และรวมชุดข้อมูลจากทั้งสองแหล่งให้อยู่ในรูปแบบที่วิเคราะห์ได้  
- ข้อมูลเริ่มต้นจัดเก็บในรูปแบบ CSV ก่อนจะแปลงเป็น Parquet เพื่อประสิทธิภาพในการจัดเก็บและวิเคราะห์

### ขั้นตอนที่ 3: โหลดและแสดงผล (Load & Visualize)  
- ใช้ Prefect เพื่อจัดการการทำงานของระบบทั้งหมดแบบอัตโนมัติ  
- จัดเก็บข้อมูลใน LakeFS ซึ่งรองรับการจัดการเวอร์ชันของข้อมูล  
- แสดงผลข้อมูลผ่าน Streamlit พร้อมแผนที่อินเทอร์แอคทีฟด้วย GeoPandas และ Folium

## รายละเอียดตามเกณฑ์การให้คะแนน  

### ส่วนที่ 1: ผลงานทางเทคนิค (90 คะแนน)

#### ✅ การตั้งค่า Repository (10 คะแนน)  
- ใช้ GitHub Repository ชื่อ dsi321_2025 สร้างภายในสัปดาห์แรกของภาคเรียน

#### ✅ ความถี่ในการ Commit (10 คะแนน)  
- มีการ commit อย่างสม่ำเสมอ อย่างน้อย 5 ครั้งต่อสัปดาห์ ติดต่อกัน 3 สัปดาห์  

#### ✅ คุณภาพของ README (10 คะแนน)  
- README นี้มีความยาวเกิน 1,000 ตัวอักษร และครอบคลุมรายละเอียดของโครงการตั้งแต่โครงสร้างระบบ วิธีดำเนินการ และการตอบเกณฑ์ประเมินทั้งหมด  

#### ✅ คุณภาพของชุดข้อมูล (50 คะแนน)

| รายการประเมิน | รายละเอียด |
|--|--|
| โครงสร้าง Schema | ใช้ไฟล์รูปแบบ Parquet แบบ Partitioned ที่จัดการ schema ชัดเจน และมีการกำหนดคอลัมน์ด้วย dtype ที่ถูกต้อง |
| จำนวน Record ≥ 1,000 | ระบบดึงข้อมูลทุก 15 นาที สามารถสะสมข้อมูลได้มากกว่า 1,000 รายการภายในระยะเวลาโครงการ |
| ข้อมูลครอบคลุม ≥ 24 ชั่วโมง | การดึงข้อมูลแบบต่อเนื่อง ทำให้มีข้อมูลครอบคลุมในช่วงเวลา 24 ชั่วโมงขึ้นไป |
| ความสมบูรณ์ ≥ 90% | มีการตรวจสอบค่าที่หายและค่าผิดปกติในกระบวนการแปลงข้อมูลอัตโนมัติ |
| ไม่มี object dtype | ข้อมูลเก็บในรูปแบบ Parquet โดยระบุชนิดข้อมูลอย่างชัดเจน เช่น float, int, datetime |
| ไม่มีข้อมูลซ้ำ | มีการลบข้อมูลซ้ำระหว่างขั้นตอน preprocessing โดย Prefect |

ข้อมูลที่จัดเก็บแยกเป็น 3 โฟลเดอร์:
- df_thai: จุดความร้อนจาก FIRMS (ผ่าน firm.py)
- df_weather: ข้อมูลอากาศจาก OpenWeatherAPI (ผ่าน apiweatherdeploy.py)
- shape_file: ข้อมูลภูมิประเทศ ดาวน์โหลดจากแหล่งเปิด

### ส่วนที่ 2: รายงานโครงการ (10 คะแนน)

#### ✅ การนำเสนอข้อมูลด้วยภาพ (5 คะแนน)
- ใช้ Streamlit แสดงข้อมูลแผนที่จุดความร้อนแบบอินเทอร์แอคทีฟผ่าน Folium
- แสดงผลเป็น Heatmap โดยพิจารณาจากความเข้มของแสง (brightness) และจำนวนจุดความร้อน

#### ✅ การใช้ Machine Learning (5 คะแนน)
- ใช้ Random Forest วิเคราะห์ความสัมพันธ์ระหว่างข้อมูลสภาพอากาศ (เช่น ความชื้น อุณหภูมิ ลม) กับความรุนแรงของจุดไฟ
- วิเคราะห์ Feature Importance และความสัมพันธ์ของตัวแปรแบบ Correlation Matrix
- แสดงผลผ่านกราฟ scatter และตารางวิเคราะห์ พร้อมคำอธิบายการแปรผล

