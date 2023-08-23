function varargout = zero_pole(varargin)
% ZERO_POLE MATLAB code for zero_pole.fig
%      ZERO_POLE, by itself, creates a new ZERO_POLE or raises the existing
%      singleton*.
%
%      H = ZERO_POLE returns the handle to a new ZERO_POLE or the handle to
%      the existing singleton*.
%
%      ZERO_POLE('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in ZERO_POLE.M with the given input arguments.
%
%      ZERO_POLE('Property','Value',...) creates a new ZERO_POLE or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before zero_pole_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to zero_pole_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help zero_pole

% Last Modified by GUIDE v2.5 09-May-2022 23:34:39

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @zero_pole_OpeningFcn, ...
                   'gui_OutputFcn',  @zero_pole_OutputFcn, ...
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


% --- Executes just before zero_pole is made visible.
function zero_pole_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to zero_pole (see VARARGIN)

% Choose default command line output for zero_pole
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
set(handles.poluprecnik_n_entry, 'Enable', 'off')
set(handles.ugao_n_entry, 'Enable', 'off')
% UIWAIT makes zero_pole wait for user response (see UIRESUME)
% uiwait(handles.figure1);



% --- Outputs from this function are returned to the command line.
function varargout = zero_pole_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function poluprecnik_n_entry_Callback(hObject, eventdata, handles)
% hObject    handle to poluprecnik_n_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of poluprecnik_n_entry as text
%        str2double(get(hObject,'String')) returns contents of poluprecnik_n_entry as a double


% --- Executes during object creation, after setting all properties.
function poluprecnik_n_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to poluprecnik_n_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ugao_n_entry_Callback(hObject, eventdata, handles)
% hObject    handle to ugao_n_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ugao_n_entry as text
%        str2double(get(hObject,'String')) returns contents of ugao_n_entry as a double


% --- Executes during object creation, after setting all properties.
function ugao_n_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ugao_n_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function poluprecnik_p_entry_Callback(hObject, eventdata, handles)
% hObject    handle to poluprecnik_p_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of poluprecnik_p_entry as text
%        str2double(get(hObject,'String')) returns contents of poluprecnik_p_entry as a double


% --- Executes during object creation, after setting all properties.
function poluprecnik_p_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to poluprecnik_p_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ugao_p_entry_Callback(hObject, eventdata, handles)
% hObject    handle to ugao_p_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ugao_p_entry as text
%        str2double(get(hObject,'String')) returns contents of ugao_p_entry as a double


% --- Executes during object creation, after setting all properties.
function ugao_p_entry_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ugao_p_entry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in tip_menu.
function tip_menu_Callback(hObject, eventdata, handles)
% hObject    handle to tip_menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns tip_menu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from
%        tip_menu
if get(hObject,'Value') == 1
    
    set(handles.poluprecnik_n_entry, 'Enable', 'off')
    set(handles.ugao_n_entry, 'Enable', 'off')
    
elseif get(hObject,'Value') == 2
    
    set(handles.poluprecnik_n_entry, 'Enable', 'off')
    set(handles.ugao_n_entry, 'Enable', 'off')   
    
elseif get(hObject,'Value') == 3
    
    set(handles.poluprecnik_n_entry, 'Enable', 'off')
    set(handles.ugao_n_entry, 'Enable', 'off')
    
elseif get(hObject,'Value') == 4
    
    set(handles.poluprecnik_n_entry, 'Enable', 'on')
    set(handles.ugao_n_entry, 'Enable', 'on')
end


% --- Executes during object creation, after setting all properties.
function tip_menu_CreateFcn(hObject, eventdata, handles)
% hObject    handle to tip_menu (see GCBO)
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

global filtar

if get(handles.tip_menu, 'Value') == 1 % NF
    teta_p = eval(get(handles.ugao_p_entry, 'String'));
    r_p = str2double(strsplit(get(handles.poluprecnik_p_entry, 'String')));
    b = [1 2 1];
    a = [1 -2*r_p * cos(teta_p) r_p^2];
    
    [h, w] = freqz(b, a);
    
    filtar.w = w;
    filtar.h = h;
    filtar.zeros = b;
    filtar.poles = a;
    close(zero_pole)

elseif get(handles.tip_menu, 'Value') == 2 % VF
    
    teta_p = eval(get(handles.ugao_p_entry, 'String'));
    r_p = str2double(strsplit(get(handles.poluprecnik_p_entry, 'String')));
    
    b = [1 -2 1];
    a = [1 -2*r_p*cos(teta_p) r_p^2];
    
    [h, w] = freqz(b, a);
    
    filtar.w = w;
    filtar.h = h;
    filtar.zeros = b;
    filtar.poles = a;
    close(zero_pole)
    
elseif get(handles.tip_menu, 'Value') == 3 % BP
    teta_p = eval(get(handles.ugao_p_entry, 'String'));
    r_p = str2double(strsplit(get(handles.poluprecnik_p_entry, 'String')));
    b = conv([1 -1], [1 1]);
    a = [1 -2*r_p*cos(teta_p) r_p^2];

    [h, w] = freqz(b, a);
    
    filtar.w = w;
    filtar.h = h;
    filtar.zeros = b;
    filtar.poles = a;
    close(zero_pole)

elseif get(handles.tip_menu, 'Value') == 4 % BS
    teta_p = split(get(handles.ugao_p_entry, 'String'));
    teta_p = [eval(char(teta_p(1))) eval(char(teta_p(2)))];
    r_p = str2double(strsplit(get(handles.poluprecnik_p_entry, 'String')));
    
    teta_z = split(get(handles.ugao_n_entry, 'String'));
    teta_z = [eval(char(teta_z(1))) eval(char(teta_z(2)))];
    r_z = str2double(strsplit(get(handles.poluprecnik_n_entry, 'String')));
    
    b = conv([1 -2*r_z(1)*cos(teta_z(1)) r_z(1)^2], [1 -2*r_z(2)*cos(teta_z(2)) r_z(2)^2]);
    a = conv([1 -2*r_p(1)*cos(teta_p(1)) r_p(1)^2], [1 -2*r_p(2)*cos(teta_p(2)) r_p(2)^2]);

    [h, w] = freqz(b, a);
    
    filtar.w = w;
    filtar.h = h;
    filtar.zeros = b;
    filtar.poles = a;
    close(zero_pole)
end
