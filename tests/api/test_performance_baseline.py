"""
Opt-in API performance baseline tests.

These tests are excluded from normal runs and are meant for lightweight,
repeatable local/CI timing checks rather than strict benchmarking.
"""

import os
import time

import pytest


@pytest.mark.api
@pytest.mark.performance
def test_api_login_performance_baseline(auth_client):
    """Verify the login endpoint stays within a conservative latency budget."""
    if os.getenv("RUN_PERFORMANCE", "").lower() != "true":
        pytest.skip("Performance baselines are opt-in")

    durations = []
    for _ in range(5):
        start = time.perf_counter()
        result = auth_client.login("testuser@example.com", "password123")
        durations.append(time.perf_counter() - start)
        assert result["status_code"] == 200

    average_duration = sum(durations) / len(durations)
    worst_case = max(durations)

    assert (
        average_duration < 0.5
    ), f"Average login latency too high: {average_duration:.3f}s"
    assert worst_case < 1.0, f"Worst-case login latency too high: {worst_case:.3f}s"
