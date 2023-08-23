function [result] = wavelet_spektrogram(x,fs, fmin, fmax) 

result = [];
sigm = 0.7;
    
fo = 1;
pas = 0.5; 
number = fix(length(x)/2)*2; 




y = fft(x); 
brojac = 1;    
    
for fff=fmin:pas:fmax 
     
    a = 1/fff; 
    wavelet = exp(-2/sigm*(pi)^2*(([0:number/2-1,-number/2:-1]*(fs*a/number))-(fo)).^2);
    
    g = wavelet.*y; 
    t = ifft(g); 
    result(brojac,:)=(a.^0.5).*t;
   
    brojac=brojac+1;
         
end

end
