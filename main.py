import serial
from rabbitmq import RabbitMQ

ARDUINO_PORT = "COM6"
RABBITMQ_URL = "100.25.186.143"
RABBITMQ_USER = "crzindustries"
RABBITMQ_PASSWORD = "Colmillo12"

RABBIT_SCHEMA = {
    "name": "meteorological",
    "type": "topic",
    "queues": [
        {"name": "meteorologicalSensorsData", "routing_key": "new.data"},
    ],
}


def main():
    rabbit = RabbitMQ(
        RABBITMQ_URL, RABBITMQ_USER, RABBITMQ_PASSWORD, schema=RABBIT_SCHEMA
    )

    port = serial.Serial(ARDUINO_PORT, 9600)
    port.flush()

    while True:
        if port.in_waiting > 0:
            line = port.readline().decode("utf-8").rstrip()

            # TODO: Improve hardcoded data
            rabbit.send("meteorological", "new.data", line)


if __name__ == "__main__":
    main()
