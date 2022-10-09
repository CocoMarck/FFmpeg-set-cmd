import os
import pathlib

def Audio(txt = 'Dispositivos de audio'):
    print(Titulo(txt = txt), "\n"
        "#Seleccione un numero\n"
        "#EJEMPLO\n"
        "#    Audio: 1\n")
    os.system('pactl list short sources')
    print('\n')
    adi = input('Audio: ')
    adi = f"-f pulse -i {adi}"
    LimpiarPantalla()
    return(adi)

def AudioFiltro( flt = 2 ):
    adi = [''] * flt
    nmr = flt
    txt = ''
    if flt >= 1:        
        Continuar(txt = f'¿La cantidad de audios a grabar son {flt}?')
        while flt > 0:
            adi[flt - 1] = Audio(txt = f'Dispositivo numero {flt}')
            flt = flt - 1        
    else:
        LimpiarPantalla()
        input(f'"{flt}" Significa que no quieres grabar audio.')
        main()

    while nmr > 0:
        txt = adi[nmr - 1] + ' ' + txt
        #input(f"{adi[nmr - 1]}"), Para mostrar las fuentes de audio
        nmr = nmr - 1
    return txt

def Resolucion(txt = ''):
    print(f"//    Resolucion de {txt}    //\n"
        "//  (ancho X alto)  //\n"
        "#EJEMPLOS\n"
        "1920x1080\n"
        "1280x720\n"
        "854x480\n"
    )
    rsl=[0]*3
    rsl[0] = int(input('Ancho: '))
    rsl[1] = int(input('Alto: '))
    LimpiarPantalla()
    rsl[2] = f'-s {rsl[0]}x{rsl[1]}'
    return rsl[2]

def Fotogramas():
    print("//    Fotogramas deseados    //\n"
        "//  (fotogramas X segundo)  //\n"
        "#EJEMPLOS\n"
        "15\n"
        "30\n"
        "60\n"
    )
    fps = [0]*2
    fps[0] = int(input('Fotogramas: '))
    fps[1] = f'-r {fps[0]}'
    LimpiarPantalla()
    return fps[1]

def Calidad():
    print(Titulo(txt = 'Calidad'), '\n'
        "Rango de 0-50. Donde 0 es la mejor calidad y 50 la peor.\n"
    )
    crf = int(input('CRF: '))
    if crf <= 50:
        crf = f'-crf {crf}'
    else:
        crf = '-crf 23'
        print(f"Fuera de rango (de 0 a 50)\n"
            f"El CRF sera {crf}.\n"
        )
        Continuar()
    LimpiarPantalla()
    return crf

def Preset():
    print("//    Uso de CPU    //\n"
        "PRESETS:\n"
        "#Rango del 1 al 9. Donde 1 es la opcion que usa menos cpu y 9 la que\n"
        "#usa mas cpu.\n"
        "1.ultrafast\n"
        "2.superfast\n"
        "3.veryfast\n"
        "4.faster\n"
        "5.fast\n"
        "6.medium\n"
        "7.slow\n"
        "8.slower\n"
        "9.veryslow\n"
    )
    pst_opc = int(input('Preset: '))

    if pst_opc == 1:
        pst = '-preset ultrafast'
    elif pst_opc == 2:
        pst = '-preset superfast'
    elif pst_opc == 3:
        pst = '-preset veryfast'
    elif pst_opc == 4:
        pst = '-preset faster'
    elif pst_opc == 5:
        pst = '-preset fast'
    elif pst_opc == 6:
        pst = '-preset medium'
    elif pst_opc == 7:
        pst = '-preset slow'
    elif pst_opc == 8:
        pst = '-preset slower'
    elif pst_opc == 9:
        pst = '-preset veryslow'
    else:
        pst = '-preset medium'
        print(f"Esa opcion no existe.\nEl preset sera {pst}.\n")
        Continuar()
    LimpiarPantalla()
    return pst

def Ruta():
    rta = [""]*2

    LimpiarPantalla()
    opc = input("¿Elegir ruta? s/n: ")
    if opc == "s":
        rta[1] = input("/$HOME/")
    else:
        rta[1] = ""

    rta[0] = f"/$HOME/{rta[1]}"
    LimpiarPantalla()
    return rta[0]

