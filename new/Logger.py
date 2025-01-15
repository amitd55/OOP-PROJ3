class Logger:
    def __init__(self, log_file="library_logs.txt"):
        self.log_file = log_file

    def log_action(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # Call the actual function
            if isinstance(result, dict):
                status = "successfully" if result.get("success") else "fail"
                action = result.get("action", func.__name__).lower()
                log_message = f"- {action} {status}\n"

                # Append to log file
                with open(self.log_file, "a") as log_file:
                    log_file.write(log_message)

            return result  # Return the original function's result
        return wrapper
