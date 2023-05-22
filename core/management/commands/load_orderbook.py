from django.core.management import BaseCommand, CommandError

from core.tasks import load_market_orderbook


class Command(BaseCommand):
    help = 'Loads orderbook of an specific market to the project.'

    def add_arguments(self, parser):
        parser.add_argument(
            "market",
            nargs="+",
            help="The market which you intend to load it's orderbook."
        )

    def handle(self, *args, **options):
        market = options.get('market')
        if not market:
            raise CommandError(f"Market {market} does not exist")
        try:
            self.stdout.write(f"Orderbook of market {market} is being loaded into project")
            load_market_orderbook(market) # Todo: Run the task for loading market into project
            self.stdout.write(f"Orderbook of market {market} loaded into project Successfully")
        except Exception as exp:
            self.stderr(f"An error occurred during loadding orderbook of market {market} into the project."
                        f"The error is: {exp}")


