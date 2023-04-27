from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import random
import time


driver = webdriver.Chrome ()
    
driver.get('https://www.lecturainteligente.com.mx/knotion/') # only knotion
school_select = Select(driver.find_element(By.NAME, 'sel_escuela'))

def element(mode , value : str, timeout : int = 10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((mode, value)))

def login(value, id, password): 
    school_select.select_by_value(value)
    element(By.ID, "sel_alumno").send_keys(id)
    element(By.ID, "txt_pass").send_keys(password)
    element(By.ID, "but_entrar").click()
    time.sleep(0.300)
    driver.execute_script("botonInicioClick();")
    time.sleep(0.200)
    try:
        time.sleep(0.400)
        element(By.ID, 'notas_titulo')
        driver.execute_script("cierraNotas();")
    except NoSuchElementException:
        pass


def select_session():
    element(By.ID, "boton_entrar_leccion").click()
    element(By.CSS_SELECTOR, ".btn.btn-success").click()

def timebypass():
    try:
        driver.execute_script("verificaNorma(3000,0,0,true)")
        element(By.ID, "ok").click()
        time.sleep(0.300) # wait the alert unable to reduce
        alert = driver.switch_to.alert
        alert.accept()
    except JavascriptException:
        pass


def matrixbypass():
    answs = []
    for i in range(30):
        try:
            driver.find_element(By.ID, f"resp{i}")
            answs.append(i)
        except NoSuchElementException:
            pass
        
    # start bypass
    driver.execute_script(f'act{random.choice(answs)} = respClickMS("resp{answs[0]}", "activo{answs[0]}", act{answs[0]}, "au{answs[0]}", 0)')

    # bypass
    time.sleep(0.3)
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

    driver.execute_script("contOK = true; ajaxPreguntaPost();")
    

def normal_answ_bypass():
    try:
        driver.find_element(By.ID, 'op1')
        driver.execute_script('selPregResp("op1", "op1", 0);')
    except NoSuchElementException:
        try: 
            driver.find_element(By.ID, 'opB')
            driver.execute_script('selPregResp("opA", "opA", 0);')
        except NoSuchElementException:
            time.sleep(0.100)
            element(By.ID, "div2018_opA").click()
            try:
                element(By.ID, "continuar").click()
            except:
                pass
    

def write_mode():
    element(By.ID, "respuesta").send_keys("A")
    try:
        driver.execute_script('contTX(0, "TX")')
    except JavascriptException:
        driver.execute_script("contOK = true; ajaxPreguntaPost();")
    time.sleep(0.150)
    driver.execute_script("contOK = true; ajaxPregTxPost(3);")


def fake_mode():
    driver.execute_script('selPregResp("opA", "div_opA", 0);')


def blank_mode():
    anws = []
    for i in range(15):
        try:
            driver.find_element(By.ID, f"resp{i}")
            anws.append(f"resp{i}")
        except NoSuchElementException:
            pass
    for i in anws:
        try:
            element(By.ID, f"{i}").send_keys("A")
        except TimeoutException:
            pass
    driver.execute_script("contOK = true; ajaxPreguntaPost();")

def ip_mode():
    driver.execute_script("contOK = true; ajaxPreguntaPost();")
    time.sleep(0.200)
    driver.execute_script("contOK = true; ajaxPreguntaPost();")

def select_reading():
    driver.execute_script("contOK = true; ajaxSelLecPost(1);")
    time.sleep(0.150)


def master(mode : int):
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
        driver.find_element(By.ID, 'preg_matriz')
        return 1
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.ID, 'preg_ops')
        return 0
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.CLASS_NAME, 'textarea2Text')
        driver.find_element(By.ID, 'respuesta')
        return 2
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.ID, 'div_opA')
        return 3
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.XPATH, '//div[@name="preg" and contains(@class, "descPregCP")]')
        return 4
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.ID, 'pregIP')
        return 5
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.CSS_SELECTOR, 'button.buttonlecturas[onclick="contOK = true; return ajaxSelLecPost(1);"]')
        return 6
    except NoSuchElementException:
        pass


def ex_lesson():
    time.sleep(0.150)
    driver.execute_script("contOK = true; ajaxResultadosPost();")    

def finish_lesson():
    time.sleep(0.150)
    driver.execute_script("contOK = true; ajaxReportePost();")



def start():
    element(By.ID, "continuar").click()
    time.sleep(0.150)
    
    while True:
        try:
            driver.find_element(By.CLASS_NAME, 'lectura ')
            timebypass()
        except NoSuchElementException:
            pass
        master(recognize_target())
        time.sleep(0.200)
        try:
            driver.find_element(By.ID, 'numeroResultados')
            ex_lesson()
            break
        except NoSuchElementException:
            pass
        try:
            driver.find_element(By.CLASS_NAME, "table table-striped table-bordered tabla-resultados")
            finish_lesson()
            break
        except NoSuchElementException:
            pass


def hacktool():
    login("316", "Avm.abelgaca", "xbrw5kx6") # user  & password
    time.sleep(2.1)
    select_session()
    while True:
        start()


if __name__ == "__main__":
    hacktool()
