class PID:
    def __init__(
        self,
        set_point,
        dt,
        kp,
        ki,
        kd,
        lower_limit,
        upper_limit,
        differential_on_measurement=True,
    ):
        """Initializes the PID controller with the set point and the PID constants.

        Args:
            set_point (float): The desired value for the process variable.
            dt (float): The time step between two updates of the controller.
            kp (float): The proportional gain.
            ki (float): The integral gain.
            kd (float): The derivative gain.
            lower_limit (float): The lower limit of the output in degrees.
            upper_limit (float): The upper limit of the output in degrees.
            differential_on_measurement (bool, optional): Whether to use the
            derivative on measurement or on error.
        """
        self.set_point = set_point
        self.dt = dt
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.lower_limit = lower_limit * 3.1416 / 180  # Convert to radians
        self.upper_limit = upper_limit * 3.1416 / 180  # Convert to radians
        self.differential_on_measurement = differential_on_measurement
        self.error = 0
        self.integral = 0
        self.derivative = 0
        self.previous_error = 0
        self.output = 0
        self.time = 0
        self.previous_time = 0

    def __call__(self, input):
        """Computes the PID output based on the input."""
        error = self.set_point - input
        d_input = input - last_input
        d_error = error - last_err

        # Compute the proportional term
        proportional = self.kp * error

        # Compute integrative and derivative terms
        integrative += self.ki * error * self.dt
        integrative = self.anti_wind_up(
            integrative,
            self.lower_limit * 180 / 3.1416,  # Convert to degrees
            self.upper_limit * 180 / 3.1416,  # Convert to degrees
        )  # Avoid integrative windup (-lowerInput, +upperInput)

        if self.differential_on_measurement:
            derivative = -self.kd * d_input / self.dt
        else:
            derivative = self.kd * d_error / self.dt

        # Compute final output
        output = proportional + integrative + derivative
        output = self.clamp(output)

        # Keep track of state
        last_input = input
        last_err = error
        return output

    def clamp(self, value):
        """Clamps the value between the lower and upper limits."""
        if value > self.upper_limit:
            return self.upper_limit
        elif value < self.lower_limit:
            return self.lower_limit
        return value

    def anti_wind_up(self, integrative, lower_limit, upper_limit):
        """Clamps the integrative term between the lower and upper limits."""
        if integrative > upper_limit:
            return upper_limit
        if integrative < lower_limit:
            return lower_limit
        return integrative
