# Usage Examples

> **English version** | **[Русская версия](USAGE_EXAMPLES.ru.md)**

This document provides detailed examples of using the Square Root Calculator.

## Table of Contents
- [Real Number Examples](#real-number-examples)
- [Complex Number Examples](#complex-number-examples)
- [High Precision Examples](#high-precision-examples)
- [Error Handling Examples](#error-handling-examples)

## Real Number Examples

### Example 1: Simple Integer Square Root
**Input:** 16  
**Precision:** 10  
**Result:** 4

This is a perfect square, so the result is an exact integer.

### Example 2: Irrational Number
**Input:** 2  
**Precision:** 50  
**Result:** 1.41421356237309504880168872420969807856967187537694...

The square root of 2 is an irrational number that continues infinitely without repeating.

### Example 3: Large Number
**Input:** 123456789  
**Precision:** 20  
**Result:** 11111.11106055555544054166...

Even very large numbers can be computed with high precision.

### Example 4: Decimal Input
**Input:** 0.25  
**Precision:** 10  
**Result:** 0.5

Decimal inputs work seamlessly.

### Example 5: Scientific Notation
**Input:** 1e10  
**Precision:** 15  
**Result:** 100000.000000000000000...

Large numbers in scientific notation are supported.

## Complex Number Examples

### Example 1: Standard Complex Number
**Real Part:** 3  
**Imaginary Part:** 4  
**Precision:** 15  
**Result:** 2+1i

This is a classic complex number calculation where √(3+4i) = 2+1i.

### Example 2: Negative Real Number
**Real Part:** -1  
**Imaginary Part:** 0  
**Precision:** 20  
**Result:** 0+1i

The square root of -1 is the imaginary unit i, which is represented as 0+1i.

### Example 3: Pure Imaginary Number
**Real Part:** 0  
**Imaginary Part:** 1  
**Precision:** 20  
**Result:** 0.70710678118654752440+0.70710678118654752440i

The square root of i equals (1+i)/√2.

### Example 4: Negative Complex Number
**Real Part:** -3  
**Imaginary Part:** -4  
**Precision:** 15  
**Result:** 1-2i

Negative complex numbers are fully supported.

### Example 5: Large Complex Number
**Real Part:** 100  
**Imaginary Part:** 100  
**Precision:** 15  
**Result:** 11.0977222864644...+4.5341652313282...i

The calculator handles large complex numbers accurately.

## High Precision Examples

### Example 1: Computing π/2 Approximation
We can use the fact that √2 ≈ 1.414... to high precision.

**Input:** 2  
**Precision:** 100  
**Result:**
```
1.4142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727
```

### Example 2: Golden Ratio Component
The golden ratio φ = (1+√5)/2. Here's √5 to high precision:

**Input:** 5  
**Precision:** 80  
**Result:**
```
2.23606797749978969640917366873127623544061835961152572427089724541052092563780...
```

### Example 3: Very Small Numbers
**Input:** 0.000001  
**Precision:** 30  
**Result:** 0.001000000000000000000000000000

Even very small numbers maintain precision.

## Error Handling Examples

### Example 1: Negative Number in Real Mode
**Input:** -5  
**Mode:** Real Numbers  
**Result:** Error message displayed

The calculator correctly identifies that negative numbers cannot have real square roots and suggests switching to Complex mode.

### Example 2: Invalid Input
**Input:** "abc"  
**Mode:** Real Numbers  
**Result:** Error message about invalid number format

Non-numeric input is caught and reported clearly.

### Example 3: Empty Input
**Input:** (empty)  
**Mode:** Real Numbers  
**Result:** Error message requesting valid input

The calculator validates that input is provided.

### Example 4: Complex Number with Negative in Real Mode
If you try to calculate the square root of a negative number in Real mode, the calculator will show an error and suggest switching to Complex mode:

**Error Message:** "Cannot calculate square root of negative real number. Switch to Complex mode."

## Mathematical Background

### Real Numbers
For a positive real number x, its square root √x is the number y such that y² = x.

### Complex Numbers
For a complex number z = a + bi, the square root is calculated using:
- √z = √((|z| + a)/2) + i·sign(b)·√((|z| - a)/2)
- where |z| = √(a² + b²)

This formula ensures accurate results for all complex numbers, including:
- Positive real numbers (b = 0, a > 0)
- Negative real numbers (b = 0, a < 0)
- Pure imaginary numbers (a = 0)
- General complex numbers (a ≠ 0, b ≠ 0)

## Tips for Best Results

1. **Choose Appropriate Precision:** Start with 50 decimal places for most calculations. Increase if you need more accuracy.

2. **Use Complex Mode for Negative Numbers:** If your input might be negative, use Complex mode to avoid errors.

3. **Large Numbers:** The calculator can handle very large numbers, but computation time may increase with higher precision.

4. **Validation:** Always check that your input is in the correct format before calculating.

5. **Language Support:** Switch between English and Russian using the language dropdown for your preferred interface.

## Common Use Cases

### Scientific Research
Use high precision (100+ digits) for scientific calculations requiring extreme accuracy.

### Engineering
Use moderate precision (20-50 digits) for engineering calculations where standard floating-point accuracy is insufficient.

### Education
Use any precision to demonstrate the properties of irrational numbers, complex numbers, and mathematical concepts.

### Finance
Use appropriate precision for financial calculations where exact decimal representation is crucial.
