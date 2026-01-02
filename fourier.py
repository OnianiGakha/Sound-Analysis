
import matplotlib.pyplot as pyp
import numpy
import sys
from pydub import AudioSegment


try: 
    audio = AudioSegment.from_file(sys.argv[1])
    audio = audio.set_channels(1)

except FileExistsError:
    print("Couldnt find audio. Correct Usage: fourier.py [Audio Path]")
    sys.exit(1)
except FileNotFoundError:
    print("Couldnt find audio. Correct Usage: fourier.py [Audio Path]")
    sys.exit(1)
print("Processing... This may take a while!")

note_names=['A','A#',"B",'C','C#','D','D#','E','F','F#','G','G#']

notedominance={'A': 0,'A#': 0,"B": 0,'C': 0,'C#': 0,'D': 0,'D#': 0,'E': 0,'F': 0,'F#': 0,'G': 0,'G#': 0}
freqs=[]
f0=27.5
for i in range(0,90):
    freqs.append(f0*pow(2,i/12))
    
def freqtonote(freq):
    shift=int(round(12*numpy.log2(freq/440.0)))
    note = note_names[shift%12]
    #octave = 4+int(round((shift+9)/12))
    return note

def fourier(fx):
    Fs = audio.frame_rate#/sample

    output=numpy.zeros(len(freqs), dtype=complex)
    
    for i, f in enumerate(freqs):
    
        area=0
        for t in range(0,N):
            area += fx[t] * numpy.exp(-2j*f*t*numpy.pi/Fs)
            
        notedominance[freqtonote(f)] += int(abs(area))
        output[i]=area
        
    return output
    
data=numpy.array(audio.get_array_of_samples())
sample_rate=audio.frame_rate
N=len(data)
acc=N
xt=data

fourierlist=fourier(xt)

pyp.figure()

pyp.subplot(2,2,1)
pyp.plot(xt)
pyp.title("Sound plot")
pyp.xlabel("Sample Index")
pyp.ylabel("Value")

pyp.subplot(2,2,2)
pyp.plot(numpy.real(fourierlist))
            
sortedict= sorted(notedominance.items(), key=lambda t: t[1])
sortedict.reverse()

place=1
for note in sortedict:
    print(f"{place}. {note[0]}, Presence: {note[1]}")
    place+=1
pyp.title("Fourier Transform (Real)")
pyp.xlabel("Sample Index")
pyp.ylabel("X(t) Value")

pyp.subplot(2,2 ,3)

pyp.bar(notedominance.keys(),notedominance.values(),color="blue")
pyp.xticks([0,1,2,3,4,5,6,7,8,9,10,11],notedominance.keys())

pyp.title("Notes presence")
pyp.xlabel("Note Name")
pyp.ylabel("Presence")

pyp.subplot(2,2,4)
pyp.plot(numpy.imag(fourierlist))
pyp.title("Fourier Transform (Imaginary)")
pyp.xlabel("Sample Index")
pyp.ylabel("X(t) Value")

manager = pyp.get_current_fig_manager()
manager.full_screen_toggle()

pyp.show()
