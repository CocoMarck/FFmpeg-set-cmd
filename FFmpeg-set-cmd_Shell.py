from Modulos import Modulo_FFmpeg as FFmpeg

from Modulos.Modulo_System import(
    get_system,
    CleanScreen,
    Command_Run
)

from Modulos.Modulo_Language import (
    get_text as Lang
)

from Modulos.Modulo_ShowPrint import (
    Title,
    Continue,
    Separator,
    Archive_Path
)
import pathlib, os


sys = get_system()

def Menu_FFmpeg():
    cfg_file = 'FFmpeg_cfg.txt'
    
    loop = True
    while loop == True:
        CleanScreen()
        opc = input(
            Title(text=Lang('option'), print_mode=False) +
            f'1. {Lang("cfg")} - Video\n'
            f'2. {Lang("record")}\n'
            f'3. {Lang("reproduce")}\n'
            f'4. {Lang("help")}\n'
            f'9. {Lang("view_cfg")}\n'
            f'0. {Lang("exit")}\n\n'
            
            f'{Lang("set_option")}: '
        )
        cfg = '' # Sin Configurar
        cfg_save = False
        CleanScreen()
        if opc == '1':
            cfg = Config_Video()
            cfg_save = True
        
        elif opc == '2':
            cfg = Record()
            cfg_save = True
        
        elif opc == '3':
            cfg = Reproduce()
            cfg_save = True
            
        elif opc == '4':
            cfg = FFmpeg.Command('Help')
            cfg_save = True
            
        elif opc == '9':
            if pathlib.Path(cfg_file).exists():
                with open(cfg_file, 'r') as file_cfg:
                    read_cfg = file_cfg.read()
                    input(
                        read_cfg +
                        '\n\n'
                        f'{Lang("continue_enter")}...'
                    )
                    
        elif opc == '0':
            loop = False
            print(f"{Lang('bye')}...")
        
        else:
            input(
                f'No existe la opción "{opc}".\n'
                f'{Lang("continue_enter")}...'
            )
            
        if cfg_save == True:
            if cfg == '': pass
            else:
                CleanScreen()
            
                opc = Continue(
                    Title(Lang('cfg'), print_mode=False) +
                    f'{cfg}\n\n¿{Lang("continue")}?'
                )
                
                if opc == 's':
                    Command_Run(
                        str(cfg), 
                        text_input=Lang('continue_enter'),
                        open_new_terminal=False
                    )
                    with open(cfg_file, 'a') as file_cfg:
                        file_cfg.write(
                            cfg + '\n' + Separator(print_mode=False) + '\n\n'
                        )
                
                elif opc == 'n':
                    pass
                    
                else:
                    Continue(text=opc, message_error = True)
            
        else:
            pass
            
            
def Config_Video():
    # ffmpeg -i '/Ruta/VideoEntrada.mkv' -cfg 0/50 -r 0 '/Ruta/VideoSalida.mkv'
    
    path = Archive_Path()
    
    opc = Continue(
        Title(f'CRF {Lang("quality")}', print_mode=False) +
        f'¿{Lang("continue")} (crf)?'
    )
    if opc == 's':
        Title(f'CRF {Lang("quality")}')
        print(FFmpeg.Message('crf') + '\n')
        
        crf = FFmpeg.CRF(input('CRF: '))
        
    else:
        crf = ''
        
    print()
    opc = Continue(
        Title(f'{Lang("resolution")} - Video', print_mode=False) +
        f'¿{Lang("continue")}?'
    )
    if opc == 's':
        Title(f'{Lang("resolution")} - Video')
        print(FFmpeg.Message('resolution') + '\n')
    
        rez = FFmpeg.Resolution(
            rez_H = input(f'{Lang("resolution")} - Horizontal: '),
            rez_V = input(f'{Lang("resolution")} - Vertical: ')
        )
        
    else:
        rez = ''
    
    print()
    opc = Continue(
        Title(Lang('fps'), print_mode=False) +
        f'¿{Lang("continue")}?'
    )
    if opc == 's':
        Title(Lang('fps'))
        print(FFmpeg.Message('fps') + '\n')
        fps = FFmpeg.FPS(input('FPS: '))
        
    else:
        fps = ''
        
    opc = Continue(f'¿{Lang("cfg")} - video?')
    if opc == 's':    
        cfg = (
            f'ffmpeg -i "{path}" {crf} {rez} {fps} "{path}_Config.mkv"'
        )
    
    else:
        cfg = ''
    
    return cfg
    
    
