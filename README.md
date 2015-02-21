onset_detection
===============
onset_detection and an application of CQT to figure out the amplitude spectrum.
The result of CQT contains the ampiltude on 82 musical notes from #C0 to #A7.

tool
---------------
This folder inherits from soloAnalysis.tool and contains cqt.py.

wav_in.py
---------------
use module wave.py and support .wav file with different framerates, but the sampling resulotion has to be 2 bytes.

freq_analysis.py
----------------
The result of CQT contains the ampiltudes of 82 musical notes from C4 to #A7 at each onset point.

fCQT.py
----------------
function fCQT takes the name of file as an input and returns the time and features of each onset points.
function onset_svm takeing the signal, the framerate, length and compression ration as inputs(the latter two are optional),returns the time and pitch of each onset points.

makedata.py
----------------
It is used to make trainingdata for svm.

onset+svm.py
----------------
simple application of fCQT. You can run it to analyze your .wav file just remembering change its directory.(See comments)


