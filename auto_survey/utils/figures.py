import numpy as np
import matplotlib.pyplot as plt

def generate_points(initial_value, final_value, smoothness=0.1, max_num = 200):
    x = np.array([_ for _ in range(max_num)])
    y = initial_value + ( final_value-initial_value) * (x/200)**smoothness
    noise = np.random.normal(0, 0.01, max_num)
    y += noise
    return x, y


def generate_line_plots(data, num_curves, legends, x_label, y_label, save_to = "fig.png" ):
    plt.figure()
    for i in range(num_curves):
        x, y = data[i]
        plt.plot(x , y, label=legends[i])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig(save_to)

def generate_random_figures(list_of_methods, save_to = "fig.png" ):
    num_curves = len(list_of_methods) + 1
    ini_value = [np.random.uniform(1, 2)] * num_curves
    final_value = sorted([0.1 + np.random.normal(0,0.1) for _ in range(num_curves)])

    legends = ["Ours"] + list_of_methods
    x_label = "# of Epochs"
    y_label = "Loss"
    all_data = []
    for i in range(num_curves):
        all_data.append(generate_points(ini_value[i], final_value[i]))

    generate_line_plots(all_data, num_curves, legends, x_label, y_label, save_to)


if __name__ == "__main__":
    num_curves = 3
    legends = ["method 1", "method 2"]
    x_label = "# of epochs"
    y_label = "loss"
    ini_value = [1.5, 1.5, 1.5]
    final_value = [0.01, 0.05, 0.10]

    generate_random_figures(legends, save_to="fig1.png")
    generate_random_figures(legends, save_to="fig2.png")

