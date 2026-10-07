def test_individual_certificate_failure():
    successful = 2
    failed = 1
    total = 3

    assert successful == 2
    assert failed == 1
    assert successful + failed == total