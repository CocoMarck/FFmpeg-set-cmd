import Modulo_Util as Util
import os

import gi
import Modulo_FFmpeg as FFmpeg

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


sys = Util.System()

class Dialog_Start(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Dialogo Empezar', transient_for=parent, flags=0)
        self.set_default_size(256, 64)
                
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        label_title = Gtk.Label()
        label_title.set_markup('<b>Dialogo Empezar</b>')
        label_title.set_justify(Gtk.Justification.CENTER)
        box_v.pack_start(label_title, True, True, 0)
        
        btn_demo = Gtk.Button(label='Boton de prueba')
        btn_demo.connect('clicked', self.evt_demo)
        box_v.pack_start(btn_demo, True, True, 0)
        
        box_main = self.get_content_area()
        box_main.add(box_v)
        self.show_all()
        
    def evt_demo(self, widget):
        print('Boton de prueba, precionado')


class Dialog_FFmpegVideo(Gtk.Dialog):
    def __init__(self, parent, opc='CompressVideos'):
        if opc == 'VideoCompress': txt_title = 'Comprimir Videos'
        elif opc == 'VideoRecord': txt_title = 'Grabar Videos'
        else: 'Title for else'
    
        super().__init__(title=f'{opc}', transient_for=parent, flags=0)
        self.set_default_size(256, 128)
        
        box_data = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        
        label_title = Gtk.Label()
        label_title.set_markup(f'<b>{txt_title}</b>\n')
        box_data.pack_start(label_title, True, True, 8)
        
        btn_path = Gtk.Button(label='Elegir Video')
        btn_path.connect("clicked", self.evt_path)
        self.pth = ''
        box_data.pack_start(btn_path, True, True, 0)


        crf_box = Gtk.Box(spacing=4)
        box_data.pack_start(crf_box, True, True, 0)

        crf_label = Gtk.Label(label='Calidad (CRF de 0-50)')
        crf_label.set_justify(Gtk.Justification.LEFT)
        crf_box.pack_start(crf_label, False, False, 0)

        crf_SpinButton_adj = Gtk.Adjustment(
                                upper=50, step_increment=1, page_increment=10, 
                                value=30
                             )
        self.crf_SpinButton = Gtk.SpinButton()
        self.crf_SpinButton.set_adjustment(crf_SpinButton_adj)
        self.crf_SpinButton.set_numeric(True)
        crf_box.pack_start(self.crf_SpinButton, True, True, 0)
        

        fps_box = Gtk.Box(spacing=4)
        box_data.pack_start(fps_box, True, True, 0)
        
        fps_label = Gtk.Label(label='Fotogramas (FPS)')
        fps_label.set_justify(Gtk.Justification.LEFT)
        fps_box.pack_start(fps_label, False, False, 0)
        
        self.fps_SpinButton = Gtk.SpinButton()
        fps_SpinButton_adj = Gtk.Adjustment(
            step_increment=1, page_increment=10
        )
        self.fps_SpinButton.set_adjustment(fps_SpinButton_adj)
        self.fps_SpinButton.set_range(1, 100)
        self.fps_SpinButton.set_value(25)
        self.fps_SpinButton.set_numeric(True)
        fps_box.pack_start(self.fps_SpinButton, True, True, 0)
        
        
        rez_box = Gtk.Box(spacing=4)
        box_data.pack_start(rez_box, True, True, 0)
        
        rez_label = Gtk.Label(label='Resolucion (H x V)')
        rez_label.set_justify(Gtk.Justification.LEFT)
        rez_box.pack_start(rez_label, False, False, 0)
        
        self.rez_entryH = Gtk.Entry()
        self.rez_entryH.set_text('1280')
        rez_box.pack_start(self.rez_entryH, True, True, 0)
        
        rez_label_HxV = Gtk.Label(label='x')
        rez_box.pack_start(rez_label_HxV, True, True, 0)
        
        self.rez_entryV = Gtk.Entry()
        self.rez_entryV.set_text('720')
        rez_box.pack_start(self.rez_entryV, True, True, 0)
        
        
        self.label_path = Gtk.Label(label='(Aqui se mostrara el Video)')
        self.label_path.set_line_wrap(True)
        box_data.pack_start(self.label_path, True, True, 8)
        
        btn_add_cfg = Gtk.Button(label='Aceptar')
        btn_add_cfg.connect('clicked', self.evt_add_cfg)
        box_data.pack_start(btn_add_cfg, True, True, 0)
        
        box_main = self.get_content_area()
        box_main.add(box_data)
        self.show_all()
        
    def evt_add_cfg(self, widget):
        Util.CleanScreen()
        
        if self.pth == '': print('No se a seleccionado el Video')
        else:
            crf = FFmpeg.CRF(self.crf_SpinButton.get_value_as_int())
            
            fps = FFmpeg.FPS(self.fps_SpinButton.get_value_as_int())

            rez_HxV = FFmpeg.Resolution(
                rez_H=self.rez_entryH.get_text(), 
                rez_V=self.rez_entryV.get_text()
            )

            print(
                f'Video seleccionado: "{self.pth}\n"'
                f'El CRF sera "{crf}"\n'
                f'Los FPS seran "{fps}"\n'
                f'La resolución sera "{rez_HxV}"'
            )
            os.system('xfce4-terminal --startup-id= -e '
                f"""'ffmpeg -i "{self.pth}" {crf} {fps} {rez_HxV} "{self.pth}_Comprimido.mkv"'"""
            )
        
            
    def evt_path(self, widget):
        dialog = Gtk.FileChooserDialog(
            title='Porfavor elige un video', parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        
        # crear "def add_flt ()" para agregar los filtros correspondientes
        self.add_flt(dialog)
        
        rsp = dialog.run()
        if rsp == Gtk.ResponseType.OK:
            self.pth = dialog.get_filename()
            self.label_path.set_text(f'Archivo: {self.pth}')
            print('Abrir clickeado')
        elif rsp == Gtk.ResponseType.CANCEL:
            print('Cancelar clickeado')
            
        dialog.destroy()
        
    def add_flt(self, dialog):
        flt_video = Gtk.FileFilter()
        flt_video.set_name("Archivos de Video")
        flt_video.add_mime_type("video/*")
        dialog.add_filter(flt_video)
            

class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__(title='Ventana Main')
        self.set_resizable(False)
        self.set_default_size(224, 128)
        
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        label_title = Gtk.Label()
        label_title.set_markup('<b>Opciones</b>\n')

        box_v.pack_start(label_title, True, True, 8)

        btn_ffmpeg_compress = Gtk.Button(label='Comprimir videos')
        btn_ffmpeg_compress.connect("clicked", self.evt_ffmpeg_compress)
        box_v.pack_start(btn_ffmpeg_compress, True, True, 0)
        
        btn_ffmpeg_record = Gtk.Button(label='Grabar')
        btn_ffmpeg_record.connect("clicked", self.evt_ffmpeg_record)
        box_v.pack_start(btn_ffmpeg_record, True, True, 0)
        
        btn_txt_view = Gtk.Button(label='Ver comandos creados')
        btn_txt_view.connect("clicked", self.evt_text_view)
        box_v.pack_start(btn_txt_view, True, True, 0)

        btn_exit = Gtk.Button(label='Salir')
        btn_exit.connect("clicked", self.evt_exit)
        box_v.pack_start(btn_exit, True, True, 0)
        
        self.add(box_v)
        
    def evt_ffmpeg_compress(self, widget):
        dialog = Dialog_FFmpegVideo(self, opc='VideoCompress')
        response = dialog.run()
        dialog.destroy()
        print('Comprimir videos')
        
    def evt_ffmpeg_record(self, widget):
        dialog = Dialog_FFmpegVideo(self, opc='VideoRecord')
        response = dialog.run()
        dialog.destroy()
        print('Grabar Audio o video')
        
    def evt_text_view(self, widget):
        print('Abrir archivo de texto')
        
    def evt_exit(self, widget):
        exit()
        

win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
