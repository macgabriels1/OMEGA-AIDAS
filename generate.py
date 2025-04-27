import os
import subprocess
from pathlib import Path
import openai


# ————— Configuration —————

openai.api_key = os.getenv("OPENAI_API_KEY")
TEMPLATES_DIR = Path("prompt_templates")
CODE_OUTPUT_DIR = Path("generated_code")
TEST_COMMAND = ["pytest", "--maxfail=1", "--disable-warnings", "-q"]


# ————— Helpers —————


def load_template(name: str) -> str:
    p = TEMPLATES_DIR / f"{name}.txt"
    return p.read_text(encoding="utf-8")


def generate_code(prompt: str) -> str:
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are a professional Python developer."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content


def write_code(path: str, code: str):
    out = CODE_OUTPUT_DIR / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(code, encoding="utf-8")
    print(f"Wrote {out}")


def run_tests() -> (bool, str):
    # nosec: B603  -- we’re passing a list to subprocess.run, so shell injection isn’t possible
    proc = subprocess.run(TEST_COMMAND, capture_output=True, text=True)
    return (proc.returncode == 0, proc.stdout + proc.stderr)


# ————— Main Loop —————


def correction_loop(template_name: str, output_path: str, max_iters: int = 3):
    for i in range(1, max_iters + 1):
        print(f"\n=== Iteration {i} ===")
        prompt = load_template(template_name)
        code = generate_code(prompt)
        write_code(output_path, code)
        passed, results = run_tests()
        if passed:
            print("🎉 All tests passed on iteration", i)
            return

        # New: show exactly what pytest printed
        print("❌ Tests failed on iteration", i)
        print("----- PYTEST OUTPUT BEGIN -----")
        print(results)
        print("------ PYTEST OUTPUT END ------")

        print("↻ Retrying with test failures appended to prompt…")
        prompt += (
            "\n\n# Test failures:\n```\n" + results + "\n```\nPlease fix the code."
        )

    print("⚠️ Reached max iterations without passing all tests.")


if __name__ == "__main__":
    correction_loop("core_api", "omega_aidas/core/api.py")
