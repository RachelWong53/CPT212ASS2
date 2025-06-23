def bad_character_table(pattern):
    """
    Build the bad character table for Boyer-Moore algorithm.
    Maps each character to its rightmost occurrence in the pattern.
    """
    table = {}
    for i, char in enumerate(pattern):
        table[char] = i
    return table


def good_suffix_table(pattern):
    """
    Build the good suffix table for Boyer-Moore algorithm.
    """
    m = len(pattern)
    good_suffix = [0] * m
    suffixes = [0] * m
    suffixes[m - 1] = m
    g = m - 1
    f = 0

    # Compute suffixes array
    for i in range(m - 2, -1, -1):
        if i > g and suffixes[i + m - 1 - f] < i - g:
            suffixes[i] = suffixes[i + m - 1 - f]
        else:
            if i < g:
                g = i
            f = i
            while g >= 0 and pattern[g] == pattern[g + m - 1 - f]:
                g -= 1
            suffixes[i] = f - g

    # Initialize good suffix table
    for i in range(m):
        good_suffix[i] = m

    # Case 1: Pattern has a suffix that occurs elsewhere
    j = 0
    for i in range(m - 1, -1, -1):
        if suffixes[i] == i + 1:
            while j < m - 1 - i:
                if good_suffix[j] == m:
                    good_suffix[j] = m - 1 - i
                j += 1

    # Case 2: Pattern has a suffix that occurs as a prefix
    for i in range(m - 1):
        good_suffix[m - 1 - suffixes[i]] = m - 1 - i

    return good_suffix


def boyer_moore_search(text, pattern):
    """
    Complete Boyer-Moore search using both bad character and good suffix rules.
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    # Build preprocessing tables
    bad_char = bad_character_table(pattern)
    good_suffix = good_suffix_table(pattern)

    matches = []
    n = len(text)
    m = len(pattern)
    i = 0  # Position in text

    while i <= n - m:
        # Start matching from rightmost character
        j = m - 1

        # Compare characters from right to left
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1

        if j < 0:
            # Complete match found
            matches.append(i)
            print(f"Pattern found at index: {i}")
            # Shift using good suffix rule
            i += good_suffix[0]
        else:
            # Mismatch at position j
            # Calculate shifts using both rules
            bad_char_shift = max(1, j - bad_char.get(text[i + j], -1))
            good_suffix_shift = good_suffix[j]

            # Take maximum shift for optimal performance
            i += max(bad_char_shift, good_suffix_shift)

    return matches


def test_boyer_moore():
    """
    Test the complete Boyer-Moore algorithm
    """
    print("Complete Boyer-Moore Algorithm Test")
    print("=" * 50)

    test_cases = [
        ("ABAAABCDABC", "ABC"),
        ("ABABDABACDABABCABCABCABCABC", "ABABCABCABCABC"),
        ("HELLO WORLD", "WORLD"),
        ("MISSISSIPPI", "ISSI"),
        ("AAAAAAAAAA", "AAA"),
        ("ABCDEFGH", "XYZ"),
        ("ABCABCABCABC", "ABCABC"),  # Additional test for good suffix
    ]

    for i, (text, pattern) in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Text: '{text}'")
        print(f"Pattern: '{pattern}'")

        # Show preprocessing tables
        bad_char = bad_character_table(pattern)
        good_suffix = good_suffix_table(pattern)
        print(f"Bad Character Table: {bad_char}")
        print(f"Good Suffix Table: {good_suffix}")

        # Perform search
        matches = boyer_moore_search(text, pattern)

        if matches:
            print(f"Matches found at positions: {matches}")
            # Verify each match
            for pos in matches:
                substr = text[pos:pos+len(pattern)]
                print(f"  Position {pos}: '{substr}' == '{pattern}': {substr == pattern}")
        else:
            print("No matches found")


if __name__ == "__main__":
    test_boyer_moore()