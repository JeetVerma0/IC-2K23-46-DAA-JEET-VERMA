"""
Program 04: Polynomial Representation and Addition Using Linked Lists
Course: IC-307D Data Structures and Algorithms Lab
Unit 3: Linked Lists (CO1)

This program represents and manipulates algebraic polynomials using Linked Lists:
- Each node explicitly stores:
    1. coefficient (float or int)
    2. exponent (non-negative integer)
    3. next pointer reference
- Terms are strictly ordered in descending exponent order.
- Inserting terms automatically combines like-exponent terms and removes zero
  coefficients.
- Addition of two polynomials is performed using a two-pointer merge traversal
  running in optimal O(n + m) time, purely with node pointers without using
  dictionaries or Python lists as the underlying store.
- Comprehensive formatting renders mathematical polynomials (e.g. 4x^3 - 5x + 7)
  including cancellation of terms and zero polynomials.
"""

from typing import List, Optional, Tuple, Union


class PolyNode:
    """
    Represents an individual algebraic term in a Polynomial linked list.

    Attributes:
        coeff: The numeric coefficient (e.g., 5 in 5x^2).
        exp: The non-negative integer exponent (e.g., 2 in 5x^2).
        next: Pointer to the next term with a strictly lower exponent.
    """

    def __init__(self, coeff: Union[int, float], exp: int) -> None:
        if not isinstance(exp, int) or exp < 0:
            raise ValueError(f"Exponent must be a non-negative integer. Got: {exp}")
        if not isinstance(coeff, (int, float)):
            raise TypeError(f"Coefficient must be a numeric type. Got: {type(coeff).__name__}")

        self.coeff: Union[int, float] = coeff
        self.exp: int = exp
        self.next: Optional["PolyNode"] = None

    def __repr__(self) -> str:
        return f"PolyNode({self.coeff}x^{self.exp})"


