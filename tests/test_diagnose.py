"""Offline tests for setup diagnostics. Google bodies were recorded from failed Vertex calls
in October 2026, with project IDs replaced. No API calls."""

import io
import os
import unittest
from datetime import date
from unittest.mock import patch

import anthropic
import httpx
import openai
from google.auth.exceptions import DefaultCredentialsError, RefreshError
from google.genai.errors import ClientError, ServerError

from course_game.diagnose import check_settings, diagnose, render
from course_game.narrator import NarrationError

VERTEX = {"GOOGLE_CLOUD_PROJECT": "student-course-project", "GOOGLE_CLOUD_LOCATION": "global",
          "COURSE_MODEL": "gemini-3.5-flash-lite"}
TODAY = date(2026, 10, 17)


def google_error(code, reason=None, metadata=None, message="test message"):
    error = {"code": code, "message": message, "status": "PERMISSION_DENIED"}
    if reason:
        error["details"] = [{"@type": "type.googleapis.com/google.rpc.ErrorInfo", "reason": reason,
                             "domain": "googleapis.com", "metadata": metadata or {}}]
    return ClientError(code, {"error": error})


BILLING_OFF = google_error(403, "BILLING_DISABLED", {
    "consoleUrl": "https://console.developers.google.com/billing/enable?project=student-course-project",
    "containerInfo": "student-course-project", "service": "aiplatform.googleapis.com",
    "consumer": "projects/student-course-project"})
API_OFF = google_error(403, "SERVICE_DISABLED", {
    "consumer": "projects/student-course-project",
    "activationUrl": "https://console.developers.google.com/apis/api/aiplatform.googleapis.com/overview"
                     "?project=student-course-project",
    "service": "aiplatform.googleapis.com", "serviceTitle": "Agent Platform API"})
NO_PROJECT = google_error(403, "CONSUMER_INVALID", {
    "containerInfo": "student-course-project", "service": "aiplatform.googleapis.com",
    "consumer": "projects/student-course-project"},
    "Permission denied on resource project student-course-project.")
NO_MODEL = ClientError(404, {"error": {"code": 404, "status": "NOT_FOUND", "message":
    "Publisher model `projects/student-course-project/locations/global/publishers/google/models/"
    "gemini-0-nonexistent` was not found or your project does not have access to it."}})
BAD_LOCATION = ClientError(404, {"message": "<!DOCTYPE html>\n<html lang=en>\n  <title>Error 404 (Not Found)!!1</title>"})


def text(finding):
    return render("live model response", finding)


def status_error(sdk, cls, status, body):
    url = "https://api.openai.com/v1/responses" if sdk is openai else "https://api.anthropic.com/v1/messages"
    return cls("test", response=httpx.Response(status, request=httpx.Request("POST", url)), body=body)


class Render(unittest.TestCase):
    def test_problem_then_indented_fix(self):
        out = text(diagnose(BILLING_OFF, "vertex", VERTEX))
        lines = out.splitlines()
        self.assertTrue(lines[0].startswith("FAIL live model response: billing is off for project student-course-project"))
        self.assertTrue(lines[1].lstrip().startswith("Fix:"))
        self.assertTrue(all(line.startswith(" ") for line in lines[1:]))


