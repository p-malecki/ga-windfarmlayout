import matplotlib.pyplot as plt


def plot_turbine_layout(coordinates):
    """Plot the turbine layout based on the given coordinates."""
    x_coordinates = [coord[0] for coord in coordinates]
    y_coordinates = [coord[1] for coord in coordinates]
    plt.figure()
    plt.scatter(x_coordinates, y_coordinates, marker='x', color='b')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Turbine Layout')
    plt.grid(True)
    plt.show()


def plot_population_layouts(population):
    """Plot the turbine layouts of the entire population."""
    plt.figure()
    for i, layout in enumerate(population):
        x_coordinates = [coord[0] for coord in layout]
        y_coordinates = [coord[1] for coord in layout]
        plt.scatter(x_coordinates, y_coordinates, marker='x', label=f'Layout {i+1}')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Turbine Layouts of Population')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.show()


def plot_roulette_wheel(probabilities):
    """Plot a roulette wheel to visualize the selection probabilities."""
    fig, ax = plt.subplots()
    ax.axis('equal')
    wedges, texts, autotexts = ax.pie(probabilities, startangle=90, autopct='%1.1f%%', colors=plt.cm.tab20.colors)
    labels = ['Layout {}'.format(i + 1) for i in range(len(probabilities))]
    ax.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title('Roulette Wheel Selection Probabilities')
    plt.show()