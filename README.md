Content filtering:

- Als ik op een product klik dan wil ik soortgelijke producten als aanbevelingen tonen, dit doe ik door de een tabel te maken
met 4 aanbevelingen per product. De aanbevelingen zijn  producten met dezelfde sub_sub_category.

- Als ik op mijn winkelwagen klik en ik wil soortgelijke producten aanbevelen dan heeft het geen zin meer om
 producten met dezelfde sub_sub_category aan te bevelen, deze zijn nu te specifiek(ik ben nu niet meer geïntresseerd in een ander soort shampoo),
  wat ik wel zou kunnen willen is een product in dezelfde sub_category of category, zoals douchegel of deo.

al deze category tabellen worden gemaakt met de create_category_recs_table() functie


Collaborative filtering:

- Voor de aanbevelingen op producten maak ik een tabel met voor elk product 4 aanbevelingen. Ik kom aan deze aanbevelingen
door voor elk product te kijken in welke bestellingen deze voorkomen, in bestellingen waar dit product voorkomt tel ik hoe vaak de andere producten voorkomen.
Ik neem vervolgens de 4 meest voorkomende 'andere producten' in alle bestellingen als aanbeveling voor een specifiek product.
Ik kan dus zien dat het id '1034'(Andrélon Shampoo Glans & Care 300 ml) x keer samen in 
een bestelling zit met:

    74 x '2551'(Andrélon Glans & Care Conditioner 300 ml)

    27 x '23382' (Andrélon Oil & Care Conditioner 300 ml)

    19 x '27743' (Axe Deospray Africa 150 ml)

    17 x '2153' (Andrélon Shampoo Care & Repair 300 ml)
    
    het is misschien nog handig om specifiek te kijken naar producten met dezelfde sub_sub_category, maar ik denk dat het analyseren van wat er vaak samen besteld wordt
    het meest handig is voor de aanbevelingen bij de checkout.

    
- Als je op deze manier aanbevelingen wilt doen in je winkelwagen moet je wel iets veranderen, je wilt hier ook, net als bij content filtering, niet producten uit dezelfde sub_sub_category aanbevelen.
de enige verandering is dus een subquery om die er uit te filteren.

de functies zijn:
create_bought_together_recs()
create_bought_together_recs_different_type()

 
    