import asyncio
from playwright.async_api import async_playwright
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def annotate_elements(page):
    with open("mark_page.js") as f:
        mark_page_script = f.read()
    return await page.evaluate(mark_page_script + "; markPage();")

async def run_positive_test():
    test_result = {
        "test_name": "Convert MP4 to AVI with HD 720p Resolution",
        "status": "Not Started",
        "description": "",
        "failed_steps": "N/A"
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            await page.goto("https://video-converter.com/")
            print("Navigated to video converter site.")
            await asyncio.sleep(2)

            bounding_boxes = await annotate_elements(page)
            print("Bounding boxes marked on the page.")

            steps = [
                {"action": "upload_file", "label": "Open file"},
                {"action": "select_format", "label": "avi"},
                {"action": "select_resolution", "label": "Same as source"},
                {"action": "select_hd_720p"},
                {"action": "start_conversion", "label": "Convert"}
            ]
            current_step = 0

            while current_step < len(steps):
                step = steps[current_step]
                action = step["action"]
                label = step.get("label")

                if action != "select_hd_720p":
                    box = next((box for box in bounding_boxes if label and label.lower() in box["text"].lower()), None)
                    if not box:
                        raise Exception(f"{label} not found on the page.")

                if action == "upload_file":
                    await page.set_input_files("input[type='file']", "/Users/waseem/Downloads/videoplayback.mp4")
                    await asyncio.sleep(10)

                elif action == "select_format":
                    await page.mouse.click(box["x"], box["y"])
                    await asyncio.sleep(2)
                    bounding_boxes = await annotate_elements(page)
                
                elif action == "select_resolution":
                    await page.mouse.click(box["x"], box["y"])
                    await asyncio.sleep(1)

                elif action == "select_hd_720p":
                    bounding_boxes = await annotate_elements(page)
                    hd_720p_box = next((box for box in bounding_boxes if "HD 720p" in box["text"]), None)
                    if hd_720p_box:
                        await page.mouse.click(hd_720p_box["x"], hd_720p_box["y"])
                        await asyncio.sleep(20)
                    else:
                        raise Exception("HD 720p option not found")

                elif action == "start_conversion":
                    await page.mouse.click(box["x"], box["y"])
                    await asyncio.sleep(15)

                bounding_boxes = await annotate_elements(page)
                current_step += 1

            conversion_complete_text = await page.locator("text=Conversion complete").is_visible(timeout=60000)
            download_button_visible = await page.locator("text=Download").is_visible(timeout=60000)
            
            if conversion_complete_text and download_button_visible:
                test_result["status"] = "Success"
                test_result["description"], test_result["failed_steps"] = generate_test_description(test_result["test_name"], "Success")
            else:
                raise Exception("Conversion did not complete successfully or download button is missing.")

        except Exception as e:
            print("Error during test execution:", e)
            test_result["status"] = "Fail"
            test_result["description"], test_result["failed_steps"] = generate_test_description(test_result["test_name"], "Fail", str(e))

        finally:
            print("Test completed. Browser will remain open for debugging.")
    
    return test_result

async def run_negative_test_1():
    test_result = {
        "test_name": "Negative Test 1 - YouTube URL Upload",
        "status": "Not Started",
        "description": "",
        "failed_steps": "N/A"
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto("https://video-converter.com/")
            print("Navigated to video converter site.")
            await asyncio.sleep(2)

            bounding_boxes = await annotate_elements(page)
            print("Bounding boxes marked on the page.")
            
            url_button_box = next((box for box in bounding_boxes if "URL" in box["text"]), None)
            if not url_button_box:
                raise Exception("URL button not found on the page.")
            await page.mouse.click(url_button_box["x"], url_button_box["y"])
            print("Clicked on 'URL' option for upload.")
            await asyncio.sleep(2)

            bounding_boxes = await annotate_elements(page)
            youtube_url_box = next((box for box in bounding_boxes if "https://" in box.get("placeholder", "")), None)
            if not youtube_url_box:
                raise Exception("YouTube URL input field not found in the dialog.")
            
            await page.mouse.click(youtube_url_box["x"], youtube_url_box["y"])
            youtube_url = "https://www.youtube.com/watch?v=aWk2XZ_8IhA"
            await page.keyboard.type(youtube_url)
            print(f"Entered YouTube URL: {youtube_url}")
            await asyncio.sleep(1)

            bounding_boxes = await annotate_elements(page)
            ok_button_box = next((box for box in bounding_boxes if "OK" in box["text"]), None)
            if not ok_button_box:
                raise Exception("OK button not found after entering URL.")
            
            await page.mouse.click(ok_button_box["x"], ok_button_box["y"])
            print("Clicked 'OK' button to submit the URL.")
            await asyncio.sleep(2)

            print("Waiting for error message...")
            await page.wait_for_selector("text=Unable to open file", timeout=10000)
            print("Error message appeared: 'Unable to open file'")
            test_result["status"] = "Fail as expected"
            test_result["description"], test_result["failed_steps"] = generate_test_description(test_result["test_name"], "Fail as expected")

        except Exception as e:
            print("Error during test execution:", e)
            test_result["status"] = "Unexpected Result"
            test_result["description"], test_result["failed_steps"] = generate_test_description(test_result["test_name"], "Fail", str(e))

        finally:
            print("Test completed. Browser will remain open for debugging.")
    
    return test_result

async def run_negative_test_2():
    test_result = {
        "test_name": "Negative Test 2 - Large File Upload",
        "status": "Not Started",
        "description": "",
        "failed_steps": "N/A"
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            await page.goto("https://video-converter.com/")
            print("Navigated to video converter site.")
            await asyncio.sleep(2)

            bounding_boxes = await annotate_elements(page)
            print("Bounding boxes marked on the page.")

            large_file_path = "/Users/waseem/Downloads/TIA Pitch in Russian.mp4"
            await page.set_input_files("input[type='file']", large_file_path)
            await asyncio.sleep(10)

            print("Checking for file size error message...")
            await page.wait_for_selector("text=The free version allows working with files up to 500 MB", timeout=10000)
            print("File size error message appeared.")
            test_result["status"] = "Fail as expected"
            test_result["description"], test_result["failed_steps"] = generate_test_description(test_result["test_name"], "Fail as expected")

        except Exception as e:
            print("Error during test execution:", e)
            test_result["status"] = "Unexpected Result"
            test_result["description"], test_result["failed_steps"] = generate_test_description(test_result["test_name"], "Fail", str(e))

        finally:
            print("Test completed. Browser will remain open for debugging.")
    
    return test_result

def generate_test_description(test_name, status, error_message=None):
    prompt = f"Provide a brief description for the test case '{test_name}' with status '{status}'."
    if error_message:
        prompt += f" Describe the reason for failure: {error_message.split(':')[0].strip()}."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=100
    )

    description = response.choices[0].message.content.strip()

    failed_steps = error_message.split(':')[0].strip() if "Fail" in status else "N/A"

    return description, failed_steps
