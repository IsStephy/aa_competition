import os
import csv
import shutil
import tempfile
import subprocess
import stat

CSV_FILE = 'github_links.csv'  # Make sure this is in the same folder
OUTPUT_DIR = 'Algorithms'

def force_remove_readonly(func, path, _):
    """Fixes Windows permission error when deleting read-only Git files."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        url = row.get("Link to the GitHub:") or row.get("Link to the GitHub")
        if not url or not url.strip().startswith("http"):
            continue

        print(f"\n📦 Cloning: {url}")
        tmp_dir = tempfile.mkdtemp()

        try:
            # Clone repo shallowly to avoid .git issues
            subprocess.run(["git", "clone", "--depth", "1", url, tmp_dir], check=True)

            for root, _, files in os.walk(tmp_dir):
                for file in files:
                    if file.endswith(".py") and not file.lower().startswith("readme"):
                        src_path = os.path.join(root, file)
                        base_name = os.path.basename(file)

                        # Avoid overwriting by prefixing with repo name if needed
                        repo_name = url.rstrip("/").split("/")[-1]
                        dst_filename = f"{repo_name}_{base_name}"
                        dst_path = os.path.join(OUTPUT_DIR, dst_filename)

                        shutil.copy(src_path, dst_path)
                        print(f"  ✓ Copied {base_name} → {dst_filename}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clone {url}: {e}")
        except Exception as ex:
            print(f"⚠️ Unexpected error: {ex}")
        finally:
            shutil.rmtree(tmp_dir, onerror=force_remove_readonly)

print(f"\n✅ Done! All Python files collected in '{OUTPUT_DIR}'")
