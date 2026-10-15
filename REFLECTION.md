# Part B: Reflection

### 1. How many tests did you write in Part A, and how many lines of production code? What is the ratio?
In Part A, we wrote **9 unit tests** in `test_kitchen.py` (`test_multiplication`, `test_multiplication_returns_a_new_quantity`, `test_equality`, `test_grams_are_not_ounces`, `test_simple_addition`, `test_reduce_same_unit_needs_no_rate`, `test_mixed_addition`, `test_reduce_conversion_rate`, and `test_sum_times`). The production file `kitchen.py` contains **40 lines of non-empty code** (59 lines total including docstrings/formatting). This yields a ratio of approximately **1 test per 4.4 lines of production code** (or about 1.6 lines of test code for every line of production code), demonstrating that the test harness constitutes a substantial portion of the codebase in TDD.

### 2. When was your bar red for the longest time, and what made it last so long?
The bar stayed red the longest during **Step A7 (Mixed units and conversion rates)**. This occurred because transitioning from same-unit additions to mixed-unit conversions required updating the signature and behavior across multiple interconnected classes: `Converter` needed an internal rates table with identity fallbacks, while `Quantity.reduce` and `Sum.reduce` had to be modified to accept `(converter, unit)` to perform rate lookups. Coordinating changes across three classes simultaneously before all tests passed again made this step take the longest time in red.

### 3. Find one place where you used Fake It, one where you triangulated, and one where you used Obvious Implementation. Looking back, was each choice right?
- **Fake It:** In Step A1, we hardcoded `self.amount = 600`, and in Step A6, `plus` initially returned `grams(500)`. This was the right choice because it quickly verified that test discovery, imports, and assertion mechanics functioned properly before writing domain logic.
- **Triangulate:** In Step A2, adding `test_multiplication_by_two` forced out the hardcoded constant 600 and drove the generalization to `self.amount * multiplier`. This was the right choice to keep step sizes small and justify why the general formula was introduced.
- **Obvious Implementation:** In Step A8, implementing `times` on `Sum` by recursively multiplying `left` and `right` was done via Obvious Implementation. Since the expression structure and delegation mechanism were already firmly established in A6 and A7, writing the obvious recursive step was completely safe and passed immediately.

### 4. Which items are still on your test list? Which would you implement next, and which should you delete because they were speculation?
All 7 items originally on the test list were implemented, tested, and marked as complete.
- **Implement next:** Handling missing conversion rates explicitly (e.g., raising an `UnknownConversionError` if a requested unit conversion rate is missing in `Converter`), as well as operations like subtraction or non-integer scaling.
- **Delete / Speculation:** Implementing hashing (`__hash__`) or supporting arbitrary nested volume/weight cross-conversions without clear demand. These should be deleted from immediate backlogs because no active requirements or tests demand them.

### 5. Look at Quantity.reduce. If you had designed the whole system on paper first, would you have written this method?
Probably not. If designed upfront on paper, a single `Quantity` would be thought of as already reduced, making a `reduce` method on `Quantity` seem redundant. However, in TDD, `Quantity.reduce` emerged naturally because `Converter.reduce(source, unit)` needed to treat both single quantities and compound `Sum` expressions identically through polymorphism. TDD guided us directly into the Composite/Interpreter pattern without speculative architecture.

### 6. In Part 0 you wrote the tests after the code, and in Part A before it. How did the two feel different, and which tests shaped your design?
Writing tests after the code in Part 0 felt like an audit or inspection process—verifying existing implementations and finding boundary bugs (such as `shipping.py` edge cases). In contrast, writing tests first in Part A felt like an interactive design process where the tests acted as the API's first consumer. Crucially, `test_multiplication_returns_a_new_quantity` shaped the design by turning `Quantity` into an immutable Value Object, `test_equality` made assertions expressive and ergonomic, and `test_simple_addition` drove the creation of deferred expression objects (`Sum`) and polymorphic reduction.
