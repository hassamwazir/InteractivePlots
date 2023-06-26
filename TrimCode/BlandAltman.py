import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kstest

def bland_altman_plot(data1, data2, plot_title):
    """
    Draws a Bland-Altman plot to visualize the agreement between two datasets.
    :param data1: DataFrame representing the first dataset
    :param data2: DataFrame representing the second dataset
    :param plot_title: Title of the plot
    """

    xMin = min(data1['y'].min(), data2['y'].min())
    xMax = max(data1['y'].max(), data2['y'].max())

    # Convert DataFrames to numpy arrays
    data1 = data1.to_numpy()
    data2 = data2.to_numpy()

    # Calculate the differences and mean of the two datasets
    diff = data1 - data2
    mean_diff = np.mean(diff)
    median_diff = np.median(diff)
    std_diff = np.std(diff)
    comb = np.concatenate((data1, data2), axis=1)
    elem_mean = np.mean(comb, axis=1)

    # Calculate the percentage differences and mean of the combined data
    pct_diff = (diff / elem_mean) * 100
    pct_comb = np.concatenate((data1, data2), axis=1)
    pct_mean = np.mean(pct_comb, axis=1)
    pct_std = np.std(pct_diff)

    # Calculate IQR and coefficients of reproducibility
    IQR = np.percentile(diff, 75) - np.percentile(diff, 25)
    RPC = 1.96 * std_diff
    RPCnp = IQR * 1.45

    # Perform the Kolmogorov-Smirnov test
    tmp = (diff - mean_diff) / std_diff
    _, p = kstest(tmp, 'norm')

    # Create the plot
    fig, ax = plt.subplots()

    if p < 0.05:
        warning_text = "Data is not normally distributed. Using non-parametric method"
        print(warning_text)

        # Scatter plot with markers
        ax.scatter(elem_mean, diff, marker='o', edgecolors=[0, 0.3, 1], facecolors=[0, 0.5, 1], linewidths=1.5)

        # Horizontal lines
        ax.axhline(0, color='k', linestyle='-')
        ax.axhline(median_diff, color='k', linestyle='--')
        ax.axhline(median_diff + 1.45 * IQR, color='k', linestyle='--')
        ax.axhline(median_diff - 1.45 * IQR, color='k', linestyle='--')

        # Vertical line
        ax.axvline(0, color='k', linestyle='-')

        # Set plot title and axis labels
        ax.set_title(plot_title, fontsize=30)
        ax.set_xlabel('Mean', fontweight='bold', fontsize=30)
        ax.set_ylabel('Difference', fontweight='bold', fontsize=30)

        # Set x-axis limits
        ax.set_xlim([xMin, xMax])

        # Set font size
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        # Text annotations
        txt = f'{round(median_diff, 2)} [Median (M)]'
        ax.text(xMax, median_diff, txt, fontsize=22)
        txt = f'{round(median_diff + 1.45 * IQR, 2)} [M+1.45IQR]'
        ax.text(xMax, median_diff + 1.45 * IQR, txt, fontsize=22)
        txt = f'{round(median_diff - 1.45 * IQR, 2)} [M-1.45IQR]'
        ax.text(xMax, median_diff - 1.45 * IQR, txt, fontsize=22)
        txt = f'RPC: {round(RPCnp, 3)} °'
        ax.text(xMax - 1.0 * (xMax - xMin) / 20, ax.get_ylim()[1] + 0.5, txt, fontweight='bold', fontsize=22)
    else:
        # Scatter plot with markers
        ax.scatter(elem_mean, diff, edgecolors=[0, 0.3, 1], facecolors=[0, 0.5, 1], linewidths=1.5)

        # Horizontal lines
        ax.axhline(0, color='k', linestyle='-')
        ax.axhline(mean_diff, color='k', linestyle='--')
        ax.axhline(mean_diff + 1.96 * std_diff, color='k', linestyle='--')
        ax.axhline(mean_diff - 1.96 * std_diff, color='k', linestyle='--')

        # Vertical line
        ax.axvline(0, color='k', linestyle='-')

        # Set plot title and axis labels
        ax.set_title(plot_title, fontsize=30)
        ax.set_xlabel('Mean', fontweight='bold', fontsize=30)
        ax.set_ylabel('Difference', fontweight='bold', fontsize=30)

        # Set x-axis limits
        ax.set_xlim([xMin, xMax])

        # Set font size
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)

        # Text annotations
        txt = f'{round(mean_diff, 2)} [Mean (M)]'
        ax.text(xMax, mean_diff, txt, fontsize=22)
        txt = f'{round(mean_diff + 1.96 * std_diff, 2)} ° [M+1.96SD]'
        ax.text(xMax, mean_diff + 1.96 * std_diff, txt, fontsize=22)
        txt = f'{round(mean_diff - 1.96 * std_diff, 2)} ° [M-1.96SD]'
        ax.text(xMax, mean_diff - 1.96 * std_diff, txt, fontsize=22)
        txt = f'RPC: {round(RPC, 3)} °'
        ax.text(xMax - 1.0 * (xMax - xMin) / 20, ax.get_ylim()[1] + 0.5, txt, fontweight='bold', fontsize=22)

    # Show the plot
    plt.show()
