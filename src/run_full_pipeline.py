"""
Orchestrate the full data pipeline and training runs with interactive confirmations.

Key features:
- Runs scripts in sequence (skips missing ones gracefully)
- Interactive confirmations for marked steps (stdin attached to terminal)
- Tee stdout/stderr live to console while capturing for logs and report
- Per-step logs in logs/<step>.log and a consolidated pipeline_report.txt

Usage:
  python run_full_pipeline.py

Modify the SCRIPTS list in main() to change order/args/confirmation.
"""

import os
import sys
import json
import subprocess
import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional


# ---------- Data Models ----------

@dataclass
class Step:
    script: str
    args: List[str] = field(default_factory=list)
    confirm: bool = False  # If True, run interactively and ask user input in terminal


@dataclass
class StepResult:
    command: List[str]
    status: str
    return_code: int
    started_at: str
    ended_at: str
    duration_seconds: float
    stdout: str
    stderr: str


# ---------- Utilities ----------

def ensure_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def script_exists(path: str) -> bool:
    return os.path.isfile(path)


def run_step(python_exe: str, repo_root: str, step: Step) -> StepResult:
    start_time = datetime.now()
    started_at = start_time.isoformat()
    script_path = os.path.join(repo_root, step.script)
    cmd = [python_exe, script_path] + step.args

    try:
        if step.confirm:
            proc = subprocess.Popen(
                cmd,
                stdin=sys.stdin,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout_lines: List[str] = []
            stderr_lines: List[str] = []

            def reader(stream, collector, writer):
                for line in iter(stream.readline, ''):
                    collector.append(line)
                    writer.write(line)
                    writer.flush()

            t_out = threading.Thread(target=reader, args=(proc.stdout, stdout_lines, sys.stdout))
            t_err = threading.Thread(target=reader, args=(proc.stderr, stderr_lines, sys.stderr))
            t_out.start()
            t_err.start()
            proc.wait()
            t_out.join()
            t_err.join()
            return_code = proc.returncode
            status = "success" if return_code == 0 else "failed"
            stdout = ''.join(stdout_lines)
            stderr = ''.join(stderr_lines)
        else:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            return_code = proc.returncode
            status = "success" if return_code == 0 else "failed"
            stdout = proc.stdout
            stderr = proc.stderr
    except Exception as exc:
        status = "exception"
        return_code = -1
        stdout = ""
        stderr = f"Exception while running: {exc}"

    end_time = datetime.now()
    ended_at = end_time.isoformat()
    duration_s = (end_time - start_time).total_seconds()

    return StepResult(
        command=cmd,
        status=status,
        return_code=return_code,
        started_at=started_at,
        ended_at=ended_at,
        duration_seconds=duration_s,
        stdout=stdout,
        stderr=stderr,
    )


def write_step_log(log_dir: str, step_name: str, result: StepResult) -> str:
    ensure_directory(log_dir)
    log_path = os.path.join(log_dir, f"{step_name}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"COMMAND: {' '.join(map(str, result.command))}\n")
        f.write(f"STARTED: {result.started_at}\n")
        f.write(f"ENDED:   {result.ended_at}\n")
        f.write(f"DURATION_SECONDS: {result.duration_seconds:.3f}\n")
        f.write(f"STATUS: {result.status}\n")
        f.write(f"RETURN_CODE: {result.return_code}\n\n")
        f.write("===== STDOUT =====\n")
        f.write(result.stdout or "")
        f.write("\n\n===== STDERR =====\n")
        f.write(result.stderr or "")
        f.write("\n")
    return log_path


def write_report(report_path: str, run_summary: List[Dict[str, object]]) -> None:
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Pipeline Report\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated at: {datetime.now().isoformat()}\n")
        f.write(f"Python: {sys.executable}\n")
        f.write("\n")

        for step in run_summary:
            f.write("-" * 80 + "\n")
            f.write(f"Step: {step['name']}\n")
            f.write(f"Script: {step['script']}\n")
            f.write(f"Args: {' '.join(step['args']) if step['args'] else '(none)'}\n")
            f.write(f"Interactive confirm: {'yes' if step.get('confirm') else 'no'}\n")
            if step["skipped"]:
                f.write("Status: SKIPPED (script not found)\n\n")
                continue

            res: StepResult = step["result"]  # type: ignore
            f.write(f"Status: {res.status} (code {res.return_code})\n")
            f.write(f"Started: {res.started_at}\n")
            f.write(f"Ended:   {res.ended_at}\n")
            f.write(f"Duration: {res.duration_seconds:.3f} s\n")
            f.write(f"Command: {' '.join(map(str, res.command))}\n")
            f.write(f"Log file: {step['log_path']}\n")
            f.write("\n")
            f.write("STDOUT\n")
            f.write("~~~~~~\n")
            f.write(res.stdout or "")
            f.write("\n\n")
            f.write("STDERR\n")
            f.write("~~~~~~\n")
            f.write(res.stderr or "")
            f.write("\n\n")


# ---------- Main Orchestration ----------

def main() -> None:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_root)

    python_exe = sys.executable
    logs_dir = os.path.join(repo_root, "logs")
    report_path = os.path.join(repo_root, "pipeline_report.txt")

    # Define sequence here. Set confirm=True for steps that may prompt.
    steps: List[Step] = [
        # Step("delete_magnitude_folders.py", confirm=True),  # destructive; enable manually
        # Step("delete_phase_folders.py", confirm=True),      # destructive; enable manually
        Step("convert_tif_to_png.py"),
        Step("separate_png_files.py"),
        Step("move_reflection_coefficient.py", confirm=True),
        Step("delete_post_files.py", confirm=True),
        Step("consolidate_png_files.py"),
        Step("flatten_crc_structure.py"),
        Step("count_png_files.py"),
        Step("filter_1858_files.py"),
        Step("filter_uniform_images_1858.py"),
        Step("divide_images_generic.py"),
        Step("create_histograms_for_processed.py"),
        Step("medical_image_classifier.py"),
        Step("histogram_image_classifier.py"),
        Step("divided_image_classifier.py"),
    ]

    run_summary: List[Dict[str, object]] = []

    print("Starting pipeline...\n")
    pipeline_start = datetime.now()

    for s in steps:
        step_name = os.path.splitext(os.path.basename(s.script))[0]
        step_entry: Dict[str, object] = {
            "name": step_name,
            "script": s.script,
            "args": s.args,
            "confirm": s.confirm,
            "skipped": False,
            "result": None,
            "log_path": None,
        }

        script_path = os.path.join(repo_root, s.script)
        if not script_exists(script_path):
            print(f"[SKIP] {s.script} (not found)")
            step_entry["skipped"] = True
            run_summary.append(step_entry)
            continue

        print(f"[RUN ] {s.script} {' '.join(s.args)}")
        result = run_step(python_exe, repo_root, s)
        log_path = write_step_log(logs_dir, step_name, result)
        step_entry["result"] = result
        step_entry["log_path"] = log_path
        run_summary.append(step_entry)

        # Write/refresh report after each step for durability
        write_report(report_path, run_summary)

    pipeline_end = datetime.now()
    total_duration = (pipeline_end - pipeline_start).total_seconds()

    # Append final summary block
    with open(report_path, "a", encoding="utf-8") as f:
        f.write("-" * 80 + "\n")
        f.write("Final Summary\n")
        f.write("-" * 80 + "\n")
        f.write(f"Started: {pipeline_start.isoformat()}\n")
        f.write(f"Ended:   {pipeline_end.isoformat()}\n")
        f.write(f"Total Duration: {total_duration:.3f} s\n\n")

        totals = {"success": 0, "failed": 0, "exception": 0, "skipped": 0}
        for step in run_summary:
            if step["skipped"]:
                totals["skipped"] += 1
                continue
            status = step["result"].status  # type: ignore
            if status in totals:
                totals[status] += 1
        f.write(json.dumps(totals, indent=2))
        f.write("\n")

    print(f"\nPipeline completed. Report written to: {report_path}")
    print(f"Individual logs available under: {logs_dir}")


if __name__ == "__main__":
    main()


