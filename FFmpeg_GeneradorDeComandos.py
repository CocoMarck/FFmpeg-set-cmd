import FFmpeg_Modulo as Util
import os, pathlib, platform

sys = Util.System()

def App_FFmpeg():
#    input(Util.FFmpeg('Resolution', False))
    
    cfg_file = 'FFmpeg_cfg.txt'

    if sys == 'win': txt, smb = 'start cmd /c ', '"'
    else: txt, smb = '', ''

    loop = True
    while loop == True:
        Util.CleanScreen()
        opc = input(Util.Title(txt='Opciones', see=False) +
                '1. Comprimir videos\n'
                '2. Grabar\n'
                '3. Reproducir\n'
                '9. Ver comandos creados\n'
                '0. Salir\n\n'
                'Elige una opción: ')
        cfg = '#SinConfigurar'
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
                    reader = file_cfg.read()
                    input(f'{reader}\n\nPreciona enter para continuar...')
        elif opc == '0':
            loop = False
            print('Saliendo...')
        else:
            input(f'No existe la opción "{opc}".\n'
                  'Preciona enter para continuar...')

        if cfg_save == True:
            if cfg == '': pass
            else:
                opc = Util.Continue(
                     Util.Title('Esta es tu configuración', see=False) +
                     f'{cfg}\n\n¿Continuar?')

                if opc == 's':
                    os.system(f'{txt}{smb}{cfg}{smb}')
                    with open(cfg_file, 'a') as file_cfg:
                        file_cfg.write(cfg + '\n')
                elif opc == 'n': pass
                else:
                    Util.Continue(txt=opc, msg = True)
        else: pass    

def Reproduce(opc = ''):
    if opc == '':
        nmr = input(Util.Title('Reproducir', see=False) +
                    '1. Archivo\n'
                    '2. Audio\n'
                    '\n'
                    'Opcion: ')
    else: pass


    if nmr == '1': opc = 'Archive'
    elif nmr == '2': opc = 'Audio'
    else: pass


    if opc == 'Archive':
        cfg = f'ffplay "{Util.Path()}{Util.Name()}"'
    elif opc == 'Audio':
        try:
            adi = int(input('¿Cuantos audios quieres reproducir?: '))
        except:
            adi = 0
            input('Esa opción no existe, no se configurara el audio\n'
                  'Preciona enter para continuar...')
        cfg = f'ffplay {Util.FFmpeg("AudioFilter", flt=adi)}'
    else: cfg = ''


    return cfg

def Compress_Video():
#ffmpeg -i '/Ruta/VideoEntrada.mkv' -crf 0/50 -r 0 '/Ruta/VideoSalida.mkv'
#    Util.Title(txt='Comprimir videos')

    pth = Util.Path()
    nme = Util.Name()
    
    opc = input(Util.Title('CRF Calidad', see=False) +
                '¿Comprimir Video (crf)? s/n: ')
    Util.CleanScreen()
    if opc == 's':
        crf = Util.FFmpeg('Quality', 'Calidad')
    else: crf = ''

    
    opc = input(Util.Title(txt='Resolución de video', see=False) +
                '¿Rescalar video (resolución)? s/n: ')
    Util.CleanScreen()
    if opc == 's':
        rlt = Util.FFmpeg('Resolution', 'Resolución de video')
    else: rlt = ''

    opc = input(Util.Title('Fotogramas por segundo', see=False) +
                '¿Cambiar fps? s/n: ')
    Util.CleanScreen()
    if opc == 's':
        fps = Util.FFmpeg('Frame', 'Fotorgramas (FPS)')
    else: fps = ''

    cfg = (f'ffmpeg -i "{pth}{nme}" {crf} {rlt} {fps} '
           f'"{pth}{nme}_Comprimido.mkv"')
    
    return cfg