class Polynomial:
    """
    Represents a single-variable polynomial P(x) using a singly linked list.

    Invariants:
        1. Terms are strictly arranged in descending order of exponent:
           head.exp > head.next.exp > head.next.next.exp ...
        2. No two nodes have identical exponents (like terms are automatically combined).
        3. No node stores a coefficient of zero (cancelling terms are deleted).
        4. A zero polynomial has head = None.
    """

    def __init__(self) -> None:
        self.head: Optional[PolyNode] = None

    def is_zero(self) -> bool:
        """Returns True if the polynomial is identically zero (empty list)."""
        return self.head is None

    def insert_term(self, coeff: Union[int, float], exp: int) -> None:
        """
        Inserts a single term (coeff * x^exp) into the polynomial.
        Maintains descending exponent order and combines terms with equal exponents.

        Time Complexity: O(n) where n is current number of terms.
        Auxiliary Space Complexity: O(1)
        """
        if coeff == 0:
            return  # Adding a 0-term has no effect

        # 1. Empty list or exponent strictly greater than head
        if self.head is None or exp > self.head.exp:
            new_node = PolyNode(coeff, exp)
            new_node.next = self.head
            self.head = new_node
            return

        # 2. Exponent matches head
        if exp == self.head.exp:
            self.head.coeff += coeff
            if self.head.coeff == 0:
                self.head = self.head.next
            return

        # 3. Traverse to locate insertion point
        current = self.head
        while current.next is not None and current.next.exp > exp:
            current = current.next

        # Check if next node matches exponent
        if current.next is not None and current.next.exp == exp:
            current.next.coeff += coeff
            if current.next.coeff == 0:
                # Remove zero coefficient node
                current.next = current.next.next
        else:
            # Insert new node between current and current.next
            new_node = PolyNode(coeff, exp)
            new_node.next = current.next
            current.next = new_node

    @classmethod
    def from_terms(cls, terms: List[Tuple[Union[int, float], int]]) -> "Polynomial":
        """
        Factory method to construct a Polynomial from a list of (coeff, exp) tuples.

        Time Complexity: O(k * n)
        """
        poly = cls()
        for coeff, exp in terms:
            poly.insert_term(coeff, exp)
        return poly

    def add(self, other: "Polynomial") -> "Polynomial":
        """
        Adds two polynomials and returns a new Polynomial representing their sum:
            P_res(x) = P_self(x) + P_other(x)

        Algorithm (Two-Pointer Merge):
            1. Pointers p1 and p2 track nodes in self and other.
            2. If p1.exp == p2.exp:
               Sum coefficients: sum_coeff = p1.coeff + p2.coeff
               If sum_coeff != 0, append new node with (sum_coeff, p1.exp)
               Advance both p1 and p2.
            3. If p1.exp > p2.exp:
               Append copy of p1 node to result. Advance p1.
            4. If p2.exp > p1.exp:
               Append copy of p2 node to result. Advance p2.
            5. Append remaining nodes from whichever polynomial is not exhausted.

        Time Complexity: O(n + m) where n = terms(self), m = terms(other)
        Auxiliary Space Complexity: O(n + m) for the new result polynomial nodes
        """
        if not isinstance(other, Polynomial):
            raise TypeError("Can only add another Polynomial instance.")

        result = Polynomial()
        p1 = self.head
        p2 = other.head

        # Maintain tail pointer for O(1) appending to result
        result_tail: Optional[PolyNode] = None

        def append_to_result(coeff: Union[int, float], exp: int) -> None:
            nonlocal result_tail
            if coeff == 0:
                return
            new_node = PolyNode(coeff, exp)
            if result.head is None:
                result.head = new_node
                result_tail = new_node
            else:
                assert result_tail is not None
                result_tail.next = new_node
                result_tail = new_node

        while p1 is not None and p2 is not None:
            if p1.exp == p2.exp:
                combined_coeff = p1.coeff + p2.coeff
                append_to_result(combined_coeff, p1.exp)
                p1 = p1.next
                p2 = p2.next
            elif p1.exp > p2.exp:
                append_to_result(p1.coeff, p1.exp)
                p1 = p1.next
            else:
                append_to_result(p2.coeff, p2.exp)
                p2 = p2.next

        # Drain remaining terms from self
        while p1 is not None:
            append_to_result(p1.coeff, p1.exp)
            p1 = p1.next

        # Drain remaining terms from other
        while p2 is not None:
            append_to_result(p2.coeff, p2.exp)
            p2 = p2.next

        return result

    def __add__(self, other: "Polynomial") -> "Polynomial":
        return self.add(other)

    def evaluate(self, x: Union[int, float]) -> Union[int, float]:
        """
        Evaluates P(x) at numeric value x.

        Time Complexity: O(n)
        Auxiliary Space Complexity: O(1)
        """
        val: Union[int, float] = 0
        current = self.head
        while current is not None:
            val += current.coeff * (x ** current.exp)
            current = current.next
        return val

    def to_tuples(self) -> List[Tuple[Union[int, float], int]]:
        """Returns terms as list of (coeff, exp) tuples (for testing verification)."""
        res: List[Tuple[Union[int, float], int]] = []
        current = self.head
        while current is not None:
            res.append((current.coeff, current.exp))
            current = current.next
        return res

    def display(self) -> str:
        """
        Renders the polynomial into canonical mathematical format:
        Examples:
            "4x^3 + 2x^2 - 5x + 7"
            "-x^2 + 1"
            "0"
        """
        if self.head is None:
            return "0"

        pieces: List[str] = []
        current = self.head

        while current is not None:
            c = current.coeff
            e = current.exp

            # Format coefficient magnitude
            if isinstance(c, float) and c.is_integer():
                c = int(c)

            abs_c = abs(c)

            # Determine variable component
            if e == 0:
                term_body = f"{abs_c}"
            elif e == 1:
                term_body = "x" if abs_c == 1 else f"{abs_c}x"
            else:
                term_body = f"x^{e}" if abs_c == 1 else f"{abs_c}x^{e}"

            # Append sign and term
            if not pieces:
                # Leading term
                sign = "-" if c < 0 else ""
                pieces.append(f"{sign}{term_body}")
            else:
                sign = " - " if c < 0 else " + "
                pieces.append(f"{sign}{term_body}")

            current = current.next

        return "".join(pieces)

    def __str__(self) -> str:
        return self.display()


# ===========================================================================
# Automated Verification & Self-Tests
# ===========================================================================

