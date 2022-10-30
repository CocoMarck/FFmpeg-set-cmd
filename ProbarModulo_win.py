import ModuloDePrueba as Util
import os, pathlib

def App_FFmpeg():
#    input(Util.FFmpeg('Resolution', False))
    
    cfg_file = 'ProbarModulo_cfg.txt'
    loop = True
    while loop == True:
        Util.CleanScreen('win')
        opc = input(Util.Title(txt='Opciones', see=False) +
                '1. Comprimir videos\n'
                '2. Grabar\n'
                '0. Salir\n\n'
                'Elige una opción: ')
        cfg = '#SinConfigurar'
        cfg_save = False
        Util.CleanScreen('win')
        if opc == '1':
            cfg = Compress_Video()
            cfg_save = True
        elif opc == '2':
            cfg = Record()
            cfg_save = True
        elif opc == '0':
            loop = False
            print('Saliendo...')
        else:
            pass

        if cfg_save == True:
            if cfg == '': pass
            else:
                opc = Util.Continue(
                     Util.Title('Esta es tu configuración', see=False) +
                     f'{cfg}\n\n¿Continuar?', sys='win')

                if opc == 's':
                    os.system(cfg)
                    with open(cfg_file, 'a') as file_cfg:
                        file_cfg.write(cfg + '\n')
                elif opc == 'n': pass
                else:
                    input(f'La opcion "{opc}" no existe\n'
                          'Precione enter para continuar...')
        else: pass    


def Compress_Video():
#ffmpeg -i '/Ruta/VideoEntrada.mkv' -crf 0/50 -r 0 '/Ruta/VideoSalida.mkv'
#    Util.Title(txt='Comprimir videos')

    pth = Util.Path('win')
    nme = Util.Name(sys='win')
    
    opc = input(Util.Title('CRF Calidad', see=False) +
                '¿Comprimir Video (crf)? s/n: ')
    Util.CleanScreen('win')
    if opc == 's':
        crf = Util.FFmpeg('Quality', 'Calidad')
    else: crf = ''

    
    opc = input(Util.Title(txt='Resolución de video', see=False) +
                '¿Rescalar video (resolución)? s/n: ')
    Util.CleanScreen('win')
    if opc == 's':
        rlt = Util.FFmpeg('Resolution', 'Resolución de video')
    else: rlt = ''

    opc = input(Util.Title('Fotogramas por segundo', see=False) +
                '¿Cambiar fps? s/n: ')
    Util.CleanScreen('win')
    if opc == 's':
        fps = Util.FFmpeg('Frame', 'Fotorgramas (FPS)')
    else: fps = ''

    cfg = (f"ffmpeg -i {pth}'{nme}' {crf} {rlt} {fps} "
           f"{pth}'{nme}_Comprimido.mkv'")
    
    return cfg

def Record(opc = ''):
    if opc == '':
        nmr = input(Util.Title('Opciones para grabar', see=False) +
                    '1. Grabar Audio\n'
                    '2. Grabar Pantalla\n\n'
                    f'Que opción eligieste: ')
    else: pass

    if nmr == '1': opc = 'Audio'
    elif nmr == '2': opc = 'Desktop'
    else: pass

    Util.CleanScreen('win')
    cfg = ''

    if opc == 'Audio':
        adi = int(input('¿Cuantos audios quieres grabar?: '))
        Util.CleanScreen('win')
        if adi >= 2:
            cfg = (f"ffmpeg {Util.FFmpeg('AudioFilter', flt = adi, sys='win')} "
                f"-filter_complex amix=inputs={adi} "
                f"{Util.Path(sys='win')}'{Util.Name('Audio', sys='win')}.ogg'")
        elif adi == 1:
            cfg = (f"ffmpeg {Util.FFmpeg('Audio', sys='win')} "
                f"{Util.Path(sys='win')}'{Util.Name('Audio', sys='win')}.ogg'")
        else:
            cfg = Util.FFmpeg('AudioFilter', flt=adi)

    elif opc == 'Desktop':
        opc = Util.Continue('¿Configuración Avanzada?', sys='win')
        Util.CleanScreen('win')
        if opc == 's':
            Util.Title('Modo Avanzado')
            Quality = Util.FFmpeg('Quality', sys='win')

            Util.Title('Modo Avanzado')
            Preset = Util.FFmpeg('Preset', sys='win')

            Util.Title('Modo Avanzado')
            Resolution = Util.FFmpeg('Resolution', 'Salida', sys='win')

            Util.Title('Modo Avanzado')
            Frame = Util.FFmpeg('Frame', sys='win')

            opc = Util.Continue(Util.Title('Modo Avanzado', see=False) +
                                '¿Grabar con audio?', sys='win')
            Util.CleanScreen('win')
            if opc == 's':
                adi = int(input(Util.Title('Modo Avanzado', see=False) +
                              '¿Cuantos audios quieres grabar?: '))
                Util.CleanScreen('win')

                if adi >= 2:
                    cfg = (f"ffmpeg -f gdigrab -i desktop "
                        f"{Util.FFmpeg('AudioFilter', flt = adi, sys='win')} "
                        f"{Quality} {Preset} {Resolution} {Frame} "
                        f"-filter_complex amix=inputs={adi} "
                        f"{Util.Path('win')}'{Util.Name('Video', sys='win')}.mkv'")
                elif adi == 1:
                    cfg = (f"ffmpeg -f x11grab -i :0 "
                        f"{Util.FFmpeg('Audio', sys='win')} "
                        f"{Quality} {Preset} {Resolution} {Frame} "
                        f"{Util.Path('win')}'{Util.Name('Video', sys='win')}.mkv'")
                else: pass
            else:
                cfg = (f"ffmpeg -f gdigrab -i desktop "
                    f"{Quality} {Preset} {Resolution} {Frame} "
                    f"{Util.Path('win')}'{Util.Name('Video', sys='win')}.mkv'")
        elif opc == 'n':
            opc = Util.Continue(Util.Title('Modo Basico', see=False) +
                      '¿Grabar con audio?')
            Util.CleanScreen('win')
            if opc == 's':
                adi = int(input(Util.Title('Modo Basico', see=False) +
                              '¿Cuantos audios quieres grabar?: '))
                Util.CleanScreen('win')
                Util.Title('Modo Basico')
                if adi >= 2:
                    cfg = (f"ffmpeg -f gdigrab -i desktop "
                        f"{Util.FFmpeg('AudioFilter', flt=adi, sys='win')} "
                        f"-r 24 -s 1280x720 -filter_complex amix=inputs={adi} "
                        f"{Util.Path('win')}'{Util.Name('Video', sys='win')}.mkv'")
                elif adi == 1:
                    cfg = (f"ffmpeg -f gdigrab -i desktop "
                        f"{Util.FFmpeg('Audio', sys='win')} "
                        f"-r 24 -s 1280x720 "
                        f"{Util.Path('win')}'{Util.Name('Video', sys='win')}.mkv'")
                else: pass
            else:
                cfg = (f"ffmpeg -f gdigrab -i desktop -r 24 -s 1280x720 "
                    f"{Util.Path('win')}'{Util.Name('Video', sys='win')}.mkv'")
        else: pass

    return cfg

if __name__ == '__main__':
    App_FFmpeg()