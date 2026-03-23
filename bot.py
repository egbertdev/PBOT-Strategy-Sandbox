from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class Paka(object):

    def __init__(self,number,password):
        self.number = number
        self.password = password
        self.url = "https://play.pakakumi.com/login"
        self.number_xpath = "//*[@id='root']/div[2]/div/div/div/div/form/div[1]/div/div[1]/input" 
        
        self.password_xpath = "//*[@id='root']/div[2]/div/div/div/div/form/div[2]/div/input"
        self.login_xpath = "//*[@id='root']/div[2]/div/div/div/div/form/button"

        self.amount_xpath = "//*[@id='root']/div[1]/div[2]/div/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div/input"
        self.odds_xpath = "//*[@id='root']/div[1]/div[2]/div/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div/input"
        self.bet_xpath = "//*[@id='tour_bet_button']/span"
        self.balance_xpath = "//*[@id='root']/div[1]/div[1]/div/div[4]/div/div[1]/a"
        self.outcome_xpath = "//*[@id='tour_multiplier']"

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        self.driver.get(self.url)
        self.box_amount = None
        self.box_odds = None
        self.btn_bet = None
        self.box_balance = None
        self.box_outcome = None
        self.wait_for_xpath(self.number_xpath)
        self.round = 0;
        
    def wait_for_xpath(self,xpath):
        try:   
            element = WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.XPATH,xpath)))
        except:
            print("Waiting Error : XPATH")

    def login(self):
        self.driver.find_element(by=By.XPATH, value=self.number_xpath).send_keys(self.number)
        self.driver.find_element(by=By.XPATH, value=self.password_xpath).send_keys(self.password)
        self.driver.find_element(by=By.XPATH, value=self.login_xpath).click()
        self.wait_for_xpath(self.amount_xpath)
        self.box_amount = self.driver.find_element(by=By.XPATH, value=self.amount_xpath)
        self.box_odds = self.driver.find_element(by=By.XPATH, value=self.odds_xpath)
        self.btn_bet = self.driver.find_element(by=By.XPATH,value=self.bet_xpath)

        self.wait_for_xpath(self.balance_xpath)
        self.box_balance = self.driver.find_element(by=By.XPATH,value=self.balance_xpath)
        self.box_outcome = self.driver.find_element(by=By.XPATH,value=self.outcome_xpath)

    def get_current_multiplier(self):
        """Extract the current multiplier from outcome element"""
        try:
            # Get the text (e.g., "Busted @ 6.02x" or "1.23x")
            text = self.box_outcome.text  # Keep original case
            
            if "Busted" in text:
                # Extract multiplier from "Busted @ 6.02x" format
                parts = text.split("@")
                multiplier_text = parts[1].replace('x', '').strip()  # lowercase 'x'
                return float(multiplier_text)
            else:
                # Extract number from "1.23x" format (current running multiplier)
                multiplier = float(text.replace('x', '').strip())  # lowercase 'x'
                return multiplier
        except Exception as e:
            print(f"Error extracting multiplier: {e}")
            return 1.0  # Final fallback only

    def wait_for_consecutive_crashes(self, odds_threshold, consecutive_count):
        """Wait for Y consecutive crashes below specified odds threshold"""
        print(f"Waiting for {consecutive_count} consecutive crashes below {odds_threshold}x...")
        consecutive_crashes = 0
        
        while consecutive_crashes < consecutive_count:
            try:
                print("⏳ Waiting for Busted text to appear...")
                
                # Wait for a crash to happen (Busted appears) - 10 MINUTES
                WebDriverWait(self.driver, 600).until(
                    EC.text_to_be_present_in_element((By.XPATH, self.outcome_xpath), "Busted")  # "Busted" not "BUSTED"
                )
                
                print("✅ Busted text detected!")
                
                # Get the multiplier at which it crashed
                crash_multiplier = self.get_current_multiplier()
                print(f"🎯 Crash observed at: {crash_multiplier}x")
                
                # Check if crash is below our threshold
                if crash_multiplier < odds_threshold:
                    consecutive_crashes += 1
                    print(f"✅ Consecutive crash #{consecutive_crashes} below {odds_threshold}x")
                else:
                    # Reset counter if crash is above threshold
                    consecutive_crashes = 0
                    print(f"❌ Crash above threshold ({crash_multiplier}x), resetting counter")
                
                print("⏳ Waiting for Busted text to disappear (next round)...")
                
                # Wait for the next round to start (Busted text disappears) - 3 MINUTES
                WebDriverWait(self.driver, 180).until_not(
                    EC.text_to_be_present_in_element((By.XPATH, self.outcome_xpath), "Busted")  # "Busted" not "BUSTED"
                )
                
                print("✅ New round started!")
                
            except Exception as e:
                print(f"❌ Error waiting for crashes: {e}")
                continue
        
        print(f"🎯 Completed! {consecutive_count} consecutive crashes below {odds_threshold}x detected. Starting betting sequence...")

    def clear_bet_fields(self):
        self.box_amount.send_keys(Keys.CONTROL, 'a')
        self.box_amount.send_keys(Keys.BACKSPACE)
            
        self.box_odds.send_keys(Keys.CONTROL, 'a')
        self.box_odds.send_keys(Keys.BACKSPACE)

    def fill_bet_fields(self,amount,odds):
        self.box_amount.send_keys(amount)
        self.box_odds.send_keys(odds)

    def bet(self,amount,odds):
        prev_balance = float(self.box_balance.text.replace('KES ','').replace(',',''))
        
        self.clear_bet_fields()
        self.fill_bet_fields(amount,odds)
        self.btn_bet.click()

        result = self.is_won(prev_balance)
        
        # NEW: Wait for new round to start before returning
        print("⏳ Waiting for new round to start...")
        WebDriverWait(self.driver, 180).until_not(
            EC.text_to_be_present_in_element((By.XPATH, self.outcome_xpath), "Busted")
        )
        
        return result
            
    def is_won(self,prev_balance):
        running = True
        while(running):
            self.wait_for_xpath(self.balance_xpath)
            curr_balance = float(self.box_balance.text.replace('KES ','').replace(',',''))
            if("Busted" in self.box_outcome.text):  # Changed to "Busted"
                if (curr_balance  > prev_balance):
                    return True
                elif(curr_balance < prev_balance):
                    return False

if __name__ == '__main__':
    number = "0718527910"
    password = "kimkimkim10"

    amounts = [10,11,12,13,14,15]
    odds = 3
    
    paka = Paka(number,password)
    paka.login()

    # Wait for 3 consecutive crashes below 2.0x before starting (example)
    paka.wait_for_consecutive_crashes(2.0, 3)

    index = 0
    while(index < len(amounts)):
        amount = amounts[index]
        won = paka.bet(amount,odds)
        if (won):
            index = 0
        else:
            index = index + 1
