import HYPF2D as C
import HYPF2D_Iter as CC
import sys
import time

hyp0 = "../files/hyp/SampleAD-01.HYP"
csv0 = "../files/csv/SampleAD-01.csv"
o0 = "../files/output/SampleAD-01.csv"
pn0 = ['VCC_IO', 'VCC_SYS', 'VCC_DDR', 'VCC_BAT+', 'VCC50_USB', 'VDD_LOG', 'GND', 'VDD_CPU', 'VCC18_DDR', 'VDD_GPU', 'LCD_VBAT', 'VADP', 'PA_5V', 'VCC_FLASH', 'VCC50_BOOST', 'VCC_LCD', 'VCC_WL', 'VCC18_DVP', 'VCC_18', 'VCC_SD', 'VCC_TP', 'VCCA_CODEC', 'VCCIO_PMU', 'VDDA_18', 'VREFAO_DDR1', 'VDD10_LCD', 'VDD_LOG','VDD_GPU', 'VDD_CPU', 'VDD_10']

hyp1 = "../files/hyp/AD8367_VGA.HYP"
csv1 = "../files/csv/AD8367_VGA.csv"
o1 = "../files/output/AD8367_VGA.csv"
pn1 = ['GND', 'DGND', '5V']

hyp2 = "../files/hyp/SampleAD-02.HYP"
csv2 = "../files/csv/SampleAD-02.csv"
o2 = "../files/output/SampleAD-02.csv"
pn2 = ['GND', 'DVDD+3.3V', 'DVDD+1.5V', 'DV+24V', 'VCCINT', 'VMGTAVTT', 'DVDD+1.2V', 'DVDD+2.5V', 'D+4.5V', 'SI_5388_3.3V', 'VTTDDR', 'VCCAUX', 'VTTVREF', 'VMGTAVCC', 'GTXCLK_GND', 'DV+2.8V', '+3.3VA_VCCT', '+3.3VA_VCCR', 'ANALOG+3.8V', 'VMGTVCCAUX','DIGITAL+3.8V', 'AGND', 'AV+4.5V', 'DV+24VIN']

hyp3 = "../files/hyp/SampleAD-03.HYP"
csv3 = "../files/csv/SampleAD-03.csv"
o3 = "../files/output/SampleAD-03.csv"
pn3 = ['VCC_1V0', 'VCC_1V8', 'VCC_3V3', 'VCC_INT', 'VCCPLL','+2V5_VREF_ISO', '+3V3_ISO', '+3V3', '+5VE', '+5V', '+15V_ISO', '+15V', 'GND']

hyp4 = "../files/hyp/EP2C5T144C8.HYP"
csv4 = "../files/csv/EP2C5T144C8.csv"
o4 = "../files/output/EP2C5T144C8.csv"
pn4 = ['+1.2', '+3.3', '+5', 'GND']

hyp5 = "../files/HYP2/demo2.hyp"
csv5 = "../files/HYP2/demo2.csv"
o5 = "../files/HYP2/output/demo2.csv"
pn5 = ['gnd', 'vcc']

hyp6 = "../files/HYP2/mainboard.hyp"
csv6 = "../files/HYP2/mainborad.csv"
o6 = "../files/HYP2/output/mainboard.csv"
pn6 = ['VCC', 'GND']

hyp7 = "../files/HYP2/mt18vddt6472ag-265c4.hyp"
csv7 = "../files/HYP2/mt18vddt6472ag-265c4.csv"
o7 = "../files/HYP2/output/mt18vddt6472ag-265c4.csv"
pn7 = ['VCC', 'VREF', 'GND']

hypPath = hyp0
csvPath = csv0
outputPath = o0
planeNames = pn0

begin = time.time()
CC.readHYP2File(hypPath, csvPath, outputPath, planeNames)
end = time.time()
print('read file time:', end - begin)

pins = CC.getActiveAndNegtivePins(csvPath)
num = 0
for key in pins:
    if pins.get(key) == 1:
        num += 1
print(num)
# segs, aPins, nPins = CC.getSegsAndPins(hypPath, csvPath)
# models = CC.findAllAPinPath(segs, aPins, nPins)

# print(len(segs), len(aPins), len(nPins))
# for idx, seg in enumerate(segs):
#     if idx > 100:
#         break
#     print(segs.get(seg))
# print(aPins)
# print(nPins)
