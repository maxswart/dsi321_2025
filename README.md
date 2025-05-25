# DSI321_wildfire
This project included 2 data folder
- **df_thai** this folder contained heat spot location which come form **firm.py** then keep it as Hive-partition in parquet format
- **shape_file** can download from [here](https://data.humdata.org/dataset/d24bdc45-eb4c-4e3d-8b16-44db02667c27/resource/d0c722ff-6939-4423-ac0d-6501830b1759/download/tha_adm_rtsd_itos_20210121_shp.zip)
Okay, here is a draft markdown for a `README.md` file, designed to address the specified grading criteria based *only* on the information provided in the source excerpts and our conversation history.


# Project Assessment Summary based on Report Excerpts

The project focuses on developing a wildfire alert system to monitor the situation in Thailand in near real-time and support the National Disaster Management Subcommittee. This report details aspects of the system, its data governance framework, and technical outcomes.


### Part 1: Technical Work (90 points)

This section assesses the technical implementation and data quality.

#### Repository Setup (10 points)

*   The source material indicates the project is part of the **"DSI321 PRACTICAL DATA GOVERNANCE PROJECT"**.
*   GitHub Repository name: dsi321_2025

#### Quality of Dataset (50 points)

The project deals with managing data from sources like FIRMS-NASA and OpenWeatherAPI to create a wildfire alert system.

*   **Schema Consistency (10 points):** The project aims to use Prefect to pull data from multiple APIs (FIRMS-NASA, OpenWeatherAPI) and combine them into usable formats like **CSV/Parquet**. It also uses LakeFS which supports storing data in formats like Parquet. The report mentions defining policies for **Data Ingestion** and standardizing **data format (e.g., CSV, Parquet, GeoJSON)**, unit of measurement, and geographic coordinates. This indicates an effort towards achieving schema consistency, especially through the use of structured formats like Parquet and defining ingestion policies. However, the sources do not provide the specific target schema definition or explicitly state that the schema consistency meets a particular criterion.
*   **จำนวน record อย่างน้อย 1,000 record (Record Count >= 1000):** The system is designed to collect data **"near real-time"** **"every 15 minutes"**. It is also mentioned that LakeFS is used for storing **"large-scale data"** (ข้อมูลขนาดใหญ่). While the system is designed for frequent data collection and managing large data volumes, the provided report excerpts **do not explicitly state the total number of records collected or used for the project's analysis or system demonstration**, or confirm that it exceeds 1,000 records. The example datasets shown in the images are small subsets.
*   **ครอบคลุมช่วงเวลา 24 ชั่วโมง (Time Coverage 24 hours):** The system collects data **"near real-time"** **"every 15 minutes"** and offers **"flexible selection of the time period"** for data inspection. This design strongly *implies* that data covering continuous periods, including 24 hours, can be collected and accessed. However, the sources **do not explicitly state that data covering a specific 24-hour period was successfully collected and utilized** for the results presented in the report excerpts.
*   **ความสมบูรณ์ของข้อมูล 90% (Data Completeness 90%):** **Data Quality** is identified as a key value of Data Governance. The project lists **"Quality of Data (Data Quality Rate)"** as a KPI for Data Integration, with the goal that data should be **"complete (no Missing/Corrupt)"**. Defining **"standard data quality and verification mechanisms"** is a goal for Data Storage & Operations, explicitly mentioning **"completeness (Completeness)"** as a standard. This demonstrates the *intent* and *mechanisms* for ensuring data completeness. However, the sources **do not provide a specific percentage of data completeness that was achieved**, or confirm it meets or exceeds 90%.
*   **ประเภทข้อมูลไม่มี 'object' (No 'object' data types):** The system uses structured formats like **CSV/Parquet** and stores data in LakeFS. It uses libraries like Geopandas for geographical data handling. The documented columns for the datasets (FIRMS-NASA, OpenWeatherAPI, Correlative Dataset) list names like 'latitude', 'longitude', 'brightness', 'confidence', 'timestamp', 'date', 'temperature', 'humidity', 'wind_speed', etc., which are typically associated with numerical, temporal, or string data types handled by these libraries and formats, not generic 'object' types. However, the sources **do not explicitly state that 'object' data types were specifically avoided** or confirm this criterion was met.
*   **ไม่มีข้อมูลซ้ำ (No duplicate data):**
![Info Dataframe FIRMSNASA](image/fire.png)
![Info Dataframe OpenWeatherApi](image/weather.png)


### Part 2: รายงานโครงการ (10 points)

This section assesses aspects presented in the report.

#### การนำเสนอข้อมูลด้วยภาพ (Data Visualization) (5 คะแนน)

*   The project objective includes displaying the wildfire situation on an **"interactive map"** (แผนที่เชิงโต้ตอบ).
*   The report details using **Folium for rendering the map**.
*   It describes displaying results as a **Heatmap** based on the number and brightness of fire points.
*   **Image 7-2** shows a diagram explicitly labeling **"Heat Map"** as a feature.
*   The project is explicitly presented as part of the **DSI324** course.
*   This strongly demonstrates the creation of clear and meaningful visualizations related to the course topic.

#### การใช้ Machine Learning (Using Machine Learning) (5 คะแนน)

*   The project explicitly states using **"MACHINE LEARNING (RANDOM FOREST)"** to find the relationship between weather conditions and fire hotspots.
*   It specifically details using **Random Forest** to analyze the relationship between the brightness of hotspots and weather variables (Temperature, Humidity, Wind speed).
*   The report includes performing **Feature Importance** analysis on the model.
*   The report presents and **explains the results** through a Correlation Matrix Heatmap/Table, and Scatter Plots showing the relationship between confidence/weather variables and Brightness. Detailed interpretations of these results are provided.
*   This demonstrates the use of an ML technique (Random Forest), provides explanation of the results, and is clearly related to the project topic within the **DSI324** course context. Although the criterion mentioned Linear Regression as an example, Random Forest is a valid ML technique demonstrated and explained in the sources.

```
