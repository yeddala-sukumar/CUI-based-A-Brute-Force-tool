import time

def brute_force_code(target_code, length=4):
    start_time = time.time()
    attempts = 0
    max_attempts = 10**length  # Calculate the maximum number of attempts (e.g., 10000 for 4 digits)
    
    # Open a file to log attempts
    with open("brute_force_attempts.log", "w") as log_file:
        for code in range(max_attempts):
            guess = f"{code:0{length}}"  # Format as zero-padded string (e.g., 0001, 0234)
            log_file.write(f"Trying: {guess}\n")
            attempts += 1

            # Display progress every 1000 attempts
            if attempts % 1000 == 0 or guess == target_code:
                progress = (code + 1) / max_attempts * 100
                print(f"Progress: {progress:.2f}% - Trying: {guess}")

            # Check if the code matches
            if guess == target_code:
                end_time = time.time()
                print(f"\nCode cracked! The code is {guess}")
                print(f"Attempts: {attempts}")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                return guess
        
    # If the code is not found (unlikely in brute-force):
    print("Code not found!")
    return None

# Example usage
if __name__ == "__main__":
    print("Welcome to the Brute Force Code Cracker!")
    target = input("Enter the target code (e.g., 1234): ")
    
    if target.isdigit() and len(target) == 4:  # Validate input for a 4-digit code
        brute_force_code(target, length=4)
    else:
        print("Invalid input! Please enter a 4-digit numeric code.")
