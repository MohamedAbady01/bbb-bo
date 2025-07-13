import asyncio
from playwright.async_api import async_playwright
import gradio as gr
import nest_asyncio
nest_asyncio.apply()
import time
import asyncio
from playwright.async_api import async_playwright
from logic.bbbsheets import get_next_business, update_submission_result
from logic.drive import download_images_for_purposes
import random 
async def start_signup_async():
    global playwright, browser, context, page, business_data
    try:
        business_data = get_next_business()
        if not business_data:
            return "✅ No businesses to process. No verification code needed.", gr.update(visible=False)
        async with async_playwright() as p:
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(headless=False, args=[
                '--disable-blink-features=AutomationControlled',
                '--window-size=1600,1000'
            ])
            context = await browser.new_context(
                locale="en-US",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
            )
            page = await context.new_page()
            # Clear cookies and storag

            email = business_data.get("Email") or business_data.get("LastMail") or "test@example.com"
            password = business_data.get("Password") or "SecurePass123!"
            phone = business_data.get("Phone") or "818-659-9684"
            first_name = business_data.get("First Name") or business_data.get("Business Name", "Sam").split()[0]
            last_name = business_data.get("Last Name") or business_data.get("Business Name", "Morsy").split()[-1]
            Zip = business_data.get("Zip Code") or "affordableedgeroofing.com"
            try:
                await page.goto("https://www.bbb.org/account/register", timeout=60000)
                print("[+] Page loaded.")
            except Exception as e:
                print("[-] Failed to load page:", e)
                return

            try:
                await asyncio.sleep(random.uniform(2,4))
                await page.fill('#firstName', first_name)
                print("[+] First name filled.")
            except Exception as e:
                print("[-] Failed to fill first name:", e)

            try:
                await asyncio.sleep(random.uniform(2,4))
                await page.fill('#lastName', last_name)
                print("[+] Last name filled.")
            except Exception as e:
                print("[-] Failed to fill last name:", e)

            try:
                await asyncio.sleep(random.uniform(2,4))
                await page.fill('#email',email)
                print("[+] Email filled.")
            except Exception as e:
                print("[-] Failed to fill email:", e)

            try:
                await asyncio.sleep(random.uniform(2,4))
                await page.fill('#password', password)
                print("[+] Password filled.")
            except Exception as e:
                print("[-] Failed to fill password:", e)

            try:
                await asyncio.sleep(random.uniform(2,4))
                await page.fill('#confirmPassword',password)
                print("[+] Confirm password filled.")
            except Exception as e:
                print("[-] Failed to fill confirm password:", e)
            try:
                
                await page.evaluate("window.scrollTo(0,500)")
                await asyncio.sleep(random.uniform(2,4))
                await page.fill('#zip',str(Zip))
                print("[+] Zip code filled.")
            except Exception as e:
                print("[-] Failed to fill zip code:", e)

            try:
                await asyncio.sleep(random.uniform(2,4))
                await page.check('input[name="agreeToTerms"]')
                print("[+] Terms checkbox checked.")
            except Exception as e:
                print("[-] Failed to check terms checkbox:", e)

            try:
                await asyncio.sleep(random.uniform(2,4))
                await page.click('button[type="submit"]')
                print("[+] Submitted the form.")
                return "Signup submitted successfully! Please enter the verification code you received.", gr.update(visible=True)
            except Exception as e:
                print("[-] Failed to submit the form:", e)
    
    except Exception as e:
        print("[-] Fatal error during automation:", e)
        return f"S[!] No redirect or confirmation detected:{e}", gr.update(visible=True)
async def submit_code_async(code):
    global page, browser, context, playwright, business_data
    email = business_data.get("Email") or business_data.get("LastMail") or "test@example.com"
    password = business_data.get("Password") or"SecurePass123!"
    try:
        await asyncio.sleep(2)
        await page.wait_for_selector('#confirmationCode', timeout=15000)
        print("[+] Confirmation code field appeared.")
        await page.fill('#confirmationCode', code)
        print("[+] Confirmation code filled.")
    except: 
        print("[ERROR] Entering  Confirmation code .")
    
    try:# Click the "Submit" button
        await asyncio.sleep(random.uniform(2,4))
        await page.click('button.submit-btn')
        print("[+] Confirmation code submitted.")
    except:
        print("[ERROR] Submite  Confirmation code .")

    await page.wait_for_load_state('networkidle')
    print("[+] Possibly verified and redirected.")
    await asyncio.sleep(random.uniform(2,4))
    if 'confirm-account-success' in page.url: 
        print( "✅ First Verfication code  successful.")
        try:
            await page.goto("https://www.bbb.org/account/login", timeout=60000)
            print("[+] Page loaded.")
            await asyncio.sleep(random.uniform(2,4))
            await page.wait_for_selector('#email', timeout=10000)
            await page.fill('#email',email)
            print("[+] Email filled.")

            await asyncio.sleep(random.uniform(2,4))
            await page.fill('#password', password)
            print("[+] Password filled.")

            await asyncio.sleep(random.uniform(2,4))
            await page.click('button.bds-button[type="submit"]')
            print("[+] Sign In clicked.")
    
            await page.wait_for_load_state('networkidle')
            print("[+] Login flow finished.")
            return ("[+] Possibly verified and redirected.the secoend verfication has been sentKindly Check", gr.update(visible=True))
            
        except Exception as e:
            print("[-] Login failed:", e)
            
    else:
        return f"[Error] First Verfication code{page.url}"

async def sec_submit_code_async(sec_code):
    global playwright, browser, context, page, business_data
    try:
        business_data = get_next_business()
        if not business_data:
            return "✅ No businesses to process. No verification code needed.", gr.update(visible=False)
        email = business_data.get("Email") or business_data.get("LastMail") or "test@example.com"
        password = business_data.get("Password") or "SecurePass123!"
        phone = business_data.get("Phone") or "818-659-9684"
        first_name = business_data.get("First Name") or business_data.get("Business Name", "Sam").split()[0]
        last_name = business_data.get("Last Name") or business_data.get("Business Name", "Morsy").split()[-1]
        Zip = business_data.get("Zip Code") or "affordableedgeroofing.com"
        try:
        # Wait for the 2FA input field to appear
            await page.wait_for_selector('#twoFactorCode', timeout=15000)
            print("[+] 2FA input field detected.")
            await asyncio.sleep(random.uniform(2,4))
            try:
                await page.fill('#twoFactorCode', sec_code)
                print("[+] 2FA code filled.")
            except Exception as e:
                print(e)
                
            await asyncio.sleep(random.uniform(2,4))
            await page.click('button.submit-btn')
            print("[+] 2FA code submitted.")
            await asyncio.sleep(random.uniform(5,10))
            # Wait for potential redirection
            await page.wait_for_load_state('networkidle')
            print(page.url)
            print("[+] Possibly logged in successfully.")
            result  = "success"
            update_submission_result(business_data["RowID"], result, page.url)

            return "✅ Verification successful"
        except Exception as e:
            print(f"[ERROR] Automation failed: {e}")
            update_submission_result(business_data["RowID"], "Failed", str(e))
            return f"❌ Automation failed: {e}"
    finally:
        if browser:
            await browser.close()