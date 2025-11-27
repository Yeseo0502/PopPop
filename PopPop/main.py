#1. 캐릭터가 공에 맞았을 때

#다시하기 버튼 만들기
#랭킹만들기
#엔딩 만들기 (이스터에그 엔딩)

import pygame
import os
from pyvideo import Video

pygame.init() #초기화

# 화면 크기 설정
screen_width = 1536
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("풍선팝팝")


vid = Video("opening.mp4")
vid.set_size((1500,1000))
def intro() :
    clock = pygame.time.Clock()
    while True:

        for event in pygame.event.get() :
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                return
        # 비디오 프레임 가져오기
        vid.draw(screen, (0, 0), force_draw=True)
        pygame.display.update()
        clock.tick(30)

intro()


current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path,"pygame_pop") #pygame_pop 폴더 위치 반환
# 배경 이미지 불러오기
background = pygame.image.load(os.path.join(image_path,"background.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size #사이즈를 알려주는, 너비 높이
stage_height = stage_size[1] #스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 불러오기
character = pygame.image.load(os.path.join(image_path,"character.png"))
# character = pygame.image.load(os.path.join(image_path,"gogo.png"))
character_size = character.get_rect().size #가로세로 크기 알 수 있음
character_width = character_size[0] #가로
character_height = character_size[1] #세로
character_x_pos = (screen_width/2) - (character_width/2) #화면 가로의 절반 크기에 해당하는 곳에 위치(가로)
character_y_pos = screen_height-character_height-stage_height #화면 세로 크기 가장 아래에 해당하는 곳에 위치(세로)

#캐릭터 이동 방향
character_to_x = 0
#캐릭터 이동 속도
character_speed = 5
#무기 만들기
weapon = pygame.image.load(os.path.join(image_path,"hoo_ball.png"))
weapon_size = weapon.get_rect().size #사이즈 배열
weapon_width = weapon_size[0]

#무기는 한 번에 여러 발 발사 가능
weapons = []
#무기 이동 속도
weapon_speed = 10
#공 만들기(4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path,"bigball.png")),
    pygame.image.load(os.path.join(image_path,"sm_ball1.png")),
    pygame.image.load(os.path.join(image_path,"sm_ball2.png")),
    pygame.image.load(os.path.join(image_path,"sm_ball3.png"))
]
#각 크기에 따라 속도 다르기 공
ball_speed_y = [-20,-18,-16,-14 ] #index 0,1,2, 3에  해당하는 값

#공돌
balls = []

balls.append({
    "pos_x" : 50, #공의 x좌표
    "pos_y": 50, #공의 y좌표
    "img_idx" : 0, #공의 이미지 인덱스
    "to_x":3, #x축 이동방향, -3이면 왼쪽이고, 3이면 오른쪽으로
    "to_y":-6,#y축 이동방향,
    "init_spd_y":ball_speed_y[0] #y 최초 속도
})
#사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

#Font 정의
game_font = pygame.font.Font(None,40)
total_time = 100
start_ticks = pygame.time.get_ticks() #시작 시간 정의

#게임 종료 메시지
# -> TimeOut(시간 초과 탈락), Mission Complete(성공), Game Over(캐릭터 공에 맞음 탈락)
game_result = "Game Over"

# 이벤트 루프 <- 이거있어야 계속 실행이 됨.
running = True #게임 진행상황
while running:
    for event in pygame.event.get(): #어떤 동작(이벤트)가 발생하는지?
        if event.type == pygame.QUIT: #창 닫히는거
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #캐릭터를 왼쪽으로
                character_to_x -=character_speed
            elif event.key == pygame.K_RIGHT: #캐릭터를 오른쪽으로
                character_to_x +=character_speed
            elif event.key == pygame.K_SPACE: #무기발사
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos]) #x,y좌표 배열로
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
    # 게임 캐릭터 위치 정의
    character_x_pos +=character_to_x
    #화면 밖으로 못 나가도록 처리
    if character_x_pos <0 :
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width
    #무디 위치 조정 ->세로만 조정하는 거라서 w[1]에다가 weapon_speed를 뺌
    weapons = [[w[0],w[1] - weapon_speed] for w in weapons] #무기 위치를 위로
    #천장에 닿은 무기 없애기
    weapons = [[w[0],w[1]]for w in weapons if w[1] > 0]

    #공의 위치 정의 idx=배열방 val=배열방에있는 값
    for ball_idx, ball_val in enumerate(balls) :
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #가로벽에 닿으면 공 이동 위치 변경(튕겨 나오는 이벤트)
        if ball_pos_x < 0 or ball_pos_x>screen_width-ball_width:
            ball_val["to_x"] = ball_val["to_x"]*-1

        #세로 위치
        #스테이지에 튕겨서 올라가는 이벤트 처리 포물선 갬성~~~
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else : #그 외의 모든 경우에는 속도를 증가
            ball_val["to_y"]+=0.2
        ball_val["pos_x"] +=ball_val["to_x"]
        ball_val["pos_y"] +=ball_val["to_y"]

    #충돌 처리
    #캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls) :
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        #공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        #공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect) :
            running = False
            break
        #공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons) :
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            #무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #충돌 체크
            if weapon_rect.colliderect(ball_rect) :
                weapon_to_remove = weapon_idx #해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx #해당 공 없애기 위한 값 설정
                #가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    #현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),  # 공의 x좌표
                        "pos_y": ball_pos_y + (ball_height /2)- (small_ball_height /2),  # 공의 y좌표
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": -3,  # x축 이동방향, -3이면 왼쪽이고, 3이면 오른쪽으로
                        "to_y": -6,  # y축 이동방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]  # y 최초 속도
                    })
                    #오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),  # 공의 x좌표
                        "pos_y": ball_pos_y + (ball_height /2)- (small_ball_height /2),  # 공의 y좌표
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": 3,  # x축 이동방향, -3이면 왼쪽이고, 3이면 오른쪽으로
                        "to_y": -6,  # y축 이동방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]  # y 최초 속도
                    })
                break
            else: #계속 게임을 진행
                continue #왼쪽 for문 조건이 맞지 않으면 contiue. 바깥 for문 계속 수행
            break #안쪽 for문에서 break를 만나면 여기로 진입. 2중 for문을 한번에
        # for 바깥조건 :
        #     바깥동작
        #     for 안쪽조건:
        #         안쪽동장
        #         if 충돌하면 :
        #             break
        #     else :
        #         continue
        #     break

    #충될된 공 or 무기 없애기
    if ball_to_remove > -1 :
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1 :
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    #모든 공을 없앤 경우 게임종료
    if len(balls) == 0 :
        game_result = "Mission Complete"
        running = False

    #화면에 그리기
    screen.blit(background,(0,0))
    #사람이동
    for weapon_x_pos,weapon_y_pos in weapons :
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))

    #공 이동
    for idx,val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx],(ball_pos_x,ball_pos_y))
    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))

    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True,(255,255,255))
    screen.blit(timer,(10,10))

    #시간 초과했다면? 1번 Time Out 종료 이벤트 처리
    if total_time - elapsed_time <= 0 :
        game_result = "Time Over"
        running = False

    pygame.display.update() #게임화면을 다시 그리기

#게임 오버 메시지
msg = game_font.render(game_result, True,(255,255,0)) #노란색 이벤트 문구 처리
msg_rect = msg.get_rect(center=(int(screen_width / 2),int(screen_height/2)))
screen.blit(msg,msg_rect)
pygame.display.update() #게임화면을 다시 그리기

#2초 대기
pygame.time.delay(2000)

pygame.quit()

#종료
pygame.quit()