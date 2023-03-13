import Modulo_Util as Util

sys = Util.System()


def Resolution(rez_H=854, rez_V=480):
    try:
        rez_H = int(rez_H)
        rez_V = int(rez_V)
    except:
        rez_H = 854
        rez_V = 480
        print('Tienes que escribir numereos enteros\n'
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
        print(f'Debido a los datos errones, los fps seran {fps}')
        
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
        print('Datos erroneos, por lo tanto el crf sera {crf}')

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


def Audio_Filter(flt=0, audio=0):
    adi = [''] * flt
    nmr = flt
    #txt = ''
    audio_filter = ''
    if flt > 0:
        while flt > 0:
            adi[flt - 1] = Audio(audio=audio)
            flt = flt - 1
    else:
        audio_Filter = ''
        
    while nmr > 0:
        #txt = adi[nmr - 1] + ' ' + txt
        audio_filter = adi[nmr - 1] + ' ' + audio_filter
        nmr = nmr - 1
        
    return audio_filter
    
def Help():
    os.system('ffmpeg -help')
    
def Desktop_Render(sys=sys):
    if sys == 'linux':
        desk_rend = '-f x11grab -i :0'
    elif sys == 'win':
        desk_rend = '-f gdigrab -i desktop'
    else:
        desk_rend = 'Desktop render for else'
        
    return desk_rend