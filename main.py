from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QComboBox, QTabWidget,
                               QMessageBox, QSpinBox, QCheckBox, QListWidget, QProgressBar,
                               QGroupBox, QSlider)
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import Qt
import qtawesome as qta
import sys
from windows_customizer import WindowsCustomizer
import darkdetect

class CustomizationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.customizer = WindowsCustomizer()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Windows Customizer')
        self.setMinimumSize(800, 600)
        
        # Головний віджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Вибір теми
        theme_layout = QHBoxLayout()
        theme_label = QLabel('Theme:')
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Light', 'Dark', 'Blue', 'Green'])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)
        
        # Вкладки
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Вкладка "Appearance"
        appearance_tab = QWidget()
        appearance_layout = QVBoxLayout(appearance_tab)
        
        # Налаштування теми
        theme_group = QGroupBox("Тема Windows")
        theme_layout = QVBoxLayout()
        
        # Колір акценту
        accent_layout = QHBoxLayout()
        accent_color_btn = QPushButton("Вибрати колір акценту")
        accent_color_btn.clicked.connect(self.change_accent_color)
        accent_preview = QWidget()
        accent_preview.setFixedSize(30, 30)
        accent_preview.setStyleSheet("background-color: #0078D7;")
        accent_layout.addWidget(accent_color_btn)
        accent_layout.addWidget(accent_preview)
        
        # Темна тема
        dark_mode_check = QCheckBox("Темна тема")
        dark_mode_check.stateChanged.connect(lambda state: self.toggle_dark_mode())
        
        theme_layout.addLayout(accent_layout)
        theme_layout.addWidget(dark_mode_check)
        theme_group.setLayout(theme_layout)
        
        # Налаштування робочого столу
        desktop_group = QGroupBox("Робочий стіл")
        desktop_layout = QVBoxLayout()
        
        # Шпалери
        wallpaper_btn = QPushButton("Змінити шпалери")
        wallpaper_btn.clicked.connect(self.change_wallpaper)
        
        wallpaper_style = QComboBox()
        wallpaper_style.addItems(["Заповнити", "Розтягнути", "За центром", 
                                "Мозаїка", "За розміром"])
        
        # Екран блокування
        lockscreen_btn = QPushButton("Змінити екран блокування")
        lockscreen_btn.clicked.connect(self.change_lockscreen)
        
        desktop_layout.addWidget(wallpaper_btn)
        desktop_layout.addWidget(wallpaper_style)
        desktop_layout.addWidget(lockscreen_btn)
        desktop_group.setLayout(desktop_layout)
        
        # Візуальні ефекти
        effects_group = QGroupBox("Візуальні ефекти")
        effects_layout = QVBoxLayout()
        
        effects_combo = QComboBox()
        effects_combo.addItems(["Найкраща продуктивність", 
                              "Найкращий вигляд", 
                              "Користувацькі"])
        
        transparency_check = QCheckBox("Прозорість вікон")
        animations_check = QCheckBox("Анімації")
        shadows_check = QCheckBox("Тіні")
        
        effects_layout.addWidget(effects_combo)
        effects_layout.addWidget(transparency_check)
        effects_layout.addWidget(animations_check)
        effects_layout.addWidget(shadows_check)
        effects_group.setLayout(effects_layout)
        
        # Додаємо всі групи до вкладки
        appearance_layout.addWidget(theme_group)
        appearance_layout.addWidget(desktop_group)
        appearance_layout.addWidget(effects_group)
        appearance_layout.addStretch()
        
        # Вкладка "System"
        system_tab = QWidget()
        system_layout = QVBoxLayout(system_tab)
        
        # Налаштування живлення
        power_group = QGroupBox("Живлення")
        power_layout = QVBoxLayout()
        
        power_scheme = QComboBox()
        power_scheme.addItems(["Збалансована", "Висока продуктивність", 
                             "Економія енергії"])
        
        monitor_timeout = QSpinBox()
        monitor_timeout.setRange(1, 60)
        monitor_timeout.setValue(10)
        monitor_timeout.setSuffix(" хв")
        
        disk_timeout = QSpinBox()
        disk_timeout.setRange(1, 60)
        disk_timeout.setValue(20)
        disk_timeout.setSuffix(" хв")
        
        apply_power_btn = QPushButton("Застосувати налаштування")
        apply_power_btn.clicked.connect(self.apply_power_settings)
        
        power_layout.addWidget(QLabel("Схема живлення:"))
        power_layout.addWidget(power_scheme)
        power_layout.addWidget(QLabel("Вимкнення екрану через:"))
        power_layout.addWidget(monitor_timeout)
        power_layout.addWidget(QLabel("Вимкнення диску через:"))
        power_layout.addWidget(disk_timeout)
        power_layout.addWidget(apply_power_btn)
        power_group.setLayout(power_layout)
        
        # Налаштування звуку
        sound_group = QGroupBox("Звук")
        sound_layout = QVBoxLayout()
        
        volume_slider = QSlider(Qt.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(50)
        
        mute_check = QCheckBox("Вимкнути звук")
        system_sounds_check = QCheckBox("Системні звуки")
        
        apply_sound_btn = QPushButton("Застосувати налаштування")
        apply_sound_btn.clicked.connect(self.apply_sound_settings)
        
        sound_layout.addWidget(QLabel("Гучність:"))
        sound_layout.addWidget(volume_slider)
        sound_layout.addWidget(mute_check)
        sound_layout.addWidget(system_sounds_check)
        sound_layout.addWidget(apply_sound_btn)
        sound_group.setLayout(sound_layout)
        
        # Налаштування дисплею
        display_group = QGroupBox("Дисплей")
        display_layout = QVBoxLayout()
        
        brightness_slider = QSlider(Qt.Horizontal)
        brightness_slider.setRange(0, 100)
        brightness_slider.setValue(75)
        
        resolution_combo = QComboBox()
        resolution_combo.addItems(["1920x1080", "1680x1050", "1600x900", "1366x768"])
        
        refresh_rate = QComboBox()
        refresh_rate.addItems(["60 Гц", "75 Гц", "120 Гц", "144 Гц"])
        
        apply_display_btn = QPushButton("Застосувати налаштування")
        apply_display_btn.clicked.connect(self.apply_display_settings)
        
        display_layout.addWidget(QLabel("Яскравість:"))
        display_layout.addWidget(brightness_slider)
        display_layout.addWidget(QLabel("Роздільна здатність:"))
        display_layout.addWidget(resolution_combo)
        display_layout.addWidget(QLabel("Частота оновлення:"))
        display_layout.addWidget(refresh_rate)
        display_layout.addWidget(apply_display_btn)
        display_group.setLayout(display_layout)
        
        # Кнопки для вкладки "System"
        start_menu_btn = self.create_button('Налаштувати меню Пуск', 'fa5s.bars', 
                                          self.customize_start_menu)
        taskbar_btn = self.create_button('Налаштувати панель завдань', 'fa5s.window-maximize', 
                                       self.customize_taskbar)
        notifications_btn = self.create_button('Налаштувати сповіщення', 'fa5s.bell', 
                                            self.customize_notifications)
        privacy_btn = self.create_button('Налаштування конфіденційності', 'fa5s.user-shield', 
                                       self.customize_privacy)
        
        system_layout.addWidget(power_group)
        system_layout.addWidget(sound_group)
        system_layout.addWidget(display_group)
        system_layout.addWidget(start_menu_btn)
        system_layout.addWidget(taskbar_btn)
        system_layout.addWidget(notifications_btn)
        system_layout.addWidget(privacy_btn)
        system_layout.addStretch()
        
        # Вкладка "Desktop"
        desktop_tab = QWidget()
        desktop_layout = QVBoxLayout(desktop_tab)
        
        # Налаштування робочого столу
        icon_size_layout = QHBoxLayout()
        icon_size_label = QLabel('Розмір іконок:')
        self.icon_size_spin = QSpinBox()
        self.icon_size_spin.setRange(32, 96)
        self.icon_size_spin.setSingleStep(16)
        self.icon_size_spin.setValue(48)
        icon_size_layout.addWidget(icon_size_label)
        icon_size_layout.addWidget(self.icon_size_spin)
        
        self.hide_icons_check = QCheckBox('Приховати іконки')
        self.auto_arrange_check = QCheckBox('Автоматичне впорядкування')
        
        apply_desktop_btn = self.create_button('Застосувати налаштування', 'fa5s.check', 
                                             self.apply_desktop_settings)
        
        desktop_layout.addLayout(icon_size_layout)
        desktop_layout.addWidget(self.hide_icons_check)
        desktop_layout.addWidget(self.auto_arrange_check)
        desktop_layout.addWidget(apply_desktop_btn)
        desktop_layout.addStretch()
        
        # Вкладка "Optimization"
        optimization_tab = QWidget()
        optimization_layout = QVBoxLayout(optimization_tab)
        
        # Список автозапуску
        startup_label = QLabel('Програми автозапуску:')
        self.startup_list = QListWidget()
        self.update_startup_list()
        
        toggle_startup_btn = self.create_button('Увімкнути/Вимкнути вибрану програму', 
                                              'fa5s.power-off', self.toggle_startup)
        
        # Очищення системи
        clean_system_btn = self.create_button('Очистити систему', 'fa5s.broom', 
                                            self.clean_system)
        self.cleanup_progress = QProgressBar()
        self.cleanup_progress.hide()
        
        # Оптимізація служб
        optimize_services_btn = self.create_button('Оптимізувати служби', 'fa5s.server', 
                                                 self.optimize_services)
        
        optimization_layout.addWidget(startup_label)
        optimization_layout.addWidget(self.startup_list)
        optimization_layout.addWidget(toggle_startup_btn)
        optimization_layout.addWidget(clean_system_btn)
        optimization_layout.addWidget(self.cleanup_progress)
        optimization_layout.addWidget(optimize_services_btn)
        
        # Додаємо вкладки
        tabs.addTab(appearance_tab, 'Appearance')
        tabs.addTab(system_tab, 'System')
        tabs.addTab(desktop_tab, 'Desktop')
        tabs.addTab(optimization_tab, 'Optimization')
        
        # Застосовуємо початкову тему
        self.apply_initial_theme()
    
    def create_button(self, text, icon_name, callback):
        btn = QPushButton(text)
        btn.setIcon(qta.icon(icon_name))
        btn.clicked.connect(callback)
        return btn
    
    def apply_initial_theme(self):
        is_dark = darkdetect.isDark()
        self.theme_combo.setCurrentText('Dark' if is_dark else 'Light')
        self.change_theme('Dark' if is_dark else 'Light')
    
    def change_theme(self, theme_name):
        if theme_name == 'Light':
            self.apply_light_theme()
        elif theme_name == 'Dark':
            self.apply_dark_theme()
        elif theme_name == 'Blue':
            self.apply_blue_theme()
        elif theme_name == 'Green':
            self.apply_green_theme()
    
    def apply_light_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QWidget { background-color: #f0f0f0; color: #000000; }
            QPushButton { 
                background-color: #ffffff;
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover { background-color: #e6e6e6; }
            QComboBox { 
                background-color: #ffffff;
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 3px;
            }
            QTabWidget::pane { 
                border: 1px solid #cccccc;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #e6e6e6;
                padding: 8px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
            }
        """)
    
    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QWidget { background-color: #2b2b2b; color: #ffffff; }
            QPushButton { 
                background-color: #3b3b3b;
                border: 1px solid #505050;
                padding: 5px;
                border-radius: 3px;
                color: #ffffff;
            }
            QPushButton:hover { background-color: #505050; }
            QComboBox { 
                background-color: #3b3b3b;
                border: 1px solid #505050;
                padding: 5px;
                border-radius: 3px;
                color: #ffffff;
            }
            QTabWidget::pane { 
                border: 1px solid #505050;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #3b3b3b;
                padding: 8px;
                color: #ffffff;
            }
            QTabBar::tab:selected {
                background-color: #505050;
            }
        """)
    
    def apply_blue_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1a237e; }
            QWidget { background-color: #1a237e; color: #ffffff; }
            QPushButton { 
                background-color: #283593;
                border: 1px solid #3949ab;
                padding: 5px;
                border-radius: 3px;
                color: #ffffff;
            }
            QPushButton:hover { background-color: #3949ab; }
            QComboBox { 
                background-color: #283593;
                border: 1px solid #3949ab;
                padding: 5px;
                border-radius: 3px;
                color: #ffffff;
            }
            QTabWidget::pane { 
                border: 1px solid #3949ab;
                background-color: #1a237e;
            }
            QTabBar::tab {
                background-color: #283593;
                padding: 8px;
                color: #ffffff;
            }
            QTabBar::tab:selected {
                background-color: #3949ab;
            }
        """)
    
    def apply_green_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1b5e20; }
            QWidget { background-color: #1b5e20; color: #ffffff; }
            QPushButton { 
                background-color: #2e7d32;
                border: 1px solid #388e3c;
                padding: 5px;
                border-radius: 3px;
                color: #ffffff;
            }
            QPushButton:hover { background-color: #388e3c; }
            QComboBox { 
                background-color: #2e7d32;
                border: 1px solid #388e3c;
                padding: 5px;
                border-radius: 3px;
                color: #ffffff;
            }
            QTabWidget::pane { 
                border: 1px solid #388e3c;
                background-color: #1b5e20;
            }
            QTabBar::tab {
                background-color: #2e7d32;
                padding: 8px;
                color: #ffffff;
            }
            QTabBar::tab:selected {
                background-color: #388e3c;
            }
        """)
    
    def change_accent_color(self):
        try:
            color = QColor(0, 120, 212)  # Стандартний синій колір Windows
            self.customizer.set_accent_color((color.red(), color.green(), color.blue()))
            QMessageBox.information(self, 'Success', 'Колір акценту змінено')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Помилка при зміні кольору акценту: {str(e)}')
    
    def toggle_dark_mode(self):
        current_theme = self.theme_combo.currentText()
        is_dark = current_theme == 'Dark'
        self.customizer.set_system_theme(not is_dark)
        self.theme_combo.setCurrentText('Light' if is_dark else 'Dark')
    
    def change_system_font(self):
        self.customizer.set_system_font('Segoe UI')
        QMessageBox.information(self, 'Success', 'Системний шрифт змінено')
    
    def toggle_visual_effects(self):
        self.customizer.set_visual_effects(True)
        QMessageBox.information(self, 'Success', 'Візуальні ефекти налаштовано')
    
    def customize_start_menu(self):
        self.customizer.customize_start_menu(True, True)
        QMessageBox.information(self, 'Success', 'Меню Пуск налаштовано')
    
    def customize_taskbar(self):
        self.customizer.set_taskbar_transparency(True)
        QMessageBox.information(self, 'Success', 'Панель завдань налаштовано')
    
    def customize_notifications(self):
        self.customizer.set_notification_settings(True, False)
        QMessageBox.information(self, 'Success', 'Налаштування сповіщень змінено')
    
    def customize_privacy(self):
        self.customizer.set_privacy_settings(False, True, True)
        QMessageBox.information(self, 'Success', 'Налаштування конфіденційності змінено')
    
    def apply_desktop_settings(self):
        icon_size = self.icon_size_spin.value()
        hide_icons = self.hide_icons_check.isChecked()
        auto_arrange = self.auto_arrange_check.isChecked()
        
        self.customizer.set_desktop_icon_size(icon_size)
        self.customizer.customize_desktop(hide_icons, auto_arrange)
        QMessageBox.information(self, 'Success', 'Налаштування робочого столу застосовано')
    
    def update_startup_list(self):
        self.startup_list.clear()
        startup_programs = self.customizer.get_startup_programs()
        for program in startup_programs:
            self.startup_list.addItem(f"{program['name']} ({program['type']})")
    
    def toggle_startup(self):
        current_item = self.startup_list.currentItem()
        if current_item:
            program_name = current_item.text().split(' (')[0]
            startup_programs = self.customizer.get_startup_programs()
            for program in startup_programs:
                if program['name'] == program_name:
                    is_enabled = not program['path'].endswith('.disabled')
                    self.customizer.toggle_startup_program(program, not is_enabled)
                    self.update_startup_list()
                    break
    
    def clean_system(self):
        self.cleanup_progress.show()
        self.cleanup_progress.setRange(0, 100)
        self.cleanup_progress.setValue(0)
        
        cleaned_space = self.customizer.clean_system()
        total_cleaned = (cleaned_space['temp'] + cleaned_space['recycle_bin']) / (1024 * 1024)  # MB
        
        self.cleanup_progress.setValue(100)
        QMessageBox.information(self, 'Success', 
                              f'Очищено {total_cleaned:.2f} MB')
        self.cleanup_progress.hide()
    
    def optimize_services(self):
        self.customizer.optimize_services()
        QMessageBox.information(self, 'Success', 'Служби оптимізовано')

    def change_wallpaper(self):
        try:
            self.customizer.set_wallpaper()
            QMessageBox.information(self, 'Success', 'Шпалери змінено')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Помилка при зміні шпалер: {str(e)}')

    def change_lockscreen(self):
        try:
            self.customizer.set_lockscreen()
            QMessageBox.information(self, 'Success', 'Екран блокування змінено')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Помилка при зміні екрану блокування: {str(e)}')

    def apply_power_settings(self):
        try:
            power_scheme = self.findChild(QComboBox, 'power_scheme')
            monitor_timeout = self.findChild(QSpinBox, 'monitor_timeout')
            disk_timeout = self.findChild(QSpinBox, 'disk_timeout')
            scheme = power_scheme.currentText()
            monitor = monitor_timeout.value()
            disk = disk_timeout.value()
            self.customizer.set_power_settings(scheme, monitor, disk)
            QMessageBox.information(self, 'Success', 'Налаштування живлення змінено')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Помилка при зміні налаштувань живлення: {str(e)}')

    def apply_sound_settings(self):
        try:
            volume_slider = self.findChild(QSlider, 'volume_slider')
            mute_check = self.findChild(QCheckBox, 'mute_check')
            system_sounds_check = self.findChild(QCheckBox, 'system_sounds_check')
            volume = volume_slider.value()
            mute = mute_check.isChecked()
            system_sounds = system_sounds_check.isChecked()
            self.customizer.set_sound_settings(volume, mute, system_sounds)
            QMessageBox.information(self, 'Success', 'Налаштування звуку змінено')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Помилка при зміні налаштувань звуку: {str(e)}')

    def apply_display_settings(self):
        try:
            brightness_slider = self.findChild(QSlider, 'brightness_slider')
            resolution_combo = self.findChild(QComboBox, 'resolution_combo')
            refresh_rate = self.findChild(QComboBox, 'refresh_rate')
            brightness = brightness_slider.value()
            resolution = resolution_combo.currentText()
            refresh = refresh_rate.currentText()
            self.customizer.set_display_settings(brightness, resolution, refresh)
            QMessageBox.information(self, 'Success', 'Налаштування дисплею змінено')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Помилка при зміні налаштувань дисплею: {str(e)}')

def main():
    try:
        app = QApplication(sys.argv)
        window = CustomizationApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        raise

if __name__ == '__main__':
    main()
