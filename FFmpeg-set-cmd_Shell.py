import Modulo_Util as Util
import Modulo_FFmpeg as FFmpeg
import pathlib, os


sys = Util.System()

def Menu_FFmpeg():
    cfg_file = 'FFmpeg_cfg.txt'
    
    loop = True
    while loop == True:
        Util.CleanScreen()
        opc = input(
            Util.Title(txt='Opciones', see=False) +
            '1. Comprimir videos\n'
            '2. Grabar\n'
            '3. Reproducir\n'
            '9. Ver comandos creados\n'
            '0. Salir\n\n'
            
            'Elige una opción: '
        )
        cfg = '' # Sin Configurar
        cfg_save = False
        Util.CleanScreen()
        if opc == '1':
            cfg = Compress_Video()
            cfg_save = True
        
        elif opc == '2':
            cfg = Record()
            cfg_save = True
        
        elif opc == '3':
            cfg = Reproduce()
            cfg_save = True
            
        elif opc == '9':
            if pathlib.Path(cfg_file).exists():
                with open(cfg_file, 'r') as file_cfg:
                    read_cfg = file_cfg.read()
                    input(read_cfg + '\n\nPreciona enter para continuar...')
                    
        elif opc == '0':
            loop = False
            print('Hasta la proxima...')
        
        else:
            input(
                f'No existe la opción "{opc}".\n'
                'Preciona enter para continuar...'
            )
            
        if cfg_save == True:
            if cfg == '': pass
            else:
                Util.CleanScreen()
            
                opc = Util.Continue(
                    Util.Title('Esta es la configuración', see=False) +
                    f'{cfg}\n\n¿Continuar?'
                )
                
                if opc == 's':
                    Util.Command_Run(str(cfg))
                    with open(cfg_file, 'a') as file_cfg:
                        file_cfg.write(cfg + '\n' + Util.Separator() + '\n\n')
                
                elif opc == 'n':
                    pass
                    
                else:
                    Util.Continue(txt=opc, msg = True)
            
        else:
            pass
            
            
def Compress_Video():
    # ffmpeg -i '/Ruta/VideoEntrada.mkv' -cfg 0/50 -r 0 '/Ruta/VideoSalida.mkv'
    
    path = Util.Archive_Path()
    
    opc = Util.Continue(
        Util.Title('CRF Calidad', see=False) +
        '¿Comprimir Video (crf)?'
    )
    if opc == 's':
        Util.Title('CRF Calidad')
        print(FFmpeg.Message('crf') + '\n')
        
        crf = FFmpeg.CRF(input('CRF: '))
        
    else:
        crf = ''
        
    print()
    opc = Util.Continue(
        Util.Title('Resolución de Video', see=False) +
        '¿Rescalar resolución de video?'
    )
    if opc == 's':
        Util.Title('Resolución de Video')
        print(FFmpeg.Message('resolution') + '\n')
    
        rez = FFmpeg.Resolution(
            rez_H = input('Resolución Horizontal: '),
            rez_V = input('Resolución Vertical: ')
        )
        
    else:
        rez = ''
    
    print()
    opc = Util.Continue(
        Util.Title('Fotogramas por segundo', see=False) +
        '¿Cambiar FPS?'
    )
    if opc == 's':
        Util.Title('Fotogramas por segundo')
        print(FFmpeg.Message('fps') + '\n')
        fps = FFmpeg.FPS(input('FPS: '))
        
    else:
        fps = ''
        
    opc = Util.Continue('¿Comprimir Video?')
    if opc == 's':    
        cfg = (
            f'ffmpeg -i "{path}" {crf} {rez} {fps} "{path}_Comprimido.mkv"'
        )
    
    else:
        cfg = ''
    
    return cfg
    
    
def Record(opc=''):
    if opc == '':
        opc = input(
            Util.Title('Opciones para grabar', see=False) +
            '1. Grabar Audio\n'
            '2. Grabar Pantalla\n'
            '\n'
            'Opción: '
        )
        if opc == '1': opc = 'Audio'
        elif opc == '2': opc = 'Desktop'
        else: pass
        
    else: pass
    
    if sys == 'linux':
        Desktop = '-f x11grab -i :0'
    
    elif sys == 'win':
        Desktop = '-f gdigrab -i desktop'
        
    Util.CleanScreen()
    
    if (
        opc == 'Audio' or
        opc == 'Desktop'
    ):
        path = Util.Archive_Path('Video/Audio')
    else:
        pass
    
    if opc == 'Audio':
        try:
            adi = int(input('¿Cuantos Audios quieres grabar?: '))
        
        except:
            adi = 0
            
        Util.CleanScreen()
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
        opc = Util.Continue('¿Configuración Avanzada?')
        
        if opc == 's':
            opc = 'Modo Avanzado'
            
        elif opc == 'n':
            opc = 'Modo Basico'
            
        if opc == 'Modo Avanzado':
            Util.Title('Calidad - CRF')
            print(FFmpeg.Message('crf') + '\n')
            CRF = FFmpeg.CRF(input('CRF: '))
            
            print()
            Util.Title(f'{opc} / Uso de CPU - Preset')
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
            Util.Title(f'{opc} / Resolución')
            print(FFmpeg.Message('resolution') + '\n')
            Resolution = FFmpeg.Resolution(
                rez_H = input('Resolución Horizontal: '),
                rez_V = input('Resolución Vertical: '),
            )
            
            print()
            Util.Title(f'{opc} / Fotogramas - FPS')
            print(FFmpeg.Message('fps') + '\n')
            FPS = FFmpeg.FPS(input('FPS: '))
            
            print()
            opc = Util.Continue(
                Util.Title(opc, see=False) +
                '¿Grabar Audio?'
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
            opc = Util.Continue(
                Util.Title(txt=opc, see=False) +
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
            Util.Title('Reproducir', see=False) +
            '1. Archivo Video/Audio\n'
            '2. Dispositivo de Audio\n'
            '\n'
            'Opción: '
        )
        
    else:
        pass
        
    if nmr == '1': opc = 'Archive'
    if nmr == '2': opc = 'Audio'
    else:
        pass
        
    Util.CleanScreen()
    if opc == 'Archive':
        Util.Title('Ruta de archivo de Video o Audio')
        cfg = (
            'ffplay -i ' + 
            '"' +
            Util.Archive_Path('Video/Audio') + 
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