import pygame
import sys
from alerts_in_ua import Client as AlertsClient
from pygame import mixer

pygame.init()

X, Y = 400, 150
WHITE = (255, 255, 255)
GREEN_BG = (20, 90, 50)
RED_BG = (130, 30, 30)
GRAY_BG = (50, 50, 50)

ABLAK = pygame.display.set_mode((X, Y))
pygame.display.set_caption("---")
FONT_LARGE = pygame.font.Font(None, 60)

SIREN_SOUND = None
try:
    SIREN_SOUND = pygame.mixer.Sound("siren.mp3")
    SIREN_SOUND.play(loops=-1)
    SIREN_SOUND.set_volume(0.0)
except pygame.error as e:
    SIREN_SOUND = None

try:
    ALERTS_CLIENT = AlertsClient(token="GetYourselfAnAPIKeyAndIDontGiveYouThat")
except Exception as e:
    ALERTS_CLIENT = None

API_CHECK_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(API_CHECK_EVENT, 12000)

FUTÓTŰZ = True

if ALERTS_CLIENT:
    pygame.event.post(pygame.event.Event(API_CHECK_EVENT))

while FUTÓTŰZ:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            FUTÓTŰZ = False

        if event.type == API_CHECK_EVENT and ALERTS_CLIENT:
            try:
                print("---INIT---")
                ACTIVE_ALERTS = ALERTS_CLIENT.get_active_alerts()
                ALERTS_LIST = [ALERT for ALERT in ACTIVE_ALERTS]
                for ALERT in ALERTS_LIST:
                    print(f":( {ALERT.id} {ALERT.started_at} {ALERT.finished_at}")
                
                print ()
                LAST_ALERT = ALERTS_LIST[-1]
                LAST_ALERT_ID = str(LAST_ALERT.id)
                #print(LAST_ALERT_ID[0])
                
                if LAST_ALERT_ID[0] == "1":
                    CURRENT_STATUS = "ALERT"
                else:
                    CURRENT_STATUS = "OK"

            except Exception as e:
                CURRENT_STATUS = "ERROR"

    if CURRENT_STATUS == "ALERT":
        STATUS_TEXT = FONT_LARGE.render("Riasztás!", True, WHITE)
        ABLAK.fill(RED_BG)
        if SIREN_SOUND:
            SIREN_SOUND.set_volume(1.0)
    elif CURRENT_STATUS == "OK":
        STATUS_TEXT = FONT_LARGE.render("Nincs aktív riasztás", True, WHITE)
        ABLAK.fill(GREEN_BG)
        if SIREN_SOUND:
            SIREN_SOUND.set_volume(0.0)
    else:
        ABLAK.fill(GRAY_BG)
        if CURRENT_STATUS == "ERROR":
            STATUS_TEXT = FONT_LARGE.render("API Hiba", True, WHITE)
        else:
             STATUS_TEXT = FONT_LARGE.render("Indítás...", True, WHITE)
        if SIREN_SOUND:
            SIREN_SOUND.set_volume(0.0)

    TEXT_RECT = STATUS_TEXT.get_rect(center=ABLAK.get_rect().center)
    ABLAK.blit(STATUS_TEXT, TEXT_RECT)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
