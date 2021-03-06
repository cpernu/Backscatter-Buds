EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 4
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
NoConn ~ 6100 3550
NoConn ~ 6100 3650
NoConn ~ 6100 3750
Text GLabel 2350 4850 2    50   Input ~ 0
Vreg
Text GLabel 3350 5150 0    50   Input ~ 0
Vreg
Text GLabel 2650 4650 1    50   Input ~ 0
Vreg
$Comp
L Device:R_US R?
U 1 1 62066369
P 2650 4800
AR Path="/62066369" Ref="R?"  Part="1" 
AR Path="/61ABB238/62066369" Ref="R?"  Part="1" 
AR Path="/61D68702/62066369" Ref="R6"  Part="1" 
F 0 "R6" H 2718 4846 50  0000 L CNN
F 1 "47k" H 2718 4755 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 2690 4790 50  0001 C CNN
F 3 "~" H 2650 4800 50  0001 C CNN
	1    2650 4800
	1    0    0    -1  
$EndComp
$Comp
L TPS780270200DDCT:TPS780270200DDCT U4
U 1 1 620757C2
P 7750 1200
F 0 "U4" H 9050 1587 60  0000 C CNN
F 1 "TPS780270200DDCT" H 9050 1481 60  0000 C CNN
F 2 "Local Components:TPS780270200DDCT" H 9050 1440 60  0001 C CNN
F 3 "" H 7750 1200 60  0000 C CNN
	1    7750 1200
	1    0    0    -1  
$EndComp
$Comp
L SI1016X-T1-GE3:SI1016X-T1-GE3 U3
U 1 1 620761BD
P 2950 1400
F 0 "U3" H 3750 1887 60  0000 C CNN
F 1 "SI1016X-T1-GE3" H 3750 1781 60  0000 C CNN
F 2 "Local Components:SI1016X-T1-GE3" H 3750 1740 60  0001 C CNN
F 3 "" H 2950 1400 60  0000 C CNN
	1    2950 1400
	1    0    0    -1  
$EndComp
Text GLabel 2950 5550 3    50   Input ~ 0
Vreg
Text GLabel 8650 5450 2    50   Input ~ 0
SPK_EN
$Comp
L Device:C C?
U 1 1 62047C78
P 2950 5400
AR Path="/62047C78" Ref="C?"  Part="1" 
AR Path="/61ABB238/62047C78" Ref="C?"  Part="1" 
AR Path="/61D68702/62047C78" Ref="C10"  Part="1" 
F 0 "C10" H 3065 5446 50  0000 L CNN
F 1 "0.01uF" H 3065 5355 50  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2988 5250 50  0001 C CNN
F 3 "~" H 2950 5400 50  0001 C CNN
	1    2950 5400
	-1   0    0    1   
$EndComp
Wire Wire Line
	2950 5250 2850 5250
$Comp
L power:GND #PWR0120
U 1 1 62045215
P 2850 5250
F 0 "#PWR0120" H 2850 5000 50  0001 C CNN
F 1 "GND" H 2855 5077 50  0000 C CNN
F 2 "" H 2850 5250 50  0001 C CNN
F 3 "" H 2850 5250 50  0001 C CNN
	1    2850 5250
	0    1    1    0   
$EndComp
Connection ~ 2650 4950
Wire Wire Line
	2650 4950 2350 4950
Connection ~ 2950 5250
$Comp
L power:GND #PWR0123
U 1 1 6208E3CB
P 2900 1400
F 0 "#PWR0123" H 2900 1150 50  0001 C CNN
F 1 "GND" H 2905 1227 50  0000 C CNN
F 2 "" H 2900 1400 50  0001 C CNN
F 3 "" H 2900 1400 50  0001 C CNN
	1    2900 1400
	0    1    1    0   
$EndComp
Wire Wire Line
	4550 1400 4550 1800
