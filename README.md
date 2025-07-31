# LoRa Auto-Responder

A tiny Python script that lives on a desktop or laptop, plugs into a Meshtastic-flashed LoRa node via USB‐serial, and automatically echoes any text message it hears.
I use it to measure real-world range & reliability while the *carried* node rides in a backpack and forwards messages from the Meshtastic Android/iOS app over BLE.

```
📩 Message from !234: Hello base, you copy?
Auto-reply sent…
```

---

## Features

* **Auto-echoing** – replies with the exact same message it receives after a 5-second cooldown, useful for hands-free range testing.
* **Meshtastic native** – uses the official `meshtastic-python` library & protobufs.
* **Plug-and-play** – zero firmware changes; any T-Beam, Heltec V3, etc. running Meshtastic works.

---

## Hardware / Software Requirements

| Item                              | Notes                                              |
| --------------------------------- | -------------------------------------------------- |
| LoRa node flashed with Meshtastic | USB-C or micro-USB connection to the computer      |
| Computer with Python 3.7+         | Windows, macOS, or Linux                           |
| `meshtastic-python` ≥ 2.3         | Installs `protobuf`, `pyserial`, and `pubsub` deps |

---

## Quick Start

1. **Clone the repo**

   ```bash
   git clone https://github.com/<you>/lora-auto-responder.git
   cd lora-auto-responder
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   # or, minimal
   pip install meshtastic
   ```

3. **Connect your LoRa node**

   * On Windows note the `COM` port (e.g. `COM3`);
   * On macOS/Linux note the `/dev/ttyUSB*` or `/dev/tty.SLAB_USBtoUART` path.

4. **Run**

   ```bash
   python lora-auto-responder.py --port COM3   # Windows example
   python lora-auto-responder.py --port /dev/ttyUSB0  # Linux example
   ```

   > ✅ *Auto-responder running for node 123…*

---

## Command-Line Options

| Flag         | Default          | Description                           |
| ------------ | ---------------- | ------------------------------------- |
| `--port`     | `COM3` in script | Serial port of the Meshtastic radio   |
| `--cooldown` | `5` seconds      | Minimum interval between auto-replies |

*(The sample script hard-codes these values; PRs to add ********`argparse`******** welcome!)*

---

## How It Works

1. `SerialInterface` opens the radio’s USB serial port.
2. The script subscribes to the `meshtastic.receive` pub-sub topic.
3. When a text payload arrives it decodes UTF-8, prints it, and—if the cooldown timer has expired—sends an echo prefixed with `Auto-reply:`.
4. A while-loop keeps the process alive with minimal CPU use.

---

## Typical Use-Case: Range Testing

1. **Desktop Node**: Auto-responder connected to rooftop antenna.
2. **Carried Node (in backpack)**: Paired to phone via BLE running the Meshtastic app.
3. Walk/drive/cycle until your phone stops showing replies. The last GPS point logged equals your practical range under those conditions.

---

## Troubleshooting

| Symptom                                     | Fix                                                                     |
| ------------------------------------------- | ----------------------------------------------------------------------- |
| `PermissionError: [Errno 13] Access denied` | On Linux/macOS: `sudo usermod -aG dialout $USER` then log out/in        |
| No messages received                        | Check the channel settings (key, region, hop limit) match across nodes  |
| Garbled characters                          | Ensure the message sent is UTF-8 text (binary payloads will be ignored) |

---

## Roadmap / Ideas

* Add optional auto-ping feature to send a fixed message every X seconds.
* Make port & cooldown configurable via `argparse`.
* Add CSV logging for RTT & RSSI.
* Docker one-liner for headless Raspberry Pi base stations.

---

## Contributing

Issues and pull requests are welcome—especially improvements that generalize port detection or add unit tests.

---

## License

MIT. See `LICENSE` file for details.

---

Made with 🤖, 🛠️, and long walks to test LoRa range.