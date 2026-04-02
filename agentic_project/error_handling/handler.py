import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CircuitBreaker:
    """
    Implements a circuit breaker pattern.
    """
    def __init__(self, threshold: int, timeout: int):
        self.threshold = threshold
        self.timeout = timeout
        self.failures = 0
        self.open = False
        self.last_failure = None

    def is_open(self) -> bool:
        """Checks if the circuit breaker is open."""
        if self.open:
            time_since_failure = time.time() - self.last_failure
            if time_since_failure > self.timeout:
                logging.info("Circuit breaker timeout reached. Resetting.")
                self.reset()
                return False
            else:
                return True
        return False

    def record_failure(self):
        """Records a failure and potentially opens the circuit breaker."""
        self.failures += 1
        self.last_failure = time.time()
        if self.failures > self.threshold:
            logging.warning("Circuit breaker opened.")
            self.open = True

    def reset(self):
        """Resets the circuit breaker."""
        logging.info("Circuit breaker reset.")
        self.failures = 0
        self.open = False
        self.last_failure = None

def retry(func, attempts: int, delay: int, circuit_breaker: CircuitBreaker = None):
    """
    Retries a function with exponential backoff and circuit breaker.
    """
    for attempt in range(attempts):
        if circuit_breaker and circuit_breaker.is_open():
            return "Service unavailable. Please try again later."
        try:
            return func()
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if circuit_breaker:
                circuit_breaker.record_failure()
            if attempt == attempts - 1:
                logging.error("Max retries reached.")
                raise
            time.sleep(delay * (attempt + 1))  # Exponential backoff

# Example usage:
if __name__ == '__main__':
    def flaky_function():
        """A function that sometimes fails."""
        import random
        if random.random() < 0.5:
            raise ValueError("Function failed")
        return "Function succeeded"

    circuit_breaker = CircuitBreaker(threshold=3, timeout=60)

    try:
        result = retry(flaky_function, attempts=5, delay=2, circuit_breaker=circuit_breaker)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")