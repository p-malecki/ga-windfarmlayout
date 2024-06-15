import matplotlib.pyplot as plt


def plot_turbine_layout(coordinates, title=''):
    x_coordinates = [coord[0] for coord in coordinates]
    y_coordinates = [coord[1] for coord in coordinates]
    plt.figure()
    plt.scatter(x_coordinates, y_coordinates, marker='x', color='b')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Turbine Layout')
    plt.title('Turbine Layout' if not title else title)
    plt.grid(True)
    plt.show()


def plot_multiple_layouts(layouts, title='', alpha_ascending=False, lim=None):
    plt.figure()
    alpha = 1.0 if not alpha_ascending else 0.0
    for i, layout in enumerate(layouts):
        x_coordinates = [coord[0] for coord in layout]
        y_coordinates = [coord[1] for coord in layout]
        if alpha_ascending:
            alpha += 1 / len(layouts)
            alpha = min(alpha, 1)
            plt.scatter(x_coordinates, y_coordinates, marker='x', alpha=min(alpha + 0.5, 1), color=[(alpha, 0, (1-alpha))], label=f'Layout {i+1}')
        else:
            plt.scatter(x_coordinates, y_coordinates, marker='x', label=f'Layout {i+1}')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    if lim:
        plt.xlim(*lim[0])
        plt.ylim(*lim[1])
    plt.title('Layouts of Turbines' if not title else title)
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


def plot_solutions_data_stats(multiple_solution_data, title="", axhline=None):
    plt.figure()
    for i, values in enumerate(multiple_solution_data):
        plt.plot(values, label=f'solution {i+1}')
    plt.title(title)
    if axhline:
        x_range = range(len(multiple_solution_data[0]))
        plt.plot(x_range, [axhline] * len(x_range), color='r', linestyle='--', label=f'value = {axhline}')
    plt.legend(loc='lower right')
    plt.show()


def plot_fitness_over_generations(fitness_values, title):
    plt.figure(figsize=(10, 5))
    plt.plot(fitness_values, 'g-', linewidth=2)
    plt.title(title)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.show()