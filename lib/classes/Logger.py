class Logger:
    def __init__(self, log_file="library_logs.txt"):
        self.log_file = log_file

    def log_action(self, func):
        def wrapper(*args, **kwargs):
            try:
                # Call the original function and get the result
                result = func(*args, **kwargs)

                # Log action details
                action = func.__name__.replace('_', ' ').title()
                status = "Successfully completed" if result else "Failed"
                log_message = f"- {action} {status}\n"

                # Write the log message to the log file
                with open(self.log_file, "a") as log_file:
                    log_file.write(log_message)

                # Return the result (the iterator or list)
                return result

            except Exception as e:
                # Log the error if an exception occurs
                action = func.__name__.replace('_', ' ').title()
                log_message = f"- {action} failed: {str(e)}\n"
                with open(self.log_file, "a") as log_file:
                    log_file.write(log_message)
                raise  # Re-raise the exception after logging it

        return wrapper
