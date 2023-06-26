import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider, Slider, Button
from tkinter import Tk, filedialog
from scipy.signal import find_peaks
from GetValidImages import copy_images

class GetPeaksAndTroughs:
    def __init__(self, data, img_source_path="", prox_threshold = 10):
        self.data = data
        self.filtered_data = data
        self.img_source_path = img_source_path
        self.peaks = []
        self.troughs = []

        self.left_peak_index = 0
        self.right_peak_index = len(data) - 1
        self.left_trough_index = 0
        self.right_trough_index = len(data) - 1

        self.lowestVal = np.floor(min(data['y']))
        self.highestVal = np.ceil(max(data['y']))

        midpt = (self.lowestVal + self.highestVal) // 2

        self.peak_cut_off = midpt
        self.trough_cut_off = midpt
        self.prox_threshold = prox_threshold

        # Plot parameters
        self.fig, self.ax = plt.subplots( figsize=(10, 6))

        self.peak_slider_ax = self.fig.add_axes([0.2, 0.95, 0.6, 0.03])
        self.trough_slider_ax = self.fig.add_axes([0.2, 0.9, 0.6, 0.03])
        self.peak_cut_off_slider_ax = self.fig.add_axes([0.92, 0.2, 0.01, 0.6])
        self.trough_cut_off_slider_ax = self.fig.add_axes([0.96, 0.2, 0.01, 0.6])

        self.save_button_ax = self.fig.add_axes([0.9, 0.93, 0.08, 0.04])
        self.save_button = Button(self.save_button_ax, 'Save Data', hovercolor='0.975')
        self.save_button.on_clicked(self.save)

        # self.peak_slider = Slider(self.peak_slider_ax, 'Peaks', 0, 180, valinit=90, valstep=1)
        self.trough_slider = None
        self.trough_cut_off_slider = None

        self.slider_trough_bool = False
        self.slider_peak_bool = False

        self.fig.canvas.mpl_connect('button_release_event', self.on_button_release)

    def find_peaks_and_troughs(self, initial=False):
        y = self.data['y']
        peaks, _ = find_peaks(y)
        troughs, _ = find_peaks(-y)

        self.peaks = self.filter_peaks(peaks, y, initial=initial)
        self.troughs = self.filter_troughs(troughs, y, initial=initial)

    def filter_peaks(self, peaks, elev_values, initial=False):
        filtered_peaks = []
        last_index = None
        cutoff = self.peak_cut_off
        prox_threshold = self.prox_threshold
        if initial:
            cutoff = self.lowestVal
            prox_threshold = 0
        for index in peaks:
            if last_index is None or index - last_index > prox_threshold:
                if elev_values[index] > cutoff:
                    filtered_peaks.append(index)
                last_index = index
            elif elev_values[index] > elev_values[last_index]:
                filtered_peaks.pop()  # Remove the last peak if the current peak is higher
                filtered_peaks.append(index)
                last_index = index
        return filtered_peaks

    def filter_troughs(self, troughs, elev_values, initial=False):
        filtered_troughs = []
        last_index = None
        cutoff = self.trough_cut_off
        prox_threshold = self.prox_threshold
        if initial:
            cutoff = self.highestVal
            prox_threshold = 0
        for index in troughs:
            if last_index is None or index - last_index > prox_threshold:
                if elev_values[index] < cutoff:
                    filtered_troughs.append(index)
                last_index = index
            elif elev_values[index] < elev_values[last_index]:
                filtered_troughs.pop()  # Remove the last trough if the current trough is lower
                filtered_troughs.append(index)
                last_index = index
        return filtered_troughs

    
    def on_button_release(self, event):
        if event.button == 1 and self.slider_peak_bool:
            # Find peaks and troughs
            # self.peak_cut_off = int(self.peak_cut_off_slider.val)
            self.find_peaks_and_troughs()
            self.slider_peak_bool = False
            self.plot_filtered_data(self.ax)

        elif event.button == 1 and self.slider_trough_bool:
            # Find peaks and troughs
            # self.trough_cut_off = int(self.trough_cut_off_slider.val)
            self.find_peaks_and_troughs()
            self.update_range_troughs(self.trough_slider.val)
            self.slider_trough_bool = False
            self.plot_filtered_data(self.ax)

    def create_sliders(self):
        line, = self.ax.plot(self.data['x'], self.data['y'], label='Signal')

        # Find peaks and troughs
        self.find_peaks_and_troughs(initial=False)

        # Calculate the number of peaks and troughs
        num_peaks = len(self.peaks)
        num_troughs = len(self.troughs)

        self.peak_slider = RangeSlider(self.peak_slider_ax, 'Peaks', 0, num_peaks, valinit=(0, num_peaks), valstep=1)
        self.trough_slider = RangeSlider(self.trough_slider_ax, 'Troughs', 0, num_troughs, valinit=(0, num_troughs), valstep=1)

        self.peak_cut_off_slider = Slider(self.peak_cut_off_slider_ax, 'Peak\nCutoff', self.lowestVal, self.highestVal, valinit=self.peak_cut_off, valstep=1, orientation='vertical')
        self.trough_cut_off_slider = Slider(self.trough_cut_off_slider_ax, 'Trough\nCutoff', self.lowestVal, self.highestVal, valinit=self.trough_cut_off, valstep=1, orientation='vertical')
        
        self.peak_cut_off_slider.on_changed(self.update_peak_cut_off)
        self.trough_cut_off_slider.on_changed(self.update_trough_cut_off)
        
        self.peak_slider.on_changed(self.update_range_peaks)
        self.trough_slider.on_changed(self.update_range_troughs)
        self.plot_filtered_data(self.ax)
        plt.show()
    
    def update_peak_cut_off(self, val):
        self.slider_peak_bool = True
        self.peak_cut_off = int(self.peak_cut_off_slider.val)
        self.plot_filtered_data(self.ax)
    
    def update_trough_cut_off(self, val):
        self.slider_trough_bool = True
        self.trough_cut_off = int(self.trough_cut_off_slider.val)
        self.plot_filtered_data(self.ax)

    def update_range_peaks(self, val):
        self.left_peak_index = int(self.peak_slider.val[0])
        self.right_peak_index = int(self.peak_slider.val[1])
        self.plot_filtered_data(self.ax)

    def update_range_troughs(self, val):
        self.left_trough_index = int(self.trough_slider.val[0])
        self.right_trough_index = int(self.trough_slider.val[1])
        self.plot_filtered_data(self.ax)

    def plot_filtered_data(self, ax):
        ax.clear()
        ax.plot(self.data['x'], self.data['y'], label='Signal')

        filtered_peaks = self.peaks[self.left_peak_index:self.right_peak_index]
        filtered_troughs = self.troughs[self.left_trough_index:self.right_trough_index]
        # print(f'TROUGHS: {filtered_troughs}')

        start_index = filtered_troughs[0]
        end_index = filtered_troughs[-1]
        self.filtered_data = self.data.iloc[start_index:end_index]
        print(f'{self.filtered_data.head()}')


        ax.plot(self.data['x'][filtered_peaks], self.data['y'][filtered_peaks], 'ro', label='Filtered Peaks')
        ax.plot(self.data['x'][filtered_troughs], self.data['y'][filtered_troughs], 'bo', label='Filtered Troughs')
        ax.grid()
        # ax.legend()
        plt.draw()

    def save(self, event):
        file_path = filedialog.asksaveasfilename(filetypes=[("Numpy Array", "*.npy")])
        if file_path != "":
            try:
                
                # filtered_data = self.data[(self.data['x'] >= self.data['x'][start_index]) & (self.data['x'] <= self.data['x'][end_index])][['x', 'y']].values
                np.save(file_path, self.filtered_data)
                # remove file extension
                file_path = file_path.split(".")[0]
                print(f'DATA SAVED: {self.filtered_data}')
                print(f'DATA SIZE: {len(self.filtered_data)}')
                print("Data saved successfully.")

                # copy valid images
                if self.img_source_path != "":

                    copy_images(self.filtered_data, self.img_source_path + "images/", self.img_source_path + "modData/images/" )
                    print("Images copied successfully.")
                else:
                    print("No image source path specified.")

                # close the plot
                plt.close()
            except Exception as e:
                print("Error saving data to file:", str(e))

    def run(self):
        self.create_sliders()
        # self.update_range_peaks()
        # self.update_range_troughs()

# Example usage
# data = pd.DataFrame({'x': np.linspace(0, 10, 1000), 'y': 150*np.sin(10*np.linspace(0, 10, 1000))})
# # add a third column to the dataframe
# data['z'] = 150*np.sin(10*np.linspace(0, 10, 1000))
# peaks_troughs = GetPeaksAndTroughs(data)
# peaks_troughs.trough_threshold = -0.5  # Set the trough threshold
# peaks_troughs.run()
