import tempfile
import subprocess
import os
import urllib.request
import shutil


def create_download_link(
    publisher: str,
    name: str,
    version: str,
    target_platform: str | None = None  # feel free to use this argument
) -> str:
    """Create VSIX download link from given extension identifier and publisher.

   https://stackoverflow.com/questions/79359919
   """
    return f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{name}/{version}/vspackage" + (f"/?targetPlatform={target_platform}" if target_platform else "")


if __name__ == "__main__":

    # get all extension identifiers from the `code` cli
    result = subprocess.run(
        ["code", "--list-extensions", "--show-versions"], stdout=subprocess.PIPE)
    extensions_installed = result.stdout.decode("utf-8").split("\n")
    extensions_installed = [s for s in extensions_installed if s != ""]

    # format is: publisher.name@version
    # first, get the versions
    versions = [s.split("@")[1] for s in extensions_installed]
    # remove them from the strings
    extensions_installed = [s.split("@")[0] for s in extensions_installed]
    # then, get publishers and names
    publishers = [s.split(".")[0] for s in extensions_installed]
    names = [s.split(".")[1] for s in extensions_installed]

    assert len(publishers) == len(names) and len(names) == len(versions)
    print(f"{len(names)} extensions found:")
    print("".join([f"- {n}\n" for n in names]))
    for (publisher, name, version) in zip(publishers, names, versions):
        print(f"Attempting to download {name} {version} by {publisher} ")
        download_url = create_download_link(publisher, name, version)
        downloaded_file = f"{publisher}.{name}-{version}.vsix"
        urllib.request.urlretrieve(
            download_url, downloaded_file)

        print(f"Fixing broken zip packages")
        dst = f"{publisher}.{name}-{version}.fixed.vsix"
        tmp = tempfile.mkdtemp(prefix="vsixfix_")

        print("Fixing bad zip archives (sudo apt install libarchive-tools)")
        with tempfile.TemporaryDirectory() as tmpdirname:
            print("Extracting")
            subprocess.run(
                f"bsdtar -xf {downloaded_file} -C {tmpdirname}/".split(" "), stdout=subprocess.PIPE)
            print("Repackaging")
            shutil.make_archive(dst, 'zip', tmpdirname)
        os.rename(dst+".zip", dst)

        print(f"Installing {dst} with codium")
        subprocess.run(
            ["codium", "--install-extension", dst], check=True)
