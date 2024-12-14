import winreg
import ctypes
import win32api
import win32con
import win32gui
import win32ui
import os
import subprocess
import psutil
from typing import Optional, List, Dict, Tuple
import json
import shutil
import sys
from PIL import Image
import win32com.client
import winshell

class WindowsCustomizer:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.PERSONALIZE_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        self.DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
        self.shell = win32com.client.Dispatch("WScript.Shell")
        
    def set_accent_color(self, color_rgb: tuple) -> bool:
        """Встановлює колір акценту Windows"""
        try:
            key_path = self.PERSONALIZE_PATH
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                        winreg.KEY_WRITE)
            
            color_bgr = (color_rgb[2], color_rgb[1], color_rgb[0])
            color_value = color_bgr[0] + (color_bgr[1] << 8) + (color_bgr[2] << 16)
            
            winreg.SetValueEx(registry_key, "ColorPrevalence", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(registry_key, "AccentColor", 0, winreg.REG_DWORD, color_value)
            
            win32gui.SystemParametersInfo(win32con.SPI_SETCOLORIZATIONCOLOR,
                                        color_value, 0)
            return True
        except Exception as e:
            print(f"Помилка при зміні кольору акценту: {e}")
            return False

    def set_wallpaper(self, image_path: str, style: str = "fill") -> bool:
        """Встановлює шпалери робочого столу"""
        try:
            style_values = {
                "center": "0",
                "tile": "1",
                "stretch": "2",
                "fit": "3",
                "fill": "10",
                "span": "22"
            }
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                "Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE)
            
            if style == "tile":
                winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "1")
                winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "0")
            else:
                winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
                winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, 
                                style_values.get(style, "2"))
                
            win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, 
                                        image_path, win32con.SPIF_UPDATEINIFILE)
            return True
        except Exception as e:
            print(f"Помилка при встановленні шпалер: {e}")
            return False

    def set_lock_screen_image(self, image_path: str) -> bool:
        """Встановлює зображення екрану блокування"""
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP"
            
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                winreg.SetValueEx(key, "LockScreenImagePath", 0, winreg.REG_SZ, 
                                image_path)
                winreg.SetValueEx(key, "LockScreenImageUrl", 0, winreg.REG_SZ, 
                                image_path)
                winreg.SetValueEx(key, "LockScreenImageStatus", 0, winreg.REG_DWORD, 1)
            return True
        except Exception as e:
            print(f"Помилка при встановленні зображення екрану блокування: {e}")
            return False

    def set_mouse_settings(self, speed: int, acceleration: bool, 
                          swap_buttons: bool) -> bool:
        """Налаштовує параметри миші"""
        try:
            # Швидкість миші (1-20)
            win32gui.SystemParametersInfo(win32con.SPI_SETMOUSESPEED, 0, 
                                        min(max(speed, 1), 20))
            
            # Прискорення миші
            win32gui.SystemParametersInfo(win32con.SPI_SETMOUSE, 0, 
                                        [0, 0, int(not acceleration)])
            
            # Зміна кнопок миші
            win32gui.SwapMouseButton(swap_buttons)
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні миші: {e}")
            return False

    def set_keyboard_settings(self, repeat_delay: int, repeat_rate: int) -> bool:
        """Налаштовує параметри клавіатури"""
        try:
            win32gui.SystemParametersInfo(win32con.SPI_SETKEYBOARDDELAY, 
                                        repeat_delay)
            win32gui.SystemParametersInfo(win32con.SPI_SETKEYBOARDSPEED, 
                                        repeat_rate)
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні клавіатури: {e}")
            return False

    def set_power_settings(self, scheme: str, monitor_timeout: int, 
                          disk_timeout: int) -> bool:
        """Налаштовує параметри живлення"""
        try:
            schemes = {
                "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
                "high_performance": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                "power_saver": "a1841308-3541-4fab-bc81-f71556f20b4a"
            }
            
            if scheme in schemes:
                subprocess.run(['powercfg', '/s', schemes[scheme]], 
                             check=True, capture_output=True)
            
            subprocess.run(['powercfg', '/change', 'monitor-timeout-ac', 
                          str(monitor_timeout)], check=True, capture_output=True)
            subprocess.run(['powercfg', '/change', 'disk-timeout-ac', 
                          str(disk_timeout)], check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні живлення: {e}")
            return False

    def set_sound_settings(self, volume: int, mute: bool, 
                          system_sounds: bool) -> bool:
        """Налаштовує параметри звуку"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, 
                                      CLSCTX_ALL, None)
            volume_obj = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Гучність (0-100)
            volume_obj.SetMasterVolumeLevelScalar(volume / 100.0, None)
            
            # Вимкнення звуку
            volume_obj.SetMute(mute, None)
            
            # Системні звуки
            key_path = r"AppEvents\Schemes"
            if system_sounds:
                scheme = ".Default"
            else:
                scheme = ".None"
            
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                        winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, "", 0, winreg.REG_SZ, scheme)
            
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні звуку: {e}")
            return False

    def set_display_settings(self, brightness: int, resolution: Tuple[int, int], 
                           refresh_rate: int) -> bool:
        """Налаштовує параметри дисплея"""
        try:
            # Яскравість (потрібні права адміністратора)
            import wmi
            wmi_obj = wmi.WMI(namespace='wmi')
            monitors = wmi_obj.WmiMonitorBrightnessMethods()
            for monitor in monitors:
                monitor.WmiSetBrightness(brightness, 0)
            
            # Роздільна здатність і частота оновлення
            device = win32.EnumDisplayDevices(None, 0)
            settings = win32.EnumDisplaySettings(device.DeviceName, -1)
            
            settings.PelsWidth = resolution[0]
            settings.PelsHeight = resolution[1]
            settings.DisplayFrequency = refresh_rate
            
            win32.ChangeDisplaySettings(settings, 0)
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні дисплея: {e}")
            return False

    def set_network_settings(self, adapter_name: str, ip: str, subnet: str, 
                           gateway: str, dns: List[str]) -> bool:
        """Налаштовує мережеві параметри"""
        try:
            # Потрібні права адміністратора
            netsh_commands = [
                f'interface ip set address "{adapter_name}" static {ip} {subnet} {gateway}',
                f'interface ip set dns "{adapter_name}" static {dns[0]}'
            ]
            
            if len(dns) > 1:
                netsh_commands.append(f'interface ip add dns "{adapter_name}" {dns[1]} index=2')
            
            for command in netsh_commands:
                subprocess.run(['netsh'] + command.split(), 
                             check=True, capture_output=True)
            
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні мережі: {e}")
            return False

    def set_security_settings(self, firewall: bool, defender: bool, 
                            updates: bool) -> bool:
        """Налаштовує параметри безпеки"""
        try:
            # Брандмауер
            subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 
                          'state', 'on' if firewall else 'off'], 
                         check=True, capture_output=True)
            
            # Windows Defender
            if defender:
                subprocess.run(['powershell', 'Set-MpPreference', '-DisableRealtimeMonitoring', 
                              '$false'], check=True, capture_output=True)
            else:
                subprocess.run(['powershell', 'Set-MpPreference', '-DisableRealtimeMonitoring', 
                              '$true'], check=True, capture_output=True)
            
            # Автоматичні оновлення
            service_name = "wuauserv"  # Windows Update
            if updates:
                subprocess.run(['sc', 'config', service_name, 'start=', 'auto'], 
                             check=True, capture_output=True)
                subprocess.run(['sc', 'start', service_name], 
                             check=True, capture_output=True)
            else:
                subprocess.run(['sc', 'config', service_name, 'start=', 'disabled'], 
                             check=True, capture_output=True)
                subprocess.run(['sc', 'stop', service_name], 
                             check=True, capture_output=True)
            
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні безпеки: {e}")
            return False

    def create_restore_point(self, description: str) -> bool:
        """Створює точку відновлення системи"""
        try:
            subprocess.run(['wmic.exe', 'os', 'get', 'restorepoint'], 
                         check=True, capture_output=True)
            
            subprocess.run(['wmic.exe', 'recoveros', 'createsystemrestorepoint', 
                          f'Description="{description}"', 
                          'RestorePointType=12'], 
                         check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"Помилка при створенні точки відновлення: {e}")
            return False

    def backup_registry(self, backup_path: str) -> bool:
        """Створює резервну копію реєстру"""
        try:
            subprocess.run(['reg', 'export', 'HKLM', 
                          os.path.join(backup_path, 'HKLM.reg'), '/y'], 
                         check=True, capture_output=True)
            subprocess.run(['reg', 'export', 'HKCU', 
                          os.path.join(backup_path, 'HKCU.reg'), '/y'], 
                         check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"Помилка при створенні резервної копії реєстру: {e}")
            return False

    def set_user_account(self, username: str, password: Optional[str] = None, 
                        picture_path: Optional[str] = None) -> bool:
        """Налаштовує обліковий запис користувача"""
        try:
            if password:
                subprocess.run(['net', 'user', username, password], 
                             check=True, capture_output=True)
            
            if picture_path and os.path.exists(picture_path):
                account_path = os.path.join(os.environ['PUBLIC'], 
                                          'AccountPictures')
                if not os.path.exists(account_path):
                    os.makedirs(account_path)
                
                shutil.copy2(picture_path, 
                           os.path.join(account_path, f'{username}.jpg'))
            
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні облікового запису: {e}")
            return False

    def set_app_defaults(self, file_type: str, app_path: str) -> bool:
        """Встановлює програму за замовчуванням для типу файлів"""
        try:
            key_path = f"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.{file_type}\\UserChoice"
            
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                        winreg.KEY_WRITE)
            
            prog_id = os.path.splitext(os.path.basename(app_path))[0]
            winreg.SetValueEx(registry_key, "Progid", 0, winreg.REG_SZ, prog_id)
            
            return True
        except Exception as e:
            print(f"Помилка при встановленні програми за замовчуванням: {e}")
            return False

    def set_folder_options(self, show_hidden: bool, show_extensions: bool, 
                          show_system: bool) -> bool:
        """Налаштовує параметри відображення папок"""
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                        winreg.KEY_WRITE)
            
            winreg.SetValueEx(registry_key, "Hidden", 0, winreg.REG_DWORD, 
                            1 if show_hidden else 2)
            winreg.SetValueEx(registry_key, "HideFileExt", 0, winreg.REG_DWORD, 
                            0 if show_extensions else 1)
            winreg.SetValueEx(registry_key, "ShowSuperHidden", 0, winreg.REG_DWORD, 
                            1 if show_system else 0)
            
            # Оновлюємо Explorer
            win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 
                               0, "Environment")
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні параметрів папок: {e}")
            return False

    def set_taskbar_settings(self, auto_hide: bool, use_small_icons: bool, 
                           position: str = "bottom") -> bool:
        """Налаштовує панель завдань"""
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3"
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                        winreg.KEY_WRITE)
            
            settings = winreg.QueryValueEx(registry_key, "Settings")[0]
            
            # Автоматичне приховування
            if auto_hide:
                settings[8] |= 1
            else:
                settings[8] &= ~1
            
            # Розмір іконок
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            adv_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                   winreg.KEY_WRITE)
            winreg.SetValueEx(adv_key, "TaskbarSmallIcons", 0, winreg.REG_DWORD, 
                            1 if use_small_icons else 0)
            
            # Позиція
            positions = {"top": 1, "left": 0, "right": 2, "bottom": 3}
            if position in positions:
                settings[12] = positions[position]
            
            winreg.SetValueEx(registry_key, "Settings", 0, winreg.REG_BINARY, settings)
            
            # Перезапускаємо провідник для застосування змін
            os.system("taskkill /f /im explorer.exe && start explorer.exe")
            
            return True
        except Exception as e:
            print(f"Помилка при налаштуванні панелі завдань: {e}")
            return False

    def set_wallpaper(self):
        """Встановлює шпалери робочого столу."""
        try:
            from win32com.shell import shell, shellcon
            import winreg
            import ctypes

            # Відкриваємо діалог вибору файлу
            file_path = QFileDialog.getOpenFileName(
                None,
                "Виберіть зображення для шпалер",
                "",
                "Image files (*.jpg *.jpeg *.png *.bmp)"
            )[0]

            if file_path:
                # Встановлюємо шпалери
                ctypes.windll.user32.SystemParametersInfoW(
                    20, 0, file_path, 0)

                # Зберігаємо шлях до шпалер в реєстрі
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    "Control Panel\\Desktop",
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(
                    key,
                    "WallPaper",
                    0,
                    winreg.REG_SZ,
                    file_path
                )
                winreg.CloseKey(key)
        except Exception as e:
            raise Exception(f"Помилка при встановленні шпалер: {str(e)}")

    def set_lockscreen(self):
        """Встановлює зображення екрану блокування."""
        try:
            import winreg
            from shutil import copy2

            # Відкриваємо діалог вибору файлу
            file_path = QFileDialog.getOpenFileName(
                None,
                "Виберіть зображення для екрану блокування",
                "",
                "Image files (*.jpg *.jpeg *.png *.bmp)"
            )[0]

            if file_path:
                # Копіюємо файл в системну папку
                system_path = os.path.expandvars(
                    "%SystemRoot%\\Web\\Screen"
                )
                new_path = os.path.join(
                    system_path,
                    "lockscreen.jpg"
                )
                copy2(file_path, new_path)

                # Оновлюємо налаштування в реєстрі
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\PersonalizationCSP",
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(
                    key,
                    "LockScreenImagePath",
                    0,
                    winreg.REG_SZ,
                    new_path
                )
                winreg.SetValueEx(
                    key,
                    "LockScreenImageUrl",
                    0,
                    winreg.REG_SZ,
                    new_path
                )
                winreg.SetValueEx(
                    key,
                    "LockScreenImageStatus",
                    0,
                    winreg.REG_DWORD,
                    1
                )
                winreg.CloseKey(key)
        except Exception as e:
            raise Exception(f"Помилка при встановленні екрану блокування: {str(e)}")

    def set_power_settings(self, scheme, monitor_timeout, disk_timeout):
        """Встановлює налаштування живлення."""
        try:
            import subprocess

            # Встановлюємо схему живлення
            schemes = {
                "Збалансована": "381b4222-f694-41f0-9685-ff5bb260df2e",
                "Висока продуктивність": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                "Економія енергії": "a1841308-3541-4fab-bc81-f71556f20b4a"
            }
            scheme_guid = schemes.get(scheme)
            if scheme_guid:
                subprocess.run([
                    "powercfg",
                    "/setactive",
                    scheme_guid
                ])

            # Встановлюємо час до вимкнення екрану
            subprocess.run([
                "powercfg",
                "/change",
                "monitor-timeout-ac",
                str(monitor_timeout)
            ])

            # Встановлюємо час до вимкнення диску
            subprocess.run([
                "powercfg",
                "/change",
                "disk-timeout-ac",
                str(disk_timeout)
            ])
        except Exception as e:
            raise Exception(f"Помилка при встановленні налаштувань живлення: {str(e)}")

    def set_sound_settings(self, volume, mute, system_sounds):
        """Встановлює налаштування звуку."""
        try:
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            import winreg

            # Встановлюємо гучність
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume_interface = interface.QueryInterface(IAudioEndpointVolume)
            volume_interface.SetMasterVolumeLevelScalar(volume / 100.0, None)
            volume_interface.SetMute(mute, None)

            # Встановлюємо системні звуки
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                "AppEvents\\Schemes",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(
                key,
                "App",
                0,
                winreg.REG_SZ,
                ".None" if not system_sounds else ".Default"
            )
            winreg.CloseKey(key)
        except Exception as e:
            raise Exception(f"Помилка при встановленні налаштувань звуку: {str(e)}")

    def set_display_settings(self, brightness, resolution, refresh):
        """Встановлює налаштування дисплея."""
        try:
            import wmi
            import ctypes

            # Встановлюємо яскравість
            wmi_obj = wmi.WMI(namespace='wmi')
            monitors = wmi_obj.WmiMonitorBrightnessMethods()
            if monitors:
                monitors[0].WmiSetBrightness(brightness, 0)

            # Встановлюємо роздільну здатність і частоту оновлення
            width, height = map(int, resolution.split('x'))
            frequency = int(refresh.split()[0])

            ENUM_CURRENT_SETTINGS = -1
            DM_PELSWIDTH = 0x80000
            DM_PELSHEIGHT = 0x100000
            DM_DISPLAYFREQUENCY = 0x400000

            ctypes.windll.user32.EnumDisplaySettingsW(None, ENUM_CURRENT_SETTINGS)
            devmode = ctypes.create_string_buffer(140)
            ctypes.windll.user32.EnumDisplaySettingsW(None, ENUM_CURRENT_SETTINGS, devmode)

            settings = ctypes.cast(devmode, ctypes.POINTER(ctypes.c_int))
            settings[DM_PELSWIDTH] = width
            settings[DM_PELSHEIGHT] = height
            settings[DM_DISPLAYFREQUENCY] = frequency

            CDS_UPDATEREGISTRY = 0x01
            DISP_CHANGE_SUCCESSFUL = 0
            result = ctypes.windll.user32.ChangeDisplaySettingsW(devmode, CDS_UPDATEREGISTRY)

            if result != DISP_CHANGE_SUCCESSFUL:
                raise Exception("Не вдалося змінити налаштування дисплея")
        except Exception as e:
            raise Exception(f"Помилка при встановленні налаштувань дисплея: {str(e)}")

    def get_startup_programs(self):
        """Отримує список програм, які запускаються при старті Windows."""
        try:
            import winreg
            startup_programs = []

            # Перевіряємо реєстр для всіх користувачів
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, 
                                   winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        startup_programs.append({
                            'name': name,
                            'path': value,
                            'type': 'HKLM'
                        })
                        i += 1
                    except WindowsError:
                        break
                winreg.CloseKey(key)
            except WindowsError:
                pass

            # Перевіряємо реєстр для поточного користувача
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                   winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        startup_programs.append({
                            'name': name,
                            'path': value,
                            'type': 'HKCU'
                        })
                        i += 1
                    except WindowsError:
                        break
                winreg.CloseKey(key)
            except WindowsError:
                pass

            # Перевіряємо папку автозапуску
            startup_folder = os.path.join(
                os.environ['APPDATA'],
                r'Microsoft\Windows\Start Menu\Programs\Startup'
            )
            if os.path.exists(startup_folder):
                for item in os.listdir(startup_folder):
                    if item.endswith(('.lnk', '.url')):
                        startup_programs.append({
                            'name': os.path.splitext(item)[0],
                            'path': os.path.join(startup_folder, item),
                            'type': 'Startup Folder'
                        })

            return startup_programs
        except Exception as e:
            print(f"Помилка при отриманні списку автозапуску: {e}")
            return []

    def add_to_startup(self, name, path):
        """Додає програму до автозапуску."""
        try:
            import winreg
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                               winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Помилка при додаванні до автозапуску: {e}")
            return False

    def remove_from_startup(self, name, startup_type):
        """Видаляє програму з автозапуску."""
        try:
            import winreg
            if startup_type in ('HKLM', 'HKCU'):
                key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
                root_key = winreg.HKEY_LOCAL_MACHINE if startup_type == 'HKLM' else winreg.HKEY_CURRENT_USER
                key = winreg.OpenKey(root_key, key_path, 0, 
                                   winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, name)
                winreg.CloseKey(key)
            elif startup_type == 'Startup Folder':
                startup_folder = os.path.join(
                    os.environ['APPDATA'],
                    r'Microsoft\Windows\Start Menu\Programs\Startup'
                )
                file_path = os.path.join(startup_folder, f"{name}.lnk")
                if os.path.exists(file_path):
                    os.remove(file_path)
            return True
        except Exception as e:
            print(f"Помилка при видаленні з автозапуску: {e}")
            return False
