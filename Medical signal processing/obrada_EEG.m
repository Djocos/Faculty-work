function varargout = obrada_EEG(varargin)
% OBRADA_EEG MATLAB code for obrada_EEG.fig
%      OBRADA_EEG, by itself, creates a new OBRADA_EEG or raises the existing
%      singleton*.
%
%      H = OBRADA_EEG returns the handle to a new OBRADA_EEG or the handle to
%      the existing singleton*.
%
%      OBRADA_EEG('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in OBRADA_EEG.M with the given input arguments.
%
%      OBRADA_EEG('Property','Value',...) creates a new OBRADA_EEG or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before obrada_EEG_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to obrada_EEG_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help obrada_EEG

% Last Modified by GUIDE v2.5 04-Jun-2022 22:36:48

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @obrada_EEG_OpeningFcn, ...
                   'gui_OutputFcn',  @obrada_EEG_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before obrada_EEG is made visible.
function obrada_EEG_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to obrada_EEG (see VARARGIN)

% Choose default command line output for obrada_EEG
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes obrada_EEG wait for user response (see UIRESUME)
% uiwait(handles.figure1);
global EEG 
global EMG
global t Fs
EMG = load('EMG_signal3.mat');
t_end = numel(EMG.data.EMG)*1/EMG.data.Fs;
t = 0:1/EMG.data.Fs:t_end;
t = t(1:numel(t)-1);
axes(handles.axes2)
plot(t, EMG.data.EMG)


EEG = load('EEG.mat');
t_end = numel(EEG.data.EEG)*1/EEG.data.Fs;
t = 0:1/EEG.data.Fs:t_end;
t = t(1:numel(t)-1);
axes(handles.axes1)
plot(t, EEG.data.EEG)
Fs = EEG.data.Fs;


% --- Outputs from this function are returned to the command line.
function varargout = obrada_EEG_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function sirina_entry_Callback(hObject, eventdata, handles)
% hObject    handle to sirina_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of sirina_entry as text
%        str2double(get(hObject,'String')) returns contents of sirina_entry as a double


% --- Executes during object creation, after setting all properties.
function sirina_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sirina_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function preklapanje_entry_Callback(hObject, eventdata, handles)
% hObject    handle to preklapanje_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of preklapanje_entry as text
%        str2double(get(hObject,'String')) returns contents of preklapanje_entry as a double


% --- Executes during object creation, after setting all properties.
function preklapanje_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to preklapanje_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in spectrogram_button.
function spectrogram_button_Callback(hObject, eventdata, handles)
% hObject    handle to spectrogram_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global EEG Fs s f t ts
preklop = eval(get(handles.preklapanje_entry, 'String'));
sirina = eval(get(handles.sirina_entry, 'String'));

% Slede?a linija koda je ura?ena jer mislim da korisnik ne bi trebalo da 
% bira broj ta?aka za fft a ovo radi dobar posao

Nfft = 1000;
[s, f, ts] = spectrogram(EEG.data.EEG, sirina, preklop, Nfft, Fs);
axes(handles.axes3)
imagesc(ts, f, abs(s))
f_max = 30;
ylim([0 f_max])
colorbar

[result] = wavelet_spektrogram(EEG.data.EEG, Fs, 0, f_max);

[F, T] = size(result);
t_skala = linspace(t(1), t(end), T);
f_skala = linspace(0, f_max, F);

axes(handles.axes4)
imagesc(t_skala, f_skala, abs(result))



% --- Executes on button press in oznaci_button.
function oznaci_button_Callback(hObject, eventdata, handles)
% hObject    handle to oznaci_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global s f t ts

kljucna_vrsta = abs(s(11, :));
ERD = kljucna_vrsta/10000<0.5;

for i = 2:length(ERD)-1
    if ERD(i) == 1 && ERD(i+1) == 0 && ERD(i-1) == 0
        ERD(i) = 0;
    end
end

axes(handles.axes3)

for i = 2:length(ERD)
    if ERD(i) == 1 && ERD(i-1) == 0
        axes(handles.axes3)
        text(ts(i), 12, 'ERD', 'Color', 'r', 'FontWeight', 'bold')
        axes(handles.axes4)
        text(ts(i), 12, 'ERD', 'Color', 'r', 'FontWeight', 'bold')
    end
end
        

    
