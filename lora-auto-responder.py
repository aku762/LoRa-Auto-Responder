from meshtastic.serial_interface import SerialInterface
from meshtastic.util import findPorts
from pubsub import pub
import time

# Replace COM port as needed
iface = SerialInterface(devPath="COM3")

import time
last_reply = 0

def on_receive(packet, interface):
    global last_reply
    now = time.time()
    
    decoded = packet.get('decoded', {})
    payload = decoded.get('payload')
    from_id = packet['fromId']

    if isinstance(payload, bytes):
        try:
            text = payload.decode("utf-8").strip()
            if text and now - last_reply > 5:  # wait at least 5s between replies
                print(f"📩 Message from {from_id}: {text}")
                interface.sendText(f"Auto-reply: Got '{text}' from {from_id}")
                last_reply = now
        except UnicodeDecodeError:
            pass

# Subscribe to message events
pub.subscribe(on_receive, "meshtastic.receive")

print(f"✅ Auto-responder running for node {iface.myInfo.my_node_num}...")

# Keep alive
while True:
    time.sleep(1)