class Settings(unittest.TestCase):
    def problems(self, provider, env):
        return [(f.level, f.problem) for f in check_settings(provider, env, TODAY)]

    def test_good_vertex_settings_pass(self):
        self.assertEqual(check_settings("vertex", VERTEX, TODAY), [])

    def test_missing_setting_names_variable_and_command(self):
        env = {**VERTEX}
        del env["GOOGLE_CLOUD_PROJECT"]
        [finding] = check_settings("vertex", env, TODAY)
        self.assertEqual(finding.level, "FAIL")
        self.assertIn("GOOGLE_CLOUD_PROJECT", finding.problem)
        self.assertIn("export GOOGLE_CLOUD_PROJECT=", "\n".join(finding.fix))

    def test_placeholders_from_the_readme_and_page(self):
        for name, value in (("GOOGLE_CLOUD_PROJECT", "YOUR_PROJECT_ID"), ("GOOGLE_CLOUD_PROJECT", "YOUR_COURSE_PROJECT"),
                            ("GOOGLE_CLOUD_LOCATION", "replace-with-approved-location"),
                            ("COURSE_MODEL", "[Placeholder: funded Gemini model ID, instructor decision]"),
                            ("COURSE_MODEL", "YOUR_CHOSEN_MODEL_ID")):
            with self.subTest(value=value):
                [finding] = check_settings("vertex", {**VERTEX, name: value}, TODAY)
                self.assertEqual(finding.level, "FAIL")
                self.assertIn("placeholder", finding.problem)

    def test_project_name_instead_of_id(self):
        [finding] = check_settings("vertex", {**VERTEX, "GOOGLE_CLOUD_PROJECT": "Game Dev F26"}, TODAY)
        self.assertIn("project ID", finding.problem)
        self.assertIn("gcloud projects list", "\n".join(finding.fix))

    def test_unknown_location_shape(self):
        [finding] = check_settings("vertex", {**VERTEX, "GOOGLE_CLOUD_LOCATION": "us central"}, TODAY)
        self.assertIn("export GOOGLE_CLOUD_LOCATION='global'", "\n".join(finding.fix))

    def test_known_locations_pass(self):
        for location in ("global", "us", "eu", "us-central1", "europe-west4"):
            with self.subTest(location=location):
                self.assertEqual(check_settings("vertex", {**VERTEX, "GOOGLE_CLOUD_LOCATION": location}, TODAY), [])

    def test_retired_model_fails_before_any_call(self):
        [finding] = check_settings("vertex", {**VERTEX, "COURSE_MODEL": "gemini-2.5-flash"}, date(2026, 10, 20))
        self.assertEqual(finding.level, "FAIL")
        self.assertIn("retired", finding.problem)
        self.assertIn("export COURSE_MODEL='gemini-3.5-flash-lite'", "\n".join(finding.fix))

    def test_model_retiring_soon_warns(self):
        [finding] = check_settings("vertex", {**VERTEX, "COURSE_MODEL": "gemini-3.6-flash"}, TODAY)
        self.assertEqual(finding.level, "WARN")
        self.assertIn("2026-11-19", finding.problem)

    def test_claude_model_with_vertex_provider(self):
        [finding] = check_settings("vertex", {**VERTEX, "COURSE_MODEL": "claude-sonnet-5-5"}, TODAY)
        self.assertEqual(finding.level, "FAIL")
        self.assertIn("--provider anthropic", "\n".join(finding.fix))

    def test_gemini_model_with_openai_provider(self):
        env = {"OPENAI_API_KEY": "sk-test-key-value", "COURSE_MODEL": "gemini-3.5-flash-lite"}
        [finding] = check_settings("openai", env, TODAY)
        self.assertIn("--provider vertex", "\n".join(finding.fix))

    def test_key_value_is_never_printed(self):
        env = {"ANTHROPIC_API_KEY": "secret-looking-value", "COURSE_MODEL": "claude-sonnet-5-5"}
        for finding in check_settings("anthropic", env, TODAY):
            self.assertNotIn("secret-looking-value", text(finding))

    def test_placeholder_key(self):
        env = {"OPENAI_API_KEY": "YOUR_OPENAI_KEY", "COURSE_MODEL": "gpt-5-mini"}
        [finding] = check_settings("openai", env, TODAY)
        self.assertEqual(finding.level, "FAIL")


