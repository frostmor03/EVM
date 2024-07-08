import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from generator import uniform_on_interval, normal_on_interval, uniform_vector, normal_vector, uniform_vectors_in_parallelepiped, normal_vectors_in_parallelepiped, uniform_vector_in_circle, normal_vector_in_circle, normal_vector_in_sphere, uniform_vector_in_sphere

def chi_square_uniform_test(data, num_bins, a, b):
    bins, _ = np.histogram(data, bins=num_bins, range=(a, b))
    expected_count = len(data) / num_bins
    chi_square_stat = np.sum((bins - expected_count) ** 2 / expected_count)
    return chi_square_stat

def chi_square_normal_test(data, num_bins, a, b):
    bins, bin_edges = np.histogram(data, bins=num_bins, range=(a, b))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    mean = np.mean(data)
    stddev = np.std(data)
    expected_counts = norm.pdf(bin_centers, loc=mean, scale=stddev) * len(data) * (bin_edges[1] - bin_edges[0])
    chi_square_stat = np.sum((bins - expected_counts) ** 2 / expected_counts)
    return chi_square_stat

def chi_square_test_circular(data, num_sectors):
    angles = np.arctan2(data[:, 1], data[:, 0])
    angles[angles < 0] += 2 * np.pi
    bins, _ = np.histogram(angles, bins=num_sectors, range=(0, 2 * np.pi))
    expected_count = len(data) / num_sectors
    chi_square_stat = np.sum((bins - expected_count) ** 2 / expected_count)
    return chi_square_stat

def normal_pdf(x, mean, stddev):
    return norm.pdf(x, loc=mean, scale=stddev)

def chi_square_test_normal_in_circle(data, num_bins, radius):
    radii = []
    for point in data:
        r = np.sqrt(point[0] ** 2 + point[1] ** 2)
        if point[0] < 0:
            r = -r
        radii.append(r)
    radii = np.array(radii)
    
    bins, bin_edges = np.histogram(radii, bins=num_bins, range=(-radius, radius))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    mean_radius = np.mean(radii)
    stddev_radius = np.std(radii)
    expected_counts = normal_pdf(bin_centers, mean_radius, stddev_radius) * len(data) * (bin_edges[1] - bin_edges[0])
    chi_square_stat = np.sum((bins - expected_counts) ** 2 / expected_counts)
    return chi_square_stat

def chi_square_test_normal_in_sphere(data, num_bins, radius):
    radii = []
    for point in data:
        r = np.linalg.norm(point)
        if point[0] < 0:
            r = -r
        radii.append(r)
    radii = np.array(radii)
    
    bins, bin_edges = np.histogram(radii, bins=num_bins, range=(-radius, radius))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    mean_radius = np.mean(radii)
    stddev_radius = np.std(radii)
    expected_counts = normal_pdf(bin_centers, mean_radius, stddev_radius) * len(data) * (bin_edges[1] - bin_edges[0])
    chi_square_stat = np.sum((bins - expected_counts) ** 2 / expected_counts)
    return chi_square_stat

def chi_square_uniform_test_sectors(data, num_sectors):
    radii = np.linalg.norm(data, axis=1)
    phi = np.arccos(data[:, 2] / radii)
    bins, _ = np.histogram(phi, bins=num_sectors, range=(0, np.pi))
    expected_count = len(data) / num_sectors
    chi_square_stat = np.sum((bins - expected_count) ** 2 / expected_count)
    return chi_square_stat

def save_test_results_to_file(test_name, chi_square_stat, result, filename):
    result_text = "Гипотеза Принята" if result else "Гипотеза Не принята"
    with open(filename, 'a') as file:
        file.write(f"Тест: {test_name}\n")
        file.write(f"Х^2 статистика: {chi_square_stat:.2f}\n")
        file.write(f"Результат: {result_text} при уровне значимости 0.05\n")
        file.write("--------------------------------------\n")

critical_value = 30.144
def check(value):
    return value < critical_value


def plot_points(points, title, xlabel, ylabel, zlabel=None):
    if points.shape[1] == 2:
        plt.scatter(points[:, 0], points[:, 1], alpha=0.6, edgecolors='w', linewidth=0.5)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
    elif points.shape[1] == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], alpha=0.6, edgecolors='w', linewidth=0.5)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        plt.show()

