import random
import time
import sys
import pyinputplus as pyip

# Definierar värden och färg i variabler
suits : str = ["♥", "♦", "♠", "♣"]
values  = list(range(2, 11)) + ["J", "Q", "K", "A"]

# En dictionary för de klädda kortens poäng:
face_cards : str = {
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14  
}

# Klass för att representera ett kort:
class Card:
    def __init__(self, value, suit):
        self.value : int = value
        self.suit : str = suit

    def __str__(self) -> str : 
        return f"{self.suit}{self.value}"

# En funktion som låter användaren välja om A ska vara värt 1 eller 14
    def get_value(self, is_player = True):
        if self.value == "A" and is_player:
            while True:
                try:
                    ace_value = int(input("Du drog ett ess! Vill du att det ska vara värt 14 eller 1? "))
                    if ace_value == 14 or ace_value == 1:
                        return ace_value
                    else:
                        print("Ogiltigt val. Ange 14 eller 1.")
                except ValueError:
                    print("Ogiltigt val. Ange 14 eller 1.")

         # Datorn gör det smartaste valet automatiskt
        elif self.value == "A" and not is_player:
            return 14 if is_player == False and (21 - 14) >= 0 else 1
        elif self.value in face_cards:
            return face_cards[self.value]
        else:
            return self.value

# Funtion som genererar en kortlek
def generate_deck(values : int, suits : str):
    deck = []
    for value in values:
        for suit in suits:
            deck.append(Card(value, suit))
    return deck

# Dra ett kort från kortleken och tar bort det kortet ur kortleken den omgången
def draw_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))


#funktion för att printa en bokstav i taget.
def print_slow(str):  
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.05)


print_slow("Välkommen till Tjugoett! \n") #hälsningsfras i början 

# Funktion för att spela spelet
def play_21():
    # Generera och blanda kortleken
    deck = generate_deck(values, suits)
    random.shuffle(deck)
    
    # Spelarens tur
    player_sum : str = 0


    #dra kort och visa användaren vad de har för summa
    while True:
        card = draw_card(deck)
        card_value = card.get_value()
    
        
        player_sum += card_value
        
        print_slow(f"Du fick ett kort med värdet {card}. Din totala summa är nu {player_sum}.\n")

        #automatisk förlust när användaren får över 21       
        if player_sum > 21:
            print("Du fick över 21. Datorn vinner!")
            return False  

        continue_game = pyip.inputYesNo("Vill du dra ett kort till? (yes/no): ").lower()
        if continue_game != 'yes':
            break

    # Datorns tur
    computer_sum : str = 0

    #dra kort och visa användaren vad datorn har för summa
    while computer_sum < 17:
        card = draw_card(deck)
        card_value = card.get_value(is_player=False)      
        computer_sum += card_value  

        print_slow(f"Datorn drog ett kort med värdet {card}. Datorns totala summa är nu {computer_sum}.\n")
        
        #automatisk vinst när datorn får över 21       
        if computer_sum > 21:
            print_slow("Datorn fick över 21. Du vinner!\n")
            return True 
    
    # Avgör vinnaren
    print_slow(f"Din slutliga summa: {player_sum}\n")
    print_slow(f"Datorns slutliga summa: {computer_sum}\n")
    
    if computer_sum > player_sum:
        print_slow("Datorn vinner!\n")
        return False 
    elif computer_sum < player_sum:
        print_slow("Du vinner!\n")
        return True 
    else:
        print_slow("Oavgjort!\n")
        return None 

# Funktion för att börja om spelet om man vill
def main():
    while True:
        result = play_21()

        # Fråga om spelaren vill spela igen
        play_again = pyip.inputYesNo("Vill du spela igen? (yes/no): ").lower()
        if play_again == 'no':
            print("Tack för att du spelade!")
            break

if __name__ == "__main__":
    main()
