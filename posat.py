from coin import Coin
from client import Client


def main():
    client = Client()
    coin = Coin()

    while True:
        cmd = input("commands: ").strip()

        if cmd.startswith('q') or cmd.startswith('exit'):
            break

        elif cmd.startswith('addtx'):
            tx = input("tx: ").strip()
            client.send_tx(tx)

        elif cmd.startswith('gettx'):
            client.receive_tx()

        elif cmd.startswith('addblock'):
            block = client.pos_leader_election(coin)
            print(block)

            client.send_block(block)

        elif cmd.startswith('getblock'):
            client.receive_block()

        elif cmd.startswith('blockchain'):
            client.print_all_block()

        else:
            print('Invalid command')


if __name__ == '__main__':
    main()
