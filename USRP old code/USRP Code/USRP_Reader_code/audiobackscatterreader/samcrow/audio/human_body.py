#!/usr/bin/env python

# Extremely High order filter for noise suppresion with realtime plot
# Plotting the output of agc in real time
# Noise Spectrum Subtraction in real time

from gnuradio import gr, gru, uhd
from gnuradio import usrp
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option

from gnuradio.qtgui import qtgui
from PyQt4 import QtGui
import sys, sip

from string import split
from string import strip
from string import atoi
import time
import os
import math

which_usrp = 0

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
        sig = gr.sig_source_f(1e6, gr.GR_CONST_WAVE,0, 1, 0)
        out1 = gr.file_sink(gr.sizeof_gr_complex, "realtime_speech.dat")
	out3 = gr.file_sink(gr.sizeof_gr_complex, "before_agc.dat")
        out2 = gr.file_sink(gr.sizeof_gr_complex, "today.dat")
	#USRP1 or USRP2
        usrp_version = 2


        freq = 915e6

        rx_gain = 10

#USRP2
        if usrp_version == 2:
            tx = uhd.single_usrp_sink('addr=192.168.10.2', uhd.io_type_t.COMPLEX_FLOAT32,1)
            tx.set_samp_rate(1e6)
            print tx.get_samp_rate()
            tx.set_center_freq(freq, 0)
            tx.set_antenna('TX/RX',0)
            tx.set_gain(10000)

            rx = uhd.single_usrp_source('addr=192.168.10.2', uhd.io_type_t.COMPLEX_FLOAT32,1)
            rx.set_samp_rate(1e6)
            rx.set_gain(rx_gain)
            rx.set_center_freq(freq, 0)
            rx.set_antenna('RX2')



#END USRP2
#USRP
        if usrp_version == 1:
            tx = usrp.sink_c(which=which_usrp,fusb_block_size = 1024, fusb_nblocks=4)
            tx.set_interp_rate(64)
            tx_subdev = (0,0)
            tx.set_mux(usrp.determine_tx_mux_value(tx, tx_subdev))
            subdev = usrp.selected_subdev(tx, tx_subdev)
            subdev.set_enable(True)
            subdev.set_gain(subdev.gain_range()[2])
            t = tx.tune(subdev.which(), subdev, freq)
            if not t:
                print "Couldn't set tx freq"

            rx = usrp.source_c(which=which_usrp, decim_rate = 64, fusb_block_size = 512, fusb_nblocks = 8)
            rx_subdev_spec = (1,0)
            rx.set_mux(usrp.determine_rx_mux_value(rx, rx_subdev_spec))
            rx_subdev = usrp.selected_subdev(rx, rx_subdev_spec)
            rx_subdev.set_gain(rx_gain)
            rx_subdev.set_auto_tr(False)
            rx_subdev.set_enable(True)
            #rx_subdev.select_rx_antenna('RX2')
            r = usrp.tune(rx, 0, rx_subdev, freq)
            if not r:
                print "Couldn't set rx freq"