class Google(unittest.TestCase):
    def test_billing_disabled_links_to_the_projects_billing_page(self):
        out = text(diagnose(BILLING_OFF, "vertex", VERTEX))
        self.assertIn("https://console.developers.google.com/billing/enable?project=student-course-project", out)
        self.assertIn("step 4", out)

    def test_api_disabled_uses_googles_activation_link_and_both_names(self):
        out = text(diagnose(API_OFF, "vertex", VERTEX))
        self.assertIn("Vertex AI API", out)
        self.assertIn("Agent Platform API", out)
        self.assertIn("apis/api/aiplatform.googleapis.com/overview?project=student-course-project", out)

    def test_project_missing_or_not_yours(self):
        out = text(diagnose(NO_PROJECT, "vertex", VERTEX))
        self.assertIn("student-course-project", out)
        self.assertIn("gcloud projects list", out)

    def test_permission_denied_on_someone_elses_project(self):
        error = google_error(403, "IAM_PERMISSION_DENIED", {"permission": "aiplatform.endpoints.predict"})
        self.assertIn("permission", diagnose(error, "vertex", VERTEX).problem)

    def test_unknown_model(self):
        out = text(diagnose(NO_MODEL, "vertex", {**VERTEX, "COURSE_MODEL": "gemini-0-nonexistent"}))
        self.assertIn("gemini-0-nonexistent", out)
        self.assertIn("export COURSE_MODEL='gemini-3.5-flash-lite'", out)

    def test_bad_location_comes_back_as_an_html_404(self):
        finding = diagnose(BAD_LOCATION, "vertex", {**VERTEX, "GOOGLE_CLOUD_LOCATION": "us-centrl1"})
        self.assertIn("'us-centrl1' is not a Vertex AI location", finding.problem)
        self.assertIn("export GOOGLE_CLOUD_LOCATION='global'", text(finding))

    def test_rate_limited(self):
        error = ClientError(429, {"error": {"code": 429, "status": "RESOURCE_EXHAUSTED", "message": "Resource exhausted."}})
        self.assertIn("Wait a minute", text(diagnose(error, "vertex", VERTEX)))

    def test_server_error_is_temporary(self):
        error = ServerError(503, {"error": {"code": 503, "status": "UNAVAILABLE", "message": "unavailable"}})
        self.assertIn("temporary", diagnose(error, "vertex", VERTEX).problem)

    def test_no_sign_in(self):
        error = DefaultCredentialsError("Your default credentials were not found.")
        self.assertIn("gcloud auth application-default login", text(diagnose(error, "vertex", VERTEX)))

    def test_sign_in_file_setting_points_nowhere(self):
        env = {**VERTEX, "GOOGLE_APPLICATION_CREDENTIALS": "/nowhere/adc.json"}
        out = text(diagnose(DefaultCredentialsError("File /nowhere/adc.json was not found."), "vertex", env))
        self.assertIn("unset GOOGLE_APPLICATION_CREDENTIALS", out)

    def test_expired_sign_in(self):
        out = text(diagnose(RefreshError("invalid_grant: Bad Request"), "vertex", VERTEX))
        self.assertIn("gcloud auth application-default login", out)

    def test_no_connection(self):
        self.assertIn("internet", text(diagnose(httpx.ConnectError("boom"), "vertex", VERTEX)))


class OpenAIErrors(unittest.TestCase):
    env = {"OPENAI_API_KEY": "sk-test", "COURSE_MODEL": "gpt-5-mini"}

    def test_no_api_credit_explains_chatgpt_plus(self):
        error = status_error(openai, openai.RateLimitError, 429, {
            "message": "You exceeded your current quota, please check your plan and billing details.",
            "type": "insufficient_quota", "param": None, "code": "insufficient_quota"})
        out = text(diagnose(error, "openai", self.env))
        self.assertIn("ChatGPT Plus", out)
        self.assertIn("--provider vertex", out)

    def test_bad_key_never_echoes_openais_message(self):
        error = status_error(openai, openai.AuthenticationError, 401, {
            "message": "Incorrect API key provided: sk-abc123***wxyz.", "type": "invalid_request_error",
            "code": "invalid_api_key", "param": None})
        out = text(diagnose(error, "openai", self.env))
        self.assertIn("OPENAI_API_KEY", out)
        self.assertNotIn("sk-abc123", out)

    def test_unknown_model(self):
        error = status_error(openai, openai.NotFoundError, 404, {
            "message": "The model `gpt-x` does not exist or you do not have access to it.",
            "type": "invalid_request_error", "code": "model_not_found", "param": None})
        self.assertIn("gpt-5-mini", diagnose(error, "openai", self.env).problem)


