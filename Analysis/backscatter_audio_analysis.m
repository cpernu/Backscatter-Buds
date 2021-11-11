

fs = 400e3;
T = 1/fs;
fc = 40e3;

%fa = 1e3;
%x = sin(2*pi*fa*t);
%[x,Fs] = audioread('file_example_WAV_1MG.wav');

x = interp(x(:,1), int8(fs/Fs));

t= 0:1/fs:(length(x) -1)/fs;
sqr = (sign(sin(2*pi*fc*t)) +1)/2;
mod = transpose(x).*sqr;

figure
subplot(2,1,1)
plot(x)
subplot(2,1,2)
plot(mod)

[freq, fft_mod] = fft_custom(x, fs);

figure
subplot(3,1,1)
plot(freq, abs(fft_mod))


f_cut_low = (fc - 2e3)/(fs/2);
f_cut_high = (fc + 2e3)/(fs/2);

b=fir1(200,[f_cut_low f_cut_high],'bandpass'); 
mod_filtered=filter(b,1,mod);


[freq, fft_mod_filtered] = fft_custom(mod_filtered, fs);

subplot(3,1,2)
plot(freq, abs(fft_mod_filtered))

mod_filtered_downcoverted = mod_filtered.*sin(2*pi*fc*t);

[freq, fft_mod_filtered_downcoverted] = fft_custom(mod_filtered_downcoverted, fs);

subplot(3,1,3)
plot(freq, abs(fft_mod_filtered_downcoverted))

f_cut_low = (4e3)/(fs/2);

b=fir1(200,[f_cut_low],'low'); 
recovered_sig=filter(b,1,mod);

figure
subplot(2,1,1)
plot(x)
subplot(2,1,2)
plot(2*recovered_sig)

