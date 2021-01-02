"""Example app to react to an intent to tell you the time."""
import logging
from datetime import datetime
import os
import random

from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp

_LOGGER = logging.getLogger("JokeApp")

host=os.getenv("MQTT_HOST", "localhost")
port=os.getenv("MQTT_PORT", 1883)
username=os.getenv("MQTT_USERNAME")
password=os.getenv("MQTT_PASSWORD")

app = HermesApp("JokeApp", host=host, port=port, username=username, password=password)

jokes = [
    "Ich habe jetzt erst begriffen, dass Frucht-Tiger die Steigerung von fruchtig ist… Es wird nie wieder so sein wie vorher. #fruchttigerlöschtdendurstunddaraufkommtesan",
    "Wie lautet der Vorname vom Reh? – Kartoffelpü",
    "Meine Frau will mit mir über mein kindisches Verhalten reden. – Tja, aber ohne das Geheimwort kommt sie nicht in meine Kissenburg.",
    "Dieser Moment, wenn in der Schule die Anwesenheit kontrolliert wird und du dich vorher nervös auf das „Ja“ vorbereitest.",
    "„Auf einer Skala von 1 bis 10 wie deutsch sind sie?“",
    "„Dürfte ich erstmal ihren Umfrageberechtigungsschein sehen?“",
    "Wie nennt man ein helles Mammut? – Hellmut.",
    "Falls ihr euch zwischen Diät oder Schokolade entscheiden müsstet, würdet ihr dann schwarze, weiße oder Schokolade mit Vollmilch nehmen?",
    "Ich kann auch ohne Karriere leben.",
    "Dieser Moment, wenn jemand „Hallo“ sagt, du dich panisch umdrehst und denkst du hast Freunde, doch die Person hinter dir nur ans Telefon gegangen ist.",
    "Welches Kätzchen ist kein Tier? – Das Weidenkätzchen.",
    "Meine Oma ist jetzt Türsteher, wir nennen sie nun Hilde-Guard.",
    "Was ist gesund und kräftig und spielt den Beleidigten? – Ein Schmollkornbrot.",
    "Was hoppelt durch den Wald und ist ganz heiß? – Ein Kaminchen.",
    "Mit Hunger einkaufen – unbezahlbar.",
    "Wohin geht ein Wal zum Essen? – Ins Wa(h)llokal.",
    "„Ich hab jetzt schon tagelang nicht mehr geschlafen“ – „Bist du da nicht total am Ende?“ – „Nein, nachts schlaf ich ja gut.“",
    "Was ist süß und hangelt sich von Tortenstück zu Tortenstück? – Ein Tarzipan.",
    "Treffen sich zwei Deutschlehrer am Strand. „Genitiv ins Wasser!“ – „Wieso, ist es Dativ?“",
    "Was hat Spaß daran, jemanden zu stechen? – Eine Sadistel.",
    "Hab mich vorhin ausgesperrt. War ganz aus dem Häuschen.",
    "Hab gehört Bushido will AirBerlin kaufen. Die neue Fluggesellschaft soll dann Airsguterjunge heißen.",
    "Neben mir wohnt eine indische Familie. Mir ist gerade erst aufgefallen, dass ihr WLAN „Indernet“ heißt.",
    "Was ist grün, glücklich und hüpft von Grashalm zu Grashalm? – Eine Freuschrecke.",
    "Was ist ein Keks unter einem Baum? – Ein schattiges Plätzchen.",
    "Ich hasse es, wenn ich im Bewerbungsgespräch gefragt werde, wie meine Freunde mich beschreiben würden, weil ich bezweifle, dass „dummer Spast“ mir den Job bringen wird.",
    "Ich habe einen Joghurt fallen gelassen. Er war nicht mehr haltbar.",
    "Was machen Pilze auf einer Pizza? Als Belag funghieren.",
    "Ich kann total gut Mitmenschen umgehen.",
    "Hans-Dieter trägt Socken in Sandalen. Er wurde verhaftet wegen Sandalismus.",
    "Was liegt am Strand und spricht undeutlich? – Eine Nuschel.",
    "Ich esse nicht jede Sorte Chips. Ich bin da sehr pringelig.",
    "Wenn kleine Affen Äffchen heißen, wie heißen dann kleine Maden?",
    "Was ist grün und steht vor der Tür? – Ein Klopfsalat.",
    "Was antwortet Kevin, wenn er gefragt wird, was die Hälfte von sechs ist? – Halb sechs.",
    "Was ist der Unterschied zwischen einem Beinbruch und einem Einbruch? – Nach einem Beinbruch muss man drei Monate liegen, nach einem Einbruch drei Monate sitzen.",
    "Wieso war noch nie ein Veganer auf dem Mond? – Weil er da niemandem erzählen kann, dass er Veganer ist.",
    "Was schmeckt besser als es riecht? – Die Zunge.",
    "Was machen zwei wütende Schafe? – Sie kriegen sich in die Wolle.",
    "Was waren Kevins härtesten zehn Jahre? – Die Grundschule.",
    "Welche Biere schäumen am meisten? – Die Barbiere.",
    "Wieso wird im Winter so wenig auf Baustellen gearbeitet? – Bei Frost platzen doch die Bierflaschen!",
    "Unterhalten sich zwei Kerzen: „Ist Wasser eigentlich gefährlich?“ „Davon kannst du ausgehen.“",
    "Was ist der Unterschied zwischen einem Bäcker und einem Teppich? – Der Bäcker muss morgens früh um halb 4 aufstehen. Der Teppich kann liegenbleiben.",
    "Wie nennt man einen studierten Bauern? Ackerdemiker.",
    "Was ist flüssiger als Wasser? – Hausaufgaben, die sind überflüssig.",
    "Chuck Norris bringt Zwiebeln zum Weinen.",
    "Chuck Norris schafft seinen Bachelor unter der Regelstudienzeit.",
    "Die Erde dreht sich nur, weil Chuck Norris ihr einen Roundhouse-Kick verpasst hat.",
    "Chuck Norris ist gestern gestorben. Heute geht es ihm schon wieder besser.",
    "Chuck Norris wurde mal auf Latein beleidigt – seitdem gilt es als tote Sprache.",
    "Die Zeit rennt, um Chuck Norris zu entkommen.",
    "Chuck Norris kennt die letzte Ziffer von Pi.",
    "Chuck Norris kann schneller stehen, als andere rennen können.",
    "Wenn Google etwas nicht findet, fragt es Chuck Norris.",
    "Chuck Norris darf während der Fahrt mit dem Busfahrer sprechen.",
    "Chuck Norris niest mit offenen Augen.",
    "Als Chuck Norris geboren wurde, sagte der Arzt zur Mutter: „Glückwunsch, es ist ein MANN!“",
    "Chuck Norris kann über seinen eigenen Schatten springen.",
    "Chuck Norris isst sein Knoppers schon um neun Uhr morgens in Deutschland.",
    "Voldemort nennt Chuck-Norris „Du-weißt-schon-wer“.",
    "Chuck Norris bekommt bei Praktiker 20 Prozent auf alles. Auch auf Tiernahrung.",
    "Chuck Norris benutzt keine Augentropfen. Er benutzt Tabasco.",
    "Wimpern hat Chuck Norris nicht. Das sind AUGENBÄRTE.",
    "Chuck Norris verzichtet auf seine Rechte – seine Linke ist sowieso schneller.",
    "Chuck Norris bestellt Chicken McNuggets bei Burger King und bekommt sie auch.",
    "Deine Mutter arbeitet bei IKEA als unterste Schublade.",
    "Dein Vater nennt deine Mutter „Du-weißt-schon-wer“.",
    "Deine Mutter schüttet Actimel über den Computer, damit er gegen Viren geschützt ist.",
    "Deine Mutter hat sich als Weihnachtsmann bei Coca Cola beworben.",
    "Deine Mutter kämpft mit Enten im Park um die letzten Brotkrümel.",
    "Google Earth hat angerufen, deine Mutter steht im Bild.",
    "Wenn deine Mutter niest, weiß jeder wovon Tokio Hotel gesungen hat.",
    "Deine Mutter denkt nachhaltig und trinkt am Pfandautomaten die Reste aus den Flaschen.",
    "Der Einzige, der noch über Deine-Mutter-Witze-Lacht ist dein Vater.",
    "Deine Mutter zieht Katapulte nach Gondor.",
    "Deine Mutter hat Schulden bei Peter Zwegat.",
    "Popeye ist Spinat, um stark zu werden. Deine Mutter isst alles und hört gar nicht mehr damit auf.",
    "Deine Mutter liebt ihren Hund. Er ist der Einzige der WAU sagt, wenn er sie sieht.",
    "Als der Nachtkönig deine Mutter gesehen hat, drehte er um und kam nie wieder zurück.",
    "Deine Mutter kippt beim Joghurt mit der Ecke die große in die kleine."
]

@app.on_intent("TellJoke")
async def tell_joke(intent: NluIntent):
    """Tell a random joke."""
    _LOGGER.info("TellJoke")
    
    return EndSession(random.choice(jokes))

_LOGGER.info(f"Starting app {app.client_name}.")
app.run()