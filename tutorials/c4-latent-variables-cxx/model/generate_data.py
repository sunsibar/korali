import numpy as np


def draw_from_single_gaussian(nr_points=10, dimensions=2, mu=0, sigma=1 ):
    ''' '''
    results, _ = draw_from_multiple_gaussian(nr_points, dimensions=dimensions, mus=[mu], sigma=sigma)
    return results

def draw_from_multiple_gaussian(nr_points=10, dimensions=2, mus=[0,2], sigma=1):
    results = np.zeros((nr_points, dimensions))
    cluster_assignment = np.zeros((nr_points,))
    nr_clusters = len(mus)
    for i in range(nr_points):
        c = np.random.choice(list(range(nr_clusters)))
        mu = mus[c]
        pt = np.random.normal(loc=mu, scale=sigma)
        cluster_assignment[i] = c
        results[i, :] = pt
    return results, cluster_assignment


def generate_data():
    nr_points = 10
    dimensions = 2
    single_output_file = "data_single.in"
    multiple_output_file = "data_multiple.in"

    single_data = draw_from_single_gaussian(nr_points, dimensions)
    multiple_data, ass = draw_from_multiple_gaussian(nr_points, dimensions)

    # store to files:
    with open(single_output_file, "w") as fd:
        d = single_data
        fd.write(str(nr_points) +" " + str(dimensions) +"\n")
        lines = [" ".join([str(d[i, j]) for j in range(dimensions)])  + "\n"   for i in range(nr_points)]
        fd.writelines(lines)
        fd.write("points (dim=" + str(dimensions) +") ")

    # store to files:
    with open(multiple_output_file, "w") as fd:
        d = multiple_data
        fd.write(str(nr_points) +" " + str(dimensions)  +"\n")
        lines = [" ".join([str(d[i, j])  for j in range(dimensions) ])  + " " + str(ass[i]) + "\n"   for i in range(nr_points)]
        fd.writelines(lines)
        fd.write("points (dim=" + str(dimensions) +") | last column: cluster assignment")

    print("Done")


if __name__ == '__main__':
    generate_data()