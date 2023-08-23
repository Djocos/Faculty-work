function varargout = obrada_EMG(varargin)
% OBRADA_EMG MATLAB code for obrada_EMG.fig
%      OBRADA_EMG, by itself, creates a new OBRADA_EMG or raises the existing
%      singleton*.
%
%      H = OBRADA_EMG returns the handle to a new OBRADA_EMG or the handle to
%      the existing singleton*.
%
%      OBRADA_EMG('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in OBRADA_EMG.M with the given input arguments.
%
%      OBRADA_EMG('Property','Value',...) creates a new OBRADA_EMG or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before obrada_EMG_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to obrada_EMG_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help obrada_EMG

% Last Modified by GUIDE v2.5 03-Jun-2022 13:37:47

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @obrada_EMG_OpeningFcn, ...
                   'gui_OutputFcn',  @obrada_EMG_OutputFcn, ...
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


% --- Executes just before obrada_EMG is made visible.
function obrada_EMG_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to obrada_EMG (see VARARGIN)

% Choose default command line output for obrada_EMG
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes obrada_EMG wait for user response (see UIRESUME)
% uiwait(handles.figure1);
global EMG1 
global EMG2
global t
EMG1 = load('EMG_signal1.mat');
t_end = numel(EMG1.data.signal)*1/EMG1.data.Fs;
t = 0:1/EMG1.data.Fs:t_end;
t = t(1:numel(t)-1);
axes(handles.axes1)
plot(t, EMG1.data.signal)

EMG2 = load('EMG_signal2.mat');
t_end = numel(EMG2.data.signal)*1/EMG2.data.Fs;
t = 0:1/EMG2.data.Fs:t_end;
t = t(1:numel(t)-1);
axes(handles.axes2)
plot(t, EMG2.data.signal)



% --- Outputs from this function are returned to the command line.
function varargout = obrada_EMG_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in anvelopa_button.
function anvelopa_button_Callback(hObject, eventdata, handles)
% hObject    handle to anvelopa_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global EMG1
global EMG2
global t fleks ext

[b,a] = butter(2, 0.005, 'low');
EMG1_filt = filter(b, a, (EMG1.data.signal.^2));
anvelope1 = sqrt(EMG1_filt);
axes(handles.axes1)

hold on
plot(t, abs(anvelope1), 'linewidth', 2)


% Traženje gde se nalazi flex

pik1 = max(anvelope1);
fleks = anvelope1 > pik1*0.707;

EMG2_filt = filter(b, a, (EMG2.data.signal.^2));
anvelope2 = sqrt(EMG2_filt);

% Traženje ext

pik2 = max(anvelope2);
ext = anvelope2 > pik2*0.65;

axes(handles.axes2)

hold on
plot(t, abs(anvelope2), 'linewidth', 2)

% --- Executes on button press in oznaci_button.
function oznaci_button_Callback(hObject, eventdata, handles)
% hObject    handle to oznaci_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fleks ext t EMG1 EMG2

for i = 1:length(fleks)
    if fleks(i) == 1
        try
            if sum(fleks(i-EMG1.data.Fs:i-1))>=1
                continue
            end
            axes(handles.axes1)
            text(t(i), -0.5, '*Flex', 'Color', 'y')
            axes(handles.axes2)
            text(t(i), -0.5, '*Flex', 'Color', 'y')
        catch
            if sum(fleks(1:i-1))>=1
                continue
            end
            axes(handles.axes1)
            text(t(i), -0.5, '*Flex', 'Color', 'y')
            axes(handles.axes2)
            text(t(i), -0.5, '*Flex', 'Color', 'y')
        end
    elseif ext(i) == 1
        try
            if sum(ext(i-EMG2.data.Fs:i-1))>=1
                continue
            end
            axes(handles.axes1)
            text(t(i), -0.5, '*Ext', 'Color', 'y')
            axes(handles.axes2)
            text(t(i), -0.5, '*Ext', 'Color', 'y')
        catch
            if sum(ext(1:i-1))>=1
                continue
            end
            axes(handles.axes1)
            text(t(i), -0.5, '*Ext', 'Color', 'y')
            axes(handles.axes2)
            text(t(i), -0.5, '*Ext', 'Color', 'y')
        end
    end
end
