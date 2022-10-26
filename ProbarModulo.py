import ModuloDePrueba as Util
import os, pathlib

def App_FFmpeg():
#    input(Util.FFmpeg('Resolution', False))
    
    cfg_file = 'ProbarModulo_cfg.txt'
    loop = True
    while loop == True:
        Util.CleanScreen()
        opc = input(Util.Title(txt='Opciones', see=False) +
                '1. Comprimir videos\n'
                '2. Grabar Audio\n'
                '0. Salir\n\n'
                'Elige una opción: ')
        cfg = '#SinConfigurar'
        cfg_save = False
        Util.CleanScreen()
        if opc == '1':
            cfg = Compress_Video()
            cfg_save = True
        elif opc == '2':
            cfg = Record_Audio()
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
                     f'{cfg}\n\n¿Continuar?')

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

    pth = Util.Path()
    nme = Util.Name()

    Util.Title(txt='CRF Calidad')
    opc = input('¿Comprimir Video (crf)? s/n: ')
    Util.CleanScreen()
    if opc == 's':
        crf = Util.FFmpeg('Quality', 'Calidad')
    else: crf = ''

    Util.Title(txt='Resolución de video')
    opc = input('¿Rescalar video (resolución)? s/n: ')
    Util.CleanScreen()
    if opc == 's':
        rlt = Util.FFmpeg('Resolution', 'Resolución de video')
    else: rlt = ''

    Util.Title(txt='Fotogramas por segundo')
    opc = input('¿Cambiar fps? s/n: ')
    Util.CleanScreen()
    if opc == 's':
        fps = Util.FFmpeg('Frame', 'Fotorgramas (FPS)')
    else: fps = ''

    cfg = (f"ffmpeg -i {pth}'{nme}' {crf} {rlt} {fps} "
           f"{pth}'{nme}_Comprimido.mkv'")
    
    return cfg

def Record_Audio():
    adi = int(input('¿Cuantos audios quieres grabar?: '))
    Util.CleanScreen()
    if adi >= 2:
        cfg = (f"ffmpeg {Util.FFmpeg('AudioFilter', flt = adi)} "
            f"-filter_complex amix=inputs={adi} "
            f"{Util.Path()}'{Util.Name('Audio')}.ogg'")
    elif adi == 1:
        cfg = (f"ffmpeg {Util.FFmpeg('Audio')} "
            f"{Util.Path()}'{Util.Name('Audio')}.ogg'")
    else:
        cfg = Util.FFmpeg('AudioFilter', flt=adi)

    return cfg

if __name__ == '__main__':
    App_FFmpeg()