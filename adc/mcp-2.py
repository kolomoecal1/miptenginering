import mcp3021_driver
import time
import adc_plot

mcp3021 = mcp3021_driver.MCP3021(5.2, 1)
voltage_values = []
time_values = []
duration = 3.0
try:
    begin = time.time()
    while time.time() - begin < duration:
        voltage_values.append(mcp3021.get_voltage())
        time_values.append(time.time() - begin)
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, 5.2)
    adc_plot.plot_sampling_period_hist(time_values)
finally:
    mcp3021.deinit()