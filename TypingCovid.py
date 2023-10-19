import pygame,random
from pygame import mixer
pygame.mixer.pre_init()
class Button():
    def __init__(self,x,y,text,font,fg,bg1,bg2):
        self.text=text
        self.image=font.render(f"{text}",True,fg)
        self.w=self.image.get_width()+20
        self.h=self.image.get_height()+20
        self.x=x
        self.y=y
        self.bg1=bg1
        self.bg2=bg2
    def update(self,surface):
        action=False
        pos=pygame.mouse.get_pos()
        if pos[0]>=self.x and pos[0]<=self.x+self.w and pos[1]>=self.y and pos[1]<=self.y+self.h:
             pygame.draw.rect(surface,self.bg2,(self.x,self.y,self.w,self.h))
             if pygame.mouse.get_pressed()[0]==1:
                 action=True
             else:
                action=False
        else:
            pygame.draw.rect(surface,self.bg1,(self.x,self.y,self.w,self.h))
            action=False
        surface.blit(self.image,(self.x+10,self.y+10))
        return action
class Alpha(pygame.sprite.Sprite):
    def __init__(self,x,y,name,color,type):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.name=name
        self.color=color
        name=type%15
        if name==3 or name==4 or name==5 or name==6 or name==7:
            if name!=type:
                name=0
        self.type=name
        self.image=pygame.transform.scale(pygame.image.load(f"img\\{name}.png"),(55,55))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
    def update(self,game,speed):
        self.rect.y+=speed
        pygame.draw.circle(game.surface,(255,255,255),(self.rect.centerx,self.rect.centery),45)
        game.surface.blit(self.image,self.rect)
        game.surface.blit(font.render(f"{self.name}",True,self.color),(self.rect.centerx-5,self.rect.top-20))
        if self.rect.bottom+speed>=game.h-120:
            if self.type!=3 and self.type!=4 and self.type!=5 and self.type!=6 and self.type!=7:
                if not game.survival:
                    game.hp=game.hp-10
                    hp_fx.play()
            self.kill()