$Comp
L Device:R_US R?
U 1 1 6208F896
P 4750 1800
AR Path="/6208F896" Ref="R?"  Part="1" 
AR Path="/61ABB238/6208F896" Ref="R?"  Part="1" 
AR Path="/61D68702/6208F896" Ref="R13"  Part="1" 
F 0 "R13" H 4818 1846 50  0000 L CNN
F 1 "150k" H 4818 1755 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 4790 1790 50  0001 C CNN
F 3 "~" H 4750 1800 50  0001 C CNN
	1    4750 1800
	0    1    1    0   
$EndComp
Wire Wire Line
	4600 1800 4550 1800
Connection ~ 4550 1800
Wire Wire Line
	4900 1800 5050 1800
Wire Wire Line
	5050 1800 5050 2200
Wire Wire Line
	5050 1800 5250 1800
Connection ~ 5050 1800
Wire Wire Line
	2950 1400 2900 1400
Wire Wire Line
	2950 2200 2450 2200
Wire Wire Line
	2450 2200 2450 2300
$Comp
L Device:R_US R?
U 1 1 62094276
P 2450 2450
AR Path="/62094276" Ref="R?"  Part="1" 
AR Path="/61ABB238/62094276" Ref="R?"  Part="1" 
AR Path="/61D68702/62094276" Ref="R11"  Part="1" 
F 0 "R11" H 2518 2496 50  0000 L CNN
F 1 "10k" H 2518 2405 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 2490 2440 50  0001 C CNN
F 3 "~" H 2450 2450 50  0001 C CNN
	1    2450 2450
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R?
U 1 1 62094C20
P 2450 2850
AR Path="/62094C20" Ref="R?"  Part="1" 
AR Path="/61ABB238/62094C20" Ref="R?"  Part="1" 
AR Path="/61D68702/62094C20" Ref="R12"  Part="1" 
F 0 "R12" H 2518 2896 50  0000 L CNN
F 1 "10k" H 2518 2805 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 2490 2840 50  0001 C CNN
F 3 "~" H 2450 2850 50  0001 C CNN
	1    2450 2850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0125
U 1 1 6209606E
P 2000 2200
F 0 "#PWR0125" H 2000 1950 50  0001 C CNN
F 1 "GND" H 2005 2027 50  0000 C CNN
F 2 "" H 2000 2200 50  0001 C CNN
F 3 "" H 2000 2200 50  0001 C CNN
	1    2000 2200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0132
U 1 1 620968D5
P 2450 3150
F 0 "#PWR0132" H 2450 2900 50  0001 C CNN
F 1 "GND" H 2455 2977 50  0000 C CNN
F 2 "" H 2450 3150 50  0001 C CNN
F 3 "" H 2450 3150 50  0001 C CNN
	1    2450 3150
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R?
U 1 1 62097623
P 2000 1950
AR Path="/62097623" Ref="R?"  Part="1" 
AR Path="/61ABB238/62097623" Ref="R?"  Part="1" 
AR Path="/61D68702/62097623" Ref="R10"  Part="1" 
F 0 "R10" H 2068 1996 50  0000 L CNN
F 1 "10k" H 2068 1905 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 2040 1940 50  0001 C CNN
F 3 "~" H 2000 1950 50  0001 C CNN
	1    2000 1950
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 1800 2950 1800
Wire Wire Line
	2000 2100 2000 2200
Wire Wire Line
	2000 1800 1850 1800
Connection ~ 2000 1800
Text GLabel 1850 1800 0    50   Input ~ 0
MEAS_EN
Text GLabel 2450 2650 0    50   Input ~ 0
VMEAS
Wire Wire Line
	2450 2600 2450 2700
Wire Wire Line
	2450 3000 2450 3150
Text GLabel 5250 1800 2    50   Input ~ 0
Vstore
Text GLabel 7600 1200 0    50   Input ~ 0
Vstore
Text GLabel 10500 1400 2    50   Input ~ 0
SV
Text GLabel 10500 1200 2    50   Input ~ 0
Vreg
Text GLabel 10500 1300 2    50   Input ~ 0
Vstore
$Comp
L Device:C C?
U 1 1 6209EF0F
P 10400 1050
AR Path="/6209EF0F" Ref="C?"  Part="1" 
AR Path="/61ABB238/6209EF0F" Ref="C?"  Part="1" 
AR Path="/61D68702/6209EF0F" Ref="C11"  Part="1" 
F 0 "C11" H 10515 1096 50  0000 L CNN
F 1 "2.2uF" H 10515 1005 50  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 10438 900 50  0001 C CNN
F 3 "~" H 10400 1050 50  0001 C CNN
	1    10400 1050
	1    0    0    -1  
