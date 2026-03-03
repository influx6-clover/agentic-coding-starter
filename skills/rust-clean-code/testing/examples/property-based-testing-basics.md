# Property-Based Testing Examples

This document shows basic examples of property-based testing with proptest. For comprehensive coverage, see `intro-to-property-based-testing.md`.

## Basic Usage

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_reverse_reverse_is_identity(ref s in ".*") {
        let reversed: String = s.chars().rev().collect();
        let double_reversed: String = reversed.chars().rev().collect();
        assert_eq!(s, &double_reversed);
    }

    #[test]
    fn test_parse_format_roundtrip(x in 0..1000u32) {
        let formatted = format!("{}", x);
        let parsed: u32 = formatted.parse().unwrap();
        assert_eq!(x, parsed);
    }

    #[test]
    fn test_addition_commutative(a in 0..1000i32, b in 0..1000i32) {
        assert_eq!(a + b, b + a);
    }
}
```

## Common Property Testing Patterns

### Roundtrip Properties (Encode/Decode)

```rust
proptest! {
    #[test]
    fn test_json_roundtrip(data in any::<MyData>()) {
        let json = serde_json::to_string(&data).unwrap();
        let parsed: MyData = serde_json::from_str(&json).unwrap();
        assert_eq!(data, parsed);
    }
}
```

### Invariant Properties (Always True)

```rust
proptest! {
    #[test]
    fn test_sorted_output_is_sorted(ref input in prop::collection::vec(any::<i32>(), 0..100)) {
        let sorted = my_sort(input);
        // Invariant: output is sorted
        for window in sorted.windows(2) {
            assert!(window[0] <= window[1]);
        }
    }
}
```

### Comparison Properties (Against Reference Implementation)

```rust
proptest! {
    #[test]
    fn test_optimized_matches_reference(n in 1..1000u64) {
        let optimized = fast_fibonacci(n);
        let reference = slow_fibonacci(n);
        assert_eq!(optimized, reference);
    }
}
```

## When to Use Property-Based Testing

**Use property-based testing when:**
- ✅ Testing parsers/serializers (roundtrip properties)
- ✅ Testing mathematical functions (commutative, associative properties)
- ✅ Testing invariants (sorting, uniqueness, bounds)
- ✅ Finding edge cases automatically
- ✅ Validating optimizations against reference implementations

**Don't use for:**
- ❌ Specific business logic requiring exact values
- ❌ Tests where the property is trivial (just repeating implementation)
- ❌ Cases where example-based tests are clearer

## Dependencies

```toml
[dev-dependencies]
proptest = "1.4"
```

For more comprehensive coverage of property-based testing patterns and strategies, see `intro-to-property-based-testing.md`.