def Nombre(txt = 'Archivo'):
    print(f'//    Nombre de {txt}    //')
    nmb = input('Nombre: ')
    LimpiarPantalla()
    return nmb

def GrabarPantalla():
    opc = input('¿Configuración Avanzada? s/n: ')
    LimpiarPantalla()
    if opc == 's':        
        opc = input(f"{Titulo(txt = 'Modo Avanzado')}\n"
                  '¿Grabar con audio? s/n: ')
        LimpiarPantalla()
        if opc == 's':
            adi = int(input(f"{Titulo(txt = 'Modo Avanzado')}\n"
                          '¿Cuantos audios quieres grabar?: '))
            LimpiarPantalla()
            print(Titulo(txt = 'Modo Avanzado'))
            if adi >= 2:
                cfg = (f"ffmpeg -f x11grab -i :0 {AudioFiltro(adi)}"
                    f"{Calidad()} {Preset()} {Resolucion(txt = 'Salida')} "
                    f"{Fotogramas()} -filter_complex amix=inputs={adi} "
                    f"{Ruta()}'{Nombre(txt ='Video')}.mkv'")
            elif adi == 1:
                cfg = (f"ffmpeg -f x11grab -i :0 {Audio()} "
                    f"{Calidad()} {Preset()} "
                    f"{Resolucion(txt = 'Salida')} {Fotogramas()} "
                    f"{Ruta()}'{Nombre(txt ='Video')}.mkv'")
            else:
                AudioFiltro(adi)
        else:
            cfg = (f"ffmpeg -f x11grab -i :0 {Calidad()} {Preset()} "
                f"{Resolucion(txt = 'Salida')} {Fotogramas()} "
                f"{Ruta()}'{Nombre(txt ='Video')}.mkv'")
    else:
        opc = input(f"{Titulo(txt = 'Modo Basico')}\n"
                  '¿Grabar con audio? s/n: ')
        LimpiarPantalla()
        if opc == 's':
            adi = int(input(f"{Titulo(txt = 'Modo Basico')}\n"
                          '¿Cuantos audios quieres grabar?: '))
            LimpiarPantalla()
            print(Titulo(txt = 'Modo Basico'))
            if adi >= 2:
                cfg = (f"ffmpeg -f x11grab -i :0 {AudioFiltro(adi)}"
                    f"-r 24 -s 1280x720 -filter_complex amix=inputs={adi} "
                    f"{Ruta()}'{Nombre(txt = 'Video')}.mkv'")
            elif adi == 1:
                cfg = (f"ffmpeg -f x11grab -i :0 {Audio()} "
                    f"-r 24 -s 1280x720 "
                    f"{Ruta()}'{Nombre(txt = 'Video')}.mkv'")
            else:
                AudioFiltro(adi)
        else:
            cfg = (f"ffmpeg -f x11grab -i :0 -r 24 -s 1280x720 "
                f"{Ruta()}'{Nombre(txt = 'Video')}.mkv'")

    print('//    Esta es su configuracion    //\n'
        f'{cfg} \n')

    Continuar(txt = '¿Grabar Video?')
    return(cfg)

def GrabarAudio():
    adi = int(input('¿Cuantos audios quieres grabar?: '))
    LimpiarPantalla()
    if adi >= 2:
        cfg = (f"ffmpeg {AudioFiltro(adi)}-filter_complex amix=inputs={adi} "
            f"{Ruta()}'{Nombre(txt = 'Audio')}.ogg'")
    elif adi == 1:
        cfg = (f"ffmpeg {Audio()} "
            f"{Ruta()}'{Nombre(txt = 'Audio')}.ogg'")
    else:
        AudioFiltro(adi)

    print(f"{Titulo(txt = 'Esta es su configuración')}\n"
        f'{cfg}\n')
    Continuar(txt = '¿Grabar Audio?')
    return cfg

