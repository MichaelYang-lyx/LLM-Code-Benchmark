
def bf(planet1, planet2):
    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    if planet1 not in planets or planet2 not in planets:
        return ()
    else:
        planet1_index = planets.index(planet1)
        planet2_index = planets.index(planet2)
        start_index = min(planet1_index, planet2_index) + 1
        end_index = max(planet1_index, planet2_index)
        result = tuple(planets[start_index:end_index])
        return result
