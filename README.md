# Windows Customizer

A powerful and user-friendly Python application for customizing Windows appearance and system settings through an intuitive graphical interface.

## Features

- 🎨 **Theme Customization**
  - Change Windows accent colors
  - Toggle between light and dark themes
  - Apply predefined color schemes (Light, Dark, Blue, Green)

- 🖼️ **Desktop Personalization**
  - Set custom wallpapers with various styles (Fill, Stretch, Center, Tile, Fit)
  - Customize lock screen images
  - Configure desktop visual effects

- 🖱️ **Mouse Settings**
  - Adjust mouse speed and sensitivity
  - Toggle mouse acceleration
  - Configure button mapping

- 🎯 **Visual Effects**
  - Control window transparency
  - Toggle system animations
  - Customize window shadows
  - Optimize for performance or appearance

## Installation

1. Ensure you have Python 3.8 or higher installed
2. Clone this repository:
```bash
git clone https://github.com/yourusername/KASTOM-WINDOWS-PROGRAM.git
cd KASTOM-WINDOWS-PROGRAM
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Requirements

- Windows 10/11
- Python 3.8+
- Required packages (automatically installed via requirements.txt):
  - PySide6
  - pywin32
  - darkdetect
  - qtawesome
  - Pillow
  - psutil
  - winshell
  - and more...

## Usage

Run the application:
```bash
python main.py
```

The application will launch with a modern GUI interface where you can:
1. Select different themes from the dropdown menu
2. Customize accent colors using the color picker
3. Change wallpaper and lock screen images
4. Adjust mouse and system settings
5. Configure visual effects

## Screenshots

[Add screenshots of your application here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with PySide6 for the modern GUI interface
- Uses Windows Registry and API calls for system customization
- Icons provided by QtAwesome

## Note

Some features may require administrative privileges to work properly. Make sure to run the application with appropriate permissions when needed.