def Continuar(txt = '¿Continuar?'):
    print('')
    opc = input(f'{txt} s/n: ')

    if opc == 's':
       LimpiarPantalla()
    elif opc == 'n':
       main()
    else:
       input("Esa opcion no existe")
       main()


def LimpiarPantalla():
    os.system('clear')

def Titulo(txt = 'Texto'):
    txt_Titulo = f'//    {txt}    //'
    return txt_Titulo

def Opciones():
    LimpiarPantalla()    
    print(f"{Titulo(txt = 'Opciones')}\n"
        "1. Grabar Pantalla\n"
        "2. Grabar Audio\n"
        "0. Salir\n")

def main():
    Opciones()

    opc=[0]*3
    opc[0] = True
    opc[2] = "\nESA OPCION NO EXISTE"

    achv_txt = 'GrabadorFFmpeg_cfg.txt'
    while opc[0] == True:
        Opciones()
        opc[1] = (input('Elija una opcion: '))
        if opc[1] == "1":
            LimpiarPantalla()
            cfg = GrabarPantalla()
            grd = True
        elif opc[1] == "2":
            Continuar()
            cfg = GrabarAudio()
            grd = True
        elif opc[1] == "0":
            opc[0] = False
            grd = False
            Continuar()
            print('Hasta la proxima...')
            exit()
        else:
            input(opc[2])
            grd = False

        if grd == True:
            with open(achv_txt, 'a') as archivo:
                archivo.write(cfg + '\n')
            os.system(cfg)
        else:
            pass #No se hace nada

                
if __name__ =='__main__':
   main()
#salir = os.system('^C')
'''
-c:v libx264
-c:v libx264rgb
-c:v h264_vaapi
-c:v h264_nvenc
-c:v h264
-c:v mpeg4
-c:v ffv1
-c:v rawvideo
-c:v libvpx
-c:v mpeg2video
-c:v jpeg2000
-c:v librav1e
-c:v gif
-c:v copy
'''

'''
        if opc[1] == "1":
            cfg_SN = input("\n¿Configuracion Avanzada? s/n: ")
            if cfg_SN == 's':
                LimpiarPantalla()
                GrabarPantalla()
            elif cfg_SN == 'n':
                LimpiarPantalla()
                txt = f"ffmpeg -f x11grab -i :0 -r 24 -s 1280x720 {Ruta()}'{Nombre(txt = 'Video')}.mkv'"
                print(f"//  Esta es su configuracion  //\n{txt}")
                Continuar(txt = '¿Grabar Video? s/n')
                os.system(txt)
            else:
                input(opc[2])
'''

'''
def GrabarPantalla():
    opc = input('¿Configuración Avanzada? s/n: ')
    LimpiarPantalla()
    if opc == 's':
        opc = input('¿Grabar con audio? s/n: ')
        LimpiarPantalla()
        if opc == 's':
            cfg = (f"ffmpeg -f x11grab -i :0 -f pulse -i {Audio()} "
                f"{Calidad()} {Preset()} {Resolucion(txt = 'Salida')} "
                f"{Fotogramas()} {Ruta()}'{Nombre(txt ='Video')}.mkv'")
        else:
            cfg = (f"ffmpeg -f x11grab -i :0 {Calidad()} {Preset()} "
                f"{Resolucion(txt = 'Salida')} {Fotogramas()} "
                f"{Ruta()}'{Nombre(txt ='Video')}.mkv'")
    else:
        opc = input('¿Grabar con audio? s/n: ')
        if opc == 's':
            cfg = (f"ffmpeg -f x11grab -i :0 -f pulse -i {Audio()} "
                f"-r 24 -s 1280x720 {Ruta()} "
                f"'{Nombre(txt = 'Video')}.mkv'")
        else:
            cfg = (f"ffmpeg -f x11grab -i :0 -r 24 -s 1280x720 {Ruta()} "
                f"'{Nombre(txt = 'Video')}.mkv'")

    print('//    Esta es su configuracion    //\n'
        f'{cfg} \n')

    Continuar(txt = '¿Grabar Video? s/n')
    os.system(cfg)
'''

'''
-async 1 -filter_complex amix=inputs=2
'''
