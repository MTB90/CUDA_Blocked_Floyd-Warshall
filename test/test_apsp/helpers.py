import json
from subprocess import run, PIPE
from typing import Tuple, List


class APSP(object):
    NAIVE_FW = '0'
    CUDA_NAIVE_FW = '1'
    CUDA_BLOCKED_FW = '2'


def execute_algorithm(exec_path: str, algorithm: APSP, data_input: str) -> Tuple:
    """
    Execute specific algorithm and return algorithm result

    :param exec_path: Path to executable
    :param algorithm: Type of algorithm
    :param data_input: Data input for algorithm

    :return: Data output and stderr
    """
    process = run([exec_path, '-a', algorithm],
                  input=data_input, encoding='ascii',
                  stdout=PIPE, stderr=PIPE)
    if process.stderr:
        return {'graph': [], 'predecessors': []}, process.stderr
    data = json.loads(process.stdout)
    return data, ''


def gen_graph_out(size: int, value: int = -1, diagonal: int =-1) -> List:
    """
    Generate graph output

    :param size: size of graph
    :param value: value for each cell
    :param diagonal: value for diagonal cells
    """
    graph = [[value] * size for _ in range(size)]
    if diagonal != value:
        for i in range(size):
            graph[i][i] = 0
    return graph


def gen_k1_graph_out(size: int) -> List:
    """
    Generate K1 graph output

    :param size: size of graph
    """
    graph = gen_graph_out(size, diagonal=0)
    for i in range(size // 2):
        graph[2 * i][2 * i + 1] = 1
        graph[2 * i + 1][2 * i] = 1
    return graph


def gen_k1_graph_in(size):
    """
    Generate K1 graph input

    :param size: size of graph
    """
    input_graph = f"{size} {size}"
    for i in range(size // 2):
        input_graph += f" {i*2} {i*2+1} 1"
        input_graph += f" {i*2+1} {i*2} 1"
    return input_graph


def gen_k1_predecessors_out(size: int) -> List:
    """
    Generate predecessors for K1 graph output

    :param size: size of graph
    """
    graph = gen_graph_out(size, -1)
    for i in range(size // 2):
        graph[2 * i][2 * i + 1] = 2 * i
        graph[2 * i + 1][2 * i] = 2 * i + 1
    return graph


def gen_kn_predecessors_out(size: int) -> List:
    """
    Generate predecessors for Kn graph output

    :param size: size of graph
    """
    graph = gen_graph_out(size, -1)
    for i in range(size):
        for j in range(size):
            if i != j:
                graph[i][j] = i
    return graph


def get_kn_graph_in(size):
    """
    Generate Kn graph input

    :param size: size of graph
    """
    input_graph = f"{size} {size*size}"
    for i in range(size):
        for j in range(size):
            if j != i:
                input_graph += f" {i} {j} 1"
    return input_graph