def Record(opc = ''):
    if opc == '':
        nmr = input(Util.Title('Opciones para grabar', see=False) +
                    '1. Grabar Audio\n'
                    '2. Grabar Pantalla\n\n'
                    f'Opción: ')
    else: pass

    if nmr == '1': opc = 'Audio'
    elif nmr == '2': 
        opc = 'Desktop'
        if sys == 'linux':
            Desktop = '-f x11grab -i :0'
        elif sys == 'win':
            Desktop = '-f gdigrab -i desktop'
    else: pass

    Util.CleanScreen()
    cfg = ''

    if opc == 'Audio':
        try: 
            adi = int(input('¿Cuantos audios quieres grabar?: '))
        except:
            adi = 0
            input('Esa opción no existe, no se configurara el audio\n'
                  'Preciona enter para continuar...')
        Util.CleanScreen()
        if adi >= 2:
            cfg = (f"ffmpeg {Util.FFmpeg('AudioFilter', flt = adi)} "
                f"-filter_complex amix=inputs={adi} "
                f'"{Util.Path()}{Util.Name("Audio")}.ogg"')
        elif adi == 1:
            cfg = (f"ffmpeg {Util.FFmpeg('Audio')} "
                f'"{Util.Path()}{Util.Name("Audio")}.ogg"')
        else:
            cfg = Util.FFmpeg('AudioFilter', flt=adi)

    elif opc == 'Desktop':
        opc = Util.Continue('¿Configuración Avanzada?')
        Util.CleanScreen()

        if opc == 's': 
            opc = 'Modo Avanzado'
            Util.Title(txt = opc)
            Path_Fin = f'"{Util.Path("Salida")}{Util.Name("Video")}.mkv"'
        elif opc == 'n':
            opc = 'Modo Basico'
            Util.Title(txt = opc)
            Path_Fin = f'"{Util.Path("Salida")}{Util.Name("Video")}.mkv"'
        else: pass

        if opc == 'Modo Avanzado':
            Util.Title(txt = opc)
            Quality = Util.FFmpeg('Quality')

            Util.Title(txt = opc)
            Preset = Util.FFmpeg('Preset')

            Util.Title(txt = opc)
            Resolution = Util.FFmpeg('Resolution', 'Salida')

            Util.Title(txt = opc)
            Frame = Util.FFmpeg('Frame')

            opc = Util.Continue(Util.Title('Modo Avanzado', see=False) +
                                '¿Grabar con audio?')
            Util.CleanScreen()
            if opc == 's':
                try:
                    adi = int(input(Util.Title('Modo Avanzado', see=False) +
                                  '¿Cuantos audios quieres grabar?: '))
                except:
                    adi = 0
                    input('Esa opción no existe, no se configurara el audio\n'
                          'Preciona enter para continuar...')
                Util.CleanScreen()

                if adi >= 2:
                    cfg = (f"ffmpeg {Desktop} "
                        f"{Util.FFmpeg('AudioFilter', flt = adi)} "
                        f"{Quality} {Preset} {Resolution} {Frame} "
                        f"-filter_complex amix=inputs={adi} "
                        f"{Path_Fin}")
                elif adi == 1:
                    cfg = (f"ffmpeg {Desktop} {Util.FFmpeg('Audio')} "
                        f"{Quality} {Preset} {Resolution} {Frame} "
                        f"{Path_Fin}")
                else: pass
            else:
                cfg = (f"ffmpeg {Desktop} "
                    f"{Quality} {Preset} {Resolution} {Frame} "
                    f"{Path_Fin}")
        elif opc == 'Modo Basico':
            opc = Util.Continue(Util.Title(txt = opc, see=False) +
                      '¿Grabar con audio?')
            Util.CleanScreen()
            if opc == 's':
                adi = int(input(Util.Title(txt = opc, see=False) +
                              '¿Cuantos audios quieres grabar?: '))
                Util.CleanScreen()
                Util.Title(txt = opc)
                if adi >= 2:
                    cfg = (f"ffmpeg {Desktop} "
                        f"{Util.FFmpeg('AudioFilter', flt=adi)} "
                        f"-r 24 -s 1280x720 -filter_complex amix=inputs={adi} "
                        f"{Path_Fin}")
                elif adi == 1:
                    cfg = (f"ffmpeg {Desktop} :0 {Util.FFmpeg('Audio')} "
                        f"-r 24 -s 1280x720 "
                        f"{Path_Fin}")
                else: pass
            else:
                cfg = (f"ffmpeg {Desktop} -r 24 -s 1280x720 "
                    f"{Path_Fin}")
        else: pass

    return cfg

if __name__ == '__main__':
    App_FFmpeg()