$EndComp
Wire Wire Line
	10350 1200 10400 1200
Wire Wire Line
	10400 1200 10500 1200
Connection ~ 10400 1200
Wire Wire Line
	10500 1300 10350 1300
Wire Wire Line
	10350 1400 10500 1400
Wire Wire Line
	7600 1200 7750 1200
$Comp
L power:GND #PWR0133
U 1 1 620A39F2
P 7600 1300
F 0 "#PWR0133" H 7600 1050 50  0001 C CNN
F 1 "GND" H 7605 1127 50  0000 C CNN
F 2 "" H 7600 1300 50  0001 C CNN
F 3 "" H 7600 1300 50  0001 C CNN
	1    7600 1300
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0134
U 1 1 620A48E1
P 10400 800
F 0 "#PWR0134" H 10400 550 50  0001 C CNN
F 1 "GND" H 10405 627 50  0000 C CNN
F 2 "" H 10400 800 50  0001 C CNN
F 3 "" H 10400 800 50  0001 C CNN
	1    10400 800 
	-1   0    0    1   
$EndComp
Wire Wire Line
	10400 800  10400 900 
Wire Wire Line
	7750 1300 7600 1300
Wire Wire Line
	5050 2200 4550 2200
Text GLabel 3350 4750 0    50   Input ~ 0
SV
Text GLabel 8550 4950 2    50   Input ~ 0
MEAS_EN
Text GLabel 8650 5350 2    50   Input ~ 0
AN_EN
Text Notes 6200 2400 0    50   ~ 0
Use QFN Package of some sort for small size and hand-soldering\n
Text GLabel 8650 4850 2    50   Input ~ 0
VMEAS
Text Notes 3500 3750 0    50   ~ 0
Double check clock and Audio enabole output so you can use it for switching\n\n
$Comp
L power:GND #PWR0122
U 1 1 62054400
P 2350 5550
F 0 "#PWR0122" H 2350 5300 50  0001 C CNN
F 1 "GND" H 2355 5377 50  0000 C CNN
F 2 "" H 2350 5550 50  0001 C CNN
F 3 "" H 2350 5550 50  0001 C CNN
	1    2350 5550
	-1   0    0    1   
$EndComp
Wire Wire Line
	2000 5750 1650 5750
$Comp
L Device:R_US R?
U 1 1 61AA3251
P 8300 4950
AR Path="/61AA3251" Ref="R?"  Part="1" 
AR Path="/61ABB238/61AA3251" Ref="R?"  Part="1" 
AR Path="/61D68702/61AA3251" Ref="R17"  Part="1" 
F 0 "R17" H 8368 4996 50  0000 L CNN
F 1 "0" H 8368 4905 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 8340 4940 50  0001 C CNN
F 3 "~" H 8300 4950 50  0001 C CNN
	1    8300 4950
	0    -1   -1   0   
$EndComp
$Comp
L Device:R_US R?
U 1 1 61AA3A0E
P 8400 5450
AR Path="/61AA3A0E" Ref="R?"  Part="1" 
AR Path="/61ABB238/61AA3A0E" Ref="R?"  Part="1" 
AR Path="/61D68702/61AA3A0E" Ref="R18"  Part="1" 
F 0 "R18" H 8468 5496 50  0000 L CNN
F 1 "0" H 8468 5405 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 8440 5440 50  0001 C CNN
F 3 "~" H 8400 5450 50  0001 C CNN
	1    8400 5450
	0    -1   -1   0   
$EndComp
$Comp
L Device:R_US R?
U 1 1 61AA4135
P 8400 5350
AR Path="/61AA4135" Ref="R?"  Part="1" 
AR Path="/61ABB238/61AA4135" Ref="R?"  Part="1" 
AR Path="/61D68702/61AA4135" Ref="R19"  Part="1" 
F 0 "R19" H 8468 5396 50  0000 L CNN
F 1 "0" H 8468 5305 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 8440 5340 50  0001 C CNN
F 3 "~" H 8400 5350 50  0001 C CNN
	1    8400 5350
	0    -1   -1   0   
