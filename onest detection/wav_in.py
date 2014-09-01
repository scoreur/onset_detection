# -*- coding: cp936 -*-
import wave
import numpy
import pylab as pl

#ֻ֧��16bit��wav��ʽ�ļ�

def wav_in(url):
    #��wav�ļ�
    #open����һ������һ��Wave_read���ʵ����ͨ���������ķ�����ȡWAV�ļ��ĸ�ʽ������
    
    f = wave.open(url,"rb") 
    
    #��ȡ��ʽ��Ϣ
    #һ���Է������е�WAV�ļ��ĸ�ʽ��Ϣ�������ص���һ����Ԫ(tuple)��������, ����λ����byte��λ��, ��
    #��Ƶ��, ��������, ѹ������, ѹ�����͵�������waveģ��ֻ֧�ַ�ѹ�������ݣ���˿��Ժ������������Ϣ  
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]

    #��ȡ��������
    #��ȡ�������ݣ�����һ������ָ����Ҫ��ȡ�ĳ��ȣ���ȡ����Ϊ��λ��
    str_data = f.readframes(nframes)
    f.close()
    
    #����������ת��������
    #��Ҫ������������������λ������ȡ�Ķ���������ת��Ϊһ�����Լ��������
    if sampwidth == 2:
        wave_data = numpy.fromstring(str_data,dtype = numpy.short)
    else:
        wave_data = numpy.fromstring(str_data,dtype = numpy.int8)


    wave_data.shape = -1,nchannels
    wave_data = wave_data.T
    time = numpy.arange(0,nframes)*(1.0/framerate)

    """print str_data[:1000]
    print wave_data[0][:1000]
    print max(wave_data[0])"""
    #len_time = len(time)/2
    #time = time[0:len_time]
    
    #print "time length = ",len(time)
    #print "wave_data[0] length = ",len(wave_data[0])
    
    return [wave_data[0],params]
    
    """pl.subplot(211)  
    pl.plot(time,wave_data[0])  
    pl.subplot(212)  
    pl.plot(time, wave_data[1],c="r")  
    pl.xlabel("time")  
    pl.show()  """
