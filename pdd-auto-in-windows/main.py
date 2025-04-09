import time
import subprocess
import os
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def is_chrome_running():
    """
    Check if Chrome is already running with the remote debugging port.
    This uses `wmic` to list command line arguments of running chrome.exe processes.
    """
    try:
        output = subprocess.check_output(
            'wmic process where "name=\'chrome.exe\'" get CommandLine',
            shell=True,
            encoding='utf-8',
            stderr=subprocess.DEVNULL
        )
        for line in output.splitlines():
            if "--remote-debugging-port=9222" in line:
                return True
    except subprocess.CalledProcessError:
        pass
    return False


def get_chrome_path():
    """
    Return the correct Chrome executable path by checking common install locations.
    """
    possible_paths = [
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("Google Chrome executable not found in standard locations.")


def start_chrome_with_debug_port():
    """
    Launch Chrome with the remote debugging port enabled.
    This allows Selenium to attach to the browser session.
    """
    print("Attempting to launch Chrome with remote debugging enabled...")

    chrome_path = get_chrome_path()
    user_data_dir = r"C:/Users/OrekiYuta/AppData/Local/Google/Chrome/User Data/"

    subprocess.Popen([
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("Waiting for Chrome to start...")
    time.sleep(3)


def main():
    try:
        # Step 0: Start Chrome if it's not already running with the debugging port
        if not is_chrome_running():
            start_chrome_with_debug_port()
        else:
            print("Chrome is already running. Skipping launch.")

        # Step 1: Start ChromeDriver and attach to the existing Chrome session
        print("Launching ChromeDriver...")

        chromedriver_autoinstaller.install(cwd=True)
        chrome_options = Options()
        chrome_options.debugger_address = "127.0.0.1:9222"
        driver = webdriver.Chrome(options=chrome_options)

        # Step 2: Navigate to the Pixiv bookmarks page
        print("Opening Pixiv page...")
        url = 'https://www.pixiv.net/bookmark_new_illust.php'
        driver.get(url)

        # Step 3: Wait for the page to fully load
        print("Waiting for the page to load...")
        driver.implicitly_wait(60)

        # Step 4: Execute JavaScript to trigger UI actions in the page
        print("Clicking to open the control panel...")
        driver.execute_script("document.getElementById(\"openCenterPanelBtn\").click();")

        print("Clicking to start the download process...")
        driver.execute_script("""
            document.querySelector('body > div.centerWrap.showBlobKeywords.lang_zh-cn > div.centerWrap_con.beautify_scrollbar > slot > form > div:nth-child(1) > div > slot:nth-child(2) > button:nth-child(1)').click();
        """)

        # Step 5: Monitor download status until completed or timeout
        print("Waiting for Powerful Pixiv Downloader to finish downloading...")
        allow_time = 3600  # Max time allowed for download in seconds (1 hour)
        sleep_time = 60  # Interval between checks (6 minutes)
        end_time = time.time() + allow_time

        while time.time() < end_time:
            time.sleep(sleep_time)
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print("Downloading... " + current_time)

            element = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/slot/form/div[2]/slot[1]/div/div[2]/span[2]")
            if "完毕" in element.text:
                print("All downloads completed!")
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Ensure the browser is properly closed
        if 'driver' in locals() and driver is not None:
            driver.quit()


if __name__ == '__main__':
    main()