class Game():
    def __init__(self,w,h):
        self.w=w
        self.h=h
        self.surface=pygame.display.set_mode((self.w,self.h+50))
        self.alpha_group=pygame.sprite.Group()
        self.support_group=[]
        self.bg=pygame.transform.scale(pygame.image.load("img\\bg.png"),(screen_w,screen_h+50))
        self.city=pygame.transform.scale(pygame.image.load("img\\city.png"),(screen_w,150))
        self.ct16=pygame.transform.scale(pygame.image.load("img\\3.png"),(80,80))
        self.ct15=pygame.transform.scale(pygame.image.load("img\\4.png"),(80,80))
        self.cltt=pygame.transform.scale(pygame.image.load("img\\5.png"),(80,80))
        self.vacxin=pygame.transform.scale(pygame.image.load("img\\6.png"),(80,80))
        self.lt=pygame.transform.scale(pygame.image.load("img\\7.png"),(80,80))
    def run(self):
        clock=pygame.time.Clock()
        FPS=100
        self.score=0
        self.hp=100
        self.update_time=pygame.time.get_ticks()
        self.update_time_pause=pygame.time.get_ticks()
        self.update_time_survival=pygame.time.get_ticks()
        self.survival=False
        self.pause=False
        self.start=False
        self.pause_bt=False
        self.count_end=0
        self.btStart=Button(screen_w//2-2.5*20,200,"START",fontBt,(255,255,255),(234,34,42),(100,105,250))
        self.btHScore=Button(screen_w//2-5*20,300,"HIGH SCORE",fontBt,(255,255,255),(234,34,42),(100,105,250))
        self.btTutorial=Button(screen_w//2-4*20,400," TUTORIAL",fontBt,(255,255,255),(234,34,42),(100,105,250))
        self.btBack=Button(10,755,"BACK",font,(255,255,255),(234,34,42),(100,105,250))
        self.btStart1=Button(1200-40-6*10,755,"START",font,(255,255,255),(234,34,42),(100,105,250))
        self.btRestart=Button(screen_w//2-3.5*20,screen_h//2+50,"RESTART",font,(255,255,255),(234,34,42),(100,105,250))
        self.btPause=Button(10,90,"PAUSE",font,(255,255,255),(234,34,42),(100,105,250))
        self.btReset=Button(screen_w//2-3.5*20,500,"RESCORE",fontBt,(255,255,255),(234,34,42),(100,105,250))
        self.Tutorial=0
        self.highScore=0
        while True:
            clock.tick(FPS)
            # self.speed=min(1.5+0.2*(self.score//20),20)
            self.speed=10
            if self.start:
                if self.pause:
                    self.speed=0
                    self.update_time=pygame.time.get_ticks()
                    if pygame.time.get_ticks()-self.update_time_pause>3210:
                        self.pause=False
                if self.survival:
                    if pygame.time.get_ticks()-self.update_time_survival>5432:
                        self.survival=False
                if self.pause_bt:
                    self.speed=0
                    self.update_time=pygame.time.get_ticks()
            self.display()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return
                if event.type==pygame.KEYDOWN:
                    if self.hp>0:
                        if not self.pause_bt:
                            self.destroy(event)
            pygame.display.update()
    def display(self):
        self.surface.blit(self.bg,(0,0))
        if self.start:
            if self.btPause.update(self.surface):
                self.pause_bt=not(self.pause_bt)
            self.surface.blit(self.city,(0,screen_h-100))
            self.surface.blit(font.render(f"SCORE: {self.score}",True,(255,255,255)),(10,50))
            if self.hp>100:
                self.hp=100
            pygame.draw.rect(self.surface,(232,7,41),(10,10,self.hp/100*400,30))
            pygame.draw.rect(self.surface,(225,125,32),(10,10,400,30),2)
            self.surface.blit(font.render("Mode by Ngoc Phat",True,(255,255,255)),(screen_w//2-8*11,screen_h+15))
            if self.hp>0:
                self.alpha_group.update(self,self.speed)
                self.add_alpha()
            else:
                if self.score>int(self.highScore):
                    self.writeFile(self.score)
                self.end()
        else:
            if self.Tutorial==0:
                if self.btStart.update(self.surface):
                    self.Tutorial=1
                    self.start=True
                if self.btTutorial.update(self.surface):
                    self.Tutorial=2
                if self.btHScore.update(self.surface):
                    self.Tutorial=3
                if self.btReset.update(self.surface):
                    self.writeFile(0)
            elif self.Tutorial==2:
                self.displayTutorial()
            elif self.Tutorial==3:
                self.readFile()
                img=font_txt.render("HIGH SCORE",True,(244,10,10))
                self.surface.blit(img,(screen_w//2-5*22,20))
                n=len(str(self.highScore))
                img=pygame.font.SysFont("Arial",80).render(f"{self.highScore}",True,(244,10,10))
                self.surface.blit(img,(screen_w//2-n//2*40,150))
                self.endpage()
    def displayTutorial(self):
        self.surface.fill((117,234,176))
        img=font_txt.render("HƯỚNG DẪN",True,(244,10,10))
        self.surface.blit(img,(screen_w//2-4.5*22,20))
        img=font_txt.render("-Ấn theo kí tự trên đầu mỗi con virus để tiêu diệt chúng.",True,(0,0,0))
        self.surface.blit(img,(20,100))
        img=font_txt.render("-Thành phố sẽ ban hành các chỉ thị/cách ly tập trung.",True,(0,0,0))
        self.surface.blit(img,(20,180))
        self.surface.blit(self.ct16,(10,260))
        img=font_txt.render(": Thành phố sẽ không bị tấn công trong 5 đơn vị thời gian.",True,(0,0,0))
        self.surface.blit(img,(100,270))
        self.surface.blit(self.ct15,(10,340))
        img=font_txt.render(": Virus sẽ ngừng tấn công trong 3 đơn vị thời gian.",True,(0,0,0))
        self.surface.blit(img,(100,350))
        self.surface.blit(self.cltt,(10,420))
        img=font_txt.render(": Virus bị đẩy lùi 150 đơn vị độ dài.",True,(0,0,0))
        self.surface.blit(img,(100,430))
        self.surface.blit(self.vacxin,(10,500))
        img=font_txt.render(": Toàn bộ virus trên màn hình sẽ bị tiêu diệt.",True,(0,0,0))
        self.surface.blit(img,(100,510))
        self.surface.blit(self.lt,(10,580))
        img=font_txt.render(": Thành phố được viện trợ lương thực. Sinh lực tăng 50%.",True,(0,0,0))
        self.surface.blit(img,(100,590))
        img=font_txt.render("-Ngoài những điều trên, những thứ khác đều có hại cho thành phố.",True,(0,0,0))
        self.surface.blit(img,(10,670))
        self.endpage()
    def endpage(self):
        if self.btBack.update(self.surface):
            self.surface.blit(self.bg,(0,0))
            self.Tutorial=0
        if self.btStart1.update(self.surface):
            self.new()
            self.start=1
    def readFile(self):
        f=open("img\\high_score.dat","r")
        self.highScore=f.read()
        f.close()
    def destroy(self,event):
        for i in self.alpha_group:
            if i.name==event.unicode:
                press_fx.play()
                i.kill()
                self.score+=1
                if i.type==3: #16
                    self.survival=True
                    self.update_time_survival=pygame.time.get_ticks()
                elif i.type==4: #15
                    self.pause=True
                    self.update_time_pause=pygame.time.get_ticks()
                elif i.type==5: #cltt
                    for x in self.alpha_group:
                        x.rect.y-=150
                        self.update_time=pygame.time.get_ticks()
                elif i.type==6: #vacxin
                    self.alpha_group.empty()
                elif i.type==7: #food
                    self.hp+=50
                return
    def add_alpha(self):
        if pygame.time.get_ticks()-self.update_time>1000 or len(self.alpha_group)==0:
            self.update_time=pygame.time.get_ticks()
            t=random.randint(1,3)
            if t==1:
                temp=Alpha(random.randint(1,self.w//50-1)*50,-5,chr(random.randint(65,90)),(255,25,25),random.randint(1,40))
            elif t==2:
                temp=Alpha(random.randint(1,self.w//50-1)*50,-5,chr(random.randint(97,122)),(255,25,25),random.randint(1,40))
            else:
                temp=Alpha(random.randint(1,self.w//50-1)*50,0-5,chr(random.randint(48,57)),(255,25,25),random.randint(1,40))
            self.alpha_group.add(temp)
    def end(self):
        pygame.draw.rect(self.surface,(85,86,69),(0,0,screen_w,self.count_end))
        if self.count_end<screen_h+50:
            self.count_end+=5
        else:
            img=pygame.font.SysFont("Times",60).render("GAMEOVER",True,(197,3,19))
            rect=img.get_rect()
            rect.center=(screen_w//2,screen_h//2-70)
            self.surface.blit(img,rect)
            self.surface.blit(img,rect)
            img=pygame.font.SysFont("Times",45).render(f"SCORE: {self.score}",True,(229,239,35))
            rect=img.get_rect()
            rect.center=(screen_w//2,screen_h//2)
            self.surface.blit(img,rect)
            if self.btRestart.update(self.surface):
                self.new()
    def new(self):
        self.hp=100
        self.score=0
        self.alpha_group.empty()
    def writeFile(self,data): 
            f=open("img\\high_score.dat","w")
            f.write(str(data))
            f.close()
if __name__=="__main__":
    pygame.init()
    press_fx=pygame.mixer.Sound("img\\press.mp3")
    press_fx.set_volume(1.0)
    hp_fx=pygame.mixer.Sound("img\\hp.mp3")
    hp_fx.set_volume(1.0)
    font=pygame.font.SysFont("Times",22)
    fontBt=pygame.font.SysFont("Arial",40)
    font_txt=pygame.font.SysFont("Times",40)
    screen_w=1200
    screen_h=770
    screen=Game(screen_w,screen_h)
    screen.run()

