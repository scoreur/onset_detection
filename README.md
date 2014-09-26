onset_detection
===============
onset_detection and an application of CQT to figure out the amplitude spectrum.
The result of CQT contains the ampiltude on 82 musical notes from #C0 to #A7.

fCQT
---------------
Include the function onset_svm implementing the whole process of CQT and SVM.

tool
---------------
This folder inherits from soloAnalysis.tool and contains cqt.py.

wav_in.py
---------------
use module wave.py and support .wav file with different framerates, but the sampling resulotion has to be 2 bytes.

freq_analysis.py
----------------
The result of CQT contains the ampiltudes of 82 musical notes from C4 to #A7 at each onset point.

