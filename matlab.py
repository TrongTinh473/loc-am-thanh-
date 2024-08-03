function varargout = GUI3(varargin)
gui_Singleton = 1;
gui_State = struct('gui_Name', mfilename, ...
 'gui_Singleton', gui_Singleton, ...
'gui_OpeningFcn', @GUI3_OpeningFcn,
...
 'gui_OutputFcn', @GUI3_OutputFcn,
...
 'gui_LayoutFcn', [] , ...
'gui_Callback', []);
if nargin && ischar(varargin{1})
 gui_State.gui_Callback = str2func(varargin{1});
end
if nargout
 [varargout{1:nargout}] = gui_mainfcn(gui_State,
varargin{:});
else
 gui_mainfcn(gui_State, varargin{:});
end
function GUI3_OpeningFcn(hObject, eventdata, handles,
varargin)
handles.output = hObject;
guidata(hObject, handles);
function varargout = GUI3_OutputFcn(hObject, eventdata,
handles)
varargout{1} = handles.output;
function Browser_Callback(hObject, eventdata, handles)
[filename pathname] = uigetfile({'*.wav'},'File
Selector');
handles.fullpathname = strcat(pathname, filename);
set(handles.text3, 'String',handles.fullpathname)
%showing fullpathname
guidata(hObject,handles)
function play_equalizer(hObject, handles)
global player;
[handles.y, handles.Fs] =
audioread(handles.fullpathname);
handles.g1 = get(handles.slider1,'value');
handles.g2 = get(handles.slider2,'value');
handles.g3 = get(handles.slider3,'value');
handles.g4 = get(handles.slider4,'value');
% Plotting initial wave and frequency
n_y = length(handles.y);
y_fft0 = fft(handles.y, n_y);
y_f = y_fft0(1:n_y/2);
x_fft = handles.Fs * (0:n_y/2-1) / n_y;
% Plotting initial wave
subplot(2,2,1);
plot((0:n_y-1)/handles.Fs, handles.y);
xlabel('Time (s)');
ylabel('Amplitude');
title('Initial Waveform');
% Plotting initial frequency
subplot(2,2,2);
plot(x_fft, abs(y_f));
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Initial Frequency Domain');
% Lowpass filter
h_hamming = lowpass_haming();
y_low = filter(h_hamming, handles.y);
n_y_low = length(y_low);
y1_afft0 = fft(y_low, n_y_low);
y1_af = y1_afft0(1:n_y_low/2);
y1 = handles.g1 * y1_af;
x1_afft = handles.Fs * (0:n_y_low/2-1) / n_y_low;
% Highpass filter
high_hamming = highpass_haming();
y_high = filter(high_hamming, handles.y);
n_y_high = length(y_high);
y2_afft0 = fft(y_high, n_y_high);
y2_af = y2_afft0(1:n_y_high/2);
y2 = handles.g2 * y2_af;
x2_afft = handles.Fs * (0:n_y_high/2-1) / n_y_high;
% Bandpass filter
band_hamming = bandpass_haming();
y_band = filter(band_hamming, handles.y);
n_y_band = length(y_band);
y3_afft0 = fft(y_band, n_y_band);
y3_af = y3_afft0(1:n_y_band/2);
y3 = handles.g3 * y3_af;
x3_afft = handles.Fs * (0:n_y_band/2-1) / n_y_band;
% Bandstop filter
stop_hamming = stoppass_haming();
y_stop = filter(stop_hamming, handles.y);
n_y_stop = length(y_stop);
y4_afft0 = fft(y_stop, n_y_stop);
y4_af = y4_afft0(1:n_y_stop/2);
y4 =handles.g4 * y4_af;
x4_afft = handles.Fs * (0:n_y_stop/2-1) / n_y_stop;
handles.yT = y1 + y2 + y3 + y4;
% Inverse FFT
inverse_fft = ifft(handles.yT);
n_freq = length(handles.yT); % Number of frequency bins
freq_range = handles.Fs * (0:n_freq/2-1) / n_freq; %
Frequency range for plotting
% Plotting filtered frequency and time domain
subplot(2,2,3);
plot((0:length(inverse_fft)-1)/handles.Fs, inverse_fft);
xlabel('Time (s)');
ylabel('Amplitude');
title('Filtered Waveform');
subplot(2,2,4);
plot(freq_range, abs(handles.yT(1:n_freq/2)));
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Filtered Frequency Domain');
% Update handles structure
guidata(hObject, handles);
% Assuming Volume is a scalar or an array
player = audioplayer(inverse_fft, handles.Fs);
function Play_Callback(hObject, eventdata, handles)
global player;
play_equalizer(hObject, handles);
play(player);
guidata(hObject,handles)
function Pause_Callback(hObject, eventdata, handles)

global player;
play_equalizer(hObject, handles);
pause(player);
guidata(hObject,handles)
function Resume_Callback(hObject, eventdata, handles)
global player;
play_equalizer(hObject, handles);
resume(player);
guidata(hObject,handles)
function Stop_Callback(hObject, eventdata, handles)
global player;
play_equalizer(hObject, handles);
stop(player);
guidata(hObject,handles)
function slider1_Callback(hObject, eventdata, handles)
data=get(handles.slider1,'Value')
data1=num2str(data);
set(handles.edit1,'String',data);
function slider1_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'),
get(0,'defaultUicontrolBackgroundColor'))
 set(hObject,'BackgroundColor',[.9 .9 .9]);
