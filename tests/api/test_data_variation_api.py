"""
Opt-in API tests that use seeded Faker data for broader input coverage.

These tests are not part of the core deterministic regression path; they
complement it with reproducible variation.
"""

import pytest


@pytest.mark.api
@pytest.mark.data_variation
def test_api_form_submission_accepts_seeded_faker_payload(forms_client, fake_data, fake_data_seed):
    """Submit a valid seeded Faker payload and verify it is accepted."""
    name = fake_data.name()
    email = fake_data.email()
    message = f"{fake_data.sentence(nb_words=8)} Seed:{fake_data_seed}"

    result = forms_client.submit_form(name, email, message)

    assert result["status_code"] == 201, (
        f"Seed {fake_data_seed} produced an unexpected failure: {result['body']}"
    )
    assert result["body"]["success"] is True
