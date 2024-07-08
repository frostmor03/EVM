import numpy as np

def uniform_on_interval(a, b):
    return np.random.uniform(a, b)

def normal_on_interval(a, b):
    mu = (a + b) / 2
    sigma = (b - a) / 6
    return np.random.normal(mu, sigma)

def uniform_vector(a, b, c, d):
    x = uniform_on_interval(a, b)
    y = uniform_on_interval(c, d)
    return np.array([x, y])

def normal_vector(a, b, c, d):
    x = normal_on_interval(a, b)
    y = normal_on_interval(c, d)
    return np.array([x, y])

def uniform_vector_in_circle(r):
    theta = uniform_on_interval(0, 2 * np.pi)
    radius = np.sqrt(uniform_on_interval(0, r * r))
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return np.array([x, y])

def normal_vector_in_circle(r):
    theta = uniform_on_interval(0, 2 * np.pi)
    radius = normal_on_interval(-r, r)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return np.array([x, y])

def uniform_vectors_in_parallelepiped(a, b, c, d, e, f):
    x = uniform_on_interval(a, b)
    y = uniform_on_interval(c, d)
    z = uniform_on_interval(e, f)
    return np.array([x, y, z])

def normal_vectors_in_parallelepiped(a, b, c, d, e, f):
    x = normal_on_interval(a, b)
    y = normal_on_interval(c, d)
    z = normal_on_interval(e, f)
    return np.array([x, y, z])

def uniform_vector_in_sphere(r):
    theta = uniform_on_interval(0, 2 * np.pi)
    phi = uniform_on_interval(0, np.pi)
    radius = np.cbrt(uniform_on_interval(0, r ** 3))
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)
    return np.array([x, y, z])

def normal_vector_in_sphere(r):
    theta = uniform_on_interval(0, 2 * np.pi)
    phi = uniform_on_interval(0, np.pi)
    radius = normal_on_interval(-r, r)
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)
    return np.array([x, y, z])