end
function slider2_Callback(hObject, eventdata, handles)
data=get(handles.slider2,'Value')
data2=num2str(data);
set(handles.edit2,'String',data);
function slider2_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'),
get(0,'defaultUicontrolBackgroundColor'))
 set(hObject,'BackgroundColor',[.9 .9 .9]);
end
function slider3_Callback(hObject, eventdata, handles)
data=get(handles.slider3,'Value')
data3=num2str(data);
set(handles.edit3,'String',data);

function slider3_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'),
get(0,'defaultUicontrolBackgroundColor'))
 set(hObject,'BackgroundColor',[.9 .9 .9]);
end
function slider4_Callback(hObject, eventdata, handles)
data=get(handles.slider4,'Value')
data4=num2str(data);
set(handles.edit4,'String',data);
function slider4_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'),
get(0,'defaultUicontrolBackgroundColor'))
 set(hObject,'BackgroundColor',[.9 .9 .9]);
end
function edit1_Callback(hObject, eventdata, handles)
data = str2double(get(hObject, 'String'));
set(handles.slider1, 'Value', data);
guidata(hObject, handles);
function edit1_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'),
get(0,'defaultUicontrolBackgroundColor'))
 set(hObject,'BackgroundColor','white');
end
function edit2_Callback(hObject, eventdata, handles)
data = str2double(get(hObject, 'String'));
set(handles.slider2, 'Value', data);
guidata(hObject, handles);
function edit2_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'),
get(0,'defaultUicontrolBackgroundColor'))
 set(hObject,'BackgroundColor','white');
end
function edit3_Callback(hObject, eventdata, handles)
data = str2double(get(hObject, 'String'));
set(handles.slider3, 'Value', data);
guidata(hObject, handles);
function edit3_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'),
get(0,'defaultUicontrolBackgroundColor'))
 set(hObject,'BackgroundColor','white');
end
function edit4_Callback(hObject, eventdata, handles)
data = str2double(get(hObject, 'String'));
set(handles.slider4, 'Value', data);
guidata(hObject, handles);
function edit4_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'),
get(0,'defaultUicontrolBackgroundColor'))
 set(hObject,'BackgroundColor','white');
end
function pushbutton7_Callback(hObject, eventdata,
handles)
subplot(2,2,4)
xlim([0 250]);
function pushbutton8_Callback(hObject, eventdata,
handles)
subplot(2,2,4)
xlim([1000 1500]);
function pushbutton9_Callback(hObject, eventdata,
handles)
subplot(2,2,4)
xlim([40 62]);
function pushbutton10_Callback(hObject, eventdata,
handles)
subplot(2,2,4)
xlim([300 1000]);
 