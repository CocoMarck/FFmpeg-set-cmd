import sys
from PyQt6.QtWidgets import(
    QApplication,
    QWidget,
    QDialog,
    QFileDialog,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QSpinBox,
    QComboBox,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout
)
from PyQt6.QtCore import Qt
from pathlib import Path
import subprocess
import Modulo_FFmpeg as FFmpeg
import Modulo_Util as Util
import Modulo_Util_Qt as Util_Qt


system = Util.System()
cfg_file = 'FFmpeg_cfg.txt'


class Window_Menu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle('FFmpeg - Menu')
        self.setMinimumWidth(256)
        self.setMinimumHeight(232)
        
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
        
        layout.addStretch()
        
        button_help = QPushButton('Ayuda', self)
        button_help.clicked.connect(self.evt_help)
        layout.addWidget(button_help)
        
        button_exit = QPushButton('Salir', self)
        button_exit.clicked.connect(self.evt_exit)
        layout.addWidget(button_exit)
        
        # Mostrar ventana
        self.show()
        
    def evt_compress(self):
        dialog = Dialog_VideoAudio(opc='VideoConfig')
        #dialog.setGeometry( # Para iniciar en el medio de la ventana
        #    self.geometry().center().x() - 100, 
        #    self.geometry().center().y() - 50, 200, 100
        #)
        dialog.exec()
        
    def evt_record(self):
        dialog = Dialog_VideoAudio(opc='VideoRecord')
        dialog.exec()
    
    def evt_reproduce(self):
        dialog = Dialog_Reproduce()
        dialog.exec()
        
    def evt_help(self):
        dialog = Util_Qt.Dialog_Command_Run(
            cmd='ffmpeg -h',
            cfg_file=cfg_file
        )
        dialog.exec()
    
    def evt_view_cfg(self):
        if Path(cfg_file).exists():
            text = Util.Text_Read(cfg_file, 'ModeText')
        else:
            text = f'No existe el archivo de texto "{cfg_file}"'
        dialog = Util_Qt.Dialog_TextEdit(text=text)
        dialog.exec()
    
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
        self.setMinimumWidth(512)
        self.setMinimumHeight(308)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccion Vertical - Elegir Video
        button_set_video = QPushButton('Seleccionar - Video/Audio')
        if opc == 'VideoConfig':
            button_set_video.clicked.connect(self.evt_set_VideoArchive)
        elif opc == 'VideoRecord':
            button_set_video.clicked.connect(self.evt_set_VideoSave)
        else: 
            pass
        vbox_main.addWidget(button_set_video)
        
        self.label_set_video = QLabel('')
        self.label_set_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_set_video.setWordWrap(True)
        vbox_main.addWidget(self.label_set_video)
        
        self.path_video = ''
        self.evt_path()
        
        vbox_main.addStretch()
        
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
            
        # Seccion Vertical - Unicamente en VideoRecord
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
        
        # Seccion Vertical - Unicamente de VideoRecord o AudioRecord
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
            vbox_main.addStretch()
            
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
        vbox_main.addStretch()
        
        button_add_cfg = QPushButton(f'Empezar - {opc}')
        button_add_cfg.clicked.connect(self.evt_add_cfg)
        vbox_main.addWidget(button_add_cfg)
        
    def evt_set_VideoArchive(self):
        video_name, ok = QFileDialog.getOpenFileName(
            self,
            'Seleccionar un Video',
            '', # Ruta
            'Videos (*.mkv *.mp4 *.mov *webm)'
        )
        if video_name:
            self.path_video = str(Path(video_name))
        else:
            self.path_video = ''
        self.evt_path()
        
    def evt_set_VideoSave(self):
        video_name, _ = QFileDialog.getSaveFileName(
            self,
            'Guardar Archivo', 
            '', # Ruta
            'Videos(*.mkv *.mp4 *.mov *webm);;Todo(*)'
        )
        if video_name:
            self.path_video = f'{str(Path(video_name))}.mkv'
        else:
            self.path_video = ''
        self.evt_path()

    def evt_path(self):
        if self.path_video == '':
            self.label_set_video.setText(
                '<small><b>'
                'VIDEO SIN SELECCIONAR'
                '</b></small>'
            )
        else:
            self.label_set_video.setText(
                '<small>Video seleccionado</small>'
            )
        
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


class Dialog_Reproduce(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        
        self.setWindowTitle('FFmpeg - Reproduce')
        self.setMinimumWidth(512)
        self.setMinimumHeight(256)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout(self)
        self.setLayout(vbox_main)
        
        # Crear contenedor de Pestañas y añadirla al contenedor principal
        tab = QTabWidget(self)
        vbox_main.addWidget(tab)
        
        
        # Pestaña 1 - Reproducir Archivo de Video o Audio
        page_VideoAudio = QWidget(self)
        tab.addTab(page_VideoAudio, 'Reproducir - Archivo Video/Audio')
        
        vbox = QVBoxLayout()
        page_VideoAudio.setLayout(vbox)
        
        button_VideoAudio = QPushButton(
            'Seleccionar Video o Audio', self
        )
        button_VideoAudio.clicked.connect(self.evt_reproduce_VideoAudio)
        vbox.addWidget(button_VideoAudio)
        
        
        # Pestaña 2 - Reproducir Dispositivo de Audio
        page_dispAudio = QWidget(self)
        tab.addTab(page_dispAudio, 'Reproducir - Dispositivo de Audio')
        
        # Contenedor Principal 
        vbox = QVBoxLayout()
        page_dispAudio.setLayout(vbox)
        
        # Seccion vertical 1
        label_dispAudio = QLabel('', self)
        audio_cmd = subprocess.check_output(
            FFmpeg.Command('Audio'), shell=True, text=True
        )
        label_dispAudio.setText(
            '<b>Comando para ver dispositivos de audio:</b> <br>'
            f'"{FFmpeg.Command("Audio")}" <br><br>' # <br> = salto de linea
            
            f'<b>{FFmpeg.Message("Audio")}</b> <br>'
            f'<small><i>{audio_cmd}</i></small>'
        )
        label_dispAudio.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse | 
            Qt.TextInteractionFlag.TextSelectableByKeyboard
        )
        label_dispAudio.setWordWrap(True)
        vbox.addWidget(label_dispAudio)
        
        # Seccion vertical 2
        vbox.addStretch()
        
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        
        label = QLabel('Audio:')
        hbox.addWidget(label)
        
        self.entry_dispAudio = QLineEdit(
            self,
            placeholderText='Dispositivo de Audio',
            clearButtonEnabled=True
        )
        hbox.addWidget(self.entry_dispAudio)
        
        # Seccion vertical 3 - Boton de disp Audio
        button_dispAudio = QPushButton('Reproducir audio')
        button_dispAudio.clicked.connect(self.evt_reproduce_dispAudio)
        vbox.addWidget(button_dispAudio)
        
    def evt_reproduce_VideoAudio(self):
        pass

    def evt_reproduce_dispAudio(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Menu()
    sys.exit(app.exec())