$EndComp
$Comp
L Device:R_US R?
U 1 1 61AA4C6A
P 3600 4750
AR Path="/61AA4C6A" Ref="R?"  Part="1" 
AR Path="/61ABB238/61AA4C6A" Ref="R?"  Part="1" 
AR Path="/61D68702/61AA4C6A" Ref="R16"  Part="1" 
F 0 "R16" H 3668 4796 50  0000 L CNN
F 1 "0" H 3668 4705 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 3640 4740 50  0001 C CNN
F 3 "~" H 3600 4750 50  0001 C CNN
	1    3600 4750
	0    1    1    0   
$EndComp
$Comp
L Device:R_US R?
U 1 1 61AA55F0
P 8400 4850
AR Path="/61AA55F0" Ref="R?"  Part="1" 
AR Path="/61ABB238/61AA55F0" Ref="R?"  Part="1" 
AR Path="/61D68702/61AA55F0" Ref="R15"  Part="1" 
F 0 "R15" H 8468 4896 50  0000 L CNN
F 1 "0" H 8468 4805 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 8440 4840 50  0001 C CNN
F 3 "~" H 8400 4850 50  0001 C CNN
	1    8400 4850
	0    1    1    0   
$EndComp
$Comp
L Device:R_US R?
U 1 1 61AA5E43
P 3600 5150
AR Path="/61AA5E43" Ref="R?"  Part="1" 
AR Path="/61ABB238/61AA5E43" Ref="R?"  Part="1" 
AR Path="/61D68702/61AA5E43" Ref="R14"  Part="1" 
F 0 "R14" H 3668 5196 50  0000 L CNN
F 1 "0" H 3668 5105 50  0000 L CNN
F 2 "Resistor_SMD:R_0201_0603Metric_Pad0.64x0.40mm_HandSolder" V 3640 5140 50  0001 C CNN
F 3 "~" H 3600 5150 50  0001 C CNN
	1    3600 5150
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8150 4850 8250 4850
Wire Wire Line
	8550 4850 8650 4850
Wire Wire Line
	3350 5150 3450 5150
Wire Wire Line
	3750 5150 3850 5150
Wire Wire Line
	3350 4750 3450 4750
Wire Wire Line
	8250 5250 8150 5250
Wire Wire Line
	8450 4950 8550 4950
Wire Wire Line
	8650 5450 8550 5450
Wire Wire Line
	8250 5450 8150 5450
Wire Wire Line
	8550 5350 8650 5350
Wire Wire Line
	8250 5350 8150 5350
$Comp
L MSP430FR2100IPW16:MSP430FR2100IPW16 IC2
U 1 1 61ADF04D
P 3850 4750
F 0 "IC2" H 6000 5015 50  0000 C CNN
F 1 "MSP430FR2100IPW16" H 6000 4924 50  0000 C CNN
F 2 "Local Components:MSP430FR2100IPW16" H 8000 4850 50  0001 L CNN
F 3 "http://www.ti.com/lit/gpn/MSP430FR2100" H 8000 4750 50  0001 L CNN
F 4 "16 MHz Ultra-Low-Power Microcontroller With 1 KB FRAM, 0.5 KB SRAM, 12 IO, 8 ch 10-bit ADC" H 8000 4650 50  0001 L CNN "Description"
F 5 "1.2" H 8000 4550 50  0001 L CNN "Height"
F 6 "Texas Instruments" H 8000 4450 50  0001 L CNN "Manufacturer_Name"
F 7 "MSP430FR2100IPW16" H 8000 4350 50  0001 L CNN "Manufacturer_Part_Number"
F 8 "595-SP430FR2100IPW16" H 8000 4250 50  0001 L CNN "Mouser Part Number"
F 9 "https://www.mouser.co.uk/ProductDetail/Texas-Instruments/MSP430FR2100IPW16?qs=EU6FO9ffTwedZw%2FN%252B0l%2FEA%3D%3D" H 8000 4150 50  0001 L CNN "Mouser Price/Stock"
F 10 "MSP430FR2100IPW16" H 8000 4050 50  0001 L CNN "Arrow Part Number"
F 11 "https://www.arrow.com/en/products/msp430fr2100ipw16/texas-instruments?region=nac" H 8000 3950 50  0001 L CNN "Arrow Price/Stock"
	1    3850 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 5850 2000 5750
