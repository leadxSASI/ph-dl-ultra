import browser_cookie3
from pathlib import Path

def export_cookies(browser_name, output_file):
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    browser_map = {
        "firefox": browser_cookie3.firefox,
        "chrome": browser_cookie3.chrome,
        "edge": browser_cookie3.edge,
    }

    if browser_name not in browser_map:
        raise ValueError(f"Unsupported browser: {browser_name}")

    cookies = browser_map[browser_name](domain_name="pornhub.com")
    with open(output_file, "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            if "pornhub" in cookie.domain:
                f.write(f"{cookie.domain}\t{'TRUE' if '.pornhub.com' in cookie.domain else 'FALSE'}\t{cookie.path}\t{'TRUE' if cookie.secure else 'FALSE'}\t{cookie.expires or 0}\t{cookie.name}\t{cookie.value}\n")
    print(f"Cookies saved to {output_file}")
