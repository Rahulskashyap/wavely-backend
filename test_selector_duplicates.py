from news_v4.selector import is_duplicate_event


def story(title):
    return {
        "title": title,
    }


tests = [
    # =====================================================
    # SAME EVENTS — MUST BE TRUE
    # =====================================================

    (
        "Same Bengal raid",
        story(
            "Rs 28.5 crore cash, 15 kg gold bars "
            "found at ex-Bengal bus driver's home"
        ),
        story(
            "15 kg gold, Rs 20 crore in 35 sacks: "
            "Bengal police raid former bus driver"
        ),
        True,
    ),

    (
        "Same Rushdie conviction",
        story(
            "Salman Rushdie attacker convicted "
            "of terror offences"
        ),
        story(
            "Author Salman Rushdie attacker "
            "convicted on terrorism charges"
        ),
        True,
    ),

    (
        "Same arrest wording",
        story(
            "Three suspects arrested after "
            "Bengaluru bank robbery"
        ),
        story(
            "Bengaluru bank robbery: police arrest "
            "three suspects"
        ),
        True,
    ),

    # =====================================================
    # DIFFERENT EVENTS — MUST BE FALSE
    # =====================================================

    (
        "Different Trump events",
        story(
            "Trump warns Iran of major escalation"
        ),
        story(
            "Trump administration bans new "
            "Chinese humanoid robots"
        ),
        False,
    ),

    (
        "Different India cricket events",
        story(
            "India beat Australia in first ODI"
        ),
        story(
            "India squad announced for Australia "
            "Test series"
        ),
        False,
    ),

    (
        "Same person different events",
        story(
            "Virat Kohli scores century against "
            "Australia"
        ),
        story(
            "Virat Kohli announces new business "
            "investment"
        ),
        False,
    ),

    (
        "Same place different events",
        story(
            "Heavy rain causes flooding in Bengaluru"
        ),
        story(
            "Bengaluru Metro announces new route"
        ),
        False,
    ),

    (
        "Same country different events",
        story(
            "India announces new national education "
            "policy"
        ),
        story(
            "India defeats England in cricket final"
        ),
        False,
    ),

    (
        "Similar cricket wording different matches",
        story(
            "India beat Australia in first ODI"
        ),
        story(
            "India beat Australia in second ODI"
        ),
        False,
    ),
]


passed = 0


for (
    name,
    first,
    second,
    expected,
) in tests:

    actual = is_duplicate_event(
        first,
        second,
    )

    success = (
        actual == expected
    )

    print("\n------------------------------")
    print("TEST:", name)
    print("EXPECTED:", expected)
    print("ACTUAL:", actual)

    print(
        "RESULT:",
        "PASS" if success else "FAIL",
    )

    if success:
        passed += 1


print("\n==============================")
print("SUMMARY")
print("==============================")

print("PASSED:", passed)
print("FAILED:", len(tests) - passed)
print("TOTAL:", len(tests))

if passed == len(tests):
    print(
        "\nALL DUPLICATE TESTS PASSED"
    )
else:
    print(
        "\nSOME DUPLICATE TESTS FAILED"
    )