import subprocess

class InstallerAgent:
    def _init_(self):
        pass

    def install_package(self, package_name):
        print(f"🛠 Installing: {package_name}")
        try:
            result = subprocess.run(
                ["sudo", "apt", "install", "-y", package_name],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✅ {package_name} installed successfully.")
            else:
                print(f"❌ Installation failed:\n{result.stderr}")

        except Exception as e:
            print(f"⚠ Error during installation: {e}")

    def update_packages(self):
        print("🔄 Updating package list...")
        try:
            result = subprocess.run(
                ["sudo", "apt", "update"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Package list updated.")
            else:
                print(f"❌ Update failed:\n{result.stderr}")
        except Exception as e:
            print(f"⚠ Error updating packages: {e}")