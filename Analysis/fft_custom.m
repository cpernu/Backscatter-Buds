function [freq, fft_x] = fft_custom(x, Fs)

N=length(x);
if mod(N,2)==0
    k=-N/2:N/2-1; % N even
else
    k=-(N-1)/2:(N-1)/2; % N odd
end

T=N/Fs;
freq=k/T;  

fft_x=fftshift(fft(x)/N);
