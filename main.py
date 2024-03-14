import random

words=['statistica','informatica','telefon','calculator','electromagnetic','pijamale','constructie','elefant','reciclare']

random_word = random.choice(words)

print('************ GHICESTE CUVANTUL **************')


user_guesses = ''
chances = 5

print(f"Atentie, ai doar {chances} vieti!")

while chances > 0:
    wrong_guesses = 0
    for character in random_word:
        if character in user_guesses:
            print(f"Ai ghicit litera: {character}")
        else:
            wrong_guesses += 1
            print('_')
    if wrong_guesses == 0:
        print("Felicitari!")
        print(f"Cuvantul: {random_word}")
        break
    guess = input('Mai ghiceste: ')
    user_guesses += guess

    if guess not in random_word:
        chances -= 1
        if chances != 0:
            print(f"Oops, ai gresit! Mai ai doar {chances} vieti.")

        if chances == 0:
            print("AI PIERDUT!")
            print(f"Cuvantul era: {random_word}")
