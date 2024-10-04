# 🖨️ ChituBox Printer Integration for Home Assistant

![HACS Custom](https://img.shields.io/badge/HACS-Custom-blueviolet.svg?style=for-the-badge)  
Bring any Chitu firmware printer to HA!

## 😍 Why You'll Love This Integration

- 🔄 **Real-Time Monitoring**: Keep an eagle eye on your prints, and watch the progress.
- 🌡 **Temperature Tracker**: Always know if your printer’s heating up.
- 🖼 **File Flashbacks**: Always see what you are printing.

## 🛠 Installation Guide

### 1. **HACS Setup (It’s as easy as 1-2-3!)**
- Open **Home Assistant**.
- Head to **HACS > Integrations**.
- Tap the **three dots** in the top-right and select **Custom Repositories**.
- Add this repository URL, then set the category to **Integration**. Voilà!

### 2. **Install the Integration**
- After adding the repo, search for **ChituBox Printer** under **HACS > Integrations**.
- Click that magic **Install** button.
  
### 3. **Printer Configuration**
- Restart Home Assistant (because magic needs a little reset).
- Go to **Settings > Devices & Services > Add Integration**.
- Find **ChituBox Printer**, click it, and then enter your printer’s **IP address** and **Port** (default is `80`).

## ⚙️ Easy Configuration

You’ll need just two pieces of info to get up and running:
- **Host**: This is the IP address of your printer (usally something like `192.168.0.*`).
- **Port**: The default port for the API is usually `80`.

## 🖨 Supported Printers
Our integration works with any printer that uses **ChituBox’s firmware**, including:
- 🖨️ **Elegoo Mars** (most models should work!)
- 🖨️ **Anycubic Photon** (Not tested!)
- 🖨️ **Other ChituBox-compatible models** (Not tested!)

If your printer talks to the ChituBox app, this integration can probably talk to it too!

## 🎛 The Printer Data You’ll Get

With this integration, Home Assistant will expose the following entities:

| 🖥 Entity                | 🔍 Description                        |
|--------------------------|---------------------------------------|
| `sensor.printer_status`   | Shows what your printer is doing: Idle, Printing, Error? |
| `sensor.print_progress`   | Current print progress percentage (watch it climb!) |
| `sensor.printer_temperature` | Internal printer temperature (Is it running hot or cool?) |
| `sensor.current_file`     | The name of the file that’s being printed |

## 🛠️ Troubleshooting Tips
If something doesn’t seem quite right, don’t worry, we’ve got your back! Here’s what to check:
1. Make sure your printer and Home Assistant are on the **same network**. They’re better buddies when they can chat directly.
2. Check the **logs** in Home Assistant under **Settings > System > Logs**. Look for anything related to `chitubox_printer`.
3. Got an API timeout error? Double-check your IP and port settings in the configuration.

## 👩‍💻 Contributing to the Cause
Have an idea to improve the integration or a knack for coding? Awesome! Open up a pull request or submit an issue, and let’s build something amazing together. Whether it's bug fixes, new features, or just some feedback, all contributions are welcome!

## 🧙‍♂️ License & Legal Stuff
This project is open-source and licensed under the **MIT License**. That means it’s free to use, modify, and share! Just remember to give credit where it’s due.