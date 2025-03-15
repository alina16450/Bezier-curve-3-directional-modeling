import numpy as np


class BezierSurface:
    def __init__(self, control_points, delta, direction_vector, u0, v0):
        self.control_points = control_points
        self.delta = delta
        self.direction_vector = direction_vector / np.linalg.norm(direction_vector)  # Ensure unit vector
        self.u0 = u0
        self.v0 = v0

    @staticmethod
    def bezier_point(p0, p1, p2, p3, u):
        """
        Computes a point on a cubic Bézier curve.
        Args:
        - p0, p1, p2, p3 (np.array): Control points.
        - u (float): Curve parameter (0 <= u <= 1).
        Returns:
        - np.array: The computed point on the curve.
        """
        p01 = (1 - u) * p0 + u * p1
        p12 = (1 - u) * p1 + u * p2
        p23 = (1 - u) * p2 + u * p3

        p012 = (1 - u) * p01 + u * p12
        p123 = (1 - u) * p12 + u * p23

        return (1 - u) * p012 + u * p123

    def surface_point(self, u, v):
        """
        Computes a point on the extruded Bézier surface.
        Args:
        - u (float): Parameter along the Bézier curve.
        - v (float): Parameter along the extrusion direction.
        Returns:
        - np.array: The point on the surface.
        """
        r_u = self.bezier_point(*self.control_points, u)
        r_uv = r_u + v * self.delta * self.direction_vector
        return r_uv

    @classmethod
    def from_file(cls, filepath):
        """
        Creates a BezierSurface object by reading data from a file.
        Args:
        - filepath (str): Path to the input file.
        Returns:
        - BezierSurface: The initialized object.
        """
        try:
            with open(filepath, 'r') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            if len(lines) < 7:
                raise ValueError("The input file must contain at least 7 valid lines.")

            # Read control points
            control_points = [np.array([float(x) for x in lines[i].split()]) for i in range(4)]

            # Validate control point format
            if any(len(point) != 3 for point in control_points):
                raise ValueError("Each control point must have exactly 3 coordinates.")

            # Read delta
            delta = float(lines[4])

            # Read and normalize direction vector
            direction_vector = np.array([float(x) for x in lines[5].split()])
            if len(direction_vector) != 3:
                raise ValueError("The direction vector must have exactly 3 components.")
            direction_vector = direction_vector / np.linalg.norm(direction_vector)

            # Read u0 and v0
            u0, v0 = map(float, lines[6].split())

            return cls(control_points, delta, direction_vector, u0, v0)

        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{filepath}' was not found.")
        except ValueError as ve:
            raise ValueError(f"Error while processing the input file: {ve}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def calculate_and_display_point(self):
        """
        Calculates and displays the point on the Bézier surface for the initial parameters.
        """
        r_uv = self.surface_point(self.u0, self.v0)
        print(f"\nThe point r({self.u0}, {self.v0}) on the surface is: {r_uv}")


def main():
    input_file = "input.txt"
    bezier_surface = BezierSurface.from_file(input_file)

    while True:
        print("\n=== MENU ===")
        print("1. Calculate point on Bézier surface")
        print("2. Exit")

        option = input("Choose an option: ")
        if option == '1':
            bezier_surface.calculate_and_display_point()
        elif option == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid option! Please try again.")


if __name__ == "__main__":
    main()