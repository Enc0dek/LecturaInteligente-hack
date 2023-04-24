from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time

driver = webdriver.Chrome()
    
driver.get('https://www.lecturainteligente.com.mx/knotion/') # only knotion
school_select = Select(driver.find_element(By.NAME, 'sel_escuela'))


def login(value, id, password):
    school_select.select_by_value(value)
    btn_log = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'but_entrar'))
    )
    id_alumn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'sel_alumno'))
    )
    pwd_alumn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'txt_pass'))
    )
    id_alumn.send_keys(id)
    pwd_alumn.send_keys(password)
    btn_log.click()
    time.sleep(0.350)
    driver.execute_script("botonInicioClick();")
    time.sleep(0.300)
    try: 
        notas_open = driver.find_element(By.ID, 'notasbox')
        driver.execute_script("cierraNotas();")
    except NoSuchElementException:
        pass


def select_session():
    s = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'boton_entrar_leccion')))
    s.click()
    lesson = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn.btn-success')))
    lesson.click()

def timebypass():
    try:
        driver.execute_script("verificaNorma(3000,0,0,true)")
        btn_accept_1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ok'))
        )
        btn_accept_1.click()
        time.sleep(0.300)
        alert = driver.switch_to.alert
        alert.accept()
    except JavascriptException:
        pass


def matrixbypass():
    answs = []
    for i in range(30):
        try:
            answ = driver.find_element(By.ID, f"resp{i}")
            answs.append(i)
        except NoSuchElementException:
            pass
        
    # start bypass
    driver.execute_script(f'act{answs[0]} = respClickMS("resp{answs[0]}", "activo{answs[0]}", act{answs[0]}, "au{answs[0]}", 0)')

    # bypass
    time.sleep(0.5)
    real_answ = []
    for i in answs:
        try:
            question = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, f"resp{i}"))
            )
            x = question.get_attribute('class')
            if x == "tdFalto ":
                real_answ.append(i)
        except NoSuchElementException:
            pass

    # finally
    for i in real_answ:
        driver.execute_script(f'act{i} = respClickMM("resp{i}", "activo{i}", act{i}, "au{i}", true)')

    driver.execute_script("contOK = true; return ajaxPreguntaPost();")
    

def normal_answ_bypass(): # selPregResp("op1", "op1", 0);
    try:
        type_1 = driver.find_element(By.ID, 'op1')
        driver.execute_script('selPregResp("op1", "op1", 0);')
    except NoSuchElementException:
        try: 
            type_2 = driver.find_element(By.ID, 'opB')
            driver.execute_script('selPregResp("opA", "opA", 0);')
        except NoSuchElementException:
            time.sleep(0.200)
            answ = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'div2018_opA'))
            )
            answ.click()
            try:
                continue_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'continuar'))
                )
                continue_btn.click()
            except:
                pass
    

def write_mode():
    textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'respuesta'))
    )
    textarea.send_keys("A")
    try:
        driver.execute_script('contTX(0, "TX")')
    except JavascriptException:
        driver.execute_script("contOK = true; ajaxPreguntaPost();")
    time.sleep(0.300)
    driver.execute_script("contOK = true; ajaxPregTxPost(3);")


def fake_mode():
    driver.execute_script('selPregResp("opA", "div_opA", 0);')


def blank_mode():
    anws = []
    for i in range(15):
        try:
            input_fake = driver.find_element(By.ID, f"resp{i}")
            anws.append(f"resp{i}")
        except NoSuchElementException:
            pass
    for i in anws:
        print(i)
        try:
            input_anws = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, f'{i}'))
            )
            input_anws.send_keys("A")
        except TimeoutException:
            pass
    driver.execute_script("contOK = true; return ajaxPreguntaPost();")

def ip_mode():
    driver.execute_script("contOK = true; ajaxPreguntaPost();")
    time.sleep(0.200)
    driver.execute_script("contOK = true; ajaxPreguntaPost();")

def select_reading():
    driver.execute_script("contOK = true; ajaxSelLecPost(1);")
    time.sleep(0.150)


def master(mode):
    if mode == 0:
        normal_answ_bypass()
    elif mode == 1:
        matrixbypass()
    elif mode == 2:
        write_mode()
    elif mode == 3:
        fake_mode()
    elif mode == 4:
        blank_mode()
    elif mode == 5:
        ip_mode()
    elif mode == 6:
        select_reading()
    else:
        print("question no found")


def recognize_target() -> int:
    time.sleep(0.100)
    try:
        type_question = driver.find_element(By.ID, 'preg_matriz')
        return 1
    except NoSuchElementException:
        pass

    try:
        type_question = driver.find_element(By.ID, 'preg_ops')
        return 0
    except NoSuchElementException:
        pass

    try:
        type_question = driver.find_element(By.CLASS_NAME, 'textarea2Text')
        type_question = driver.find_element(By.ID, 'respuesta')
        return 2
    except NoSuchElementException:
        pass

    try:
        type_question = driver.find_element(By.ID, 'div_opA')
        return 3
    except NoSuchElementException:
        pass

    try:
        type_question = driver.find_element(By.XPATH, '//div[@name="preg" and contains(@class, "descPregCP")]')
        return 4
    except NoSuchElementException:
        pass

    try:
        type_question = driver.find_element(By.ID, 'pregIP')
        return 5
    except NoSuchElementException:
        pass

    try:
        type_question = driver.find_element(By.CSS_SELECTOR, 'button.buttonlecturas[value="Mis emociones en la escuela"][onclick="contOK = true; return ajaxSelLecPost(1);"]')
        return 6
    except NoSuchElementException:
        pass


def finish_lesson():
    time.sleep(0.200)
    driver.execute_script("contOK = true; return ajaxResultadosPost();")    


def start():
    contiune_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'continuar'))
    )
    contiune_btn.click()
    time.sleep(0.300)
    
    while True:
        try:
            reading_mode = driver.find_element(By.CLASS_NAME, 'lectura ')
            timebypass()
        except NoSuchElementException:
            pass
        master(recognize_target())
        time.sleep(0.200)
        try:
            
            is_finish = driver.find_element(By.ID, 'numeroResultados')
            finish_lesson()
            break
        except NoSuchElementException:
            pass


def hacktool():
    login("316", "", "") # user password
    time.sleep(2.2)
    select_session()
    while True:
        start()


if __name__ == "__main__":
    hacktool()