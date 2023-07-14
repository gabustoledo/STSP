import math
import matplotlib.pyplot as plt
import time

# Función para medir el tiempo de ejecución de una función determinada
def measure_execution_time(func):
    start_time = time.time()
    func()
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time

def read_cities_file(filename):
    cities = []
    with open(filename, 'r') as file:
        for line in file:
            city_info = line.strip().split()
            city_id = int(city_info[0])
            x = float(city_info[1])
            y = float(city_info[2])
            city = (x, y)
            cities.append(city)
    return cities

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_path_length(path, cities):
    length = 0
    num_cities = len(path)
    for i in range(num_cities):
        from_city = cities[path[i]]
        to_city = cities[path[(i + 1) % num_cities]]
        length += distance(from_city, to_city)
    return length

def two_opt(path, cities):
    num_cities = len(path)
    best_path = path[:]
    improve = True
    while improve:
        improve = False
        for i in range(1, num_cities - 1):
            for j in range(i + 1, num_cities):
                new_path = best_path[:]
                new_path[i:j+1] = list(reversed(new_path[i:j+1]))
                new_length = calculate_path_length(new_path, cities)
                if new_length < calculate_path_length(best_path, cities):
                    best_path = new_path
                    improve = True
        path = best_path
    return best_path

def plot_route(route, cities):
    x = [city[0] for city in cities]
    y = [city[1] for city in cities]
    plt.plot(x, y, 'bo')

    num_cities = len(route)
    for i in range(num_cities):
        from_city = cities[route[i]]
        to_city = cities[route[(i + 1) % num_cities]]
        plt.plot([from_city[0], to_city[0]], [from_city[1], to_city[1]], 'k-')
        plt.text(from_city[0], from_city[1], str(i), color='red')

    total_length = calculate_path_length(route, cities)
    plt.text(0.5, -0.5, f"Longitud total de la ruta: {total_length:.2f}", fontsize=10, ha='center')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Ruta del vendedor viajero')
    plt.grid(True)
    plt.show()

def main():
    filename = 'qatar.txt'  # Nombre del archivo de texto
    cities = read_cities_file(filename)

    # Genera un recorrido inicial (por ejemplo, [0, 1, 2, ..., n-1])
    initial_path = list(range(len(cities)))

    # Aplica el método 2-opt para mejorar el recorrido
    optimized_path = two_opt(initial_path, cities)

    # Calcula la longitud total de la ruta original y la ruta optimizada
    initial_length = calculate_path_length(initial_path, cities)
    optimized_length = calculate_path_length(optimized_path, cities)

    # Imprime el recorrido original, el recorrido optimizado y la longitud total de la ruta
    print("Recorrido original:", initial_path)
    print("Recorrido optimizado:", optimized_path)
    print("Longitud total de la ruta original:", initial_length)
    print("Longitud total de la ruta optimizada:", optimized_length)

    # Grafica ambas rutas
    #plot_route(initial_path, cities)
    #plot_route(optimized_path, cities)

# Mide el tiempo de ejecución de la función main()
execution_time = measure_execution_time(main)
print("Tiempo de ejecución:", execution_time, "segundos")