def plot_histogram(points, title, xlabel, ylabel):
    plt.hist(points, bins=30, edgecolor='k', alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def test_on_interval():
    a = 0
    b = 100
    num_points = 10000
    uniform_data = [uniform_on_interval(a, b) for _ in range(num_points)]
    normal_data = [normal_on_interval(a, b) for _ in range(num_points)]

    num_bins = 20
    chi_square_uniform = chi_square_uniform_test(uniform_data, num_bins, a, b)
    print(f"Х^2 статистика для равномерного распределения: {chi_square_uniform:.2f} - {'Гипотеза Принята' if check(chi_square_uniform) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для равномерного распределения на отрезке", chi_square_uniform, check(chi_square_uniform), "test_results.txt")
    plot_histogram(uniform_data, 'Равномерное распределение на отрезке', 'Значение', 'Частота')

    chi_square_normal = chi_square_normal_test(normal_data, num_bins, a, b)
    print(f"Х^2 статистика для нормального распределения: {chi_square_normal:.2f} - {'Гипотеза Принята' if check(chi_square_normal) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для нормального распределения на отрезке", chi_square_normal, check(chi_square_normal), "test_results.txt")
    plot_histogram(normal_data, 'Нормальное распределение на отрезке', 'Значение', 'Частота')

def test_square():
    a = 0
    b = 1
    c = 1 
    d = 2
    num_points = 1000
    num_bins = 20
    uniform_data_pr = np.array([uniform_vector(a, b, c, d) for _ in range(num_points)])
    normal_data_pr = np.array([normal_vector(a, b, c, d) for _ in range(num_points)])

    uniform_x, uniform_y = uniform_data_pr[:, 0], uniform_data_pr[:, 1]
    normal_x, normal_y = normal_data_pr[:, 0], normal_data_pr[:, 1]

    chi_square_uniform_x = chi_square_uniform_test(uniform_x, num_bins, a, b)
    chi_square_uniform_y = chi_square_uniform_test(uniform_y, num_bins, c, d)
    print(f"Х^2 статистика для равномерного распределения координаты X прямоугольника: {chi_square_uniform_x:.2f} - {'Гипотеза Принята' if check(chi_square_uniform_x) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для равномерного распределения координаты X прямоугольника", chi_square_uniform_x, check(chi_square_uniform_x), "test_results.txt")
 

    print(f"Х^2 статистика для равномерного распределения координаты Y прямоугольника: {chi_square_uniform_y:.2f} - {'Гипотеза Принята' if check(chi_square_uniform_y) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для равномерного распределения координаты Y прямоугольника", chi_square_uniform_y, check(chi_square_uniform_y), "test_results.txt")
 

    chi_square_normal_x = chi_square_normal_test(normal_x, num_bins, a, b)
    chi_square_normal_y = chi_square_normal_test(normal_y, num_bins, c, d)
    print(f"Х^2 статистика для нормального распределения координаты X прямоугольника: {chi_square_normal_x:.2f} - {'Гипотеза Принята' if check(chi_square_normal_x) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для нормального распределения координаты X прямоугольника", chi_square_normal_x, check(chi_square_normal_x), "test_results.txt")
 

    print(f"Х^2 статистика для нормального распределения координаты Y прямоугольника: {chi_square_normal_y:.2f} - {'Гипотеза Принята' if check(chi_square_normal_y) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для нормального распределения координаты Y прямоугольника", chi_square_normal_y, check(chi_square_normal_y), "test_results.txt")


    plot_points(uniform_data_pr, 'Равномерное распределение в прямоугольнике', 'X', 'Y')
    plot_points(normal_data_pr, 'Нормальное распределение в прямоугольнике', 'X', 'Y')

def test_parallelepiped():
    a = 0
    b = 1
    c = -1
    d = 2
    e = 0.5
    f = 1.5
    num_points = 2000
    num_bins = 20
    uniform_data_par = np.array([uniform_vectors_in_parallelepiped(a, b, c, d, e, f) for _ in range(num_points)])
    normal_data_par = np.array([normal_vectors_in_parallelepiped(a, b, c, d, e, f) for _ in range(num_points)])

    uniform_x_par, uniform_y_par, uniform_z_par = uniform_data_par[:, 0], uniform_data_par[:, 1], uniform_data_par[:, 2]
    normal_x_par, normal_y_par, normal_z_par = normal_data_par[:, 0], normal_data_par[:, 1], normal_data_par[:, 2]

    chi_square_uniform_x = chi_square_uniform_test(uniform_x_par, num_bins, a, b)
    chi_square_uniform_y = chi_square_uniform_test(uniform_y_par, num_bins, c, d)
    chi_square_uniform_z = chi_square_uniform_test(uniform_z_par, num_bins, e, f)
    print(f"Х^2 статистика для равномерного распределения координаты X параллелепипеда: {chi_square_uniform_x:.2f} - {'Гипотеза Принята' if check(chi_square_uniform_x) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для равномерного распределения координаты X параллелепипеда", chi_square_uniform_x, check(chi_square_uniform_x), "test_results.txt")


    print(f"Х^2 статистика для равномерного распределения координаты Y параллелепипеда: {chi_square_uniform_y:.2f} - {'Гипотеза Принята' if check(chi_square_uniform_y) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для равномерного распределения координаты Y параллелепипеда", chi_square_uniform_y, check(chi_square_uniform_y), "test_results.txt")
 

    chi_square_uniform_z = chi_square_uniform_test(uniform_z_par, num_bins, e, f)
    print(f"Х^2 статистика для равномерного распределения координаты Z параллелепипеда: {chi_square_uniform_z:.2f} - {'Гипотеза Принята' if check(chi_square_uniform_z) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для равномерного распределения координаты Z параллелепипеда", chi_square_uniform_z, check(chi_square_uniform_z), "test_results.txt")


    chi_square_normal_x = chi_square_normal_test(normal_x_par, num_bins, a, b)
    chi_square_normal_y = chi_square_normal_test(normal_y_par, num_bins, c, d)
    chi_square_normal_z = chi_square_normal_test(normal_z_par, num_bins, e, f)
    print(f"Х^2 статистика для нормального распределения координаты X параллелепипеда: {chi_square_normal_x:.2f} - {'Гипотеза Принята' if check(chi_square_normal_x) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для нормального распределения координаты X параллелепипеда", chi_square_normal_x, check(chi_square_normal_x), "test_results.txt")


    print(f"Х^2 статистика для нормального распределения координаты Y параллелепипеда: {chi_square_normal_y:.2f} - {'Гипотеза Принята' if check(chi_square_normal_y) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для нормального распределения координаты Y параллелепипеда", chi_square_normal_y, check(chi_square_normal_y), "test_results.txt")
  

    print(f"Х^2 статистика для нормального распределения координаты Z параллелепипеда: {chi_square_normal_z:.2f} - {'Гипотеза Принята' if check(chi_square_normal_z) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для нормального распределения координаты Z параллелепипеда", chi_square_normal_z, check(chi_square_normal_z), "test_results.txt")

    plot_points(uniform_data_par, 'Равномерное распределение в параллелепипеде', 'X', 'Y', 'Z')
    plot_points(normal_data_par, 'Нормальное распределение в параллелепипеде', 'X', 'Y', 'Z')

def test_circle():
    radius = 1
    num_points = 1000
    num_bins = 20
    uniform_data_circle = np.array([uniform_vector_in_circle(radius) for _ in range(num_points)])
    normal_data_circle = np.array([normal_vector_in_circle(radius) for _ in range(num_points)])

    chi_square_uniform = chi_square_test_circular(uniform_data_circle, num_bins)
    print(f"Х^2 статистика для равномерного распределения в окружности: {chi_square_uniform:.2f} - {'Гипотеза Принята' if check(chi_square_uniform) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для равномерного распределения в окружности", chi_square_uniform, check(chi_square_uniform), "test_results.txt")


    chi_square_normal = chi_square_test_normal_in_circle(normal_data_circle, num_bins, radius)
    print(f"Х^2 статистика для нормального распределения в окружности: {chi_square_normal:.2f} - {'Гипотеза Принята' if check(chi_square_normal) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для нормального распределения в окружности", chi_square_normal, check(chi_square_normal), "test_results.txt")


    plot_points(uniform_data_circle, 'Равномерное распределение в окружности', 'X', 'Y')
    plot_points(normal_data_circle, 'Нормальное распределение в окружности', 'X', 'Y')

def test_sphere():
    radius = 1
    num_points = 1000
    num_sectors = 20
    num_bins = 20

    uniform_data_sphere = np.array([uniform_vector_in_sphere(radius) for _ in range(num_points)])
    chi_square_uniform = chi_square_uniform_test_sectors(uniform_data_sphere, num_sectors)
    print(f"Х^2 статистика для равномерного распределения в сфере: {chi_square_uniform:.2f} - {'Гипотеза Принята' if check(chi_square_uniform) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для равномерного распределения в сфере", chi_square_uniform, check(chi_square_uniform), "test_results.txt")


    normal_data_sphere = np.array([normal_vector_in_sphere(radius) for _ in range(num_points)])
    chi_square_normal = chi_square_test_normal_in_sphere(normal_data_sphere, num_bins, radius)
    print(f"Х^2 статистика для нормального распределения в сфере: {chi_square_normal:.2f} - {'Гипотеза Принята' if check(chi_square_normal) else 'Гипотеза Не принята'}")
    save_test_results_to_file("Х^2 статистика для нормального распределения в сфере", chi_square_normal, check(chi_square_normal), "test_results.txt")

    plot_points(uniform_data_sphere, 'Равномерное распределение в сфере', 'X', 'Y', 'Z')
    plot_points(normal_data_sphere, 'Нормальное распределение в сфере', 'X', 'Y', 'Z')

test_on_interval()
test_square()
test_parallelepiped()
test_circle()
test_sphere()