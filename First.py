# Program to print Fibonacci series up to n terms

# Take input from the user
n = int(input("Enter the number of terms: "))

# Initialize the first two terms
a, b = 0, 1
count = 0

# Check if the number of terms is valid
if n <= 0:
    print("Please enter a positive integer.")
elif n == 1:
    print(f"Fibonacci series up to {n} term:")
    print(a)
else:
    print("Fibonacci series:")
    while count < n:
        print(a, end=" ")
        # Update values to get the next term
        nth = a + b
        a = b
        b = nth
        count += 1