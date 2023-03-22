import Modulo_Util as Util

sys = Util.System()


def Resolution(rez_H=854, rez_V=480):
    try:
        rez_H = int(rez_H)
        rez_V = int(rez_V)
    except:
        rez_H = 854
        rez_V = 480
        print('\nDebido a los datos erroneos\n'
              f'La resolución sera {rez_H}x{rez_V}\n')
              
    if rez_H <= 0 or rez_V <= 0:
        rez_H, rez_V = 1, 1
    else: pass

    cfg = f'-s {rez_H}x{rez_V}'
    
    return cfg
    

def FPS(fps=25):
    try:
        fps = int(fps)
    except:
        fps = 25
        print(f'\nDebido a los datos erroneos, los fps seran {fps}\n')
        
    if fps <= 0:
        fps = 1
    else: pass
    
    cfg = f'-r {fps}'
    
    return cfg
    

def CRF(crf=30):
    try:
        crf = int(crf)
    except:
        crf = 30
        print(f'\nDatos erroneos, por lo tanto el crf sera {crf}\n')

    if crf >= 0 and crf <= 50: pass  
    else:
        crf = 30
        
    cfg = f'-crf {crf}'

    return cfg


def Audio(audio=0):
    if sys == 'linux':
        try:
            audio = int(audio)
        except:
            audio = 0
        
        #os.system('pactl list short sources') 
        audio = f'-f pulse -i {audio}'

    elif sys == 'win':
        #os.system('ffmpeg -list_devices true -f dshow -i dummy')
        audio = f'-f dshow -i audio={audio}'
    
    return audio


def Audio_Filter(flt=0):
    adi = [''] * flt
    nmr = flt
    #txt = ''
    audio_filter = ''
    if flt > 0:
        while flt > 0:
            adi[flt - 1] = Audio(audio=input(f'{flt} ¿Cual es el audio?: '))
            flt = flt - 1
    else:
        audio_filter = ''
        
    while nmr > 0:
        #txt = adi[nmr - 1] + ' ' + txt
        audio_filter = adi[nmr - 1] + ' ' + audio_filter
        nmr = nmr - 1
        
    return audio_filter
    
    
def Desktop_Render(sys=sys):
    if sys == 'linux':
        desk_rend = '-f x11grab -i :0'
    elif sys == 'win':
        desk_rend = '-f gdigrab -i desktop'
    else:
        desk_rend = 'Desktop render for else'
        
    return desk_rend
    

def Command(opc='Help'):
    if opc == 'Help':
        cfg = 'ffmpeg -help'
        
    elif opc == 'Audio':
        if sys == 'linux':
            cfg = 'pactl list short sources'

        elif sys == 'win':
            cfg = 'ffmpeg -list_devices true -f dshow -i dummy'
            
    else:
        cfg = ''
    
    return cfg
    

def Preset(preset='medium'):
    if (
        preset == 'ultrafast' or
        preset == 'superfast' or
        preset == 'veryfast' or
        preset == 'faster' or
        preset == 'fast' or
        preset == 'medium' or
        preset == 'slow' or
        preset == 'slower' or
        preset == 'veryslow'
    ):
        preset = f'-preset {preset}'

    else:
        preset = '-preset medium'
        print(f'Debido a los datos erroneos el presen sera "{preset}"')
        
    return preset
    
def Message(opc='crf'):
    if opc == 'crf':
        msg = (
            'Escala del 0 a 50\n'
            'Donde 0 es la mejor calidad y 50 es la peor calidad'
        )

    elif opc == 'resolution':
        msg = (
            'Ejemplos de resolución\n'
            'Horizontal x Vertical\n'
            '   1920x1080\n'
            '   1280x720\n'
            '   960x540\n'
            '   854x480'
        )
        
    elif opc == 'fps':
        msg = (
            'Entre mas Fotogramas, mas pesado es el Video\n'
            '\n'
            'Ejemplos estandar, de Fotogramas por segundo\n'
            '   FPS = 60\n'
            '   FPS = 30\n'
            '   FPS = 25\n'
            '   FPS = 15\n'
            '   FPS = 10'
        )
        
    elif opc == 'preset':
        msg = (
            "El preset, es el uso de CPU para grabar."
        )
        
    elif (
        opc == 'audio' or
        opc == 'Audio'
    ):
        msg = (
            'Estos son los dispositivos de audio, elige uno.'
        )
        
    else:
        msg = 'Mensaje FFmpeg para else.'
        
    return msg