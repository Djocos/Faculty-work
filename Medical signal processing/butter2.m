function varargout = butter2(varargin)
% BUTTER2 MATLAB code for butter2.fig
%      BUTTER2, by itself, creates a new BUTTER2 or raises the existing
%      singleton*.
%
%      H = BUTTER2 returns the handle to a new BUTTER2 or the handle to
%      the existing singleton*.
%
%      BUTTER2('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in BUTTER2.M with the given input arguments.
%
%      BUTTER2('Property','Value',...) creates a new BUTTER2 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before butter2_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to butter2_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help butter2

% Last Modified by GUIDE v2.5 11-May-2022 01:35:43

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @butter2_OpeningFcn, ...
                   'gui_OutputFcn',  @butter2_OutputFcn, ...
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


% --- Executes just before butter2 is made visible.
function butter2_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to butter2 (see VARARGIN)

% Choose default command line output for butter2
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes butter2 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = butter2_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on selection change in tip_menu.
function tip_menu_Callback(hObject, eventdata, handles)
% hObject    handle to tip_menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns tip_menu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from tip_menu


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



function fp_Callback(hObject, eventdata, handles)
% hObject    handle to fp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of fp as text
%        str2double(get(hObject,'String')) returns contents of fp as a double


% --- Executes during object creation, after setting all properties.
function fp_CreateFcn(hObject, eventdata, handles)
% hObject    handle to fp (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function fn_Callback(hObject, eventdata, handles)
% hObject    handle to fn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of fn as text
%        str2double(get(hObject,'String')) returns contents of fn as a double


% --- Executes during object creation, after setting all properties.
function fn_CreateFcn(hObject, eventdata, handles)
% hObject    handle to fn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function slabljenje_p_Callback(hObject, eventdata, handles)
% hObject    handle to slabljenje_p (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of slabljenje_p as text
%        str2double(get(hObject,'String')) returns contents of slabljenje_p as a double


% --- Executes during object creation, after setting all properties.
function slabljenje_p_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slabljenje_p (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function slabljenje_n_Callback(hObject, eventdata, handles)
% hObject    handle to slabljenje_n (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of slabljenje_n as text
%        str2double(get(hObject,'String')) returns contents of slabljenje_n as a double


% --- Executes during object creation, after setting all properties.
function slabljenje_n_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slabljenje_n (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in create_filter.
function create_filter_Callback(hObject, eventdata, handles)
% hObject    handle to create_filter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global filtar
global signal

f_gr_p = str2double(strsplit(get(handles.fp, 'String')));
f_gr_n = str2double(strsplit(get(handles.fn, 'String')));
Rp = str2double(strsplit(get(handles.slabljenje_p, 'String')));
min_s = str2double(strsplit(get(handles.slabljenje_n, 'String')));
Rs = min_s - Rp;
Wp = f_gr_p * 2/signal.fs;
Ws = f_gr_n * 2/signal.fs;
[n, Wn] = buttord(Wp, Ws, Rp, Rs);

if get(handles.tip_menu, 'Value') == 1 % NF

    [P,Q] = butter(n,Wn,'low');
    [H,w]=freqz(P,Q);

    
elseif get(handles.tip_menu, 'Value') == 2 % VF
    
    [P,Q] = butter(n,Wn,'high');
    [H,w]=freqz(P,Q);

    
elseif get(handles.tip_menu, 'Value') == 3 % BP
    
    [P,Q] = butter(n,Wn,'bandpass');
    [H,w]=freqz(P,Q);

elseif get(handles.tip_menu, 'Value') == 4 % BS
    
    [P,Q] = butter(n,Wn,'stop');
    [H,w]=freqz(P,Q);

end
    filtar.w = w;
    filtar.h = H;
    filtar.zeros = P;
    filtar.poles = Q;
    close(butter2)
