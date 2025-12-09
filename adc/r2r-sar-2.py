import r2r_adc
import time
import adc_plot

voltage_values = []
time_values = []
duration = 3.0
adc = r2r_adc.R2R_ADC(3.2)
try:
    begin = time.time()
    while time.time() - begin < duration:
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(time.time() - begin)
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, 3.2)
    adc_plot.plot_sampling_period_hist(time_values)

finally:
    adc.deinit()