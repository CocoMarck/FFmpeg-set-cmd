import sys
from PyQt6.QtWidgets import(
    QApplication,
    QWidget,
    QDialog,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QSpinBox,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout
)
from PyQt6.QtCore import Qt
import Modulo_FFmpeg as FFmpeg


class Window_Menu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle('FFmpeg - Menu')
        self.setMinimumWidth(256)
        self.setMinimumHeight(190)
        
        # Contenedor Principal
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Secciones verticales - Botones
        button_compress = QPushButton('Configurar Videos', self)
        button_compress.clicked.connect(self.evt_compress)
        layout.addWidget(button_compress)
        
        button_record = QPushButton('Grabar', self)
        button_record.clicked.connect(self.evt_record)
        layout.addWidget(button_record)
        
        button_reproduce = QPushButton('Reproducir', self)
        button_reproduce.clicked.connect(self.evt_reproduce)
        layout.addWidget(button_reproduce)
        
        button_view_cfg = QPushButton('Ver comandos creados', self)
        button_view_cfg.clicked.connect(self.evt_view_cfg)
        layout.addWidget(button_view_cfg)
        
        button_exit = QPushButton('Salir', self)
        button_exit.clicked.connect(self.evt_exit)
        layout.addWidget(button_exit)
        
        # Mostrar ventana
        self.show()
        
    def evt_compress(self):
        dialog = Dialog_VideoAudio(opc='VideoConfig')
        dialog.exec()
        
    def evt_record(self):
        dialog = Dialog_VideoAudio(opc='VideoRecord')
        dialog.exec()
    
    def evt_reproduce(self):
        pass
    
    def evt_view_cfg(self):
        pass
    
    def evt_exit(self):
        self.close()


class Dialog_VideoAudio(QDialog):
    def __init__(self, parent=None, opc='VideoConfig'):
        super().__init__(parent=None)
        
        if (
            opc == 'VideoConfig' or
            opc == 'VideoRecord' or
            opc == 'AudioRecord'
        ):
            title = f'FFmpeg - {opc}'
        else:
            title = ''

        self.setWindowTitle(title)
        self.setMinimumWidth(308)
        self.setMinimumHeight(256)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccion Vertical - Elegir Video
        button_set_video = QPushButton('Seleccionar Video')
        if opc == 'VideoConfig':
            button_set_video.clicked.connect(self.evt_set_VideoArchive)
        elif opc == 'VideoRecord':
            button_set_video.clicked.connect(self.evt_set_VideoDir)
        else: 
            pass
        vbox_main.addWidget(button_set_video)
        
        if (
            opc == 'VideoConfig' or
            opc == 'VideoRecord'
        ):
            # Seccion Vertical - CRF Calidad
            hbox = QHBoxLayout()
            vbox_main.addLayout(hbox)
            
            self.checkbox_crf = QCheckBox('CRF Calidad (Rango 0-50):')
            self.checkbox_crf.setChecked(True)
            hbox.addWidget(self.checkbox_crf)
            
            hbox.addStretch()
            
            self.spinbox_crf = QSpinBox(
                minimum=0, maximum=50, value=30, prefix=''
            )
            hbox.addWidget(self.spinbox_crf)
            
            # Seccion Vertical - FPS Fotogramas
            hbox = QHBoxLayout()
            vbox_main.addLayout(hbox)
            
            self.checkbox_fps = QCheckBox('FPS Fotogramas:')
            self.checkbox_fps.setChecked(True)
            hbox.addWidget(self.checkbox_fps)
            
            hbox.addStretch()
            
            self.spinbox_fps = QSpinBox(
                minimum=1, 
                #maximum=120,
                value=25, prefix=''
            )
            hbox.addWidget(self.spinbox_fps)
            
            # Seccion Vertical - Resolucion HxV
            hbox = QHBoxLayout()
            vbox_main.addLayout(hbox)
            
            self.checkbox_rez = QCheckBox('Resolucion:')
            self.checkbox_rez.setChecked(True)
            hbox.addWidget(self.checkbox_rez)
            
            hbox.addStretch()
            
            self.entry_rezH = QLineEdit('1280')
            self.entry_rezH.setFixedWidth(64) # Dimension en pixeles
            hbox.addWidget(self.entry_rezH)
            
            label_rez = QLabel('x')
            hbox.addWidget(label_rez)
            
            self.entry_rezV = QLineEdit('720')
            self.entry_rezV.setFixedWidth(64) # Dimension en pixeles
            hbox.addWidget(self.entry_rezV)
        else:
            pass
            
        # Seccione Vertical - Unicamente en VideoRecord
        if opc == 'VideoRecord':
            # Uso de CPU
            hbox = QHBoxLayout()
            vbox_main.addLayout(hbox)
            
            self.checkbox_preset = QCheckBox('Uso de CPU:')
            self.checkbox_preset.setChecked(True)
            hbox.addWidget(self.checkbox_preset)
            
            hbox.addStretch()
            
            self.combobox_preset = QComboBox(self)
            for preset in FFmpeg.Preset('list'):
                self.combobox_preset.addItem(preset)
            hbox.addWidget(self.combobox_preset)
        else:
            pass
        
        # Seccion Verticale - Unicamente de VideoRecord o AudioRecord
        if (
            opc == 'VideoRecord' or
            opc == 'AudioRecord'
        ):  
            # Audio
            hbox = QHBoxLayout()
            vbox_main.addLayout(hbox)
            
            self.checkbox_audio = QCheckBox('Audio:')
            hbox.addWidget(self.checkbox_audio)
            
            self.entry_audio = QLineEdit(
                self,
                placeholderText='Dispositivo de Audio',
                clearButtonEnabled=True
            )
            hbox.addWidget(self.entry_audio)
            
            # Boton Modo de Grabacion
            button_recordmode = QPushButton('NoText')
            button_recordmode.clicked.connect(self.evt_recordmode)
            vbox_main.addWidget(button_recordmode)
            self.opc = opc
            
            # Seccion de if para Audio y Boton recordmode
            if opc == 'VideoRecord':
                self.checkbox_audio.setChecked(False)
                button_recordmode.setText('Modo Grabar Audio')
            elif opc == 'AudioRecord':
                self.checkbox_audio.setChecked(True)
                button_recordmode.setText('Modo Grabar Video')
            else:
                pass
        else:
            pass
            
        # Seccion Vertical - Boton Agregar Configuracion
        button_add_cfg = QPushButton(f'Empezar - {opc}')
        button_add_cfg.clicked.connect(self.evt_add_cfg)
        vbox_main.addWidget(button_add_cfg)
        
    def evt_set_VideoArchive(self):
        pass
        
    def evt_set_VideoDir(self):
        pass
        
    def evt_recordmode(self):
        self.close()
        if self.opc == 'VideoRecord':
            dialog = Dialog_VideoAudio(opc='AudioRecord')
            dialog.exec()
        elif self.opc == 'AudioRecord':
            dialog = Dialog_VideoAudio(opc='VideoRecord')
            dialog.exec()
        else:
            pass
        
    def evt_add_cfg(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Menu()
    sys.exit(app.exec())