#END USRP
	band_pass_coeffs =  gr.firdes.band_pass(1.0, 50e3, 300, 3.4e3, 4.5, gr.firdes.WIN_HAMMING)
	high_pass_coeffs =  gr.firdes.high_pass(1.0, 50e3, 300, 3, gr.firdes.WIN_HAMMING)
	filt_decimate= gr.fir_filter_fff(20,[1]);

	matlab_taps = [4.899652e-05, 5.841297e-05, 6.282155e-05, 6.147812e-05, 5.466236e-05, 4.363053e-05, 3.039300e-05, 1.735585e-05, 6.890236e-06, 9.065930e-07, 5.097362e-07, 5.797190e-06, 1.583737e-05, 2.883232e-05, 4.243663e-05, 5.417617e-05, 6.189186e-05, 6.412924e-05, 6.040360e-05, 5.129233e-05, 3.833727e-05, 2.377317e-05, 1.013018e-05, -2.191591e-07, -5.487465e-06, -4.797665e-06, 1.653235e-06, 1.262229e-05, 2.603695e-05, 3.936199e-05, 5.005240e-05, 5.601131e-05, 5.597097e-05, 4.972749e-05, 3.818626e-05, 2.320813e-05, 7.282560e-06, -6.915186e-06, -1.700396e-05, -2.132797e-05, -1.926134e-05, -1.132998e-05, 8.726780e-07, 1.496298e-05, 2.818925e-05, 3.792431e-05, 4.214045e-05, 3.978114e-05, 3.096154e-05, 1.696002e-05, 1.363182e-18, -1.714075e-05, -3.162489e-05, -4.106624e-05, -4.396490e-05, -3.998717e-05, -3.003854e-05, -1.611393e-05, -9.497732e-07, 1.246154e-05, 2.140913e-05, 2.395657e-05, 1.930099e-05, 7.931932e-06, -8.441023e-06, -2.718172e-05, -4.519168e-05, -5.946355e-05, -6.762506e-05, -6.837512e-05, -6.173209e-05, -4.904700e-05, -3.277628e-05, -1.605190e-05, -2.123854e-06, 6.225946e-06, 7.193077e-06, 2.901695e-07, -1.354690e-05, -3.210856e-05, -5.229328e-05, -7.065576e-05, -8.402476e-05, -9.007996e-05, -8.778312e-05, -7.758334e-05, -6.135649e-05, -4.208573e-05, -2.333726e-05, -8.623252e-06, -7.653509e-07, -1.373927e-06, -1.053890e-05, -2.679111e-05, -4.734512e-05, -6.858382e-05, -8.670047e-05, -9.838473e-05, -1.014288e-04, -9.514351e-05, -8.050507e-05, -6.000349e-05, -3.721416e-05, -1.616681e-05, -6.226126e-07, 6.610938e-06, 4.202968e-06, -7.437253e-06, -2.620782e-05, -4.866891e-05, -7.064520e-05, -8.797073e-05, -9.724365e-05, -9.645414e-05, -8.537011e-05, -6.560685e-05, -4.036323e-05, -1.386705e-05, 9.374706e-06, 2.538779e-05, 3.145883e-05, 2.664641e-05, 1.197918e-05, -9.699824e-06, -3.422013e-05, -5.681887e-05, -7.299486e-05, -7.932868e-05, -7.411983e-05, -5.772246e-05, -3.251413e-05, -2.497489e-06, 2.739887e-05, 5.219844e-05, 6.777744e-05, 7.162520e-05, 6.332428e-05, 4.465886e-05, 1.932583e-05, -7.705512e-06, -3.107445e-05, -4.599501e-05, -4.913327e-05, -3.923556e-05, -1.738958e-05, 1.313471e-05, 4.744223e-05, 7.987352e-05, 1.050177e-04, 1.186964e-04, 1.187404e-04, 1.054140e-04, 8.140496e-05, 5.137554e-05, 2.114761e-05, -3.334938e-06, -1.708264e-05, -1.698106e-05, -2.386133e-06, 2.471891e-05, 6.004045e-05, 9.771527e-05, 1.313478e-04, 1.551603e-04, 1.650495e-04, 1.593563e-04, 1.392044e-04, 1.083405e-04, 7.249536e-05, 3.837581e-05, 1.246344e-05, -1.647761e-07, 3.220123e-06, 2.246654e-05, 5.452364e-05, 9.394808e-05, 1.338526e-04, 1.671312e-04, 1.877438e-04, 1.918273e-04, 1.784298e-04, 1.497285e-04, 1.106837e-04, 6.818238e-05, 2.981996e-05, 2.533592e-06, -8.665975e-06, -1.633196e-06, 2.247835e-05, 5.937352e-05, 1.023452e-04, 1.434528e-04, 1.749423e-04, 1.906552e-04, 1.871699e-04, 1.644637e-04, 1.259707e-04, 7.801175e-05, 2.869411e-05, -1.353102e-05, -4.139478e-05, -5.014624e-05, -3.845202e-05, -8.689939e-06, 3.342565e-05, 7.982922e-05, 1.215308e-04, 1.502322e-04, 1.598423e-04, 1.476159e-04, 1.147025e-04, 6.599807e-05, 9.315347e-06, -4.598760e-05, -9.067921e-05, -1.173288e-04, -1.216794e-04, -1.034667e-04, -6.652518e-05, -1.815405e-05, 3.215517e-05, 7.440730e-05, 9.990894e-05, 1.028647e-04, 8.147238e-05, 3.830998e-05, -2.006468e-05, -8.424225e-05, -1.436235e-04, -1.883212e-04, -2.109613e-04, -2.080550e-04, -1.806867e-04, -1.343832e-04, -7.817653e-05, -2.301618e-05, 2.018803e-05, 4.254541e-05, 3.882656e-05, 8.465996e-06, -4.426595e-05, -1.109651e-04, -1.805547e-04, -2.412526e-04, -2.826944e-04, -2.978308e-04, -2.842511e-04, -2.446854e-04, -1.865830e-04, -1.208284e-04, -5.981729e-05, -1.523094e-05, 4.092150e-06, -6.200577e-06, -4.512184e-05, -1.064461e-04, -1.797621e-04, -2.522982e-04, -3.112023e-04, -3.458678e-04, -3.498862e-04, -3.222664e-04, -2.676898e-04, -1.957410e-04, -1.192397e-04, -5.196267e-05, -6.161054e-06, 9.681284e-06, -7.562393e-06, -5.502014e-05, -1.242577e-04, -2.027289e-04, -2.759909e-04, -3.302943e-04, -3.550830e-04, -3.449507e-04, -3.006911e-04, -2.292400e-04, -1.425031e-04, -5.526866e-05, 1.743167e-05, 6.304153e-05, 7.378744e-05, 4.815140e-05, -8.769674e-06, -8.609788e-05, -1.690669e-04, -2.416447e-04, -2.894208e-04, -3.022396e-04, -2.760981e-04, -2.139551e-04, -1.252903e-04, -2.447692e-05, 7.175446e-05, 1.473125e-04, 1.896660e-04, 1.921593e-04, 1.552941e-04, 8.673179e-05, 1.533880e-18, -8.788167e-05, -1.594391e-04, -1.999040e-04, -1.999262e-04, -1.573403e-04, -7.765507e-05, 2.684097e-05, 1.392130e-04, 2.408829e-04, 3.149693e-04, 3.493637e-04, 3.389832e-04, 2.867794e-04, 2.033069e-04, 1.049082e-04, 1.082739e-05, -6.023841e-05, -9.353447e-05, -8.097318e-05, -2.268711e-05, 7.288625e-05, 1.904224e-04, 3.103929e-04, 4.125441e-04, 4.795522e-04, 5.001942e-04, 4.714554e-04, 3.991773e-04, 2.971112e-04, 1.845270e-04, 8.279274e-05, 1.153094e-05, -1.495803e-05, 9.645695e-06, 8.243429e-05, 1.916797e-04, 3.188433e-04, 4.418436e-04, 5.390065e-04, 5.929925e-04, 5.939872e-04, 5.415712e-04, 4.449118e-04, 3.212226e-04, 1.927469e-04, 8.279328e-05, 1.152902e-05, -7.710197e-06, 2.908007e-05, 1.157315e-04, 2.368926e-04, 3.706924e-04, 4.926179e-04, 5.799175e-04, 6.157399e-04, 5.922566e-04, 5.121900e-04, 3.884508e-04, 2.419264e-04, 9.779982e-05, -1.895480e-05, -8.809368e-05, -9.782384e-05, -4.703962e-05, 5.434790e-05, 1.870713e-04, 3.258809e-04, 4.440426e-04, 5.181593e-04, 5.324469e-04, 4.816845e-04, 3.722895e-04, 2.212987e-04, 5.341666e-05, -1.033603e-04, -2.227673e-04, -2.850418e-04, -2.805752e-04, -2.117704e-04, -9.274854e-05, 5.306868e-05, 1.970885e-04, 3.106621e-04, 3.702705e-04, 3.618449e-04, 2.834287e-04, 1.456790e-04, -2.990729e-05, -2.147499e-04, -3.782686e-04, -4.933877e-04, -5.414727e-04, -5.157976e-04, -4.228985e-04, -2.815445e-04, -1.194820e-04, 3.148316e-05, 1.411959e-04, 1.866311e-04, 1.561479e-04, 5.173303e-05, -1.111933e-04, -3.064053e-04, -5.014849e-04, -6.636096e-04, -7.654808e-04, -7.903233e-04, -7.350388e-04, -6.109218e-04, -4.417811e-04, -2.597748e-04, -9.968620e-05, 7.341366e-06, 3.948440e-05, -1.170081e-05, -1.395916e-04, -3.235181e-04, -5.323361e-04, -7.299352e-04, -8.817104e-04, -9.608358e-04, -9.532043e-04, -8.601236e-04, -6.982554e-04, -4.967765e-04, -2.922434e-04, -1.220630e-04, -1.773411e-05, 9.198589e-07, -7.052712e-05, -2.201242e-04, -4.215154e-04, -6.385398e-04, -8.316581e-04, -9.650647e-04, -1.013206e-03, -9.655190e-04, -8.285147e-04, -6.247952e-04, -3.891503e-04, -1.624057e-04, 1.589152e-05, 1.146395e-04, 1.169025e-04, 2.313427e-05, -1.487059e-04, -3.662034e-04, -5.881871e-04, -7.720780e-04, -8.815755e-04, -8.932971e-04, -8.011570e-04, -6.176668e-04, -3.718877e-04, -1.043666e-04, 1.400631e-04, 3.203367e-04, 4.066245e-04, 3.858497e-04, 2.642403e-04, 6.641768e-05, -1.688516e-04, -3.955102e-04, -5.684617e-04, -6.517419e-04, -6.251317e-04, -4.879980e-04, -2.596359e-04, 2.398859e-05, 3.165477e-04, 5.696066e-04, 7.413523e-04, 8.042241e-04, 7.500535e-04, 5.917553e-04, 3.612242e-04, 1.037769e-04, -1.298978e-04, -2.928509e-04, -3.504122e-04, -2.866063e-04, -1.072599e-04, 1.607971e-04, 4.743390e-04, 7.813676e-04, 1.030409e-03, 1.179822e-03, 1.205432e-03, 1.105094e-03, 8.993246e-04, 6.278439e-04, 3.426022e-04, 9.851988e-05, -5.641727e-05, -8.991993e-05, 8.581039e-06, 2.257705e-04, 5.265793e-04, 8.602724e-04, 1.169440e-03, 1.400296e-03, 1.512442e-03, 1.486318e-03, 1.326975e-03, 1.063432e-03, 7.437033e-04, 4.263250e-04, 1.698870e-04, 2.243529e-05, 1.265962e-05, 1.444811e-04, 3.960570e-04, 7.234327e-04, 1.068234e-03, 1.368057e-03, 1.567700e-03, 1.629232e-03, 1.539043e-03, 1.310586e-03, 9.822537e-04, 6.107221e-04, 2.609111e-04, -5.658727e-06, -1.420301e-04, -1.244667e-04, 4.298714e-05, 3.289192e-04, 6.799148e-04, 1.029963e-03, 1.312251e-03, 1.471237e-03, 1.472829e-03, 1.310801e-03, 1.008247e-03, 6.137451e-04, 1.928809e-04, -1.834155e-04, -4.516260e-04, -5.672124e-04, -5.128857e-04, -3.020455e-04, 2.329045e-05, 3.997557e-04, 7.538498e-04, 1.015118e-03, 1.128935e-03, 1.066575e-03, 8.307206e-04, 4.553565e-04, 2.608276e-18, -4.607505e-04, -8.505181e-04, -1.104929e-03, -1.183388e-03, -1.076689e-03, -8.090483e-04, -4.341112e-04, -2.559187e-05, 3.358266e-04, 5.770095e-04, 6.456974e-04, 5.202170e-04, 2.137792e-04, -2.274804e-04, -7.324363e-04, -1.217524e-03, -1.601690e-03, -1.821071e-03, -1.840740e-03, -1.661362e-03, -1.319499e-03, -8.814230e-04, -4.314838e-04, -5.706396e-05, 1.671967e-04, 1.930674e-04, 7.784038e-06, -3.631949e-04, -8.603102e-04, -1.400242e-03, -1.890673e-03, -2.246867e-03, -2.407072e-03, -2.343976e-03, -2.070057e-03, -1.635826e-03, -1.121156e-03, -6.211940e-04, -2.293440e-04, -2.033801e-05, -3.647844e-05, -2.795674e-04, -7.100591e-04, -1.253679e-03, -1.814408e-03, -2.291566e-03, -2.597956e-03, -2.675810e-03, -2.507605e-03, -2.119759e-03, -1.578412e-03, -9.779815e-04, -4.244470e-04, -1.633024e-05, 1.732257e-04, 1.100220e-04, -1.944955e-04, -6.847028e-04, -1.270275e-03, -1.842063e-03, -2.291591e-03, -2.530692e-03, -2.507726e-03, -2.217425e-03, -1.702468e-03, -1.046420e-03, -3.591683e-04, 2.425881e-04, 6.563556e-04, 8.125763e-04, 6.876584e-04, 3.088726e-04, -2.498850e-04, -8.808226e-04, -1.461291e-03, -1.875774e-03, -2.036902e-03, -1.901665e-03, -1.479831e-03, -8.329436e-04, -6.393406e-05, 7.008996e-04, 1.334396e-03, 1.731517e-03, 1.828655e-03, 1.615740e-03, 1.138821e-03, 4.925424e-04, -1.962803e-04, -7.911535e-04, -1.170476e-03, -1.249784e-03, -9.976083e-04, -4.419811e-04, 3.337210e-04, 1.205012e-03, 2.028182e-03, 2.665996e-03, 3.012613e-03, 3.013207e-03, 2.674667e-03, 2.065285e-03, 1.303348e-03, 5.364850e-04, -8.460468e-05, -4.334012e-04, -4.308710e-04, -6.055410e-05, 6.274285e-04, 1.524350e-03, 2.481587e-03, 3.336852e-03, 3.943329e-03, 4.196493e-03, 4.053717e-03, 3.543005e-03, 2.759098e-03, 1.847428e-03, 9.786325e-04, 3.180748e-04, -4.208617e-06, 8.231841e-05, 5.748650e-04, 1.396516e-03, 2.408836e-03, 3.435828e-03, 4.295123e-03, 4.830871e-03, 4.942434e-03, 4.603605e-03, 3.868702e-03, 2.864211e-03, 1.767199e-03, 7.741838e-04, 6.589155e-05, -2.257873e-04, -4.263274e-05, 5.879309e-04, 1.556132e-03, 2.688121e-03, 3.776192e-03, 4.615734e-03, 5.042355e-03, 4.962467e-03, 4.371679e-03, 3.357407e-03, 2.084932e-03, 7.690658e-04, -3.637332e-04, -1.116150e-03, -1.356390e-03, -1.043470e-03, -2.366125e-04, 9.132895e-04, 2.189002e-03, 3.344840e-03, 4.150562e-03, 4.433452e-03, 4.110948e-03, 3.207701e-03, 1.853614e-03, 2.627909e-04, -1.303263e-03, -2.581892e-03, -3.356864e-03, -3.498700e-03, -2.990289e-03, -1.932796e-03, -5.303063e-04, 9.445500e-04, 2.198264e-03, 2.969133e-03, 3.075571e-03, 2.451196e-03, 1.160018e-03, -6.115737e-04, -2.585181e-03, -4.438272e-03, -5.861387e-03, -6.614613e-03, -6.573100e-03, -5.753091e-03, -4.313193e-03, -2.529922e-03, -7.511766e-04, 6.646379e-04, 1.413299e-03, 1.301701e-03, 2.865337e-04, -1.512869e-03, -3.830660e-03, -6.297648e-03, -8.504614e-03, -1.007507e-02, -1.073467e-02, -1.036465e-02, -9.029103e-03, -6.970256e-03, -4.571386e-03, -2.292855e-03, -5.917288e-04, 1.612042e-04, -2.477853e-04, -1.829983e-03, -4.383430e-03, -7.520074e-03, -1.072763e-02, -1.345658e-02, -1.521781e-02, -1.567396e-02, -1.470788e-02, -1.245481e-02, -9.290936e-03, -5.778163e-03, -2.572697e-03, -3.119151e-04, 5.016213e-04, -4.013879e-04, -2.994432e-03, -6.941569e-03, -1.163793e-02, -1.630041e-02, -2.009576e-02, -2.228591e-02, -2.236655e-02, -2.017441e-02, -1.594281e-02, -1.029239e-02, -4.154207e-03, 1.366635e-03, 5.168124e-03, 6.342894e-03, 4.353680e-03, -8.369131e-04, -8.706422e-03, -1.819667e-02, -2.782399e-02, -3.586406e-02, -4.058789e-02, -4.051624e-02, -3.465571e-02, -2.268050e-02, -5.030549e-03, 1.709177e-02, 4.183048e-02, 6.687870e-02, 8.975005e-02, 1.080828e-01, 1.199357e-01, 1.240346e-01, 1.199357e-01, 1.080828e-01, 8.975005e-02, 6.687870e-02, 4.183048e-02, 1.709177e-02, -5.030549e-03, -2.268050e-02, -3.465571e-02, -4.051624e-02, -4.058789e-02, -3.586406e-02, -2.782399e-02, -1.819667e-02, -8.706422e-03, -8.369131e-04, 4.353680e-03, 6.342894e-03, 5.168124e-03, 1.366635e-03, -4.154207e-03, -1.029239e-02, -1.594281e-02, -2.017441e-02, -2.236655e-02, -2.228591e-02, -2.009576e-02, -1.630041e-02, -1.163793e-02, -6.941569e-03, -2.994432e-03, -4.013879e-04, 5.016213e-04, -3.119151e-04, -2.572697e-03, -5.778163e-03, -9.290936e-03, -1.245481e-02, -1.470788e-02, -1.567396e-02, -1.521781e-02, -1.345658e-02, -1.072763e-02, -7.520074e-03, -4.383430e-03, -1.829983e-03, -2.477853e-04, 1.612042e-04, -5.917288e-04, -2.292855e-03, -4.571386e-03, -6.970256e-03, -9.029103e-03, -1.036465e-02, -1.073467e-02, -1.007507e-02, -8.504614e-03, -6.297648e-03, -3.830660e-03, -1.512869e-03, 2.865337e-04, 1.301701e-03, 1.413299e-03, 6.646379e-04, -7.511766e-04, -2.529922e-03, -4.313193e-03, -5.753091e-03, -6.573100e-03, -6.614613e-03, -5.861387e-03, -4.438272e-03, -2.585181e-03, -6.115737e-04, 1.160018e-03, 2.451196e-03, 3.075571e-03, 2.969133e-03, 2.198264e-03, 9.445500e-04, -5.303063e-04, -1.932796e-03, -2.990289e-03, -3.498700e-03, -3.356864e-03, -2.581892e-03, -1.303263e-03, 2.627909e-04, 1.853614e-03, 3.207701e-03, 4.110948e-03, 4.433452e-03, 4.150562e-03, 3.344840e-03, 2.189002e-03, 9.132895e-04, -2.366125e-04, -1.043470e-03, -1.356390e-03, -1.116150e-03, -3.637332e-04, 7.690658e-04, 2.084932e-03, 3.357407e-03, 4.371679e-03, 4.962467e-03, 5.042355e-03, 4.615734e-03, 3.776192e-03, 2.688121e-03, 1.556132e-03, 5.879309e-04, -4.263274e-05, -2.257873e-04, 6.589155e-05, 7.741838e-04, 1.767199e-03, 2.864211e-03, 3.868702e-03, 4.603605e-03, 4.942434e-03, 4.830871e-03, 4.295123e-03, 3.435828e-03, 2.408836e-03, 1.396516e-03, 5.748650e-04, 8.231841e-05, -4.208617e-06, 3.180748e-04, 9.786325e-04, 1.847428e-03, 2.759098e-03, 3.543005e-03, 4.053717e-03, 4.196493e-03, 3.943329e-03, 3.336852e-03, 2.481587e-03, 1.524350e-03, 6.274285e-04, -6.055410e-05, -4.308710e-04, -4.334012e-04, -8.460468e-05, 5.364850e-04, 1.303348e-03, 2.065285e-03, 2.674667e-03, 3.013207e-03, 3.012613e-03, 2.665996e-03, 2.028182e-03, 1.205012e-03, 3.337210e-04, -4.419811e-04, -9.976083e-04, -1.249784e-03, -1.170476e-03, -7.911535e-04, -1.962803e-04, 4.925424e-04, 1.138821e-03, 1.615740e-03, 1.828655e-03, 1.731517e-03, 1.334396e-03, 7.008996e-04, -6.393406e-05, -8.329436e-04, -1.479831e-03, -1.901665e-03, -2.036902e-03, -1.875774e-03, -1.461291e-03, -8.808226e-04, -2.498850e-04, 3.088726e-04, 6.876584e-04, 8.125763e-04, 6.563556e-04, 2.425881e-04, -3.591683e-04, -1.046420e-03, -1.702468e-03, -2.217425e-03, -2.507726e-03, -2.530692e-03, -2.291591e-03, -1.842063e-03, -1.270275e-03, -6.847028e-04, -1.944955e-04, 1.100220e-04, 1.732257e-04, -1.633024e-05, -4.244470e-04, -9.779815e-04, -1.578412e-03, -2.119759e-03, -2.507605e-03, -2.675810e-03, -2.597956e-03, -2.291566e-03, -1.814408e-03, -1.253679e-03, -7.100591e-04, -2.795674e-04, -3.647844e-05, -2.033801e-05, -2.293440e-04, -6.211940e-04, -1.121156e-03, -1.635826e-03, -2.070057e-03, -2.343976e-03, -2.407072e-03, -2.246867e-03, -1.890673e-03, -1.400242e-03, -8.603102e-04, -3.631949e-04, 7.784038e-06, 1.930674e-04, 1.671967e-04, -5.706396e-05, -4.314838e-04, -8.814230e-04, -1.319499e-03, -1.661362e-03, -1.840740e-03, -1.821071e-03, -1.601690e-03, -1.217524e-03, -7.324363e-04, -2.274804e-04, 2.137792e-04, 5.202170e-04, 6.456974e-04, 5.770095e-04, 3.358266e-04, -2.559187e-05, -4.341112e-04, -8.090483e-04, -1.076689e-03, -1.183388e-03, -1.104929e-03, -8.505181e-04, -4.607505e-04, 2.608276e-18, 4.553565e-04, 8.307206e-04, 1.066575e-03, 1.128935e-03, 1.015118e-03, 7.538498e-04, 3.997557e-04, 2.329045e-05, -3.020455e-04, -5.128857e-04, -5.672124e-04, -4.516260e-04, -1.834155e-04, 1.928809e-04, 6.137451e-04, 1.008247e-03, 1.310801e-03, 1.472829e-03, 1.471237e-03, 1.312251e-03, 1.029963e-03, 6.799148e-04, 3.289192e-04, 4.298714e-05, -1.244667e-04, -1.420301e-04, -5.658727e-06, 2.609111e-04, 6.107221e-04, 9.822537e-04, 1.310586e-03, 1.539043e-03, 1.629232e-03, 1.567700e-03, 1.368057e-03, 1.068234e-03, 7.234327e-04, 3.960570e-04, 1.444811e-04, 1.265962e-05, 2.243529e-05, 1.698870e-04, 4.263250e-04, 7.437033e-04, 1.063432e-03, 1.326975e-03, 1.486318e-03, 1.512442e-03, 1.400296e-03, 1.169440e-03, 8.602724e-04, 5.265793e-04, 2.257705e-04, 8.581039e-06, -8.991993e-05, -5.641727e-05, 9.851988e-05, 3.426022e-04, 6.278439e-04, 8.993246e-04, 1.105094e-03, 1.205432e-03, 1.179822e-03, 1.030409e-03, 7.813676e-04, 4.743390e-04, 1.607971e-04, -1.072599e-04, -2.866063e-04, -3.504122e-04, -2.928509e-04, -1.298978e-04, 1.037769e-04, 3.612242e-04, 5.917553e-04, 7.500535e-04, 8.042241e-04, 7.413523e-04, 5.696066e-04, 3.165477e-04, 2.398859e-05, -2.596359e-04, -4.879980e-04, -6.251317e-04, -6.517419e-04, -5.684617e-04, -3.955102e-04, -1.688516e-04, 6.641768e-05, 2.642403e-04, 3.858497e-04, 4.066245e-04, 3.203367e-04, 1.400631e-04, -1.043666e-04, -3.718877e-04, -6.176668e-04, -8.011570e-04, -8.932971e-04, -8.815755e-04, -7.720780e-04, -5.881871e-04, -3.662034e-04, -1.487059e-04, 2.313427e-05, 1.169025e-04, 1.146395e-04, 1.589152e-05, -1.624057e-04, -3.891503e-04, -6.247952e-04, -8.285147e-04, -9.655190e-04, -1.013206e-03, -9.650647e-04, -8.316581e-04, -6.385398e-04, -4.215154e-04, -2.201242e-04, -7.052712e-05, 9.198589e-07, -1.773411e-05, -1.220630e-04, -2.922434e-04, -4.967765e-04, -6.982554e-04, -8.601236e-04, -9.532043e-04, -9.608358e-04, -8.817104e-04, -7.299352e-04, -5.323361e-04, -3.235181e-04, -1.395916e-04, -1.170081e-05, 3.948440e-05, 7.341366e-06, -9.968620e-05, -2.597748e-04, -4.417811e-04, -6.109218e-04, -7.350388e-04, -7.903233e-04, -7.654808e-04, -6.636096e-04, -5.014849e-04, -3.064053e-04, -1.111933e-04, 5.173303e-05, 1.561479e-04, 1.866311e-04, 1.411959e-04, 3.148316e-05, -1.194820e-04, -2.815445e-04, -4.228985e-04, -5.157976e-04, -5.414727e-04, -4.933877e-04, -3.782686e-04, -2.147499e-04, -2.990729e-05, 1.456790e-04, 2.834287e-04, 3.618449e-04, 3.702705e-04, 3.106621e-04, 1.970885e-04, 5.306868e-05, -9.274854e-05, -2.117704e-04, -2.805752e-04, -2.850418e-04, -2.227673e-04, -1.033603e-04, 5.341666e-05, 2.212987e-04, 3.722895e-04, 4.816845e-04, 5.324469e-04, 5.181593e-04, 4.440426e-04, 3.258809e-04, 1.870713e-04, 5.434790e-05, -4.703962e-05, -9.782384e-05, -8.809368e-05, -1.895480e-05, 9.779982e-05, 2.419264e-04, 3.884508e-04, 5.121900e-04, 5.922566e-04, 6.157399e-04, 5.799175e-04, 4.926179e-04, 3.706924e-04, 2.368926e-04, 1.157315e-04, 2.908007e-05, -7.710197e-06, 1.152902e-05, 8.279328e-05, 1.927469e-04, 3.212226e-04, 4.449118e-04, 5.415712e-04, 5.939872e-04, 5.929925e-04, 5.390065e-04, 4.418436e-04, 3.188433e-04, 1.916797e-04, 8.243429e-05, 9.645695e-06, -1.495803e-05, 1.153094e-05, 8.279274e-05, 1.845270e-04, 2.971112e-04, 3.991773e-04, 4.714554e-04, 5.001942e-04, 4.795522e-04, 4.125441e-04, 3.103929e-04, 1.904224e-04, 7.288625e-05, -2.268711e-05, -8.097318e-05, -9.353447e-05, -6.023841e-05, 1.082739e-05, 1.049082e-04, 2.033069e-04, 2.867794e-04, 3.389832e-04, 3.493637e-04, 3.149693e-04, 2.408829e-04, 1.392130e-04, 2.684097e-05, -7.765507e-05, -1.573403e-04, -1.999262e-04, -1.999040e-04, -1.594391e-04, -8.788167e-05, 1.533880e-18, 8.673179e-05, 1.552941e-04, 1.921593e-04, 1.896660e-04, 1.473125e-04, 7.175446e-05, -2.447692e-05, -1.252903e-04, -2.139551e-04, -2.760981e-04, -3.022396e-04, -2.894208e-04, -2.416447e-04, -1.690669e-04, -8.609788e-05, -8.769674e-06, 4.815140e-05, 7.378744e-05, 6.304153e-05, 1.743167e-05, -5.526866e-05, -1.425031e-04, -2.292400e-04, -3.006911e-04, -3.449507e-04, -3.550830e-04, -3.302943e-04, -2.759909e-04, -2.027289e-04, -1.242577e-04, -5.502014e-05, -7.562393e-06, 9.681284e-06, -6.161054e-06, -5.196267e-05, -1.192397e-04, -1.957410e-04, -2.676898e-04, -3.222664e-04, -3.498862e-04, -3.458678e-04, -3.112023e-04, -2.522982e-04, -1.797621e-04, -1.064461e-04, -4.512184e-05, -6.200577e-06, 4.092150e-06, -1.523094e-05, -5.981729e-05, -1.208284e-04, -1.865830e-04, -2.446854e-04, -2.842511e-04, -2.978308e-04, -2.826944e-04, -2.412526e-04, -1.805547e-04, -1.109651e-04, -4.426595e-05, 8.465996e-06, 3.882656e-05, 4.254541e-05, 2.018803e-05, -2.301618e-05, -7.817653e-05, -1.343832e-04, -1.806867e-04, -2.080550e-04, -2.109613e-04, -1.883212e-04, -1.436235e-04, -8.424225e-05, -2.006468e-05, 3.830998e-05, 8.147238e-05, 1.028647e-04, 9.990894e-05, 7.440730e-05, 3.215517e-05, -1.815405e-05, -6.652518e-05, -1.034667e-04, -1.216794e-04, -1.173288e-04, -9.067921e-05, -4.598760e-05, 9.315347e-06, 6.599807e-05, 1.147025e-04, 1.476159e-04, 1.598423e-04, 1.502322e-04, 1.215308e-04, 7.982922e-05, 3.342565e-05, -8.689939e-06, -3.845202e-05, -5.014624e-05, -4.139478e-05, -1.353102e-05, 2.869411e-05, 7.801175e-05, 1.259707e-04, 1.644637e-04, 1.871699e-04, 1.906552e-04, 1.749423e-04, 1.434528e-04, 1.023452e-04, 5.937352e-05, 2.247835e-05, -1.633196e-06, -8.665975e-06, 2.533592e-06, 2.981996e-05, 6.818238e-05, 1.106837e-04, 1.497285e-04, 1.784298e-04, 1.918273e-04, 1.877438e-04, 1.671312e-04, 1.338526e-04, 9.394808e-05, 5.452364e-05, 2.246654e-05, 3.220123e-06, -1.647761e-07, 1.246344e-05, 3.837581e-05, 7.249536e-05, 1.083405e-04, 1.392044e-04, 1.593563e-04, 1.650495e-04, 1.551603e-04, 1.313478e-04, 9.771527e-05, 6.004045e-05, 2.471891e-05, -2.386133e-06, -1.698106e-05, -1.708264e-05, -3.334938e-06, 2.114761e-05, 5.137554e-05, 8.140496e-05, 1.054140e-04, 1.187404e-04, 1.186964e-04, 1.050177e-04, 7.987352e-05, 4.744223e-05, 1.313471e-05, -1.738958e-05, -3.923556e-05, -4.913327e-05, -4.599501e-05, -3.107445e-05, -7.705512e-06, 1.932583e-05, 4.465886e-05, 6.332428e-05, 7.162520e-05, 6.777744e-05, 5.219844e-05, 2.739887e-05, -2.497489e-06, -3.251413e-05, -5.772246e-05, -7.411983e-05, -7.932868e-05, -7.299486e-05, -5.681887e-05, -3.422013e-05, -9.699824e-06, 1.197918e-05, 2.664641e-05, 3.145883e-05, 2.538779e-05, 9.374706e-06, -1.386705e-05, -4.036323e-05, -6.560685e-05, -8.537011e-05, -9.645414e-05, -9.724365e-05, -8.797073e-05, -7.064520e-05, -4.866891e-05, -2.620782e-05, -7.437253e-06, 4.202968e-06, 6.610938e-06, -6.226126e-07, -1.616681e-05, -3.721416e-05, -6.000349e-05, -8.050507e-05, -9.514351e-05, -1.014288e-04, -9.838473e-05, -8.670047e-05, -6.858382e-05, -4.734512e-05, -2.679111e-05, -1.053890e-05, -1.373927e-06, -7.653509e-07, -8.623252e-06, -2.333726e-05, -4.208573e-05, -6.135649e-05, -7.758334e-05, -8.778312e-05, -9.007996e-05, -8.402476e-05, -7.065576e-05, -5.229328e-05, -3.210856e-05, -1.354690e-05, 2.901695e-07, 7.193077e-06, 6.225946e-06, -2.123854e-06, -1.605190e-05, -3.277628e-05, -4.904700e-05, -6.173209e-05, -6.837512e-05, -6.762506e-05, -5.946355e-05, -4.519168e-05, -2.718172e-05, -8.441023e-06, 7.931932e-06, 1.930099e-05, 2.395657e-05, 2.140913e-05, 1.246154e-05, -9.497732e-07, -1.611393e-05, -3.003854e-05, -3.998717e-05, -4.396490e-05, -4.106624e-05, -3.162489e-05, -1.714075e-05, 1.363182e-18, 1.696002e-05, 3.096154e-05, 3.978114e-05, 4.214045e-05, 3.792431e-05, 2.818925e-05, 1.496298e-05, 8.726780e-07, -1.132998e-05, -1.926134e-05, -2.132797e-05, -1.700396e-05, -6.915186e-06, 7.282560e-06, 2.320813e-05, 3.818626e-05, 4.972749e-05, 5.597097e-05, 5.601131e-05, 5.005240e-05, 3.936199e-05, 2.603695e-05, 1.262229e-05, 1.653235e-06, -4.797665e-06, -5.487465e-06, -2.191591e-07, 1.013018e-05, 2.377317e-05, 3.833727e-05, 5.129233e-05, 6.040360e-05, 6.412924e-05, 6.189186e-05, 5.417617e-05, 4.243663e-05, 2.883232e-05, 1.583737e-05, 5.797190e-06, 5.097362e-07, 9.065930e-07, 6.890236e-06, 1.735585e-05, 3.039300e-05, 4.363053e-05, 5.466236e-05, 6.147812e-05, 6.282155e-05, 5.841297e-05, 4.899652e-05]


	#filt1 = gr.fir_filter_fff(1, band_pass_coeffs)
	filt2 = gr.fir_filter_fff(1, high_pass_coeffs)
	filt1 = gr.fir_filter_fff(1, matlab_taps)
	#dc_blocker = gr.dc_blocker_cc(2000)

	to_complex = gr.float_to_complex()
        amp = gr.multiply_const_ff(32767)
       	audio_sink = audio.sink (48000)

        to_mag = gr.complex_to_mag()
	to_complex_2 = gr.float_to_complex()
	to_complex_3 = gr.float_to_complex()
	scale= gr.multiply_const_ff(1)
	#to_complex_3 = gr.float_to_complex()

	#agc = gr.agc_cc(1e-4, 1, 1, .100)
	#agc = gr.feedforward_agc_cc(100,1)
	agc = gr.agc_ff(.09e-4, .1, 1)
        self.qapp = QtGui.QApplication(sys.argv)

	fftsize=2048

	self.snk = qtgui.sink_f(fftsize, gr.firdes.WIN_BLACKMAN_hARRIS)


	self.connect(sig, amp, to_complex,tx)
      	#self.connect(rx, to_mag, filt_decimate, filt1, agc, audio_sink)
	self.connect(rx, to_mag, filt_decimate, filt1, agc,audio_sink)
	self.connect(agc, self.snk)
	#self.connect(rx, to_mag, filt_decimate, filt1)
        #self.connect(filt1, to_complex_2, out1)
	self.connect(agc, to_complex_2, out3)
	self.connect(filt1, to_complex_3,out1)
	self.connect(rx, out2)
	#self.connect(filt1, to_mag, audio_sink)

# Tell the sink we want it displayed
	self.pyobj = sip.wrapinstance(self.snk.pyqwidget(), QtGui.QWidget)
       	self.pyobj.show()

def main():

    tb = my_top_block()

    tb.start()
    tb.qapp.exec_()

    while 1:

        c = raw_input("'Q' to quit. L to get log.\n")
        if c == "q":
            break

    tb.stop()

if __name__ == '__main__':
    main()