class AnthropicErrors(unittest.TestCase):
    env = {"ANTHROPIC_API_KEY": "sk-ant-test", "COURSE_MODEL": "claude-haiku-5-5"}

    def test_bad_key(self):
        error = status_error(anthropic, anthropic.AuthenticationError, 401, {
            "type": "error", "error": {"type": "authentication_error", "message": "invalid x-api-key"}})
        self.assertIn("ANTHROPIC_API_KEY", text(diagnose(error, "anthropic", self.env)))

    def test_no_credit_as_billing_error(self):
        error = status_error(anthropic, anthropic.APIStatusError, 402, {
            "type": "error", "error": {"type": "billing_error", "message": "Billing problem."}})
        self.assertIn("credit", diagnose(error, "anthropic", self.env).problem)

    def test_no_credit_as_bad_request(self):
        error = status_error(anthropic, anthropic.BadRequestError, 400, {
            "type": "error", "error": {"type": "invalid_request_error",
                                       "message": "Your credit balance is too low to access the Anthropic API."}})
        self.assertIn("credit", diagnose(error, "anthropic", self.env).problem)

    def test_overloaded_is_temporary(self):
        error = status_error(anthropic, anthropic.OverloadedError, 529, {
            "type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}})
        self.assertIn("Wait", text(diagnose(error, "anthropic", self.env)))


class Other(unittest.TestCase):
    def test_reply_failed_the_narrator_checks(self):
        out = text(diagnose(NarrationError("The narrator cited an unavailable fact."), "vertex", VERTEX))
        self.assertIn("unavailable fact", out)
        self.assertIn("gemini-3.8-flash", out)

    def test_unknown_error_asks_for_a_screenshot_and_hides_keys(self):
        out = text(diagnose(RuntimeError("odd failure with sk-ant-api03-abcdefghijkl"), "anthropic", {}))
        self.assertIn("instructor and TAs", out)
        self.assertNotIn("abcdefghijkl", out)


class SetupCheck(unittest.TestCase):
    def run_setup(self, env, narrate_effect=None):
        from course_game.setup_check import main
        ok = type("Done", (), {"returncode": 0})()
        with patch.dict(os.environ, env, clear=True), patch("sys.argv", ["setup_check", "--provider", "vertex", "--headless"]), \
                patch("subprocess.run", return_value=ok), \
                patch("course_game.setup_check.narrate", side_effect=narrate_effect) as call, \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            code = main()
        return code, output.getvalue(), call

    def test_placeholder_settings_stop_before_the_live_call(self):
        code, out, call = self.run_setup({**VERTEX, "GOOGLE_CLOUD_PROJECT": "YOUR_PROJECT_ID"})
        self.assertEqual(code, 1)
        call.assert_not_called()
        self.assertIn("FAIL settings: GOOGLE_CLOUD_PROJECT", out)
        self.assertIn("no live call was made", out)

    def test_failed_call_prints_the_fix(self):
        code, out, call = self.run_setup(VERTEX, BILLING_OFF)
        self.assertEqual(code, 1)
        self.assertIn("billing/enable?project=student-course-project", out)
        self.assertIn("SETUP INCOMPLETE", out)


class Game(unittest.TestCase):
    def test_game_names_the_problem_and_points_to_setup_check(self):
        from course_game.__main__ import main
        with patch.dict(os.environ, VERTEX, clear=True), patch("sys.argv", ["game", "--provider", "vertex"]), \
                patch("builtins.input", side_effect=["ask look", "quit"]), \
                patch("course_game.__main__.narrate", side_effect=BILLING_OFF), \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            main()
        self.assertIn("billing is off for project student-course-project", output.getvalue())
        self.assertIn("setup_check", output.getvalue())


if __name__ == "__main__":
    unittest.main()
