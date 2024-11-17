import pygame

pygame.init()

angle = 0
screen = pygame.display.set_mode((400, 200))
screen.fill("white")
clock = pygame.time.Clock()
pygame.display.update()

imageOriginal = pygame.image.load("cursor.png").convert_alpha()
imageOriginal = pygame.transform.scale(imageOriginal, (50, 50))

running = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

    screen.fill("white")
    image = pygame.transform.rotate(imageOriginal, angle)
    imageRect = image.get_rect(center=(100, 100))

    screen.blit(image, imageRect)
    angle += 10

    pygame.display.update()
    clock.tick(30)
pygame.quit()
