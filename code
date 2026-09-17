Yes — you mean you want the **code added into the README content you already have**, not a separate document.

For GitHub, put the following **complete content into `README.md`**. It includes the project description plus the question-wise code.

````markdown
# 📱 Real-Time Accelerometer Data Pipeline

A real-time data streaming project that collects accelerometer data from a smartphone using **Phyphox**, sends the data through **Apache Kafka**, consumes it using **Python**, and stores the readings in **PostgreSQL**.

## 🔄 Architecture

```text
Phyphox (Smartphone)
        ↓
Python Accelerometer Function
        ↓
Kafka Producer
        ↓
Apache Kafka
        ↓
Kafka Consumer
        ↓
Database Insert Function
        ↓
PostgreSQL
````

## 🛠️ Technologies Used

* Python
* Phyphox
* Apache Kafka 4.3.1
* PostgreSQL 18.6
* kafka-python
* psycopg
* requests

## 📂 Project Structure

```text
real_time_analytics/
│
├── accelerometer.py
├── producer.py
├── consumer.py
└── README.md
```

---

# 1. Receive Accelerometer Data

### File: `accelerometer.py`

```python
import requests

PHYphox_URL = "http://10.124.165.81:8080/get?accX&accY&accZ"

def get_accelerometer_data():
    response = requests.get(PHYphox_URL)
    data = response.json()

    x = data["buffer"]["accX"]["buffer"][0]
    y = data["buffer"]["accY"]["buffer"][0]
    z = data["buffer"]["accZ"]["buffer"][0]

    return {
        "x": round(x, 2),
        "y": round(y, 2),
        "z": round(z, 2)
    }
```

### Explanation

* Connects to the Phyphox Remote Access API.
* Retrieves X, Y and Z accelerometer values.
* Returns the readings as a Python dictionary.

> **Note:** The Phyphox IP address can change depending on the network. Update `PHYphox_URL` with the current IP address shown in Phyphox.

---

# 2. Kafka Producer

### File: `producer.py`

```python
from kafka import KafkaProducer
import json
import time

from accelerometer import get_accelerometer_data

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

while True:

    data = get_accelerometer_data()

    producer.send("accelerometer-data", data)
    producer.flush()

    print("Sent:", data)

    time.sleep(1)
```

### Explanation

* Creates a Kafka Producer connected to `localhost:9092`.
* Calls `get_accelerometer_data()` to obtain real Phyphox readings.
* Sends the data to the `accelerometer-data` Kafka topic.

### Example Output

```text
Sent: {'x': 0.66, 'y': 0.93, 'z': 9.7}
Sent: {'x': 0.71, 'y': 1.02, 'z': 9.65}
```

---

# 3. Kafka Consumer

### File: `consumer.py`

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "accelerometer-data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Consumer started...")

for message in consumer:

    data = message.value

    print("Received:", data)
```

### Explanation

* Connects to the `accelerometer-data` Kafka topic.
* Receives messages from Kafka.
* Converts the JSON message into a Python dictionary.
* Displays the received accelerometer readings.

### Example Output

```text
Consumer started...
Received: {'x': 0.66, 'y': 0.93, 'z': 9.7}
```

---

# 4. Insert Data into PostgreSQL

### File: `consumer.py`

The Consumer can also insert the received data into PostgreSQL using the following function:

```python
from kafka import KafkaConsumer
import psycopg
import json


def insert_into_database(data):

    conn = psycopg.connect(
        "dbname=kafka_demo user=arpita"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO accelerometer (x, y, z)
        VALUES (%s, %s, %s)
        """,
        (data["x"], data["y"], data["z"])
    )

    conn.commit()

    cursor.close()
    conn.close()


consumer = KafkaConsumer(
    "accelerometer-data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Consumer started...")


for message in consumer:

    data = message.value

    print("Received:", data)

    insert_into_database(data)

    print("Inserted into PostgreSQL:", data)
```

### Explanation

* Defines the `insert_into_database()` function.
* Connects to the `kafka_demo` PostgreSQL database.
* Inserts X, Y and Z values into the `accelerometer` table.
* Commits the transaction.

### Example Output

```text
Consumer started...
Received: {'x': 0.66, 'y': 0.93, 'z': 9.7}
Inserted into PostgreSQL: {'x': 0.66, 'y': 0.93, 'z': 9.7}
```

---

# 🗄️ PostgreSQL Database

## Create Database

```sql
CREATE DATABASE kafka_demo;
```

## Create Table

```sql
CREATE TABLE accelerometer (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    x DOUBLE PRECISION,
    y DOUBLE PRECISION,
    z DOUBLE PRECISION
);
```

## Check Stored Data

```sql
SELECT *
FROM accelerometer
ORDER BY id DESC
LIMIT 10;
```

---

# 🟠 Kafka Topic

Create the Kafka topic:

```bash
bin/kafka-topics.sh \
--create \
--topic accelerometer-data \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1
```

Check the topic:

```bash
bin/kafka-topics.sh \
--list \
--bootstrap-server localhost:9092
```

---

# 📦 Installation

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install kafka-python psycopg[binary] requests
```

---

# ▶️ How to Run

## 1. Start Kafka

```bash
cd ~/kafka
bin/kafka-server-start.sh config/server.properties
```

## 2. Start Phyphox

1. Open Phyphox on the smartphone.
2. Select the **Accelerometer** experiment.
3. Start the measurement.
4. Enable **Remote Access**.
5. Make sure the phone and computer are connected to the same network.

## 3. Run Producer

```bash
cd ~/real_time_analytics
source venv/bin/activate
python producer.py
```

## 4. Run Consumer

Open another terminal:

```bash
cd ~/real_time_analytics
source venv/bin/activate
python consumer.py
```

## 5. Verify PostgreSQL

```bash
psql -U arpita -d kafka_demo
```

Then:

```sql
SELECT *
FROM accelerometer
ORDER BY id DESC
LIMIT 10;
```

---

# 📊 Data Flow

```text
📱 Phyphox
     ↓
get_accelerometer_data()
     ↓
🐍 Python Kafka Producer
     ↓
🟠 Apache Kafka
     ↓
Kafka Consumer
     ↓
insert_into_database()
     ↓
🐘 PostgreSQL
```

# 🎯 Assignment Requirements

| Question | Implementation                                        |
| -------- | ----------------------------------------------------- |
| Q1       | Python function to receive Phyphox accelerometer data |
| Q2       | Kafka Producer to push data                           |
| Q3       | Kafka Consumer to read data                           |
| Q4       | Function to insert data into PostgreSQL               |

# 👩‍💻 Author

**Arpita Raykar**

MSc Data Science

````

### Important

For GitHub, I recommend keeping the **four main files separate**:

```text
real_time_analytics/
│
├── accelerometer.py
├── producer.py
├── consumer.py
└── README.md
````

The README contains the code for documentation, while the `.py` files contain the executable code.
