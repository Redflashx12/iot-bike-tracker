from dataclasses import dataclass


@dataclass
class Device:
    eui: str
    ttn_id: str


@dataclass
class Message:
    device_eui: str
    count: int
    port: int
    payload: str
    decoded_payload: dict
    rx_metadata: dict
    consumed_airtime: str