$Comp
L Device:Crystal Y1
U 1 1 62052029
P 1650 5900
F 0 "Y1" V 1604 6031 50  0000 L CNN
F 1 "Crystal" V 1695 6031 50  0000 L CNN
F 2 "Local Components:32k_crystal" H 1650 5900 50  0001 C CNN
F 3 "~" H 1650 5900 50  0001 C CNN
	1    1650 5900
	0    1    1    0   
$EndComp
Connection ~ 2350 5950
Connection ~ 2350 5850
Wire Wire Line
	2350 5850 3600 5850
$Comp
L power:GND #PWR0121
U 1 1 62053CD2
P 2350 6250
F 0 "#PWR0121" H 2350 6000 50  0001 C CNN
F 1 "GND" H 2355 6077 50  0000 C CNN
F 2 "" H 2350 6250 50  0001 C CNN
F 3 "" H 2350 6250 50  0001 C CNN
	1    2350 6250
	1    0    0    -1  
$EndComp
Wire Wire Line
	2100 5950 2350 5950
Wire Wire Line
	2100 6050 2100 5950
Wire Wire Line
	1650 6050 2100 6050
Wire Wire Line
	2350 5850 2000 5850
$Comp
L Device:C C?
U 1 1 6205189A
P 2350 6100
AR Path="/6205189A" Ref="C?"  Part="1" 
AR Path="/61ABB238/6205189A" Ref="C?"  Part="1" 
AR Path="/61D68702/6205189A" Ref="C9"  Part="1" 
F 0 "C9" H 2465 6146 50  0000 L CNN
F 1 "0pF" H 2465 6055 50  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2388 5950 50  0001 C CNN
F 3 "~" H 2350 6100 50  0001 C CNN
	1    2350 6100
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 620514FC
P 2350 5700
AR Path="/620514FC" Ref="C?"  Part="1" 
AR Path="/61ABB238/620514FC" Ref="C?"  Part="1" 
AR Path="/61D68702/620514FC" Ref="C8"  Part="1" 
F 0 "C8" H 2465 5746 50  0000 L CNN
F 1 "0pF" H 2465 5655 50  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2388 5550 50  0001 C CNN
F 3 "~" H 2350 5700 50  0001 C CNN
	1    2350 5700
	1    0    0    1   
$EndComp
Wire Wire Line
	2950 5250 3850 5250
Wire Wire Line
	3600 5350 3850 5350
Wire Wire Line
	3600 5850 3600 5350
Wire Wire Line
	3850 5950 3850 5450
Wire Wire Line
	2350 5950 3850 5950
Wire Wire Line
	2650 4950 3850 4950
Wire Wire Line
	2350 5050 3850 5050
$Comp
L power:GND #PWR0124
U 1 1 6206735D
P 2400 5150
F 0 "#PWR0124" H 2400 4900 50  0001 C CNN
F 1 "GND" H 2405 4977 50  0000 C CNN
F 2 "" H 2400 5150 50  0001 C CNN
F 3 "" H 2400 5150 50  0001 C CNN
	1    2400 5150
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x04 J1
U 1 1 62062738
P 2150 5050
F 0 "J1" H 2230 5042 50  0000 L CNN
F 1 "Conn_01x04" H 2230 4951 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 2150 5050 50  0001 C CNN
F 3 "~" H 2150 5050 50  0001 C CNN
	1    2150 5050
	-1   0    0    1   
$EndComp
Wire Wire Line
	2400 5150 2350 5150
Wire Wire Line
	8150 4750 8250 4750
Wire Wire Line
	3750 4750 3850 4750
$EndSCHEMATC
