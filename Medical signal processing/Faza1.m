function varargout = Faza1(varargin)
% FAZA1 MATLAB code for Faza1.fig
%      FAZA1, by itself, creates a new FAZA1 or raises the existing
%      singleton*.
%
%      H = FAZA1 returns the handle to a new FAZA1 or the handle to
%      the existing singleton*.
%
%      FAZA1('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in FAZA1.M with the given input arguments.
%
%      FAZA1('Property','Value',...) creates a new FAZA1 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Faza1_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Faza1_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Faza1

% Last Modified by GUIDE v2.5 03-Jun-2022 13:18:09

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Faza1_OpeningFcn, ...
                   'gui_OutputFcn',  @Faza1_OutputFcn, ...
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


% --- Executes just before Faza1 is made visible.
function Faza1_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Faza1 (see VARARGIN)

% Choose default command line output for Faza1
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Faza1 wait for user response (see UIRESUME)
% uiwait(handles.figure1);
handles.r1.Value = 0;
axes(handles.axes3)
xlabel('Frekvencija [Hz]')
axes(handles.axes4)
xlabel('Frekvencija [Hz]')
axes(handles.axes5)
xlabel('Frekvencija [Hz]')


% --- Outputs from this function are returned to the command line.
function varargout = Faza1_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function save_name_Callback(hObject, eventdata, handles)
% hObject    handle to save_name (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of save_name as text
%        str2double(get(hObject,'String')) returns contents of save_name as a double


% --- Executes during object creation, after setting all properties.
function save_name_CreateFcn(hObject, eventdata, handles)
% hObject    handle to save_name (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in save_button.
function save_button_Callback(hObject, eventdata, handles)

extension = ".mat";
name = get(handles.save_name, 'String');
title = strcat(name, extension);
data.Fs = handles.data.Fs;
data.signal = handles.data.s1;
save(title, 'data')

% hObject    handle to save_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in zoom_button.
function zoom_button_Callback(hObject, eventdata, handles)
% hObject    handle to zoom_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if get(handles.zoom, 'Value') == 1
    axes(handles.axes1)
    [x, y] = ginput(2);
    x_kvadrat = [x(1) x(2) x(2) x(1) x(1)];
    y_kvadrat = [y(1) y(1) y(2) y(2) y(1)];

    hold on
    axes(handles.axes1)
    plot(x_kvadrat, y_kvadrat)
    
    hold off
    donja_x = x(1);
    gornja_x = x(2);

    donja_y = y(2);
    gornja_y = y(1);
    data = handles.data;
    indexi = data.t > donja_x & data.t < gornja_x;
    data.t1 = data.t(indexi);
    data.s1 = data.s(indexi);
    handles.data.t1 = data.t1;
    handles.data.s1 = data.s1;
    guidata(hObject, handles)
    axes(handles.axes2)
    plot(handles.data.t1, handles.data.s1)
    
elseif get(handles.zoom, 'Value') == 2
    [x, y] = ginput(2);
    r = sqrt(abs(x(2) - x(1))^2 + abs(y(2) - y(1))^2);
    
    % Crtanje kruga
    
    angles = linspace(0, 2 * pi, numel(handles.data.t));
    krug_x = r * cos(angles) + x(1);
    krug_y = r * sin(angles) + y(1);
    hold on
    plot(krug_x, krug_y, 'r-')
    hold off
    axis equal
    
    % Ogranicavanje
    indexi = handles.data.t >= x(1)-r & handles.data.t <= x(1)+r;
    handles.data.t1 = handles.data.t(indexi);
    handles.data.s1 = handles.data.s(indexi);
    
    for i = 1:numel(handles.data.t1)
        
        if sqrt(abs(x(1) - handles.data.t1(i))^2 + abs(y(1) - handles.data.s1(i))^2) > r
            
            handles.data.s1(i) = nan;
            
        end
    end
    
    guidata(hObject, handles)
    axes(handles.axes2)
    plot(handles.data.t1, handles.data.s1)
    xlim([x(1)-r x(1)+r])
    ylim([y(1)-r y(1)+r])
    axis equal
    
end


% --- Executes on selection change in zoom.
function zoom_Callback(hObject, eventdata, handles)
% hObject    handle to zoom (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns zoom contents as cell array
%        contents{get(hObject,'Value')} returns selected item from zoom


% --- Executes during object creation, after setting all properties.
function zoom_CreateFcn(hObject, eventdata, handles)
% hObject    handle to zoom (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in r1.
function r1_Callback(hObject, eventdata, handles)
% hObject    handle to r1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of r1


% --- Executes on button press in r2.
function r2_Callback(hObject, eventdata, handles)
% hObject    handle to r2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of r2


% --- Executes on button press in r3.
function r3_Callback(hObject, eventdata, handles)
% hObject    handle to r3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of r3


% --- Executes when selected object is changed in radios.
function radios_SelectionChangedFcn(hObject, eventdata, handles)

global signal

if get(handles.r1, 'Value') == 1
    load('EMG_signal1.mat')
    t_end = numel(data.signal)*1/data.Fs;
    t = 0:1/data.Fs:t_end;
    t = t(1:numel(t)-1);
    axes(handles.axes1)
    plot(t, data.signal)
    
    signal.fs = data.Fs;
    signal.signal = data.signal;
    
elseif get(handles.r2, 'Value') == 1
    load('EMG_signal2.mat')
    t_end = numel(data.signal)*1/data.Fs;
    t = 0:1/data.Fs:t_end;
    t = t(1:numel(t)-1);
    axes(handles.axes1)
    plot(t, data.signal)
    
    signal.fs = data.Fs;
    signal.signal = data.signal;
    
elseif get(handles.r3, 'Value') == 1
    load('EMG_signal3.mat');
    signal.combined.EMG = data.EMG;
    t_end = numel(data.EMG)*1/data.Fs;
    t = 0:1/data.Fs:t_end;
    t = t(1:numel(t)-1);
    axes(handles.axes1)
    plot(t, data.EMG)
    hold on
    load('EEG.mat');
    plot(t, data.EEG)
    hold off
    
    
    signal.combined.fs = data.Fs;
    signal.combined.EMG = data.EEG;
end
handles.data.t = t;
handles.data.s = signal.signal;
handles.data.Fs = data.Fs;
guidata(hObject, handles)
    
% hObject    handle to the selected object in radios 
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on selection change in odabir_filtra.
function odabir_filtra_Callback(hObject, eventdata, handles)
% hObject    handle to odabir_filtra (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns odabir_filtra contents as cell array
%        contents{get(hObject,'Value')} returns selected item from odabir_filtra


% --- Executes during object creation, after setting all properties.
function odabir_filtra_CreateFcn(hObject, eventdata, handles)
% hObject    handle to odabir_filtra (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in create_filter_button.
function create_filter_button_Callback(hObject, eventdata, handles)
% hObject    handle to create_filter_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if get(handles.odabir_filtra, 'Value') == 1
    
    uiwait(zero_pole)

    
elseif get(handles.odabir_filtra, 'Value') == 2
    
    uiwait(butter2)
    
elseif get(handles.odabir_filtra, 'Value') == 3
    
    uiwait(cheby)
    
end


% --- Executes on button press in filtriranje_button.
function filtriranje_button_Callback(hObject, eventdata, handles)
% hObject    handle to filtriranje_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global filtar
global signal
W = filtar.w;
h = filtar.h;


axes(handles.axes3)

X = fft(signal.signal);

f_osa = 0:signal.fs/numel(X):(signal.fs-signal.fs/numel(X));
f_osa = f_osa(1:int64(numel(f_osa)/2));
X = X(1:int64(numel(X)/2));
plot(f_osa, abs(X))
xlabel('Frekvencija [Hz]')

axes(handles.axes4)

y = filter(filtar.zeros, filtar.poles, signal.signal);
Y = fft(y);
Y = Y(1:int64(numel(Y)/2));
plot(f_osa, abs(Y))
xlabel('Frekvencija [Hz]')

axes(handles.axes5)

f = W/(2*pi)*signal.fs;
plot(f,abs(h))
xlabel('Frekvencija [Hz]')




function save_filter_entry_Callback(hObject, eventdata, handles)
% hObject    handle to save_filter_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of save_filter_entry as text
%        str2double(get(hObject,'String')) returns contents of save_filter_entry as a double


% --- Executes during object creation, after setting all properties.
function save_filter_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to save_filter_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton5.
function pushbutton5_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global filtar
filtar = filtar;

extension = ".mat";
name = get(handles.save_filter_entry, 'String');
title = strcat(name, extension);
save(title, 'filtar')
msgbox('Uspesno ste sacuvali parametre filtra', 'Cuvanje filtra')



function load_filter_entry_Callback(hObject, eventdata, handles)
% hObject    handle to load_filter_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of load_filter_entry as text
%        str2double(get(hObject,'String')) returns contents of load_filter_entry as a double


% --- Executes during object creation, after setting all properties.
function load_filter_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to load_filter_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in load_filter_button.
function load_filter_button_Callback(hObject, eventdata, handles)
% hObject    handle to load_filter_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global filtar
extension = ".mat";
name = get(handles.save_filter_entry, 'String');
title = strcat(name, extension);
loaded = load(title);
filtar = loaded.filtar;

msgbox('Uspesno ste ucitali filtar, sada mozete da ga upotrebite na obelezeni signal klikom na dugme: Filtriranje')


% --- Executes on button press in emg_button.
function emg_button_Callback(hObject, eventdata, handles)
% hObject    handle to emg_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

uiwait(obrada_EMG)


% --- Executes on button press in eeg_button.
function eeg_button_Callback(hObject, eventdata, handles)
% hObject    handle to eeg_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
uiwait(obrada_EEG)