def run_tests() -> None:
    """Executes comprehensive verification covering polynomial creation, ordering, and addition."""
    print("=" * 65)
    print("RUNNING COMPREHENSIVE TESTS: Polynomial Operations (Program 04)")
    print("=" * 65)

    # 1. Zero polynomial
    p_zero = Polynomial()
    assert p_zero.is_zero() is True
    assert p_zero.display() == "0"
    assert p_zero.evaluate(5) == 0
    print("  [Test 01 Passed] Zero polynomial representation verified.")

    # 2. Term insertion & descending exponent ordering
    p1 = Polynomial()
    p1.insert_term(7, 0)
    p1.insert_term(4, 3)
    p1.insert_term(-5, 1)
    p1.insert_term(2, 2)
    # Expected order: 4x^3 + 2x^2 - 5x + 7
    assert p1.to_tuples() == [(4, 3), (2, 2), (-5, 1), (7, 0)]
    assert p1.display() == "4x^3 + 2x^2 - 5x + 7"
    print("  [Test 02 Passed] Term insertion and descending exponent ordering verified.")

    # 3. Combining like-exponent terms
    p1.insert_term(3, 2)  # 2x^2 + 3x^2 = 5x^2
    assert p1.to_tuples() == [(4, 3), (5, 2), (-5, 1), (7, 0)]
    print("  [Test 03 Passed] Like-exponent term combination verified.")

    # 4. Zero coefficient removal during insertion
    p1.insert_term(-5, 2)  # 5x^2 - 5x^2 = 0x^2 (term eliminated)
    assert p1.to_tuples() == [(4, 3), (-5, 1), (7, 0)]
    print("  [Test 04 Passed] Automatic cancellation of zero coefficients verified.")

    # 5. Polynomial addition: Matching exponents
    # (3x^2 + 5x + 2) + (4x^2 - 2x + 6) = 7x^2 + 3x + 8
    poly_a = Polynomial.from_terms([(3, 2), (5, 1), (2, 0)])
    poly_b = Polynomial.from_terms([(4, 2), (-2, 1), (6, 0)])
    sum_ab = poly_a.add(poly_b)
    assert sum_ab.to_tuples() == [(7, 2), (3, 1), (8, 0)]
    assert sum_ab.display() == "7x^2 + 3x + 8"
    print("  [Test 05 Passed] Polynomial addition with matching exponents verified.")

    # 6. Polynomial addition: Non-matching exponents
    # (5x^4 + 2x^2 + 1) + (3x^3 + 4x) = 5x^4 + 3x^3 + 2x^2 + 4x + 1
    poly_c = Polynomial.from_terms([(5, 4), (2, 2), (1, 0)])
    poly_d = Polynomial.from_terms([(3, 3), (4, 1)])
    sum_cd = poly_c + poly_d
    assert sum_cd.to_tuples() == [(5, 4), (3, 3), (2, 2), (4, 1), (1, 0)]
    assert sum_cd.display() == "5x^4 + 3x^3 + 2x^2 + 4x + 1"
    print("  [Test 06 Passed] Polynomial addition with interleaved exponents verified.")

    # 7. Complete term cancellation to zero polynomial
    # (4x^3 + 2x - 7) + (-4x^3 - 2x + 7) = 0
    poly_e = Polynomial.from_terms([(4, 3), (2, 1), (-7, 0)])
    poly_f = Polynomial.from_terms([(-4, 3), (-2, 1), (7, 0)])
    sum_ef = poly_e + poly_f
    assert sum_ef.is_zero() is True
    assert sum_ef.display() == "0"
    print("  [Test 07 Passed] Complete cancellation to zero polynomial verified.")

    # 8. Adding with zero polynomial
    sum_zero = poly_a + p_zero
    assert sum_zero.to_tuples() == poly_a.to_tuples()
    print("  [Test 08 Passed] Identity addition with zero polynomial verified.")

    # 9. Evaluation verification
    # For P(x) = 7x^2 + 3x + 8: P(2) = 7(4) + 3(2) + 8 = 28 + 6 + 8 = 42
    assert sum_ab.evaluate(2) == 42
    print("  [Test 09 Passed] Polynomial evaluation verified.")

    print("\nAll Program 04 automated tests PASSED successfully!")


def demonstrate() -> None:
    """Visual demonstration of polynomial addition and formatting."""
    print("\n" + "=" * 65)
    print("DEMONSTRATION: Polynomial Representation & Addition (Program 04)")
    print("=" * 65)

    print("\n--- Example 1: Matching Exponents ---")
    p1 = Polynomial.from_terms([(3, 2), (5, 1), (2, 0)])
    p2 = Polynomial.from_terms([(4, 2), (-2, 1), (6, 0)])
    print(f"  P1(x) = {p1}")
    print(f"  P2(x) = {p2}")
    sum1 = p1 + p2
    print(f"  P1(x) + P2(x) = {sum1}")

    print("\n--- Example 2: Interleaved Non-Matching Exponents ---")
    p3 = Polynomial.from_terms([(5, 4), (2, 2), (1, 0)])
    p4 = Polynomial.from_terms([(3, 3), (4, 1)])
    print(f"  P3(x) = {p3}")
    print(f"  P4(x) = {p4}")
    sum2 = p3 + p4
    print(f"  P3(x) + P4(x) = {sum2}")

    print("\n--- Example 3: Full Cancellation to Zero ---")
    p5 = Polynomial.from_terms([(4, 3), (2, 1), (-7, 0)])
    p6 = Polynomial.from_terms([(-4, 3), (-2, 1), (7, 0)])
    print(f"  P5(x) = {p5}")
    print(f"  P6(x) = {p6}")
    sum3 = p5 + p6
    print(f"  P5(x) + P6(x) = {sum3} (is_zero: {sum3.is_zero()})")

    print("\n--- Example 4: Evaluation at x = 3 ---")
    val = sum1.evaluate(3)
    print(f"  Evaluating sum1 at x = 3: {sum1.display()} -> {val}")


if __name__ == "__main__":
    run_tests()
    demonstrate()

