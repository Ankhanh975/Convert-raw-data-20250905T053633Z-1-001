"""
Orchestrates the full data pipeline and training runs, capturing outputs.

Features:
- Runs scripts in sequence (skips missing ones gracefully)
- Captures stdout/stderr and return codes
- Records start/end time and durations
- Writes a comprehensive pipeline_report.txt with full outputs
- Also saves individual logs per step under logs/<step_name>.log

Usage:
  python run_full_pipeline.py

Notes:
- Adjust the SCRIPTS list below to change the run order or skip steps.
- Potentially destructive cleanup scripts are commented out by default.
"""

import os
import sys
import time
import json
import shutil
import subprocess
from datetime import datetime
from typing import List, Tuple, Dict


def ensure_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def script_exists(path: str) -> bool:
    return os.path.isfile(path)


def run_script(python_exe: str, script_path: str, args: List[str], input_text: str = "") -> Dict[str, object]:
    start_time = datetime.now()
    started_at = start_time.isoformat()
    cmd = [python_exe, script_path] + args
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            input=input_text if input_text else None,
            check=False,
        )
        status = "success" if proc.returncode == 0 else "failed"
        stdout = proc.stdout
        stderr = proc.stderr
        return_code = proc.returncode
    except Exception as exc:
        status = "exception"
        stdout = ""
        stderr = f"Exception while running: {exc}"
        return_code = -1
    end_time = datetime.now()
    ended_at = end_time.isoformat()
    duration_s = (end_time - start_time).total_seconds()
    return {
        "command": cmd,
        "status": status,
        "return_code": return_code,
        "started_at": started_at,
        "ended_at": ended_at,
        "duration_seconds": duration_s,
        "stdout": stdout,
        "stderr": stderr,
    }


def write_step_log(log_dir: str, step_id: str, result: Dict[str, object]) -> str:
    ensure_directory(log_dir)
    log_path = os.path.join(log_dir, f"{step_id}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"COMMAND: {' '.join(map(str, result['command']))}\n")
        f.write(f"STARTED: {result['started_at']}\n")
        f.write(f"ENDED:   {result['ended_at']}\n")
        f.write(f"DURATION_SECONDS: {result['duration_seconds']:.3f}\n")
        f.write(f"STATUS: {result['status']}\n")
        f.write(f"RETURN_CODE: {result['return_code']}\n\n")
        f.write("===== STDOUT =====\n")
        f.write(result.get("stdout", ""))
        f.write("\n\n===== STDERR =====\n")
        f.write(result.get("stderr", ""))
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
            if step["skipped"]:
                f.write("Status: SKIPPED (script not found)\n")
                f.write("\n")
                continue

            res = step["result"]
            f.write(f"Status: {res['status']} (code {res['return_code']})\n")
            f.write(f"Started: {res['started_at']}\n")
            f.write(f"Ended:   {res['ended_at']}\n")
            f.write(f"Duration: {res['duration_seconds']:.3f} s\n")
            f.write(f"Command: {' '.join(map(str, res['command']))}\n")
            f.write(f"Auto-confirm: {'yes' if step.get('auto_confirm') else 'no'}\n")
            f.write(f"Log file: {step['log_path']}\n")
            f.write("\n")
            f.write("STDOUT\n")
            f.write("~~~~~~\n")
            f.write(res.get("stdout", ""))
            f.write("\n\n")
            f.write("STDERR\n")
            f.write("~~~~~~\n")
            f.write(res.get("stderr", ""))
            f.write("\n\n")


def main() -> None:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_root)

    python_exe = sys.executable
    logs_dir = os.path.join(repo_root, "logs")
    report_path = os.path.join(repo_root, "pipeline_report.txt")

    # Curated sequence. Each entry may set confirm=True to auto-send 'y\n' to stdin.
    SCRIPTS: List[Dict[str, object]] = [
        # {"script": "delete_magnitude_folders.py", "args": [], "confirm": True},
        # {"script": "delete_phase_folders.py", "args": [], "confirm": True},
        {"script": "convert_tif_to_png.py", "args": []},
        {"script": "separate_png_files.py", "args": []},
        {"script": "move_reflection_coefficient.py", "args": [], "confirm": True},
        {"script": "delete_post_files.py", "args": [], "confirm": True},
        {"script": "consolidate_png_files.py", "args": []},
        {"script": "flatten_crc_structure.py", "args": []},
        {"script": "count_png_files.py", "args": []},
        {"script": "filter_1858_files.py", "args": []},
        {"script": "filter_uniform_images_1858.py", "args": []},
        {"script": "divide_images_generic.py", "args": []},
        {"script": "create_histograms_for_processed.py", "args": []},
        {"script": "medical_image_classifier.py", "args": []},
        {"script": "histogram_image_classifier.py", "args": []},
        {"script": "divided_image_classifier.py", "args": []},
    ]

    run_summary: List[Dict[str, object]] = []

    print("Starting pipeline...\n")
    pipeline_start = datetime.now()

    for step in SCRIPTS:
        script = str(step.get("script"))
        args = list(step.get("args", []))
        confirm = bool(step.get("confirm", False))
        confirm_text = str(step.get("confirm_text", "y\n"))
        step_name = os.path.splitext(os.path.basename(script))[0]
        step_entry: Dict[str, object] = {
            "name": step_name,
            "script": script,
            "args": args,
            "auto_confirm": confirm,
            "skipped": False,
            "result": None,
            "log_path": None,
        }

        if not script_exists(os.path.join(repo_root, script)):
            print(f"[SKIP] {script} (not found)")
            step_entry["skipped"] = True
            run_summary.append(step_entry)
            continue

        print(f"[RUN ] {script} {' '.join(args)}")
        input_text = confirm_text if confirm else ""
        result = run_script(python_exe, os.path.join(repo_root, script), args, input_text=input_text)
        log_path = write_step_log(logs_dir, step_name, result)
        step_entry["result"] = result
        step_entry["log_path"] = log_path
        run_summary.append(step_entry)

        # Flush partial report after each step for safety
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

        totals = {
            "success": 0,
            "failed": 0,
            "exception": 0,
            "skipped": 0,
        }
        for step in run_summary:
            if step["skipped"]:
                totals["skipped"] += 1
                continue
            status = step["result"]["status"]
            if status in totals:
                totals[status] += 1
        f.write(json.dumps(totals, indent=2))
        f.write("\n")

    print(f"\nPipeline completed. Report written to: {report_path}")
    print(f"Individual logs available under: {logs_dir}")


if __name__ == "__main__":
    main()


