import random
import logging
from datetime import datetime

# Configuração do logger
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    filename=f'genetic_algorithm_{timestamp}.log', 
    level=logging.INFO, 
    format='%(message)s',
    encoding='utf-8')
logger = logging.getLogger()

mutation_rate = 1/12
generations = 80
populacao_inicial = 10
range_values = 20
parar_na_solucao = True

# Função para logar e imprimir ao mesmo tempo
def log_and_print(message):
    print(message)
    logger.info(message)

# Função objetivo (fitness)
def fitness(x, y, w, z):
    difference = abs(5 * x + y**2 + w + z**3 - 185)
    return 1 / (1 + difference)

# Codificação binária para os valores de x, y, w e z no intervalo [0, 15]
def decimal_to_binary(n, bits=4):
    return format(n, f'0{bits}b')

# População inicial de 10 indivíduos
def generate_initial_population(size=populacao_inicial):
    population = []
    for _ in range(size):
        x = random.randint(0, range_values)
        y = random.randint(0, range_values)
        w = random.randint(0, range_values)
        z = random.randint(0, range_values)
        chromosome = decimal_to_binary(x) + decimal_to_binary(y) + decimal_to_binary(w) + decimal_to_binary(z)
        population.append((chromosome, x, y, w, z))
    return population

# Avaliação da população
def evaluate_population(population):
    evaluated_population = []
    for chromosome, x, y, w, z in population:
        fit = fitness(x, y, w, z)
        value = 5 * x + y**2 + w + z**3
        evaluated_population.append((chromosome, x, y, w, z, fit, value))
        log_and_print(f"Teste Cromossomo (x: {x}, y: {y}, w: {w}, z: {z}) -> Equação: 5*{x} + {y}^2 + {w} + {z}^3 = {value}")
    evaluated_population.sort(key=lambda ind: ind[5], reverse=True)
    return evaluated_population

# Seleção por roleta viciada
def weighted_selection(evaluated_population):
    weights = [4, 3, 2, 1]
    selected_population = []
    for i in range(len(weights)):
        selected_population.extend([evaluated_population[i]] * weights[i])
    return selected_population

# Crossover
def crossover(parent1, parent2, point=8):
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

# Mutação
def mutate(chromosome, mutation_rate=mutation_rate):
    chromosome = list(chromosome)
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = '1' if chromosome[i] == '0' else '0'
    return ''.join(chromosome)

# Decodificar cromossomo
def decode_chromosome(chromosome):
    x = int(chromosome[:4], 2)
    y = int(chromosome[4:8], 2)
    w = int(chromosome[8:12], 2)
    z = int(chromosome[12:], 2)
    return x, y, w, z

# Gerar nova população
def generate_new_population(selected_population):
    new_population = []
    for i in range(0, len(selected_population), 2):
        parent1, parent2 = selected_population[i][0], selected_population[i+1][0]
        offspring1, offspring2 = crossover(parent1, parent2)
        new_population.append(mutate(offspring1))
        new_population.append(mutate(offspring2))
    return [(chromosome, *decode_chromosome(chromosome)) for chromosome in new_population]

# Execução do Algoritmo Genético
population = generate_initial_population()
evaluated_population = evaluate_population(population)

# Melhor indivíduo encontrado
best_individual = evaluated_population[0]
log_and_print(f"Geração 1 - Melhor Cromossomo: (x: {best_individual[1]}, y: {best_individual[2]}, w: {best_individual[3]}, z: {best_individual[4]}) com Aptidão: {best_individual[5]}")

for generation in range(1, generations):
    selected_population = weighted_selection(evaluated_population)
    new_population = generate_new_population(selected_population)
    evaluated_population = evaluate_population(new_population)
    
    # Verifica se o melhor indivíduo da nova geração é o mesmo da geração anterior
    new_best_individual = evaluated_population[0]
    if parar_na_solucao and new_best_individual[5] == 1.0:
        log_and_print(f"Geração {generation + 1} - Solução encontrada: (x: {new_best_individual[1]}, y: {new_best_individual[2]}, w: {new_best_individual[3]}, z: {new_best_individual[4]}) com Aptidão: {new_best_individual[5]}")
        best_individual = new_best_individual
        break
    if new_best_individual[0] == best_individual[0]:
        log_and_print(f"Geração {generation + 1} - Cromossomo (x: {new_best_individual[1]}, y: {new_best_individual[2]}, w: {new_best_individual[3]}, z: {new_best_individual[4]}) ainda é o mais apto com Aptidão: {new_best_individual[5]}")
    else:
        log_and_print(f"Geração {generation + 1} - Novo Melhor Cromossomo: (x: {new_best_individual[1]}, y: {new_best_individual[2]}, w: {new_best_individual[3]}, z: {new_best_individual[4]}) com Aptidão: {new_best_individual[5]}")
        best_individual = new_best_individual

# Resultados finais
best_x, best_y, best_w, best_z = best_individual[1:5]
final_value = 5 * best_x + best_y**2 + best_w + best_z**3
difference = abs(final_value - 185)


log_and_print("Aptidão do melhor cromossomo: {}".format(best_individual[5]))
log_and_print("\nMelhor cromossomo encontrado: (x: {}, y: {}, w: {}, z: {})".format(best_x, best_y, best_w, best_z))
log_and_print("Original: 5*x + y^2 + w + z^3".format(best_x, best_y, best_w, best_z))
log_and_print("Equação: 5*{} + {}^2 + {} + {}^3".format(best_x, best_y, best_w, best_z))
log_and_print("Valor da equação: {}".format(final_value))
log_and_print("Diferença absoluta de 185: {}".format(difference))
log_and_print("Resolvido: {}".format(str(final_value == 185)))