def Record(opc=''):
    if opc == '':
        opc = input(
            Title(Lang('record'), print_mode=False) +
            f'1. {Lang("rec_audio")}\n'
            f'2. {Lang("rec_video")}\n'
            '\n'
            f'{Lang("set_option")}: '
        )
        if opc == '1': opc = 'Audio'
        elif opc == '2': opc = 'Desktop'
        else: pass
        
    else: pass
    
    if sys == 'linux':
        Desktop = '-f x11grab -i :0'
    
    elif sys == 'win':
        Desktop = '-f gdigrab -i desktop'
        
    CleanScreen()
    
    if (
        opc == 'Audio' or
        opc == 'Desktop'
    ):
        path = Archive_Path('Video/Audio')
    else:
        pass
    
    if opc == 'Audio':
        try:
            adi = int(input('¿Cuantos audios quieres grabar?: '))
        
        except:
            adi = 0
            
        CleanScreen()
        if adi >= 2:
            print(FFmpeg.Message('Audio') + '\n')
            os.system(FFmpeg.Command('Audio'))
            cfg = (
                f'ffmpeg {FFmpeg.Audio_Filter(flt=adi)} '
                f'-filter_complex amix=inputs={adi} '
                f'"{path}.ogg"'
            )
            
        elif adi == 1:
            print(FFmpeg.Message('Audio') + '\n')
            os.system(FFmpeg.Command('Audio'))
            cfg = (
                f'ffmpeg {FFmpeg.Audio(input("¿Cual es el audio?: "))} '
                f'"{path}.ogg"'
            )
        
        else:
            cfg = ''
    
    elif opc == 'Desktop':
        opc = Continue('¿Configuración Avanzada?')
        
        if opc == 's':
            opc = 'Modo Avanzado'
            
        elif opc == 'n':
            opc = 'Modo Basico'
            
        if opc == 'Modo Avanzado':
            Title('Calidad - CRF')
            print(FFmpeg.Message('crf') + '\n')
            CRF = FFmpeg.CRF(input('CRF: '))
            
            print()
            Title(f'{opc} / {Lang("cpu_use")} - Preset')
            print(FFmpeg.Message('preset') + '\n')
            Preset = input(
                "Rango del 1 al 9. Donde 1 es la opcion que usa "
                "menos cpu y 9 la que usa mas cpu.\n"
                "   1. ultrafast\n"
                "   2. superfast\n"
                "   3. veryfast\n"
                "   4. faster\n"
                "   5. fast\n"
                "   6. medium\n"
                "   7. slow\n"
                "   8. slower\n"
                "   9. veryslow\n"
                '\n'
                'Preset: '
            )

            if Preset == 1: Preset = 'ultrafast'
            elif Preset == 2: Preset = 'superfast'
            elif Preset == 3: Preset = 'veryfast'
            elif Preset == 4: Preset = 'faster'
            elif Preset == 5: Preset = 'fast'
            elif Preset == 6: Preset = 'medium'
            elif Preset == 7: Preset = 'slow'
            elif Preset == 8: Preset = 'slower'
            elif Preset == 9: Preset = 'veryslow'
            else:
                Preset = 'medium'
            
            Preset = FFmpeg.Preset(Preset)
            
            print()
            Title(f'{opc} / Resolución')
            print(FFmpeg.Message('resolution') + '\n')
            Resolution = FFmpeg.Resolution(
                rez_H = input('Resolución Horizontal: '),
                rez_V = input('Resolución Vertical: '),
            )
            
            print()
            Title(f'{opc} / {Lang("fps")} - FPS')
            print(FFmpeg.Message('fps') + '\n')
            FPS = FFmpeg.FPS(input('FPS: '))
            
            print()
            opc = Continue(
                Title(opc, print_mode=False) +
                f'¿{Lang("rec_audio")}?'
            )
            if opc == 's':
                try:
                    adi = int(input('¿Cuantos audios quieres grabar?: '))
                    
                except:
                    adi = 0
                    print(
                        '\nSolo numeros enteros, no se configurara el audio\n'
                    )
                    
                if adi >= 2:
                    print(FFmpeg.Message('audio') + '\n')
                    os.system(FFmpeg.Command('Audio'))
                    cfg = (
                        f'ffmpeg {Desktop} '
                        f'{FFmpeg.Audio_Filter(adi)} '
                        f'{CRF} {Preset} {Resolution} {FPS} '
                        f'-filter_complex amix=inputs={adi} "{path}.mkv"'
                    )
                
                elif adi == 1:
                    print(FFmpeg.Message('audio') + '\n')
                    os.system(FFmpeg.Command('Audio'))
                    cfg = (
                        f'ffmpeg {Desktop} '
                        f'{FFmpeg.Audio(input("¿Cual es el audio?"))} '
                        f'{CRF} {Preset} {Resolution} {FPS} "{path}.mkv"'
                    )
                    
                else:
                    cfg = (
                        f'ffmpeg {Desktop} '
                        f'{CRF} {Preset} {Resolution} {FPS} "{path}.mkv"'
                    )
                    
            elif opc == 'n':
                cfg = (
                    f'ffmpeg {Desktop} '
                    f'{CRF} {Preset} {Resolution} {FPS} "{path}.mkv"'
                )
        
        elif opc == 'Modo Basico':
            opc = Continue(
                Title(text=opc, print_mode=False) +
                '¿Grabar con audio?'
            )
            if opc == 's':
                try:
                    adi = int(input('¿Cuantos audios quieres grabar?: '))
                    
                except:
                    adi = 0
                    print(
                        '\nSolo numeros enteros, no se configurara el audio\n'
                    )
                
                if adi >= 2:
                    print(FFmpeg.Message('audio') + '\n')
                    os.system(FFmpeg.Command('Audio'))
                    cfg = (
                        f'ffmpeg {Desktop} '
                        f'{FFmpeg.Audio_Filter(adi)} '
                        f'-r 24 -s 1280x720 -filter_complex amix=inputs={adi} '
                        f'"{path}.mkv"'
                    )
                    
                elif adi == 1:
                    print(FFmpeg.Message('audio') + '\n')
                    os.system(FFmpeg.Command('Audio'))
                    cfg = (
                        f'ffmpeg {Desktop} '
                        f'{FFmpeg.Audio(input("¿Cual es el audio?: "))} '
                        f'-r 24 -s 1280x720 "{path}.mkv"'
                    )
                    
                else:
                    cfg = (
                        f'ffmpeg {Desktop} '
                        f'-r 24 -s 1280x720 "{path}.mkv"'
                    )
                
                
            elif opc == 'n':
                cfg = (
                    f'ffmpeg {Desktop} '
                    f'-r 24 -s 1280x720 "{path}.mkv"'
                )
            
    else:
        cfg = ''
        
    return cfg
    
    
def Reproduce(opc = ''):
    if opc == '':
        nmr = input(
            Title(Lang('reproduce'), print_mode=False) +
            f'1. {Lang("arch")} Video/Audio\n'
            f'2. {Lang("disp_audio")}\n'
            '\n'
            f'{Lang("set_option")}: '
        )
        
    else:
        pass
        
    if nmr == '1': opc = 'Archive'
    if nmr == '2': opc = 'Audio'
    else:
        pass
        
    CleanScreen()
    if opc == 'Archive':
        Title(f'{Lang("dir")} - Video/Audio')
        cfg = (
            'ffplay -i ' + 
            '"' +
            Archive_Path('Video/Audio') + 
            '"'
        )
              
    elif opc == 'Audio':
        print(FFmpeg.Message('Audio') + '\n')
        os.system(FFmpeg.Command('Audio'))
        print('\n')
    
        adi = FFmpeg.Audio(input('¿Cual es el audio?: '))
        cfg = f'ffplay {adi}'
        
    else:
        cfg = ''
        
    return cfg
        
        
if __name__ == '__main__':
    Menu_FFmpeg()