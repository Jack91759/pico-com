from LCD1602 import LCD
import machine
import utime
import sys
import select
import urandom

lcd = LCD()
lcd.message('Terminal\nBooting...')
utime.sleep(2)
lcd.clear()

# Request Name
lcd.message('Input Name:')
NAME = input('Type your name: ')
lcd.clear()
lcd.message(f'Name: {NAME}')
DEVICE_ID = f"_{NAME}"
utime.sleep(1)
lcd.clear()
lcd.message(f'Device ID:\n{DEVICE_ID}')

# Setup Pins
TX = machine.Pin(1, machine.Pin.OUT)
RX = machine.Pin(0, machine.Pin.IN)
RELAY = machine.Pin(15, machine.Pin.OUT)
RESET_RELAY = machine.Pin(14, machine.Pin.OUT)
buzzer = machine.PWM(machine.Pin(13))
buzzer.freq(1000)
buzzer.duty_u16(0)

BIT_DELAY = 0.015
START_STOP_DELAY = 0.03
PRE_TRANSMIT_DELAY = 0.05

replacement_on_receive = {
    'Ð': 'H', 'Ò': 'i', 'î': '_', 'Â': 'w', 'è': 'h',
    'ò': 'a', 'Ø': 'T', 'Ê': 'y', 'ä': 'l',
}

last_received_time = utime.time()
received_text = ""
is_receiving = False
received_messages = []

STATIC_PAGES = {
    "/home": "HEADER: TERMINAL/HTML1.0\nWelcome to the Home Page!",
    "/settings": "HEADER: TERMINAL/HTML1.0\nSettings Page Loaded",
    "/about": "HEADER: TERMINAL/HTML1.0\nSystem created by Jayden"
}

def send_message(message):
    print(f"📤 Sending: {message}")
    lcd.clear()
    lcd.message(f'Sending:\n{message[:16]}')
    full_message = f"{DEVICE_ID}:{message}~"
    RELAY.value(1)
    utime.sleep(PRE_TRANSMIT_DELAY)

    for char in full_message:
        binary_char = bin(ord(char))[2:]
        binary_char = "0" * (8 - len(binary_char)) + binary_char
        TX.value(1)
        utime.sleep(START_STOP_DELAY)
        for bit in binary_char:
            TX.value(int(bit))
            utime.sleep(BIT_DELAY)
        if char == '_':
            utime.sleep(0.05)
        TX.value(0)
        utime.sleep(START_STOP_DELAY)

    RELAY.value(0)
    TX.value(0)
    utime.sleep(0.1)

def beep(duration=0.05):
    buzzer.duty_u16(40000)
    utime.sleep(duration)
    buzzer.duty_u16(0)

def handle_complete_message(message):
    global received_messages
    if message not in received_messages:
        received_messages.append(message)
    text = message
    colon_index = text.find(":")
    result = text[colon_index + 1:] if colon_index != -1 else text
    print(result)

    if result.startswith("!open "):
        process_open_command(result[6:])
    elif result.startswith("CLEAR\n"):
        time.sleep(0)
        # render_terminal_ui(result[7:])
    else:
        lcd.clear()
        lcd.message("Msg:\n" + message[:16])
        print(f"📥 Msg: {message}")
        if message.strip().endswith("!ping"):
            delay = urandom.getrandbits(8) % 1000
            utime.sleep_ms(200 + delay)
            send_message("Online")

def process_open_command(path):
    page = STATIC_PAGES.get(path)
    if not page:
        lcd.clear()
        lcd.message("404 Page Not\nAvailable")
        print("⚠️ 404 Not Found")
        send_message('404 Not Found')
        return

    header, _, body = page.partition('\n')
    if "TERMINAL/HTML1.0" in header:
        lines = body.split("\n")
        frame_top = "#" * 30
        center_title = "#{:^28}#".format("Site Viewer 1.0")
        frame_bottom = "#" * 30
        empty_line = "#{: ^28}#".format("")

        framed_output = [frame_top, center_title, frame_bottom]
        for line in lines:
            framed_line = "# {:<26}#".format(line[:26])
            framed_output.append(framed_line)

        while len(framed_output) < 10:
            framed_output.append(empty_line)

        framed_output.append(frame_top)
        full_display = "_CLEAR\n" + "\n".join(framed_output)
        send_message(full_display)
        print(f"✅ Page sent to remote: {path}")
    else:
        lcd.clear()
        lcd.message("⚠️ Invalid Header")
        print("⚠️ Invalid Header in Page")

def render_terminal_ui(content):
    print("\033[2J\033[H", end="")  # ANSI escape to clear and move cursor to top-left
    print(content)

def trigger_reset():
    print("⚠️ Reset signal received! Activating reset relay.")
    RESET_RELAY.value(1)
    utime.sleep(0.5)
    RESET_RELAY.value(0)

def receive_message():
    global received_text, is_receiving
    if RX.value() == 1:
        is_receiving = True
        utime.sleep(START_STOP_DELAY)
        received_bits = ""
        for _ in range(8):
            bit_value = RX.value()
            received_bits += str(bit_value)
            utime.sleep(BIT_DELAY)

        try:
            char_received = chr(int(received_bits, 2))
            final_char = replacement_on_receive.get(char_received, char_received)

            if final_char == '~' or final_char == '_':
                pass
            elif final_char == 'ÿ':
                trigger_reset()
            else:
                received_text += final_char
        except ValueError:
            print(f"Invalid bits: {received_bits}")

        if received_bits == '01011111':  # underscore _
            beep()

        if received_bits == '01111110':  # tilde ~
            handle_complete_message(received_text)
            received_text = ""

        while RX.value() == 1:
            utime.sleep(0.01)

        is_receiving = False
    utime.sleep(0.01)

def check_terminal_input():
    if is_receiving:
        return
    if select.select([sys.stdin], [], [], 0)[0]:
        user_input = sys.stdin.readline().strip()
        if user_input:
            send_message(user_input)

# Boot complete
print("💡 Ready. Type in terminal to send:")
lcd.clear()
lcd.message("Waiting for\ninput...")

while True:
    receive_message()
    check_terminal_input()